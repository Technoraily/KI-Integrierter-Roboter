# HANDOFF – KI-Integrierter Roboterarm (Stand 20.10.2026 abends; Details: README.md, docs/konzept.md, index.md)
## Ziel
6-Achs-Desktop-Roboterarm (3D-Druck, NEMA 17, BTT Octopus + grblHAL) auf 1000-mm-Schiene, später Kamera-KI und Greiferwechsel. Aktuell: Prüfstand J2 aufbauen, dann Motoren vermessen.
## Stand
- J2-Prüfstand (CAD 8/10, cad/skripte/j2_pruefstand.py) wird gebaut. Bauanleitung docs/bauanleitung/Bauanleitung_J2_Pruefstand.pdf + Druckeinstellungen.md im J2-STL-Ordner (Startwerte; Montagereihenfolge nur aus CAD, nicht real getestet). Skizze der Einsatzlöcher docs/bilder/einschmelz_positionen.png.
- 20.10. am Teil: alle 41 M3-Einschmelzgewinde gesetzt (Bohrung 4,0 mm bestätigt mit Lötkolben). Längen: 5 mm obere Querträger + Z90-Hebelkreis; 4 mm Z72-Nabe, Hebelnabe, Wangen-Stellschrauben, Grundbrett; 3 mm Rest. Rahmen (2 Wangen + 4 Querträger) verschraubt; Lager in Wangen, Z90+Lasthebel+Messzeiger, Messuhrhalter an rechter Wange montiert; Stellschrauben- und Passprobe gemacht. Spalt von ca. 4 mm Tiefe (Papier) an einem Hebelloch der Z90: akzeptiert.
- Toleranztest 18.10.: Lagersitz 608 liegend Ø 22,20; Zapfen Ø 10 Haltesitz 10,10 / Steckpassung 10,20 (docs/parameter.md, CLAUDE.md).
- Motorprüfstand (8/10): STL cad/export/stl/Motorpruefstand/, Anleitung-PDF docs/bauanleitung/, Messungen docs/motorvermessung.md. Rohbau: cad/skripte/rohbau_gesamt.py.
- docs/opa-liste-j2-pruefstand.pdf: Teileliste «Opa hat» (AliExpress-Korb 49.74 CHF, StepperOnline-Korb). Nichts bestellt.
- Sync über GitHub: .claude/hooks/sync-*.sh. Lokal per .gitignore: Bambu Studio Saves, pruefstand-j2*.docx (Rückfrage: veröffentlichen?).
## Entscheidungen
- 1 kg Nutzlast überall; Schiene als 7. Achse; nur Zahnriemen; Waagebalken statt Messhebel; Closed Loop vorerst nein (Open Loop mit Reserve). Ausgleichsfeder J2 nur bei Bedarf.
## Offen
- Fehlt zum Zusammenbau: 3 Wellen (zuschneiden, anfeilen), 3 Ritzel (GT2 20 Z, 3M 16 Z, 5M 18 Z mit Nabe), 3 Riemen, M8 × 90 mit Muttern/Scheiben (2), M4 × 16 (2), M3 × 12 (4, Motor), Brett bohren, Spannrollen/Hülsen/Distanzringe/Z64 (gedruckt? klären), TMC2209, Netzteil 24 V, Messuhr, Kofferwaage. Aufreiben: Z90-/Hebelbohrung 8,0, Z72 Blockierlöcher 3,0, Z64 Mitnahme 3,9. Opa-Korb prüfen (GT2-Ritzel nur 6 mm breit, nur 1 Welle, Mean Well zu gross).
- Toleranztest: Reihe B (Welle 5/8), C nur M4, M3-Durchgang; SW_LOCH 9,5, H_INNEN 58. TMC2209-Vref offen. «CAD immer als Skript» in CLAUDE.md? (Nutzer fragen).
## Nächster Schritt
Fehlende Kaufteile besorgen (Ritzel zuerst nachmessen), Wellen vorbereiten, dann Zusammenbau nach Anleitung; Messwerte Reihe B/C-M4/M3-Durchgang eintragen; Motorprüfstand drucken und messen.
## Dateien
Fusion «Claude Roboterarm v1» (J2), «Roboterarm Gesamt NUR TEST v1» (Rohbau); Repo github.com/Technoraily/KI-Integrierter-Roboter
