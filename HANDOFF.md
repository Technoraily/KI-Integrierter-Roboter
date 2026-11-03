# HANDOFF – KI-Integrierter Roboterarm (Stand 03.11.2026 Feierabend; Details: README.md, docs/konzept.md, index.md)
## Ziel
6-Achs-Desktop-Roboterarm (3D-Druck, NEMA 17, BTT Octopus + grblHAL) auf 1000-mm-Schiene, später Kamera-KI und Greiferwechsel. Aktuell: Prüfstand J2 aufbauen, Motor vermessen, Elektronikgehäuse in Betrieb nehmen.
## Stand
- J2-Prüfstand (CAD 8/10): alle Teile gedruckt, Rahmen montiert. Netzteil LRS-350-24 und NEMA 17 sind da; Elektronikgehäuse (alle Teile) gedruckt, Netzteil passt. Lage: Klemmleiste links (Klemme 1 = L vorne), Klemmenhaube links, Lüftungsschlitze rechts.
- 230-V-Seite verdrahtet (C14, N, PE am Netzteil), L noch mit Brücke statt F1. Stromlos gemessen (Multimeter HC-303TN, kein Summer): PE 0,2 Ω, N 0,2 Ω, L 0,3 Ω; L–N 0,86 MΩ (Netzteil allein, gleich ohne Adern); L/N–PE «1». Noch NIE eingeschaltet.
- Haus-FI: zwei Kopp RCD 25-0,03 (30 mA). Gruppe 1 = Küche/WC/Wohnen/Gang, Gruppe 2 = Zimmer/Bad/Keller/Waschmaschine; Automaten Wohnen/Zimmer C13. Steckdose noch nicht am FI getestet (T-Taste legt die ganze Gruppe lahm; Alternative PRCD-Adapter).
## Entscheidungen
- Kein Einschalten ohne Sicherung F1 (5 × 20 mm, T 3,15 A träge), ohne Klemmenabdeckung, ohne FI-Kontrolle und ohne Opa. Verzwirbelte Litze mit Isolierband und Zusammendrücken von 4,8-mm-Hülsen sind abgelehnt.
- 24 V: Kfz-Sicherung 3 A nur für J2 (für ganzen Arm zu klein). 230-V-Seite nur Entwurf, Opa prüft/gibt frei. Einschaltstrom 60 A typ. (Datenblatt S. 2, docs/LRS-350.pdf lokal).
## Offen
- F1-Halter: Fahnen 4 mm breit, kein Lötkolben, keine passenden Hülsen. Optionen: Opa lötet / Kolben leihen oder kaufen / Halter mit Norm-Fahnen (Neudruck Netzblende). Belegung Stirn-/Seitenkontakt, Schrumpfschlauch, Zugentlastung C14, Schalter, T 3,15 A gegen 60 A: alles Opa.
- Messen: C14-Ausschnitt/Tiefe, F1-Gewinde, USB-Lage Uno, Shield-Höhe. RISIKO HTD-3M-Ritzel: Nabe evtl. 2–3 mm zu lang (CAD Nabe Ø 14 × 6). Danach Motorkabel crimpen, TMC2209 Vref (max 1,77 A), GRBL aufspielen.
## Nächster Schritt
F1-Halter anschliessen (Löten mit Schrumpfschlauch durch Opa), Brücke entfernen, mit Sicherung nachmessen (C14-L bis Klemme L 0,2–0,5 Ω, ohne Sicherung «1»), Haube montieren, FI-Zuordnung prüfen, dann erster Einschalttest mit Opa (24 V auf DC V 200, Poti V ADJ auf 24,0 V, ohne Last).
## Dateien
docs/schema/verdrahtung-j2.md, docs/elektronikgehaeuse.md, docs/stuecklisten/elektronikgehaeuse.md, cad/skripte/elektronikgehaeuse.py; Fusion «Claude Roboterarm v1» (J2); Repo github.com/Technoraily/KI-Integrierter-Roboter
