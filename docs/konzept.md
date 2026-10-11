# Projektplan: 6-Achs-Roboterarm «von Grund auf» (PLA, BambuLab A1, AliExpress-Teile)

*Stand: unabhängige Prüfung Runde 1 = 6/10, Runde 2 = 8/10 («kann so gelassen werden»); die Restpunkte aus Runde 2 sind eingearbeitet.*

## 1. Kontext

Ziel ist ein selbst konstruierter, vollwertiger 6-Achs-Desktop-Roboterarm – ausdrücklich **kein** abgespecktes Baukit. Er soll Aufgaben zuverlässig und so präzise wie in PLA möglich erledigen, eine saubere Verkleidung haben, mit Standardteilen von AliExpress auskommen und möglichst wenig Kaufteile brauchen. Konstruktion (Fusion 360 via MCP), bebilderte Bauanleitung und Dokumentation entstehen im Projekt selbst. Kamera-KI und automatischer Greiferwechsel folgen später, werden aber von Anfang an mechanisch/elektrisch vorgesehen.

**Festgelegt mit dem Nutzer:** 6 Achsen · ca. 400–450 mm Reichweite · 0,5–1 kg Nutzlast · Kaufteile wenn machbar < 150 CHF für den Anfang · vorhanden: 3× NEMA 17 (Typ unbekannt), Arduino Uno + CNC-Shield + A4988, Netzteil, Kleinteile.

**Ausgangslage:** Projektordner `C:\Claude\KI-Integrierter Roboter` ist leer, kein Git-Repo. Fusion-360-MCP antwortet (ping OK).

## 2. Zielspezifikation (messbar, wird in Phase 8 geprüft)

| Grösse | Ziel |
|---|---|
| Freiheitsgrade | 6 (Knickarm mit Zentralhand → geschlossene inverse Kinematik) |
| Reichweite Schulter → Flansch | 450 mm (Oberarm 200, Unterarm 190, Hand 60) – in Phase 1 per Simulation bestätigt |
| Nutzlast | 0,5 kg im ganzen Arbeitsraum; 1 kg bei ≤ 300 mm Ausladung. Enthält 150 g Reserve am Flansch für Werkzeugwechsler + Kamera |
| Wiederholgenauigkeit | ≤ ±0,5 mm, **unidirektional nach Referenzfahrt**; Wunsch ±0,3 mm |
| Gelenkgeschwindigkeit | J2/J3 ≥ 25°/s, Handachsen ≥ 90°/s (Grenze ist die Momentenkurve der Motoren, nicht die Schrittrate) |
| Grösstes Druckteil | ≤ 240 × 240 × 240 mm |

**Fehlerbudget (aus dem Flanschziel rückwärts gerechnet; 0,1° an 450 mm = 0,8 mm):**
- J1 (keine Schwerkraft-Vorspannung): Umkehrspiel ≤ 0,05° → spielfreie Bauart zwingend.
- J2/J3: durch Schwerkraft + Ausgleichsfeder einseitig anliegend; Umkehrspiel ≤ 0,3° zulässig, dafür Steifigkeit als Messgrösse (Nm/°).
- J4/J5: ≤ 0,15° (wirkt bis zur Greiferspitze, ~140 mm Hebel); J6: ≤ 0,3°.
- Wiederholbarkeit der Referenzsensoren wird separat gemessen – sie begrenzt die Genauigkeit direkt.

## 3. Architekturentscheide

### 3.1 Steuerung – Abweichung vom Wunsch (begründet)
- **Uno + CNC-Shield reicht nicht:** GRBL auf dem Uno steuert nur 3 unabhängige Achsen, der Speicher ist voll.
- **Empfehlung: Mega-2560-basiertes Board mit Firmware `grbl-Mega-5X`** (6 Achsen, verifiziert: Achsen 4/5 auf den Sockeln E0/E1, Achse 6 auf D49/D51/D53 an AUX-3; Endschalter der Achsen 4–6 auf D42/D44/D57).
  - Board: **MKS Gen L V2.x als Erstwahl** (Mega integriert, 12–24 V). RAMPS 1.4/1.6 nur mit Umbau (Diode D1 entfernen, Mega separat speisen) – daher nicht empfohlen. Pin-Belegung wird in Phase 1 gegen `cpu_map.h` geprüft, bevor bestellt wird.
  - 6. Treiber auf externem Treiberträger.
  - **24 V als Soll** (deutlich mehr Drehmoment bei Drehzahl). Vorhandenes Netzteil in Phase 1 prüfen.
  - In Phase 1 kurz gegenprüfen: Marlin mit Rotationsachsen auf demselben Board als Alternative.
- **Warum nicht ESP32/FluidNC:** Die auf AliExpress gängigen Boards haben nur 3–5 Achsen; echte 6-Achs-Boards sind teurer und schwerer zu beschaffen. Bleibt Upgrade-Pfad.
- **Treiber pro Achse:**
  - J2, J3, J5 (schwerkraftbelastet): TMC2209 mit Kühlkörper + Lüfter, **voller Haltestrom**, Motoren dauernd bestromt (`$1=255`).
  - J1, J4, J6: TMC2209 mit Stillstandsstrom-Absenkung.
  - Vorhandene A4988 nur für den Prüfstand.
- **Uno + CNC-Shield** bleiben im Einsatz: Prüfstand-Steuerung (Phase 2), später Greiferwechsel-Station.
- **Aufgabenteilung:** Firmware fährt nur synchron Gelenkwinkel (G-Code in Grad). Kinematik, Bahnplanung und später Kamera/KI laufen in **Python auf dem PC**.

### 3.2 Antriebe
| Gelenk | Motor | Untersetzung | Bauart |
|---|---|---|---|
| J1 Basis | NEMA 17 (vorhanden) | ~20:1 | 2-stufig Riemen, spielfrei gespannt |
| J2 Schulter | stärkster vorhandener oder NEMA 17 60 mm (0,65 Nm, ~12 CHF) | **80–100:1** | Riemen-Vorstufe + Endstufe laut Prüfstand; Ausgleichsfeder |
| J3 Ellbogen | NEMA 17 (vorhanden), Motor nahe Schulter | ~50:1 | wie J2, kleiner |
| J4 Unterarm-Rolle | NEMA 17 34 mm (neu) | ~20:1 | 2-stufig GT2 |
| J5 Hand-Nicken | NEMA 17 34 mm (neu), im Unterarm | ~20:1 | GT2 2-stufig |
| J6 Flansch-Rolle | NEMA 14 (neu) | ~8:1 | GT2 |

- **Die Endstufe für J2/J3 ist bewusst noch offen** und wird im Prüfstand entschieden (siehe Phase 2). Kandidaten:
  - (a) Capstan-Seiltrieb (Seil auf Trommel + Segment; spielfrei, sehr günstig; belegt beim gedruckten Arm «Forte» mit ≤ 0,6 mm Wiederholfehler) – **Favorit**
  - (b) gedrucktes Zykloidgetriebe mit zwei versetzten Scheiben und einstellbarem Spiel (Messung aus der Literatur: ~0,76° unbelastet → nur mit Nachweis)
  - (c) Mehrstufen-Riemen mit breiter HTD-3M/5M-Endstufe (GT2 6 mm ist für ~290 N Trumkraft an J2 zu schwach)
- **Capstan-Auslegung (Favorit):** Riemen-Vorstufe 5–6:1 (GT2 16 Z → 80–96 Z) × Capstan 14–16:1 (Segmentradius 70–80 mm, Trommel ~10 mm). Dyneema 1,5 mm oder doppelt geführt, mit Nachspannschraube. Trommel als 8-mm-Stahlwelle, beidseitig gelagert (kein gedruckter Zapfen). Segment J2 ≈ 180° (Halbscheibe), J3 ≈ 270° (Vollscheibe am Ellbogen, Riemen durch den Oberarm). Massen und Bauraum fliessen in die Simulation von Phase 1 ein.
- **Lastrechnung:** Schulter statisch ≈ 7,4 Nm (0,5 kg ausgestreckt). Gerechnet wird mit dem **nutzbaren Moment bei Betriebsdrehzahl** (~0,28 Nm statt 0,4 Nm Haltemoment, gültig bis ca. 300–500 U/min) und η ≈ 0,65: bei 90:1 ≈ 16 Nm → Sicherheit ≈ 2,2. Daraus folgen an J2 realistisch 20–33°/s; die Schrittrate (30 kHz) ist nicht der Engpass.
- Die drei vorhandenen Motoren werden in Phase 1 **vermessen** (Länge, Wicklungswiderstand, Haltemoment mit Hebel + Waage, Drehzahltest an 24 V); danach wird die Tabelle fixiert.

### 3.3 Lagerung und Struktur
- **J1: zwei gekaufte Dünnringlager (6810/6813, je ~3–5 CHF)** mit ≥ 40 mm Abstand, vorgespannt, Hohlwelle für Kabel. (Gedrucktes Kugellager nur als Experiment auf dem Prüfstand – Kippspiel an J1 wirkt mit vollem Hebel.)
- J2–J6: Standard-Rillenkugellager paarweise vorgespannt.
- Tragstruktur als geschlossene Schalen; **Verkleidung als separate, geclipste/verschraubte Deckel**.
- M3/M4 + Einschmelzgewinde, Passstifte für Wiederholbarkeit.
- **Materialwahl (PETG vom Nutzer freigegeben):** PLA bleibt Standard für Tragschalen und Verkleidung (steifer). **PETG für wärme- und kriechkritische Teile:** Motorplatten, Seilverankerungen/Spannelemente, Teile direkt am Motor. Bei Getriebeteilen (Segment, Riemenscheiben) entscheidet der Prüfstand zwischen PLA und PETG. Belüftete Motorräume.
- Kabelführung ist Teil der Tragstruktur-Konstruktion (Hohlwellen-Durchmesser, Verdrehwinkel), nicht Nacharbeit.

### 3.4 Sicherheit
- Not-Aus-Taster, der die Motorspannung trennt; Sicherung; Zugentlastungen.
- **Stromausfall:** Arm ist rückdrehbar → Ausgleichsfeder so auslegen, dass er langsam sinkt; definierte Parkposition.
- Mechanische Endanschläge an jeder Achse + Soft-Limits in der Firmware; Quetschstellen in der Verkleidung vermeiden.

### 3.5 Vorbereitung für später (nur vorsehen)
- **Werkzeugflansch ISO 9409-1-31,5-4-M5** → Schnittstelle für Greiferwechsler (kinematische Kupplung + Magnete + Pogo-Pins).
- Kabelkanal bis zum Flansch (≥ 6 Adern + USB), Kamera-Schraubpunkte am Handgelenk.
- Erster Greifer: Servo-Parallelgreifer am ISO-Flansch (5-V-Wandler vorgesehen).

### 3.6 Software
Python-Paket: Vorwärts-/Rückwärtskinematik (analytisch), Arbeitsraum- und Momentensimulation, G-Code-Streaming, Jog-Oberfläche, Teach-&-Playback, Kalibrierung. Später: OpenCV, Hand-Auge-Kalibrierung, KI-Aufgabenplanung.

## 4. Kosten Kaufteile (AliExpress, ehrlich gerechnet)

Der Arm wird in **zwei Ausbaustufen** gebaut, damit der Start unter 150 CHF bleibt:

| Stufe | Inhalt | CHF |
|---|---|---|
| **A – Prüfstand + J1–J3** | Board, 3× TMC2209 + Kühlung, Lager, Riemen/Ritzel, Seil/Stifte, Feder, Schrauben/Einsätze, Endschalter, Not-Aus, Kabel | **~90–120** |
| **B – Hand J4–J6 + Greifer** | 3 Motoren, 3× TMC2209, Lager, Riemen, Servo, 5-V-Wandler, Kabel | **~60–80** |
| Reserve 15 %, evtl. 24-V-Netzteil (~15), evtl. stärkerer J2-Motor (~12) | | ~25–50 |
| **Gesamt realistisch** | | **~175–250** |

Stufe A liegt im Startbudget; der Gesamtarm überschreitet 150 CHF voraussichtlich (ohne neues Netzteil und ohne Zusatzmotor am unteren Ende der Spanne). Filament: ca. 2–2,5 kg PLA + ca. 0,5 kg PETG.

## 5. Vorgehen in Phasen (jede endet mit einem Gate)

0. **Projektgerüst** – Ordner, lokales Git-Repo, `README.md`, Anforderungen, Parameterliste. Das Projekt läuft vollständig lokal (Entscheid vom 11.10.2026: keine Cloud-Sitzung, kein GitHub-Repo).
1. **Detailkonzept** – vorhandene Motoren + Netzteil vermessen; Python-Kinematik mit Arbeitsraum- und Momentensimulation (bestätigt Armlängen und Untersetzungen **vor** dem CAD); Board-Pinmapping prüfen; definitive BOM Stufe A mit AliExpress-Suchbegriffen. *Gate: Agent-Review.*
2. **Getriebe-Prüfstand (Risiko zuerst)** – Varianten (a)/(b)/(c) als Module in Fusion konstruieren, drucken, mit Uno + CNC-Shield antreiben. *Gate mit Grenzwerten:* Umkehrspiel gemäss Fehlerbudget (unbelastet und unter ±2 Nm Wechsellast); Steifigkeit J2 ≥ 30 Nm/°; 24-h-Haltetest unter 7 Nm mit Winkeldrift ≤ 0,1° (Kriechen/Seilvorspannung); Spiel nach 10 000 Zyklen; Erwärmung. Die beste Variante wird Standardmodul.
3. **CAD Stufe A:** Kaufteil-Dummys → Basis/J1 → Schulter/J2 → Oberarm/J3, inkl. Kabelführung, Endanschlägen, Sensoren. Pro Baugruppe Interferenz-/Druckbarkeitsprüfung + Agent-Review.
4. **Bau Stufe A** – drucken, montieren, Board + Firmware für 3 Achsen in Betrieb nehmen (inkl. Not-Aus, Referenzfahrt), mit Testgewicht anstelle der Hand prüfen (Genauigkeit, Haltetest).
5. **CAD + Bau Stufe B:** Unterarm/J4 → Handgelenk J5/J6 → Flansch → Greifer.
6. **Verkleidung und Elektronikgehäuse.**
7. **Elektronik & Firmware komplett** – Verdrahtungsplan, grbl-Mega-5X, Referenzfahrt, Soft-Limits, Not-Aus.
8. **Software & Kalibrierung** – Jog-UI, Wiederholgenauigkeit messen, Abgleich mit Abschnitt 2.
9. **Dokumentation finalisieren** – Bauanleitung mit Renderings/Explosionsbildern, BOM, Verdrahtung, Inbetriebnahme, Fehlersuche.
10. **Später:** Kamera-KI, Greiferwechsler, evtl. Closed-Loop-Motoren.

Die Dokumentation wächst in jeder Phase mit.

## 6. Prüfverfahren (Regel des Nutzers)
Jede zu prüfende Idee/Baugruppe geht an einen **unabhängigen Agenten**: Note 1–10 (0–4 unbrauchbar · 5–7 gut mit Verbesserungspotenzial · 8–10 nahezu perfekt). **Maximal 3 Runden pro Aufgabe**, danach bleibt der Stand. Protokoll in `docs/reviews/`.

## 7. Fusion-360-Arbeitsweise
- Alle Masse als Benutzerparameter (`create_parameter`), ein Bauteil = eine Komponente, klare Namen (`J2_Gehaeuse_A`).
- MCP-Einheit: **cm**. Eine Operation pro Aufruf, Ergebnis prüfen.
- Kontrolle: `check_interference`, `create_section_analysis`, `get_physical_properties` (Massen → Lastrechnung nachführen), `add_joint` für Bewegungsprüfung.
- Ausgabe: `export_stl`/`export_step` je Teil, `render_view`/`export_view_sheet` für Anleitungsbilder.
- Drucktoleranzen als Parameter (Lagersitz, Passung, Einschmelzgewinde) – nach einem Toleranz-Testdruck kalibrieren.

## 8. Projektstruktur (wird angelegt)
```
README.md
docs/        anforderungen.md, konzept.md, lastrechnung.md, bom.md, sicherheit.md,
             bauanleitung/ (Schritte + Bilder), verdrahtung.md, reviews/
cad/         export/stl, export/step, renders/
firmware/    grbl-Mega-5X-Konfiguration
software/    Python-Paket (Kinematik, Simulation, Steuerung, UI), tests/
```

## 9. Verifikation
- Simulation (Phase 1): Momente aller Gelenke über den Arbeitsraum < verfügbares Moment mit Sicherheit ≥ 1,5.
- Prüfstand: Messwerte gegen Fehlerbudget Abschnitt 2.
- CAD: keine Interferenzen über den Gelenkbereich, Teile im Bauraum, Fusion-Massen bestätigen die Lastrechnung.
- Software: Unit-Tests FK→IK→FK.
- Gesamt: Referenzfahrt-Wiederholbarkeit; 50× Punkt anfahren mit Messuhr; 0,5 kg ausgestreckt 30 min halten (Erwärmung, Kriechen); Not-Aus- und Stromausfalltest.

## 10. Hauptrisiken
- Getriebespiel/-verschleiss → Variantenvergleich in Phase 2, bevor der Arm konstruiert wird.
- PLA-Kriechen, Motorwärme → PETG-Motorplatten, Federausgleich, Lüftung.
- Schrittverlust (offener Regelkreis) → Sicherheit > 2 an J2, Referenzfahrt, späterer Closed-Loop-Pfad.
- Budget: Gesamtarm voraussichtlich 175–250 CHF statt 150 → Ausbaustufen.
- Capstan: Seilkriechen und lastabhängige Nachgiebigkeit (~0,1° bei Lastwechsel 0→0,5 kg) → Haltetest im Prüfstand, Nachspannung, ggf. Variante (c).
