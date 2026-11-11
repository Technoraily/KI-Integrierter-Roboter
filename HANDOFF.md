# HANDOFF – KI-Integrierter Roboterarm (Stand 11.11.2026 Feierabend; Details: README.md, docs/konzept.md, index.md)
## Ziel
6-Achs-Desktop-Roboterarm (3D-Druck, NEMA 17) auf 1000-mm-Schiene. Aktuell: Prüfstand J2 mit Software-Test (12-V-4-A-Netzteil, Hohlstecker ziehen = Not-Aus). LRS-350/230 V noch NIE eingeschaltet (F1, Opa, FI offen).
## Stand
- STEUERUNG GEWECHSELT: ESP32-WROOM-32 (CP2102, COM9) mit FluidNC v4.1.1 statt Uno-Klon (Uno hing beim Motoranlauf, auch ohne Shield/Akku-Test/Kabel; neuer Uno nicht gekauft). Shield OHNE Uno, TMC2209 Slot Z. Pins: GPIO26 STEP, GPIO27 DIR, GPIO25 EN, GND, 3V3 an Shield-5V-Pin (Logik). Treiber: CP210x 11.6, CH340 4.0.2026.2.
- software/ (NICHT committet, Hook pusht beim Beenden; logs/ ist jetzt ignoriert): j2_steuerung.html (Chrome/Edge, Web Serial, Bereich ±75°, Tempo bis 40 °/s, Not-Aus-Knopf, Pendeln, Haken «Hand am Hohlstecker»), j2_test.py (Python, erkennt FluidNC, Port-Autosuche), fluidnc/config_j2.yaml (X-Achse, 4,444 Schritte/°, accel 1000, max_rate 48000, max_travel 10800), fluidnc_upload.py (XMODEM). Neue config max_travel NICHT hochgeladen (COM9 war belegt). Nur EIN Programm darf den Port nutzen.
- Messwerte: Vref ca. 0,75 V (≈0,5 A geschätzt, Annahme 1,77 A bei 2,5 V Vref, Modul «V985» ungeprüft). Sauber bis ca. 15 °/s am Hebel, ab 19 °/s Geräusche und «Wand» = Schrittverlust (Nullpunkt verschiebt sich, Motorwelle stand still bei leichtem Gegendruck).
- Mechanik: eine mittlere Welle (A oder B?) leicht verbogen, schleift, fester Punkt; 5M-Riemen wich oben 2 mm vom Kranz, jetzt ca. 0,5 mm (Nutzer änderte etwas, was unklar). Behelfsring im 3M-Zahnrad ist nicht im CAD.
## Entscheidungen
- Nie Stecker ziehen/stecken bei 24 V (TMC2209 max ca. 28 V): dann Schalter/Relais. Vref max 1,4 V (≈1 A) ohne Kühlkörper. 1 kg Nutzlast J2 = 11,8 Nm → ca. 0,25 Nm nutzbar am Motor (docs/lastrechnung.md).
## Offen
- Gerade 8-mm-Welle ersetzen (≤ 8,00 mm, Hornbach Rundstahl messen / Opa / Zylinderstift 8 h8 × 70). Seitenschlag Ritzel/90er-Scheibe mit Messuhr. GT2-Stufe 1 (ca. 44 N laut Gutachten) bei mehr Strom prüfen. Endschalter (Mikroschalter COM+NC) einbauen + Homing. Doku: Welle/Ring in Stückliste. index.md nachführen. 24 V erst nach Opa-Freigabe.
## Nächster Schritt
Welle ersetzen, dann Driftmessung (Klebemarken, Pendeln 10×, Tabelle Tempo/Beschleunigung), dann Vref 1,0 V mit Temperaturcheck. Start: ESP32 per USB, j2_steuerung.html in Chrome öffnen (Python-Skripte schliessen).
## Dateien
software/j2_steuerung.html, j2_test.py, fluidnc/config_j2.yaml, fluidnc_upload.py; docs/lastrechnung.md, docs/stuecklisten/pruefstand-j2.md; Repo github.com/Technoraily/KI-Integrierter-Roboter
