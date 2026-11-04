# HANDOFF – KI-Integrierter Roboterarm (Stand 04.11.2026; Details: README.md, docs/konzept.md, index.md)
## Ziel
6-Achs-Desktop-Roboterarm (3D-Druck, NEMA 17, BTT Octopus + grblHAL) auf 1000-mm-Schiene, später Kamera-KI und Greiferwechsel. Aktuell: Prüfstand J2 aufbauen, Motor vermessen, Elektronikgehäuse in Betrieb nehmen.
## Stand
- J2-Prüfstand (CAD 8/10): alle Teile gedruckt, Rahmen montiert. Netzteil LRS-350-24, NEMA 17 da; Elektronikgehäuse gedruckt, Netzteil passt. 230-V-Seite verdrahtet (C14, N, PE), L noch mit Brücke statt F1. Noch NIE eingeschaltet. Haus-FI: zwei Kopp RCD 25-0,03; Steckdose noch nicht am FI getestet.
- 04.11. neu (nur CAD, nichts gedruckt, Kaufteilmasse ungeprüft): Zubehör J2 (Referenzschalter-Querträger + Probe, Motorkabelklemme; Gutachten 8/10), Werkzeugwechsler + Kamerahalter (8/10), Kettenklemme Schiene (7/10), je Runde 3; Noten gelten ohne Kaufteile. Magnete Ø 6 × 3 mm vorhanden: Skript werkzeugflansch.py umgestellt, STL noch NICHT neu exportiert (Fusion war am 04.11. abends nicht verbunden). Skripte: j2_zubehoer.py, werkzeugflansch.py, schiene_kette.py; Doku docs/zubehoer-j2.md, werkzeugwechsler.md, schiene-kabelfuehrung.md; Gutachten docs/reviews/2026-11-04-*.
## Entscheidungen
- Kein Einschalten ohne F1 (5 × 20, T 3,15 A), ohne Klemmenabdeckung, ohne FI-Kontrolle, ohne Opa. 230-V-Seite nur Entwurf, Opa prüft/gibt frei. 24 V: Kfz-Sicherung 3 A nur für J2.
- F1 ohne Löten: Reihenklemme passt nicht (57 mm tief, 46 mm frei). Kein neuer Halter entworfen (Befund in docs/elektronikgehaeuse.md).
- Drehmoment-Vorrichtung J2 nicht gebaut (Motorprüfstand + Lasthebel decken es ab). Nabenlehre gestrichen (Schieblehre reicht).
- Querträger mit Schalter nur für Messungen ohne grosse Last; Haltetest/Rücklauftest mit Original-Querträger.
## Offen
- F1: Opa lötet, Lötkolben besorgen/leihen oder Halter mit 6,3-mm-Flachsteckfahnen (Passprobe EG_Passprobe_F1 bleibt Prüfstein, nur Netzblende neu drucken). Belegung, Schrumpfschlauch, Zugentlastung C14, Schalter, T 3,15 A gegen 60 A: Opa.
- Messen: C14-Tiefe, F1-Gewinde, USB-Lage Uno, Shield-Höhe; RISIKO HTD-3M-Ritzel (Gesamtlänge ≤ 26,0 mm, Sollwerte in docs/zubehoer-j2.md). Danach Motorkabel crimpen, Vref (max 1,77 A), GRBL aufspielen.
- Neu: Schalter KW12-3 messen (Schalterprobe drucken), Magnetprobe (Haltekraft, Bedarf 26 N je Paar), Kette nur mit Anschlussstücken kaufen, Kette 10 × 15 evtl. zu klein (70 % Füllung). Offene Ideen: docs/offene-ideen.md.
## Nächster Schritt
F1 klären (Opa lötet / Kolben / anderer Halter), Brücke entfernen, nachmessen (C14-L bis Klemme L 0,2–0,5 Ω), Haube montieren, FI prüfen, erster Einschalttest mit Opa (24 V auf DC V 200, Poti V ADJ 24,0 V, ohne Last).
## Dateien
docs/schema/verdrahtung-j2.md, docs/elektronikgehaeuse.md, docs/stuecklisten/*.md, cad/skripte/elektronikgehaeuse.py; Fusion «Claude Roboterarm v1» (J2); Repo github.com/Technoraily/KI-Integrierter-Roboter
