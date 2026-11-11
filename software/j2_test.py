#!/usr/bin/env python3
"""J2-Testsoftware: Arduino Uno + CNC-Shield (GRBL 1.1) + TMC2209, Motor am Pruefstand.

ERSTER TEST, 12-V-Netzteil. Eine Achse (Standard X), Einheit in GRBL = MOTOR-Grad.
Ausgangswinkel J2 = Motorwinkel / 72 (Uebersetzung, docs/parameter.md).

NOT-AUS (Software):  LEERTASTE oder ESC  -> Feed-Hold (!) + Soft-Reset (Ctrl-X).
Das ist KEIN echter Not-Aus: der Treiber kann weiter bestromt bleiben.
Echter Not-Aus: Hohlstecker des 12-V-Netzteils aus dem Terminal ziehen (Kfz-Sicherung ist
zu fest). HAND DAUERND AM STECKER, Probezug vor dem Test.

Sicherungen in der Software:
  - Wegbegrenzung +-MAX_MOTOR_DEG um die Startposition (Start = Mitte, kein Referenzschalter)
  - max. Einzelweg MAX_STEP_DEG, Vorschub-Obergrenze MAX_FEED, Beschleunigung ACCEL
  - Abbruch bei ALARM/error/Zeitueberschreitung/Verbindungsverlust
  - jede Bewegung nur nach Bestaetigung (Enter); ein Test beginnt mit dem kleinsten Weg
  - Log in software/logs/

Start:  python software/j2_test.py          (Port wird automatisch gefunden)
        python software/j2_test.py COM8     (Port von Hand)
"""
import datetime
import msvcrt
import os
import re
import sys
import time

import serial
import serial.tools.list_ports

# ---------------- Grenzen (Motor-Grad, wenn nicht anders vermerkt) ----------------
UEBERSETZUNG = 72.0      # J2: 20:72 * 16:64 * 18:90
MAX_MOTOR_DEG = 720.0    # erlaubter Weg +- um Start (= +-10 Grad am Ausgang)
MAX_STEP_DEG = 720.0     # max. Weg pro Einzelbefehl (Gesamtweg bleibt auf +-MAX_MOTOR_DEG begrenzt)
START_FEED = 300.0       # Grad/min (= 5 Grad/s Motor), Anfangswert fuer die ersten Schritte
MAX_FEED = 48000.0       # Grad/min (= 800 Grad/s = 133 U/min Motor), harte Obergrenze
MAX_RATE = 48000.0       # entspricht max_rate_mm_per_min in software/fluidnc/config_j2.yaml
ACCEL = 1000.0           # Grad/s^2, entspricht acceleration_mm_per_sec2 in config_j2.yaml
SCHNELL_PENDEL = 300.0   # Schnelltest: Hebel pendelt +-300 Grad Motor um die Mitte (= +-4,2 Grad Ausgang)
SCHNELL_FEEDS = (6000.0, 12000.0, 24000.0, 48000.0)   # Grad/min Motor = 100 / 200 / 400 / 800 Grad/s
MOVE_TIMEOUT_S = 120.0
AXIS = "Z"               # Treiber steckt auf Slot Z
BAUD = 115200

LOGDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")


class Abbruch(Exception):
    pass


class NeustartErkannt(Exception):
    pass


class FehlerAntwort(Exception):
    """GRBL lehnt einen Befehl als unlesbar ab (error:1/2/3): meist eine auf der Leitung verfaelschte Zeile."""
    pass


class Test:
    def __init__(self, port, mikroschritt):
        os.makedirs(LOGDIR, exist_ok=True)
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_f = open(os.path.join(LOGDIR, f"j2_test_{stamp}.log"), "w", encoding="utf-8")
        self._buf = b""
        # DTR/RTS VOR dem Oeffnen abschalten: Unter Windows loest sonst das Oeffnen UND das Schliessen des
        # Ports einen Hardware-Reset des Uno (CH340) aus; danach hing GRBL (gefunden 11.11.2026).
        # GRBL wird stattdessen per Ctrl-X (Soft-Reset) neu gestartet.
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = BAUD
        self.ser.timeout = 0.1
        self.ser.dtr = False
        self.ser.rts = False
        self.ser.open()
        self.mikro = mikroschritt
        self.steps_per_deg = 200.0 * mikroschritt / 360.0
        self.origin = None
        self.pos = 0.0  # Motor-Grad relativ zum Start

    # ---------- Hilfen ----------
    def log(self, text):
        line = f"{datetime.datetime.now().strftime('%H:%M:%S')} {text}"
        self.log_f.write(line + "\n")
        self.log_f.flush()

    def say(self, text):
        print(text)
        self.log(text)

    def not_aus_taste(self):
        """True, wenn Leertaste oder ESC gedrueckt wurde."""
        while msvcrt.kbhit():
            if msvcrt.getwch() in (" ", "\x1b"):
                return True
        return False

    def not_aus(self, grund):
        try:
            self.ser.write(b"!")
            self.ser.write(b"\x18")
        except Exception:
            pass
        self.say(f"*** NOT-AUS: {grund} *** -> Hohlstecker ziehen, falls sich etwas bewegt!")
        raise Abbruch(grund)

    def leeren(self):
        self.ser.reset_input_buffer()
        self._buf = b""

    def zeile(self):
        """Gibt eine VOLLSTAENDIGE Zeile zurueck (oder None). Halbe Zeilen bleiben im Puffer, bis das
        Zeilenende kommt: waehrend der Fahrt sendet der Uno langsam (Schrittimpulse haben Vorrang)."""
        daten = self.ser.read(max(1, self.ser.in_waiting))
        if daten:
            self._buf += daten
        if b"\n" not in self._buf:
            return None
        raw, self._buf = self._buf.split(b"\n", 1)
        s = raw.decode("ascii", "replace").replace("\x00", "").strip()
        if s:
            self.log("<< " + s)
        return s or None

    def senden(self, cmd, warte_ok=True, timeout=5.0, versuche=3):
        """Sendet einen Befehl ohne Bewegung (Einstellungen, G21/G91) und wartet auf 'ok'.
        Startet sich der Uno dabei neu (Begruessung 'Grbl ...' statt 'ok'), wird neu synchronisiert
        und der Befehl wiederholt. Fuer Bewegungen (G1) wird diese Funktion NICHT benutzt."""
        for versuch in range(versuche):
            try:
                return self._senden_einmal(cmd, warte_ok, timeout)
            except FehlerAntwort as e:
                self.say(f"Hinweis: GRBL meldet '{e}' auf '{cmd}' (Zeile vermutlich verfaelscht angekommen), "
                         f"Versuch {versuch + 1}/{versuche}. Wiederhole.")
                time.sleep(0.3)
                self.sync()
            except NeustartErkannt:
                self.say(f"Hinweis: Uno hat sich neu gestartet (Versuch {versuch + 1}/{versuche}). "
                         "Synchronisiere und wiederhole den Befehl.")
                time.sleep(1.0)
                self.sync()
        self.not_aus(f"Uno startet immer wieder neu bei '{cmd}' (USB/anderes Programm auf COM-Port?)")

    def _senden_einmal(self, cmd, warte_ok, timeout):
        self.log(">> " + cmd)
        self.ser.write((cmd + "\n").encode("ascii"))
        antworten = []
        t0 = time.time()
        while warte_ok:
            if self.not_aus_taste():
                self.not_aus("Taste gedrueckt")
            if time.time() - t0 > timeout:
                self.not_aus(f"Keine Antwort auf '{cmd}'")
            s = self.zeile()
            if s is None:
                continue
            if s == "ok":
                return antworten
            if s.startswith("Grbl"):
                raise NeustartErkannt()
            if s in ("error:1", "error:2", "error:3"):
                raise FehlerAntwort(s)
            if s.startswith("error") or s.startswith("ALARM"):
                self.not_aus(f"GRBL meldet '{s}' auf '{cmd}'")
            antworten.append(s)
        return antworten

    def status(self):
        """Liest <...> Status. Gibt (zustand, motor_grad_abs) zurueck."""
        self.ser.write(b"?")
        t0 = time.time()
        nochmal = False
        while time.time() - t0 < 2.0:
            if not nochmal and time.time() - t0 > 0.8:
                self.ser.write(b"?")   # erste Abfrage unbeantwortet/verstuemmelt: einmal wiederholen
                nochmal = True
            s = self.zeile()
            if s and s.startswith("<") and s.endswith(">"):
                # GRBL 1.1: <Idle|MPos:0.000,0.000,0.000|...>   GRBL 0.9: <Idle,MPos:0.000,0.000,0.000,WPos:...,Lim:000>
                zustand = re.split(r"[,|>]", s.lstrip("<"))[0]
                m = re.search(r"MPos:(-?[\d.]+),(-?[\d.]+),(-?[\d.]+)", s) or \
                    re.search(r"WPos:(-?[\d.]+),(-?[\d.]+),(-?[\d.]+)", s)
                pos = float(m.group("XYZ".index(AXIS) + 1)) if m else None
                lim = re.search(r"Lim:([01]+)", s) or re.search(r"Pn:(\w+)", s)
                self.limit = lim.group(1) if lim else None
                if pos is None:
                    self.not_aus(f"Position nicht lesbar in Status: {s}")
                return zustand, pos
            if s and s.startswith("error"):
                self.not_aus(f"GRBL meldet '{s}' (Befehl abgelehnt, evtl. auf der Leitung verfaelscht)")
            if s and s.startswith("Grbl"):
                self.not_aus("Uno hat sich waehrend des Betriebs neu gestartet (Position verloren)")
            if s and s.startswith("ALARM"):
                self.not_aus(s)
        self.not_aus("Kein Status von GRBL (Verbindung weg?)")

    # ---------- Ablauf ----------
    def verbinden(self):
        self.say("Verbinde ... (GRBL-Soft-Reset per Ctrl-X)")

        def warte_auf_gruss(sekunden):
            t0 = time.time()
            while time.time() - t0 < sekunden:
                s = self.zeile()
                if s and s.startswith("Grbl"):
                    self.say("Gefunden: " + s)
                    self._erkannt(s)
                    return True
            return False

        # 1) Soft-Reset (Ctrl-X): GRBL startet neu und meldet sich (kein Hardware-Reset noetig)
        self.leeren()
        for _ in range(3):
            self.ser.write(b"\x18")
            if warte_auf_gruss(2.5):
                return
        # 2) Evtl. laeuft gerade der Bootloader (frisch angesteckt): Begruessung abwarten
        if warte_auf_gruss(4.0):
            return
        # 2b) ESP32 mit CP2102: Neustart ueber RTS (haengt am EN-Pin). Beim Uno (CH340) ohne Wirkung.
        self.say("Keine Antwort, starte den ESP32 ueber RTS neu ...")
        self.ser.rts = True
        time.sleep(0.15)
        self.ser.rts = False
        if warte_auf_gruss(10.0):
            return
        # 3) Notloesung: Status-Abfrage. Antwortet GRBL, laeuft es, nur ohne Begruessung.
        self.leeren()
        self.ser.write(b"?")
        t0 = time.time()
        while time.time() - t0 < 2.0:
            s = self.zeile()
            if s and s.startswith("<"):
                self.say("GRBL antwortet (ohne Begruessung gesehen): " + s)
                return
        raise Abbruch("Keine Antwort von der Steuerung. Reset-/EN-Taste am Board druecken und nochmals starten; "
                      "USB-Kabel/Port pruefen, Arduino-IDE geschlossen? Falls GRBL nicht (mehr) drauf ist, neu flashen.")

    def _erkannt(self, gruss):
        """Merkt sich die Steuerung. FluidNC (ESP32): Einstellungen stehen in config.yaml, Achse X."""
        global AXIS
        self.gruss = gruss
        if "FluidNC" in gruss:
            self.fluidnc = True
            AXIS = "X"

    def einstellungen_fluidnc(self):
        """FluidNC kennt $100=... nicht (Read-only). Die Werte stehen in software/fluidnc/config_j2.yaml und
        werden hier nur GEPRUEFT. Weicht etwas ab: Konfiguration neu hochladen (fluidnc_upload.py)."""
        self.say("FluidNC erkannt (Einstellungen kommen aus config.yaml, werden nur geprueft):")
        erwartet = {
            "/axes/x/steps_per_mm": self.steps_per_deg,
            "/axes/x/max_rate_mm_per_min": MAX_RATE,
            "/axes/x/acceleration_mm_per_sec2": ACCEL,
        }
        for key, soll in erwartet.items():
            wert = None
            for z in self.senden(f"${key}"):
                m = re.match(re.escape(f"${key}=") + r"([-\d.]+)", z)
                if m:
                    wert = float(m.group(1))
            self.say(f"  ${key} = {wert}  (soll {soll:g})")
            if wert is None or abs(wert - soll) > max(0.01, abs(soll) * 0.005):
                raise Abbruch(f"FluidNC-Einstellung {key} stimmt nicht (ist {wert}, soll {soll:g}). "
                              "python software/fluidnc_upload.py software/fluidnc/config_j2.yaml")
        if input("Einstellungen stimmen. Weiter? [j/N] ").strip().lower() != "j":
            raise Abbruch("nicht bestaetigt")

    def sync(self):
        """Wartet, bis GRBL wirklich Befehle annimmt (leere Zeile -> 'ok'). Bis zu 5 Versuche."""
        for _ in range(5):
            self.leeren()
            self.ser.write(b"\n")
            t0 = time.time()
            while time.time() - t0 < 1.0:
                if self.zeile() == "ok":
                    return
        raise Abbruch("GRBL nimmt keine Befehle an (kein 'ok' auf Leerzeile)")

    def einstellungen(self):
        if getattr(self, "fluidnc", False):
            return self.einstellungen_fluidnc()
        # ALLE drei Achsen setzen: Steht bei einer Achse Schritte/Einheit = 0, rechnet GRBL 0.9j in der
        # Positionsanzeige durch 0 und stuerzt ab (Uno startet neu, Status verstuemmelt). Gefunden 11.11.
        werte = {}
        for i in range(3):
            werte[100 + i] = self.steps_per_deg   # Schritte pro Grad Motor ($100/101/102)
            werte[110 + i] = MAX_RATE             # $110/111/112
            werte[120 + i] = ACCEL                # $120/121/122
        werte.update({
            10: 3,    # Statusbericht mit MPos+WPos (GRBL 0.9: bei 16 kommt nur Lim, keine Position)
            1: 255,   # Motor bleibt stromfuehrend (kein Wegrutschen im Stillstand)
            21: 0,    # Hard-Limits aus (noch keine Endschalter)
            20: 0,    # Soft-Limits aus (GRBL braucht dafuer Homing); wir begrenzen hier
            22: 0,
            6: 0,     # Sondeneingang nicht invertiert (stand ploetzlich auf 1: Hinweis auf verfaelschte Daten)
        })
        self.say("Aktuelle GRBL-Einstellungen (Auszug):")
        for z in self.senden("$$"):
            if z.startswith("$"):
                self.say("  " + z)
        self.say("Gewuenschte GRBL-Einstellungen:")
        for k, v in werte.items():
            self.say(f"  ${k}={v:g}")
        if input("In GRBL schreiben? [j/N] ").strip().lower() != "j":
            raise Abbruch("Einstellungen nicht bestaetigt")
        for k, v in werte.items():
            self.senden(f"${k}={v:g}")
        # Zurücklesen und vergleichen: erkennt Einstellungen, die verfaelscht angekommen sind
        for runde in range(3):
            ist = {}
            for z in self.senden("$$"):
                m = re.match(r"\$(\d+)=([-\d.]+)", z)
                if m:
                    ist[int(m.group(1))] = float(m.group(2))
            falsch = {k: (v, ist.get(k)) for k, v in werte.items()
                      if ist.get(k) is None or abs(ist[k] - v) > max(0.01, abs(v) * 0.001)}
            if not falsch:
                self.say("Einstellungen zurueckgelesen: alle stimmen.")
                return
            self.say(f"Einstellungen weichen ab (Runde {runde + 1}/3): "
                     + ", ".join(f"${k}: soll {v:g}, ist {i}" for k, (v, i) in falsch.items()))
            for k in falsch:
                self.senden(f"${k}={werte[k]:g}")
        raise Abbruch("Einstellungen lassen sich nicht sauber schreiben (Leitung gestoert?)")

    def pruefungen(self):
        zustand, pos = self.status()
        self.say(f"GRBL-Zustand: {zustand}")
        if zustand.startswith("Alarm"):
            if input("Alarm aktiv. Mit $X entsperren? [j/N] ").strip().lower() != "j":
                raise Abbruch("Alarm nicht entsperrt")
            self.senden("$X")
            zustand, pos = self.status()
        if not zustand.startswith("Idle"):
            raise Abbruch(f"Zustand '{zustand}' statt Idle")
        self.origin = pos
        if getattr(self, "limit", None):
            self.say(f"Hinweis: GRBL meldet Limit-Pins '{self.limit}' (000 = nichts ausgeloest). "
                     "Ohne angeschlossenen Schalter ist das fuer diesen Test ohne Wirkung ($21=0).")
        self.say(f"Startposition (Mitte): {pos:.3f} Grad Motor. Erlaubt: +-{MAX_MOTOR_DEG:g} Grad.")

    def fahre(self, delta, feed):
        feed = min(feed, MAX_FEED)
        if abs(delta) > MAX_STEP_DEG:
            raise Abbruch(f"Einzelweg {delta} > {MAX_STEP_DEG}")
        ziel = self.pos + delta
        if abs(ziel) > MAX_MOTOR_DEG:
            self.say(f"VERWEIGERT: Ziel {ziel:.1f} Grad liegt ausserhalb +-{MAX_MOTOR_DEG:g}.")
            return False
        self.say(f"Fahre {delta:+.2f} Grad Motor (= {delta / UEBERSETZUNG:+.4f} Grad Ausgang J2), "
                 f"F{feed:g} Grad/min.  Stopp: Leertaste/ESC")
        self.senden("G21 G91")
        self.ser.write(f"G1 {AXIS}{delta:.4f} F{feed:.1f}\n".encode("ascii"))
        self.log(f">> G1 {AXIS}{delta:.4f} F{feed:.1f}")
        t0 = time.time()
        gesehen_bewegung = False
        while True:
            if self.not_aus_taste():
                self.not_aus("Taste gedrueckt")
            if time.time() - t0 > MOVE_TIMEOUT_S:
                self.not_aus("Zeitueberschreitung Bewegung")
            zustand, pos = self.status()
            if pos is not None and abs(pos - self.origin) > MAX_MOTOR_DEG + 1.0:
                self.not_aus(f"Position {pos - self.origin:.1f} ausserhalb Grenze")
            if zustand.startswith("Run"):
                gesehen_bewegung = True
            if zustand.startswith(("Alarm", "Hold", "Door")):
                self.not_aus(f"Zustand {zustand}")
            if zustand.startswith("Idle") and (gesehen_bewegung or time.time() - t0 > 1.0):
                break
            time.sleep(0.05)
        # 'ok' der Bewegung abholen
        t1 = time.time()
        while time.time() - t1 < 2.0:
            s = self.zeile()
            if s == "ok":
                break
            if s and (s.startswith("error") or s.startswith("ALARM")):
                self.not_aus(s)
        neu = pos - self.origin
        # Kontrolle: Der tatsaechliche Weg muss dem Befehl entsprechen (GRBL rundet auf ganze Mikroschritte,
        # 1 Mikroschritt = 0,225 Grad). Weicht er ab, kam der Befehl verfaelscht an -> Abbruch.
        if abs(neu - ziel) > 0.3:
            self.not_aus(f"Position {neu:+.2f} weicht vom Soll {ziel:+.2f} ab (Befehl verfaelscht oder verloren?)")
        self.pos = neu
        self.say(f"Position jetzt: {self.pos:+.2f} Grad Motor ({self.pos / UEBERSETZUNG:+.4f} Grad Ausgang)")
        return True

    def pruefe_bewegung(self, soll):
        """Fragt den Nutzer, ob die Bewegung wie erwartet war."""
        a = input("Bewegung wie erwartet (Richtung, Geraeusch, kein Rutschen)? [j/N] ").strip().lower()
        if a != "j":
            raise Abbruch("Nutzer meldet Auffaelligkeit")

    def testablauf(self):
        self.say("")
        if input("Probezug Hohlstecker gemacht, Stecker leicht erreichbar, linke Hand dran? [j/N] "
                 ).strip().lower() != "j":
            raise Abbruch("Not-Aus (Hohlstecker) nicht bestaetigt")
        self.say("HAND AM HOHLSTECKER. Jeder Schritt nur nach Enter. 'q' = Ende, 's' = ueberspringen.")
        schritte = [
            (1.8, "Kleinster Test: 1 Vollschritt-Gruppe (1,8 Grad Motor)"),
            (-1.8, "Zurueck"),
            (5.0, "5 Grad Motor"),
            (-5.0, "Zurueck"),
            (45.0, "45 Grad Motor (1/8 Umdrehung)"),
            (-45.0, "Zurueck"),
            (360.0, "1 Umdrehung Motor (5 Grad am Ausgang)"),
            (-360.0, "Zurueck"),
        ]
        feed = START_FEED
        for delta, text in schritte:
            self.say(f"\nSchritt: {text}")
            a = input("Enter = ausfuehren, s = ueberspringen, q = Ende: ").strip().lower()
            if a == "q":
                break
            if a == "s":
                continue
            if self.fahre(delta, feed):
                self.pruefe_bewegung(delta)
        self.schnelltest()

    def schnelltest(self):
        """Hebel pendelt um die Mitte, Stufe fuer Stufe schneller. Jede Stufe nur nach Bestaetigung."""
        halb = SCHNELL_PENDEL / UEBERSETZUNG
        self.say(f"\nSCHNELLTEST: Hebel pendelt +-{halb:.1f} Grad am Ausgang ({SCHNELL_PENDEL * 2:g} Grad Motor), "
                 f"3x hin und zurueck pro Stufe, Stufen: "
                 + ", ".join(f"{f / 60:g} Grad/s ({f / 60 / UEBERSETZUNG:.1f} am Ausgang)" for f in SCHNELL_FEEDS))
        if input(f"Hat der Hebel frei +-{halb:.1f} Grad (mit Lasthebel, nichts im Weg)? [j/N] "
                 ).strip().lower() != "j":
            self.say("Schnelltest uebersprungen.")
            return
        for f in SCHNELL_FEEDS:
            a = input(f"\nStufe {f / 60:g} Grad/s Motor ({f / 60 / UEBERSETZUNG:.1f} Grad/s am Ausgang): "
                      "Enter = fahren, s = ueberspringen, q = Ende: ").strip().lower()
            if a == "q":
                break
            if a == "s":
                continue
            # langsam an den Startpunkt (-Pendel), dann 3x schnell hin und zurueck, dann langsam zur Mitte
            if not self.fahre(-SCHNELL_PENDEL - self.pos, 600.0):
                continue
            for _ in range(3):
                self.fahre(2 * SCHNELL_PENDEL, f)
                self.fahre(-2 * SCHNELL_PENDEL, f)
            self.fahre(-self.pos, 600.0)
            self.pruefe_bewegung(f)

    def ende(self):
        try:
            self.ser.write(b"!")
            self.ser.write(b"\x18")
        except Exception:
            pass
        self.say("Test beendet. Motor ggf. stromfuehrend -> Spannung erst abschalten, dann nichts umstecken.")
        self.log_f.close()
        self.ser.close()


def finde_port(wunsch):
    """Gibt den COM-Port des Arduino zurueck. 'auto' oder fehlend -> automatisch suchen.
    Der Uno (CH340 oder Original) bekommt von Windows je nach USB-Anschluss andere COM-Nummern."""
    ports = list(serial.tools.list_ports.comports())
    print("Gefundene serielle Anschluesse:")
    for p in ports:
        print(f"  {p.device}: {p.description}")
    # Arduino/CH340/FTDI: VID 1A86 (CH340), 2341/2A03 (Arduino), 0403 (FTDI), 10C4 (CP210x)
    arduino = [p for p in ports if (p.vid in (0x1A86, 0x2341, 0x2A03, 0x0403, 0x10C4))
               or "arduino" in (p.description or "").lower() or "ch340" in (p.description or "").lower()]
    if wunsch and wunsch.lower() != "auto":
        if any(p.device.upper() == wunsch.upper() for p in ports):
            if arduino and wunsch.upper() not in [a.device.upper() for a in arduino]:
                print(f"WARNUNG: {wunsch} sieht nicht nach einem Arduino aus, "
                      f"aber {arduino[0].device} ({arduino[0].description}). Mit 'auto' starten?")
            return wunsch
        print(f"Port {wunsch} gibt es gerade nicht.")
    if len(arduino) == 1:
        print(f"-> Arduino gefunden: {arduino[0].device} ({arduino[0].description})")
        return arduino[0].device
    if not arduino:
        print("KEIN Arduino erkannt. USB-Kabel (Daten, nicht nur Laden) und Anschluss pruefen, "
              "gruene ON-LED am Uno? Dann Skript nochmals starten.")
    else:
        print("Mehrere moegliche Arduinos, bitte Port von Hand angeben: python software/j2_test.py COMx")
    return None


def main():
    wunsch = sys.argv[1] if len(sys.argv) > 1 else "auto"
    mikro = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    port = finde_port(wunsch)
    if port is None:
        return 2
    try:
        t = Test(port, mikro)
    except serial.SerialException as e:
        print(f"Port {port} laesst sich nicht oeffnen: {e}\n"
              "Ist die Arduino-IDE / ein Serial Monitor / ein anderes Skript noch offen?")
        return 2
    try:
        t.say(f"J2-Test, Mikroschritt 1/{mikro}, Schritte pro Grad Motor: {t.steps_per_deg:.4f}")
        t.verbinden()
        t.sync()
        t.einstellungen()
        t.pruefungen()
        t.testablauf()
    except Abbruch as e:
        t.say(f"ABBRUCH: {e}")
    except KeyboardInterrupt:
        t.say("ABBRUCH: Ctrl-C")
    except serial.SerialException as e:
        t.say(f"ABBRUCH: USB-Verbindung verloren ({e}). Hohlstecker ziehen, USB-Kabel pruefen!")
    finally:
        t.ende()
    return 0


if __name__ == "__main__":
    sys.exit(main())
