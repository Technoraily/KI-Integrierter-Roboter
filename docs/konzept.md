# Projektplan: 6-Achs-Roboterarm «von Grund auf» (PLA, BambuLab A1, AliExpress-Teile)

*Stand 11.10.2026: Gesamtkonzept 8/10, Detailkonzept 8/10, Steuerung für 7 Achsen 8/10; Antrieb: alle Achsen über Zahnriemen (GT2 und HTD), Schultergelenk wird als Prüfstand gebaut. Protokolle in `docs/reviews/`.*

## 1. Kontext

Ziel ist ein selbst konstruierter, vollwertiger 6-Achs-Desktop-Roboterarm – ausdrücklich **kein** abgespecktes Baukit. Er soll Aufgaben zuverlässig und so präzise wie in PLA möglich erledigen, eine saubere Verkleidung haben, mit Standardteilen von AliExpress auskommen und möglichst wenig Kaufteile brauchen. Konstruktion (Fusion 360 via MCP), bebilderte Bauanleitung und Dokumentation entstehen im Projekt selbst. Kamera-KI und automatischer Greiferwechsel folgen später, werden aber von Anfang an mechanisch/elektrisch vorgesehen.

**Festgelegt mit dem Nutzer:** 6 Achsen · ca. 400–450 mm Reichweite · 1 kg Nutzlast im ganzen Arbeitsraum · Kaufteile wenn machbar < 150 CHF für den Anfang · vorhanden: 3× NEMA 17 (17CS04A-170E), Arduino Uno + CNC-Shield + A4988, Netzteil 12 V / 4 A, Küchenwaage, Kleinteile.

**Massgebende Zahlen:** Untersetzungen, Motoren und Lasten stehen aktuell in `docs/parameter.md` und `docs/lastrechnung.md`; dieses Dokument beschreibt Architektur und Vorgehen.

**Ausgangslage:** Projektordner `C:\Claude\KI-Integrierter Roboter` ist leer, kein Git-Repo. Fusion-360-MCP antwortet (ping OK).

## 2. Zielspezifikation (messbar, wird in Phase 8 geprüft)

| Grösse | Ziel |
|---|---|
| Freiheitsgrade | 6 (Knickarm mit Zentralhand → geschlossene inverse Kinematik) |
| Reichweite Schulter → Flansch | 450 mm (Oberarm 200, Unterarm 190, Hand 60) – in Phase 1 per Simulation bestätigt |
| Nutzlast | **1 kg im ganzen Arbeitsraum** (Entscheid 11.10.2026, durch Lastrechnung bestätigt). Zusätzlich 150 g Reserve am Flansch für Werkzeugwechsler + Kamera |
| Wiederholgenauigkeit | ≤ ±0,5 mm, **unidirektional nach Referenzfahrt, bei gleichbleibender Last**; Wunsch ±0,3 mm |
| Gelenkgeschwindigkeit | J2/J3 ≥ 25°/s, Handachsen ≥ 90°/s (Grenze ist die Momentenkurve der Motoren, nicht die Schrittrate) |
| Grösstes Druckteil | ≤ 240 × 240 × 240 mm |

**Fehlerbudget (aus dem Flanschziel rückwärts gerechnet; 0,1° an 450 mm = 0,8 mm):**
- J1 (keine Schwerkraft-Vorspannung): Umkehrspiel ≤ 0,05° → spielfreie Bauart zwingend.
- J2/J3: durch Schwerkraft + Ausgleichsfeder einseitig anliegend; Umkehrspiel ≤ 0,3° zulässig, dafür Steifigkeit als Messgrösse (Nm/°).
- J4/J5: ≤ 0,15° (wirkt bis zur Greiferspitze, ~140 mm Hebel); J6: ≤ 0,3°.
- Wiederholbarkeit der Referenzsensoren wird separat gemessen – sie begrenzt die Genauigkeit direkt.

## 3. Architekturentscheide

### 3.1 Steuerung – Abweichung vom Wunsch (begründet; neu gewählt am 11.10.2026 wegen der 7. Achse)
- **Anforderung:** Arm und Schiene fahren koordiniert, z. B. bleibt der Greifer an einem Punkt im Raum stehen, während der Arm auf der Schiene fährt. Dafür müssen **alle 7 Achsen synchron von einer Steuerung** interpoliert werden.
- **Was deshalb ausscheidet:** Uno + CNC-Shield (GRBL kann 3 Achsen) und das zuvor geplante Mega-Board mit `grbl-Mega-5X` (höchstens 6 Achsen).
- **Board: BTT Octopus mit STM32F446** (v1.1 oder Pro, ca. 45 CHF): 8 Treibersockel, 8 Endschalter-Eingänge, 24 V. Beim Kauf auf die MCU **F446** achten – die Varianten mit H723 passen nicht zur Firmware. Vor der Bestellung den Schaltplan des v1.1 gegen die Pro-Pinbelegung prüfen.
- **Firmware: grblHAL mit 7 Achsen** (kann 3–8 Achsen, hat eine Board-Map für den Octopus, unterstützt G93, bis 300 kHz Schrittrate). Bleibt in der GRBL-Welt: `$`-Einstellungen, `$H`, Statusabfrage, Streaming-Protokoll. **Marlin 2.1 (bis 9 Achsen) ist die Rückfallebene.** 7 Achsen unter grblHAL sind im Feld wenig erprobt → früher Machbarkeitstest (Phase 4).
- **Achszuordnung:** J1–J3 = X/Y/Z, J4–J6 = A/B/C, Schiene J0 = U. Die Firmware behandelt alle als reine Einheiten (Grad bzw. mm).
- **Treiber:** 7× TMC2209 im Standalone-Betrieb (UART ist unter grblHAL auf diesem Board ungetestet), 24 V, Kühlkörper + Lüfter.
  - J2, J3, J5 (schwerkraftbelastet): **voller Haltestrom**, Motoren dauernd bestromt (`$1=255`).
  - J0, J1, J4, J6: Stillstandsstrom-Absenkung.
  - Offen: Im Standalone-Betrieb wird die Absenkung über den PDN-Pin je Sockel gewählt; wie das auf dem Octopus per Jumper geht, wird beim Machbarkeitstest geklärt.
- **Greifer-Servo:** Die Board-Map hat keinen Servo-Ausgang. Der Servo läuft deshalb über den **vorhandenen Arduino Uno**, den Python per USB anspricht. Vor jedem Greiferbefehl fragt Python den Status ab und wartet, bis der Planerpuffer leer und die Bewegung beendet ist («Idle») – sonst greift der Arm, während noch Sätze laufen. Alternative: einen freien Pin in der Board-Map umdefinieren.
- **Uno + CNC-Shield + A4988** bleiben im Einsatz: Prüfstand-Steuerung (Phase 2), danach Greifer-Servo und später Greiferwechsel-Station.
- **Aufgabenteilung:** Die Firmware fährt nur Gelenk-Sollwerte synchron. Kinematik, Bahnplanung und später Kamera/KI laufen in **Python auf dem PC**.
- **Koordinierte Bewegung:** Python zerlegt die Fahrt in kurze Stücke, rechnet für jeden Stützpunkt die Gelenkwinkel und sendet Sätze mit allen 7 Achsen; die Firmware interpoliert dazwischen linear und synchron.
  - Für «Greifer steht, Schiene fährt» genügt die vorhandene 6-Achs-Rückwärtskinematik mit einem um den Schienenweg verschobenen Ziel.
  - **Adaptive Stückelung:** Start bei 5 mm Schienenweg, halbieren, bis der Fehler in der Segmentmitte unter 0,05 mm liegt (nötig nahe Singularitäten).
  - **Jeder Satz mit G93** (Zeitvorgabe statt Vorschub), weil der Vorschub bei gemischten Linear- und Drehachsen sonst mehrdeutig ist.
- **Ehrliches Genauigkeitsziel für «Greifer steht»: ±0,5–1 mm.** Das verlangt Absolutgenauigkeit. Der Engpass ist nicht die Stückelung, sondern die Ausrichtung der Schiene (0,1° Richtungsfehler = 1,7 mm über 1000 mm), die Nachgiebigkeit der Antriebe und Fehler in Nullpunkten und Armlängen. Die Schienenrichtung wird deshalb vermessen und in der Software hinterlegt.

### 3.2 Antriebe
**Entscheid des Nutzers vom 11.10.2026: alle Achsen laufen nur über Zahnriemen, kein Seiltrieb.** GT2 (2-mm-Zähne) überall dort, wo die Riemenkraft klein ist; HTD (3- bzw. 5-mm-Zähne, 15 mm breit) in den Stufen mit hoher Kraft. Hintergrund und Zahlen: `docs/reviews/2026-10-11-antrieb-j2-j3.md`.

| Gelenk | Motor | Untersetzung | Stufe 1 | Stufe 2 | Stufe 3 |
|---|---|---|---|---|---|
| J0 Schiene | NEMA 17 (neu) | – | GT2 10 mm, Ritzel 20 Z, offener Riemen | – | – |
| J1 Basis | NEMA 17 (vorhanden) | 20:1 | GT2 10 mm, 20 : 80 | HTD-3M 15 mm, 16 : 80 | – |
| J2 Schulter | NEMA 17 60 mm (neu) | 72:1 | GT2 10 mm, 20 : 72 | HTD-3M 15 mm, 16 : 64 | HTD-5M 15 mm, 18 : 90 |
| J3 Ellbogen | NEMA 17 (vorhanden), Motor nahe Schulter | 60:1 | GT2 10 mm, 16 : 60 | HTD-3M 15 mm, 16 : 64 | HTD-5M 15 mm, 15 : 60 |
| J4 Unterarm-Rolle | NEMA 17 (vorhanden) | 20:1 | GT2 10 mm, 20 : 100 | HTD-3M 15 mm, 16 : 64 | – |
| J5 Hand-Nicken | NEMA 17 34 mm (neu), im Unterarm | 18,75:1 | GT2 10 mm, 16 : 80 | HTD-3M 15 mm, 16 : 60 | – |
| J6 Flansch-Rolle | NEMA 14 (neu) | 8:1 | GT2 10 mm, 16 : 40 | GT2 10 mm, 16 : 50 | – |

- **Regel:** zulässige Riemenkraft GT2 10 mm ca. 44 N, HTD-3M 15 mm ca. 168 N, HTD-5M 15 mm ca. 268 N (Herstellertabelle, vom Gutachter nur teilweise gegengeprüft). Die letzte Stufe jedes Gelenks trägt das volle Gelenkmoment; deshalb reicht GT2 dort nur an J6 und an der Schiene.
- **J2 und J3** sind vom Gutachter durchgerechnet. **J1, J4, J5 und J6 sind eine eigene Auslegung nach derselben Regel und noch nicht begutachtet**; sie werden mit dem CAD der jeweiligen Baugruppe geprüft.
- **Trumkräfte J2:** Stufe 1: 26 N dauernd / 46 N Spitze; Stufe 2: 77 / 138 N; Stufe 3: 164 / 294 N. Stufe 3 ist in der Spitze leicht überlastet (Faktor 1,1) → falls der Prüfstand das bestätigt, 25 mm Breite.
- **Bauweise:** Kleine Scheiben (16–20 Zähne) sind gekaufte Aluscheiben, grosse werden gedruckt (PETG). Zwischenwellen 8 mm Stahl in 608-Lagern. Ob Zwischenstufen als ein Druckteil (grosses Rad + kleines Ritzel) auf fester Achse laufen oder auf mitdrehenden Wellen sitzen, entscheidet das CAD.
- **Erwartete Schwächen gegenüber einem spielfreien Antrieb** (Schätzung des Gutachters, der Prüfstand misst nach): 0,05–0,15° Umkehrspiel in der HTD-Endstufe (0,4–1,2 mm am Flansch) und 30–100 Nm/° Steifigkeit. J2 schwenkt über die Senkrechte, dort wechselt das Schwerkraftmoment das Vorzeichen und das Spiel wirkt voll.
- **Verworfen:** «alles GT2» auch in der Endstufe (3/10, Riemen 3- bis 6-fach überlastet); Seiltrieb (7/10, vom Nutzer nicht gewünscht); gedrucktes Zykloidgetriebe (nur letzte Rückfallebene).
- **Prüfstand:** das Schultergelenk J2 in Originalgrösse (siehe Phase 2).
- **Lastrechnung:** siehe `docs/lastrechnung.md` (1 kg ausgestreckt: Schulter 11,8 Nm, Sicherheit 1,8 bei vorsichtigem Wirkungsgrad 0,65 für drei Riemenstufen). Gerechnet wird mit dem **nutzbaren Moment bei Betriebsdrehzahl** (ca. 70 % des Haltemoments, gültig bis ca. 300–500 U/min), nicht mit dem Haltemoment. An J2 ergibt das rund 33°/s; die Schrittrate ist nicht der Engpass.
- Die Motoren werden als erster Schritt von Phase 2 **vermessen** (`docs/motorvermessung.md`: Länge, Wicklungswiderstand, Haltemoment mit Hebel + Waage, Drehzahltest an 24 V); danach wird die Tabelle fixiert.

### 3.3 Lagerung und Struktur
- **J1: zwei gekaufte Dünnringlager (6810/6813, je ~3–5 CHF)** mit ≥ 40 mm Abstand, vorgespannt, Hohlwelle für Kabel. (Gedrucktes Kugellager nur als Experiment auf dem Prüfstand – Kippspiel an J1 wirkt mit vollem Hebel.)
- J2–J6: Standard-Rillenkugellager paarweise vorgespannt.
- Tragstruktur als geschlossene Schalen; **Verkleidung als separate, geclipste/verschraubte Deckel**.
- M3/M4 + Einschmelzgewinde, Passstifte für Wiederholbarkeit.
- **Materialwahl (PETG vom Nutzer freigegeben):** PLA bleibt Standard für Tragschalen und Verkleidung (steifer). **PETG für wärme- und kriechkritische Teile:** Motorplatten, Spannelemente, Teile direkt am Motor. Bei Getriebeteilen (Riemenscheiben) entscheidet der Prüfstand zwischen PLA und PETG. Belüftete Motorräume.
- Kabelführung ist Teil der Tragstruktur-Konstruktion (Hohlwellen-Durchmesser, Verdrehwinkel), nicht Nacharbeit.

### 3.4 Sicherheit
- Not-Aus-Taster, der die Motorspannung trennt **und der Firmware ein Signal gibt** (sonst rechnet sie mit einer verlorenen Position weiter); Sicherung; Zugentlastungen.
- Schiene: Endschalter an beiden Enden als harte Grenze.
- **Stromausfall:** Arm ist rückdrehbar → Ausgleichsfeder so auslegen, dass er langsam sinkt; definierte Parkposition.
- Mechanische Endanschläge an jeder Achse + Soft-Limits in der Firmware; Quetschstellen in der Verkleidung vermeiden.

### 3.5 Vorbereitung für später (nur vorsehen)
- **Werkzeugflansch ISO 9409-1-31,5-4-M5** → Schnittstelle für Greiferwechsler (kinematische Kupplung + Magnete + Pogo-Pins).
- Kabelkanal bis zum Flansch (≥ 6 Adern + USB), Kamera-Schraubpunkte am Handgelenk.
- Erster Greifer: Servo-Parallelgreifer am ISO-Flansch (5-V-Wandler vorgesehen).

### 3.6 Software
Python-Paket: Vorwärts-/Rückwärtskinematik (analytisch), Arbeitsraum- und Momentensimulation, Stückelung koordinierter 7-Achs-Bewegungen, G-Code-Streaming, Jog-Oberfläche, Teach-&-Playback, Kalibrierung. Später: OpenCV, Hand-Auge-Kalibrierung, KI-Aufgabenplanung.

### 3.7 Schiene J0 (ergänzt 11.10.2026, Bau als Stufe C)

Der ganze Roboter steht auf einem Schlitten, der ihn auf einer Schiene verfährt. Übersicht: `docs/bilder/uebersicht.png`.

- **Verfahrweg ca. 1000 mm**, Schiene rund 1250 mm lang.
- **Führung:** zwei parallele Linearführungen (MGN12) auf Aluprofilen, Spurweite ≥ 150 mm. Zwei Führungen sind nötig, weil der ausgestreckte Arm mit 1 kg ein Kippmoment von rund 12 Nm auf den Schlitten bringt.
- **Antrieb:** NEMA 17 (ein vierter 40-mm-Motor, neu) mit offenem GT2-Riemen 10 mm; Kabel in einer Schleppkette.
- **Steuerung:** als siebte Achse (U) auf demselben Board wie der Arm, voll synchron (siehe 3.1). Der separate Uno für die Schiene entfällt.
- **Kalibrierung:** Richtung der Schiene im Koordinatensystem des Arms messen und in der Software hinterlegen; Referenzfahrt-Reihenfolge für alle 7 Achsen festlegen.
- **Jetzt schon vorgesehen:** Die Basis bekommt ein Lochbild für den Schlitten (4× M5 auf 120 × 120 mm), damit die Schiene später ohne Umbau darunterkommt. Bis dahin wird die Basis mit denselben Löchern auf eine Platte geschraubt.
- **Offen für Stufe C:** Führungen und Profile mit 1250 mm Länge sind auf AliExpress teuer im Versand oder gar nicht lieferbar; evtl. Profile lokal beziehen oder die Schiene aus zwei Stücken stossen. Genauigkeit der Schiene (Ziel ≤ ±0,1 mm) und ebene Unterlage.

## 4. Kosten Kaufteile (AliExpress, ehrlich gerechnet)

Der Arm wird in Ausbaustufen gebaut. Das ursprüngliche Startbudget von 150 CHF reicht nach den Erweiterungen (1 kg aussen, 7 synchrone Achsen) nur noch für die erste Bestellung (Prüfstand, ca. 95 CHF):

| Stufe | Inhalt | CHF |
|---|---|---|
| **A – Prüfstand + J1–J3** | Board (BTT Octopus), 3× TMC2209 + Kühlung, Lager, Riemen/Scheiben, Feder, Schrauben/Einsätze, Endschalter, Not-Aus, Kabel, dazu J2-Motor, 24-V-Netzteil, Messuhr, Thermometer (Details: `docs/bom.md`) | **~200** |
| **B – Hand J4–J6 + Greifer** | 2 Motoren, Lager, Riemen/Scheiben, Servo, 5-V-Wandler, Kabel | **~65** |
| Reserve 15 % | | ~40 |
| **Arm gesamt realistisch** | | **~310** |
| **C – Schiene 1000 mm** (später) | 2 Linearführungen, Aluprofile, Motor, Riemen, Schleppkette, Endschalter | **~100–120** |

Mit Schiene rund 425 CHF. Alle Preise sind Schätzungen. Filament: ca. 2–2,5 kg PLA + ca. 0,5 kg PETG.

## 5. Vorgehen in Phasen (jede endet mit einem Gate)

0. **Projektgerüst** – Ordner, lokales Git-Repo, `README.md`, Anforderungen, Parameterliste. Das Projekt läuft vollständig lokal (Entscheid vom 11.10.2026: keine Cloud-Sitzung, kein GitHub-Repo).
1. **Detailkonzept** (abgeschlossen, Gutachten 8/10) – Python-Kinematik mit Arbeitsraum- und Momentensimulation (bestätigt Armlängen und Untersetzungen **vor** dem CAD); definitive BOM Stufe A mit AliExpress-Suchbegriffen. *Gate: Agent-Review.*
2. **Getriebe-Prüfstand (Risiko zuerst)** – erster Schritt: Haltemoment der vorhandenen Motoren mit gedrucktem Hebel und Waage messen (`docs/motorvermessung.md`) und die Lastrechnung damit bestätigen. Dann das J2-Modul (drei Riemenstufen) in Fusion konstruieren, drucken und mit Uno + CNC-Shield antreiben. *Gate mit Grenzwerten:* Umkehrspiel gemäss Fehlerbudget (unbelastet und unter ±2 Nm Wechsellast); Steifigkeit J2 ≥ 30 Nm/°; 24-h-Haltetest unter 11 Nm mit Winkeldrift ≤ 0,1° (Kriechen der Lagersitze, Riemenspannung); Spiel nach 10 000 Zyklen; Erwärmung. Besteht das Modul, wird es Standard für J2 und (kleiner) J3; sonst wird die Endstufe verbreitert oder die Nutzlast gesenkt.
2b. **Machbarkeitstest Steuerung** – sobald das Board da ist, ohne Mechanik: grblHAL mit 7 Achsen, 7 Treiber, die vorhandenen Motoren reihum umgesteckt, Streaming mit G93 aus Python, Not-Aus-Signal, Servo-Weg (Prüfpunkte in `docs/verdrahtung.md`). **Abbruchkriterium:** Lässt sich grblHAL nicht mit 7 Achsen kompilieren und flashen, oder fahren nicht alle 7 Achsen in einem Satz synchron, wird auf Marlin gewechselt.
3. **CAD Stufe A:** Kaufteil-Dummys → Basis/J1 → Schulter/J2 → Oberarm/J3, inkl. Kabelführung, Endanschlägen, Sensoren. Pro Baugruppe Interferenz-/Druckbarkeitsprüfung + Agent-Review.
4. **Bau Stufe A** – drucken, montieren, Board + Firmware in Betrieb nehmen (inkl. Not-Aus, Referenzfahrt), mit Testgewicht anstelle der Hand prüfen (Genauigkeit, Haltetest).
5. **CAD + Bau Stufe B:** Unterarm/J4 → Handgelenk J5/J6 → Flansch → Greifer.
6. **Verkleidung und Elektronikgehäuse.**
7. **Elektronik & Firmware komplett** – Verdrahtungsplan, grblHAL mit 7 Achsen, Referenzfahrt, Soft-Limits, Not-Aus.
8. **Software & Kalibrierung** – Jog-UI, Wiederholgenauigkeit messen, Abgleich mit Abschnitt 2.
9. **Dokumentation finalisieren** – Bauanleitung mit Renderings/Explosionsbildern, BOM, Verdrahtung, Inbetriebnahme, Fehlersuche.
10. **Stufe C: Schiene J0** – Schlitten, Führungen, Riemenantrieb, siebte Achse am Board, Kalibrierung der Schienenrichtung, koordinierte Bewegungen in der Python-Software.
11. **Später:** Kamera-KI, Greiferwechsler, evtl. Closed-Loop-Motoren.

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
firmware/    grblHAL-Konfiguration
software/    Python-Paket (Kinematik, Simulation, Steuerung, UI), tests/
```

## 9. Verifikation
- Simulation (Phase 1): Momente aller Gelenke über den Arbeitsraum < verfügbares Moment mit Sicherheit ≥ 1,5.
- Prüfstand: Messwerte gegen Fehlerbudget Abschnitt 2.
- CAD: keine Interferenzen über den Gelenkbereich, Teile im Bauraum, Fusion-Massen bestätigen die Lastrechnung.
- Software: Unit-Tests FK→IK→FK.
- Gesamt: Referenzfahrt-Wiederholbarkeit; 50× Punkt anfahren mit Messuhr; 1 kg ausgestreckt 30 min halten (Erwärmung, Kriechen); Not-Aus- und Stromausfalltest.

## 10. Hauptrisiken
- Getriebespiel/-verschleiss → Prüfstand mit Gate in Phase 2, bevor der Arm konstruiert wird.
- PLA-Kriechen, Motorwärme → PETG-Motorplatten, Federausgleich, Lüftung.
- Schrittverlust (offener Regelkreis) → Sicherheit ≥ 1,8 an allen Gelenken (vorsichtig gerechnet), Referenzfahrt, späterer Closed-Loop-Pfad.
- Budget: Arm rund 310 CHF, mit Schiene rund 425 CHF statt der anfangs gewünschten 150 → Ausbaustufen, erste Bestellung ca. 95 CHF.
- Riemenantrieb an J2/J3: Umkehrspiel und Nachgiebigkeit der HTD-Endstufe sind nur geschätzt; drei Stufen brauchen Platz (ca. 60–70 mm Breite) → Prüfstand misst beides, bevor der Arm konstruiert wird.
- Motormomente der vorhandenen Motoren sind noch Annahmen → Messung als erster Schritt von Phase 2; J3 ist am empfindlichsten.
