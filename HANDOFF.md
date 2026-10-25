# HANDOFF – KI-Integrierter Roboterarm (Stand 25.10.2026; Details: README.md, docs/konzept.md, index.md)
## Ziel
6-Achs-Desktop-Roboterarm (3D-Druck, NEMA 17, BTT Octopus + grblHAL) auf 1000-mm-Schiene, später Kamera-KI und Greiferwechsel. Aktuell: Prüfstand J2 aufbauen, dann Motoren vermessen.
## Stand
- J2-Prüfstand (CAD 8/10, cad/skripte/j2_pruefstand.py): Rahmen, Z90 mit Hebel/Zeiger und Messuhrhalter montiert, alle 41 M3-Einsätze gesetzt. Bauanleitung docs/bauanleitung/Bauanleitung_J2_Pruefstand.pdf, Druckeinstellungen im J2-STL-Ordner.
- Toleranzen (CLAUDE.md, docs/parameter.md): Lagersitz 608 liegend Ø 22,20; Zapfen Ø 10 Haltesitz 10,10; M3-Einsatz Bohrung 4,0.
- Motorprüfstand (8/10): STL cad/export/stl/Motorpruefstand/, Messungen docs/motorvermessung.md.
- 25.10. Elektrik-Schema J2: Verdrahtungsliste docs/schema/verdrahtung-j2.md (Grundlage). KiCad 10: cad/skripte/kicad_j2_schema.py → cad/kicad/j2-pruefstand/, PDF docs/schema/j2-pruefstand-kicad.pdf (ERC ohne Fehler, Netzliste geprüft). QElectroTech 0.100: cad/skripte/qet_j2_schema.py → cad/qet/j2-pruefstand.qet, Vorschau docs/schema/j2-pruefstand-qet-vorschau.png (in QET geladen, Verbindungen stimmen). Beide installiert (winget). Kein MCP nötig, beide per Skript erzeugt.
- Elektrik-Bestand (Nutzer): Mean Well LRS-350-24 (docs/LRS-350.pdf), Einbaukaltstecker C14, 1 Sicherung T 3,15 A 250 V + Halter, Kfz-Sicherung 3 A + Halter, Litze Radox 155 1,00 mm² rot/schwarz, Ringschuhe, Arduino Uno + USB-Kabel, Schrauben, Lager, Holzplatte, Messuhr, Kofferwaage.
## Entscheidungen
- 1 kg Nutzlast überall; Schiene als 7. Achse; nur Zahnriemen; Waagebalken; Open Loop. 24 V: rot +, schwarz 0; Kfz-Sicherung 3 A in +24 V; 230-V-Seite nur Entwurf, Elektriker (Opa) prüft/gibt frei.
## Offen
- AliExpress-Warenkorb 25.10. geprüft (Produktseiten, Stückliste nachgeführt): GT2-Ritzel (XIAOXI, 5 mm / 10 mm) ersetzt, jetzt richtig. Warenkorb hat 14 Artikel in 2 Gruppen (Gruppe «globale Verkäufer» lädt erst nach Scrollen): dort HTD-5M-Ritzel (8 mm/15 mm/18 Z, Nabenmasse unbekannt → messen), alle 3 Riemen, M3-Einsätze 100 Stück. Fehlen: 4 Wellen 8 × 100. HTD-3M-Ritzel (Nabe Ø 18, ca. 13 mm lang) gegen CAD prüfen. SN-58B crimpt Dupont, Flachstecker, Ringschuhe (0,25–1,5 mm²), vermutlich keine Aderendhülsen.
- Typenschild LRS-350-24 bestätigen (230-V-Umschalter!). Halter F2: Standard/Mini. Aderendhülsen, Kaltgerätekabel C13, Schalter/Gehäuse 230 V mit Opa klären. Vref/Jumper TMC2209 eintragen. docs/LRS-350.pdf bleibt lokal (nicht im Repo), Rückfrage Urheberrecht offen. QET-Menü französisch (Konfiguration → Sprache).
- Aufreiben: Z90-/Hebelbohrung 8,0, Z72 3,0, Z64 3,9. Brett bohren, Spannrollen/Hülsen/Z64 (gedruckt?) klären.
## Nächster Schritt
Opa zeigt QET-Plan/PDF, Rückmeldung einarbeiten; Typenschild bestätigen; Schema und Stückliste committen (nach Rückfrage); dann Zusammenbau J2 und Motor anschliessen (Vref messen).
## Dateien
Fusion «Claude Roboterarm v1» (J2); Repo github.com/Technoraily/KI-Integrierter-Roboter
