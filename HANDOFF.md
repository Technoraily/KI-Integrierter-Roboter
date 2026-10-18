# HANDOFF – KI-Integrierter Roboterarm (Stand 18.10.2026; Details: README.md, docs/konzept.md, index.md)
## Ziel
6-Achs-Desktop-Roboterarm (3D-Druck, NEMA 17, BTT Octopus + grblHAL) auf 1000-mm-Schiene, später Kamera-KI und Greiferwechsel. Aktuell: Motoren vermessen, dann Prüfstand J2.

## Stand
- Phase 0/1 fertig; CAD Prüfstand J2 fertig (8/10), cad/skripte/j2_pruefstand.py; Rücklauftest in docs/pruefstand-j2.md.
- Motorprüfstand (8/10): cad/skripte/motorpruefstand.py, STL cad/export/stl/Motorpruefstand/, Bauanleitung-PDF docs/bauanleitung/, Messungen docs/motorvermessung.md, Stückliste docs/stuecklisten/motorpruefstand.md.
- Rohbau ganzer Roboter nur zur Anschauung: cad/skripte/rohbau_gesamt.py.
- 17.10.: Toleranztest, Standardteile, Not-Aus-Gehäuse (Skripte, STL, Druckeinstellungen, docs/stuecklisten/werkstattteile.md). Toleranztest.3mf liegt jetzt im Repo.
- NEU 18.10.: docs/opa-liste-j2-pruefstand.pdf (eine Liste aller J2-Teile, Spalte «Opa hat»), aus AliExpress-Warenkorb (15 Artikel, 49.74 CHF) und StepperOnline-Warenkorb (Motor 17HS24-2104S $17.90, Mean Well LRS-350-24 $23.11) plus Stückliste. Nichts bestellt. Erzeugerskript nur im Scratchpad, nicht im Repo.
- Sync über GitHub: .claude/hooks/sync-*.sh, docs/sync-zweiter-computer.md. Lokal per .gitignore: Bambu Studio Saves, pruefstand-j2*.docx (Rückfrage: veröffentlichen?).

## Entscheidungen
- 1 kg Nutzlast überall; Schiene als 7. Achse; nur Zahnriemen. Messhebel ersetzt durch Waagebalken.
- Ausgleichsfeder J2 nur bei Bedarf (konzept.md 3.8). Z90: im Arm grösserer Lochkreis + Formschluss; PLA ok.

## Offen
- Nutzer fragt Opa nach Teilen (PDF); danach Rest bestellen. Prüfen im Warenkorb: GT2-Ritzel nur 6 mm breit (nötig: für 10-mm-Riemen), nur 1 Welle statt 3, M3×10 Torx wohl streichen, Sicherung 3 A Zweck?, Mean-Well 350 W viel zu gross (nötig 24 V ab 5 A), zweiter Motor 60 mm neben dem vorhandenen?
- Vorhanden: Netzteil 12 V / 4 A, M3-Schrauben. Not-Aus-Taster 22 mm nicht im Korb. Rückfragen: Wicklungswiderstand, Schultermotor Doppelwelle?, Schrauben M3 × 20/25/30?
- Toleranztest drucken und auswerten (docs/parameter.md); SW_LOCH 9,5 mm und H_INNEN 58 mm prüfen. J2-STL haben noch KEINE Druckeinstellungen. Regel «CAD immer als Skript» noch nicht in CLAUDE.md (Nutzer fragen).

## Nächster Schritt
Opa-Liste durchgehen, Warenkorb bereinigen; Nutzer druckt Motorprüfstand und Toleranztest und misst; danach Lastrechnung nachführen.

## Dateien
Fusion «Claude Roboterarm v1» (J2), «Roboterarm Gesamt NUR TEST v1» (Rohbau), «Nema 17 Prüfstand 40mm»; Repo github.com/Technoraily/KI-Integrierter-Roboter
