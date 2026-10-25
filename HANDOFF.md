# HANDOFF – KI-Integrierter Roboterarm (Stand 25.10.2026 abends; Details: README.md, docs/konzept.md, index.md)
## Ziel
6-Achs-Desktop-Roboterarm (3D-Druck, NEMA 17, BTT Octopus + grblHAL) auf 1000-mm-Schiene, später Kamera-KI und Greiferwechsel. Aktuell: Prüfstand J2 aufbauen, dann Motoren vermessen.
## Stand
- J2-Prüfstand (CAD 8/10, cad/skripte/j2_pruefstand.py): alle 22 Druckteile gedruckt, Rahmen/Z90/Hebel/Messuhrhalter montiert, 41 M3-Einsätze gesetzt. Werkzeug, Zwingen, Filament, Kaltgerätekabel C13, Schrauben, Lager, Wellen (Opa), Multimeter, Schieblehre: da.
- Elektrik-Schema J2 (Entwurf): Verdrahtungsliste docs/schema/verdrahtung-j2.md = Grundlage. KiCad: cad/kicad/j2-pruefstand/ + PDF; QElectroTech: cad/qet/j2-pruefstand.qet + Vorschau-PNG; beide per Skript (cad/skripte/*_j2_schema.py). Motor 17HS24-2104S: AWG24, A schwarz/grün, B rot/blau, 2,1 A.
- AliExpress-Warenkorb (14 Positionen, 68,03 CHF, in 2 Gruppen, zweite lädt erst nach Scrollen) am 25.10. auf Produktseiten geprüft, vollständig; Nutzer bestellt selbst. Enthält u. a. GT2-Ritzel 5/10, HTD-3M 16 Z, HTD-5M 18 Z, 3 Riemen, 6-Backen-Crimpzange, Aderendhülsen E1008, Kfz-Halter 3 A, 2 × TMC2209.
## Entscheidungen
- 24 V: rot +, schwarz 0; Kfz-Sicherung 3 A in +24 V (Lüsterklemmen nur 24-V-Seite); 230-V-Seite nur Entwurf, Opa prüft/gibt frei. LRS-350.pdf bleibt lokal (Urheberrecht offen).
## Offen
- RISIKO HTD-3M-Ritzel: Händlerzeichnung Nabe Ø 18, Länge 29 mm; CAD Nabe Ø 14 × 6 (Ritzel z 29–53,5, Wangenabstand 56) → ca. 2–3 mm zu lang: nach Lieferung messen, Nabe kürzen (nur wenn Gewindestiftloch ≥ 4 mm vom Ende bleibt). HTD-5M-Nabe unbekannt (CAD Ø 20 × 8).
- Nach Lieferung (ca. 1.–9.11.): Ritzel messen, aufreiben (Z90/Hebel 8,0, Z72 3,0, Z64 3,9), Motorkabel Dupont crimpen, Steckbrücken fürs Shield (liegen evtl. bei), TMC2209 Vref < 2,1 A, GRBL auf Arduino, Netzteil auf 24,0 V.
- Opa: Typenschild LRS-350-24 + Umschalter 230 V, Schalter (zweipolig?) und Gehäuse 230 V, Schema prüfen/freigeben.
## Nächster Schritt
Nutzer bestellt, Opa zeigt Schema; nach Lieferung Ritzel nachmessen und gegen CAD prüfen, dann Zusammenbau J2 und Motorlauf.
## Dateien
Fusion «Claude Roboterarm v1» (J2); Repo github.com/Technoraily/KI-Integrierter-Roboter
