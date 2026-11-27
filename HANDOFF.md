# HANDOFF – KI-Integrierter Roboterarm (Stand 27.11.2026 abends; Details: README.md, docs/konzept.md, index.md)
## Ziel
6-Achs-Desktop-Roboterarm (3D-Druck, NEMA 17) auf 1000-mm-Schiene (später); Hobbyarm, Nachbau ohne Fummelei. Optik in der Formsprache des Arctos-Arms (Weg 1: eigenes Design, keine Arctos-Dateien/Masse). Claude konstruiert alles, Nutzer druckt/baut/misst.
## Stand
- Gestaltung V4 (Low-Poly-Schalen, beidseitige Gabeln) vom Nutzer so akzeptiert: cad/skripte/arm_gestaltung_v4.py (FUSS = "B"), Renders cad/renders/arm_gestaltung_v4*.png.
- J2-Endstufe geändert (Entscheid Nutzer): 5M 18:72 mit **25-mm-Riemen**, Stufe 2 3M 16:80 (72:1 bleibt), Scheibe Ø 115 statt 143; parameter.md, konzept.md. Erklärbild cad/renders/j2_antrieb_variante_b.png.
- **Basis mit J1 V2.2 konstruiert:** cad/skripte/basis_j1.py (Fusion-Komponente Basis_J1), Montageprüfung montage_basis.py (Endzustand, Drehung ±170°, Einschiebewege, Werkzeugzugang, Wand um Einsätze) ohne Meldung. Gutachten 5 → 6 → 7/10, Nachprüfung Claude 8/10 (docs/reviews/2026-11-26-basis-j1.md). Beschreibung docs/basis-j1.md, Stückliste docs/stuecklisten/basis-j1.md, Schnittstelle Säule in parameter.md.
- STL exportiert (cad/export/stl/Basis_J1/, Druckeinstellungen.md): Passproben + alle Teile ausser Grundplatte, Nabe, Spannring (nach Passprobe 6810) und Schalterhalter (nach Ausmessen KW11).
## Entscheidungen
- J1 ±170° (340°), kein Schleifring. Anschlag ±173°, Referenz an der Halbmond-Flanke bei 0°. Motorstrom J1 1,0 A.
- Lager 6810ZZ/608ZZ ok (nicht offen). O-Ring **OD 52 × 1,5** (ID 49, Wahl 27.11.; 2 % Dehnung in der Nut, gerechnet). 3M-Riemen 318 mm, GT2 240 mm.
- Schalen mit Magneten 6×3 abnehmbar; Holzplatte mit Schraubzwingen am Regal (sonst kippt der Arm).
- Bestand Nutzer: PLA grau/rot/weiss, PETG weiss nur Notfall, 120 Magnete, M3-Einsätze, M5 8–20 mm, Schraubzwingen.
## Offen
- Basis-Teile: Warenkorb geprüft (Stand 27.11. in docs/stuecklisten/basis-j1.md), **Bestellung noch nicht bestätigt** (Nutzer meldet «bestellt»). Black Friday bis 3.12.
- Passprobe 6810 drucken/melden → L6810 nachführen → Grundplatte/Nabe/Spannring exportieren. KW11 ausmessen → Schalterhalter.
- J1-Test mit ESP32 + Shield (noch zusammengebaut): FluidNC-Konfig und Steuerseite für J1, Vref ca. 1,41 V, Endschalter NC an GPIO (z. B. 32), Adernfolge Motorstecker messen.
- Ab 16.12. (Windows-Erinnerung auf diesem PC): Octopus Pro F446 V1.0 und Pult-Teile (docs/offene-ideen.md Nr. 8), Relais-Schaltung Not-Aus zeichnen.
- Steckerfeld mit der Säule konstruieren; Kabelschlaufe ±170° in der Säule.
- Früher offen: Gutachten 3.9 Runde 3, Rücklauf ohne Netzteil, Rücklauf J3, Aufprallenergie, 70er-GT2-Scheibe J3.
## Nächster Schritt
Säule mit Schulter J2 konstruieren (Antrieb Variante B, Bremse hinter Motor, Feder-Bauraum, Parkanschlag), auf die Schnittstelle 120 mm / Ø 65 der Basis.
## Dateien
cad/skripte/basis_j1.py, montage_basis.py, render_basis.py, kollision.py, arm_gestaltung_v4.py; docs/basis-j1.md, docs/stuecklisten/basis-j1.md, docs/reviews/2026-11-26-basis-j1.md; Fusion: aktives Dokument mit Komponenten Basis_J1 und Arm_Gestaltung_V4 (per Skript neu erzeugbar)
