# HANDOFF – KI-Integrierter Roboterarm (Stand 18.10.2026; Details: README.md, docs/konzept.md, index.md)
## Ziel
6-Achs-Desktop-Roboterarm (3D-Druck, NEMA 17, BTT Octopus + grblHAL) auf 1000-mm-Schiene, später Kamera-KI und Greiferwechsel. Aktuell: Motoren vermessen, dann Prüfstand J2.

## Stand
- Phase 0/1 fertig; CAD Prüfstand J2 fertig (8/10), cad/skripte/j2_pruefstand.py; Rücklauftest in docs/pruefstand-j2.md.
- Motorprüfstand (8/10): cad/skripte/motorpruefstand.py, STL cad/export/stl/Motorpruefstand/, Bauanleitung-PDF docs/bauanleitung/, Messungen docs/motorvermessung.md, Stückliste docs/stuecklisten/motorpruefstand.md.
- Rohbau ganzer Roboter: cad/skripte/rohbau_gesamt.py. Toleranztest, Standardteile, Not-Aus-Gehäuse: Skripte + STL + docs/stuecklisten/werkstattteile.md.
- 18.10.: Toleranztest gedruckt, Werte in docs/parameter.md + CLAUDE.md + Gedächtnis: Lagersitz 608 liegend Ø 22,20 mm (stehend passte bis 22,30 nicht, «Saggen»); Zapfen Ø 10: Haltesitz Loch 10,10 (Standard), Steckpassung 10,20.
- J2: nur Wange_Links, Wange_Rechts, Spannrolle_5M neu exportiert mit Zusatz _Lager22-20 (alte STL gelöscht), Fusion war offen; Fusion-Dokument nicht gespeichert.
- docs/opa-liste-j2-pruefstand.pdf: eine Liste aller J2-Teile mit Spalte «Opa hat» (AliExpress-Korb 15 Artikel 49.74 CHF, StepperOnline-Korb: Motor 17HS24-2104S $17.90, Mean Well LRS-350-24 $23.11). Nichts bestellt.
- Sync über GitHub: .claude/hooks/sync-*.sh. Lokal per .gitignore: Bambu Studio Saves, pruefstand-j2*.docx (Rückfrage: veröffentlichen?).

## Entscheidungen
- 1 kg Nutzlast überall; Schiene als 7. Achse; nur Zahnriemen; Waagebalken statt Messhebel. Ausgleichsfeder J2 nur bei Bedarf (konzept.md 3.8). Z90: grösserer Lochkreis + Formschluss; PLA ok.

## Offen
- Nutzer fragt Opa nach Teilen. Prüfen im Korb: GT2-Ritzel nur 6 mm breit (nötig 10-mm-Riemen), nur 1 Welle statt 3, M3×10 Torx wohl streichen, Sicherung 3 A?, Mean Well 350 W zu gross (nötig 24 V ab 5 A), zweiter Motor 60 mm neben dem vorhandenen?
- Toleranztest noch auszuwerten: Reihe B (Welle Ø 5/8), C (Einschmelzgewinde M3/M4), M3-Durchgang; SW_LOCH 9,5 und H_INNEN 58 prüfen. J2-STL haben noch KEINE Druckeinstellungen. «CAD immer als Skript» noch nicht in CLAUDE.md (Nutzer fragen). Rückfragen: Wicklungswiderstand, Schultermotor Doppelwelle?, Schrauben M3 × 20/25/30?

## Nächster Schritt
Reihen B/C/D-Durchgang auswerten und eintragen; J2-Druckeinstellungen ergänzen; Opa-Liste durchgehen, Korb bereinigen; Motorprüfstand drucken und messen, danach Lastrechnung nachführen.

## Dateien
Fusion «Claude Roboterarm v1» (J2), «Roboterarm Gesamt NUR TEST v1» (Rohbau), «Nema 17 Prüfstand 40mm»; Repo github.com/Technoraily/KI-Integrierter-Roboter
