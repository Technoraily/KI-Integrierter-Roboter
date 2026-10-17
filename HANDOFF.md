# HANDOFF – KI-Integrierter Roboterarm (Stand 17.10.2026; Details: README.md, docs/konzept.md, index.md)
## Ziel
6-Achs-Desktop-Roboterarm (3D-Druck, NEMA 17, BTT Octopus + grblHAL) auf 1000-mm-Schiene, später Kamera-KI und Greiferwechsel. Aktuell: Motoren vermessen, dann Prüfstand J2.

## Stand
- Phase 0/1 fertig; CAD Prüfstand J2 fertig (8/10), cad/skripte/j2_pruefstand.py; neu Rücklauftest in docs/pruefstand-j2.md.
- Motorprüfstand ohne Kaufteile (Gutachten 6 → 8/10): cad/skripte/motorpruefstand.py (+ _bilder.py), STL cad/export/stl/Motorpruefstand/, Bauanleitung als PDF docs/bauanleitung/Bauanleitung_Motorpruefstand.pdf (Quellen + Erzeuger in docs/bauanleitung/quellen/motorpruefstand/), Messungen docs/motorvermessung.md, Stückliste docs/stuecklisten/motorpruefstand.md.
- Rohbau ganzer Roboter nur zur Anschauung: cad/skripte/rohbau_gesamt.py (Pose Q1–Q6).
- NEU 17.10.: Toleranztest (cad/skripte/toleranztest.py) + Standardteile Endschalter-Halter/Kabelhalter (standardteile.py), Not-Aus-Gehäuse (notaus.py); STL in cad/export/stl/Toleranztest/, Standardteile/, NotAus/ mit Druckeinstellungen.md, Stückliste docs/stuecklisten/werkstattteile.md. Skripte laufen mit exec(open(pfad).read()), AUSGABE=Ordner exportiert STL (spart Tokens ggü. Einzelaufrufen). Ohne Gutachten (einfache Teile).
- Sync zwischen Computern über GitHub: Skripte .claude/hooks/sync-*.sh, Anleitung docs/sync-zweiter-computer.md; CLAUDE.md (mit Arbeitsregeln) + HANDOFF.md jetzt im Repo. .claude/settings.json im Repo, getestet; globaler HANDOFF-Hook entfernt. Lokal per .gitignore: Bambu Studio Saves, pruefstand-j2*.docx (Rückfrage: veröffentlichen?).

## Entscheidungen
- 1 kg Nutzlast überall; Schiene als 7. Achse; nur Zahnriemen. Messhebel ersetzt durch Waagebalken.
- Ausgleichsfeder J2 nur bei Bedarf (Kriterien + Auslegung konzept.md 3.8). Z90: im Arm grösserer Lochkreis + Formschluss; PLA ok.

## Offen
- Vorhanden: Netzteil 12 V / 4 A, M3-Schrauben. Not-Aus-Taster 22 mm (1 Öffner + 1 Schliesser) wird für Prüfstand J2 gekauft (Öffner in Plusleitung vor CNC-Shield). Offen: 24-V-Netzteil für den Arm, Schraubzwinge, Multimeter.
- Rückfragen: Wicklungswiderstand, Schultermotor Doppelwelle?, Schrauben M3 × 20/25/30?
- Prüfstand-J2-Teile bestellen; Toleranz-Testteil drucken und auswerten (Ergebnis in docs/parameter.md eintragen). Schalterlochabstand SW_LOCH (9,5 mm) am Mikroschalter und H_INNEN (58 mm) am Not-Aus-Taster prüfen. Regel «CAD immer als Skript» noch nicht in CLAUDE.md (Nutzer fragen). J2-STL haben noch KEINE Druckeinstellungen (Regel: immer dazuschreiben).

## Nächster Schritt
Nutzer druckt Motorprüfstand und Toleranztest (ein Bett je Gruppe) und misst; danach Lastrechnung nachführen.

## Dateien
Fusion «Claude Roboterarm v1» (J2), «Roboterarm Gesamt NUR TEST v1» (Rohbau), «Nema 17 Prüfstand 40mm»; Repo github.com/Technoraily/KI-Integrierter-Roboter
