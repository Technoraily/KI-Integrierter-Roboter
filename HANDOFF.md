# HANDOFF – KI-Integrierter Roboterarm (Stand 28.10.2026; Details: README.md, docs/konzept.md, index.md)
## Ziel
6-Achs-Desktop-Roboterarm (3D-Druck, NEMA 17, BTT Octopus + grblHAL) auf 1000-mm-Schiene, später Kamera-KI und Greiferwechsel. Aktuell: Prüfstand J2 aufbauen, Motor vermessen.
## Stand
- J2-Prüfstand (CAD 8/10): alle Teile gedruckt, Rahmen montiert. Bestellung läuft, Lieferung ca. 1.–9.11. Elektrik-Schema: docs/schema/verdrahtung-j2.md.
- NEU 28.10. (lokal committed, NICHT gepusht): docs/grbl-j2.md + docs/gcode/*.nc (GRBL-Werte, 5 Testprogramme, $100=640), software/j2_testprogramme.py und j2_auswertung.py, docs/messprotokoll-j2.md.
- NEU 28.10.: Elektronikgehäuse (cad/skripte/elektronikgehaeuse.py, STL in cad/export/stl/Elektronikgehaeuse/, docs/elektronikgehaeuse.md, Stückliste, Gutachten docs/reviews/2026-10-28-...): Wanne, Deckel, Netzblende (C14 + F1), Klemmenabdeckung. Gutachten 6/6/7 – Ziel 8 nicht erreicht; Korrekturen nach Runde 3 nicht mehr begutachtet. Fusion-Dokument «Untitled» ungespeichert, Skript erzeugt es neu.
## Entscheidungen
- 24 V: Kfz-Sicherung 3 A in +24 V; 230-V-Seite nur Entwurf, Opa prüft/gibt frei. LRS-350.pdf lokal (in .gitignore). Kein Netzschalter im Gehäuse eingeplant. Deckelrand: Steg vorne + Lippe seitlich/hinten.
## Offen
- Messen an den Teilen: Netzteil-Klemmleiste (Länge/Breite, Ohren, Poti), C14 (Ausschnitt, Lochabstand, Tiefe), F1-Gewinde, USB-Lage Uno, Shield-Stapelhöhe.
- RISIKO HTD-3M-Ritzel: Nabe evtl. 2–3 mm zu lang (CAD Nabe Ø 14 × 6); nach Lieferung messen. Danach Ritzel aufreiben, Motorkabel crimpen, TMC2209 Vref (R110? Faktor 1,41; max 1,77 A), GRBL aufspielen.
- Opa: Typenschild, 230-V-Schema, Zugentlastung C14, Schalter.
## Nächster Schritt
Zuerst die Testplatten EG_Passprobe_C14 und EG_Passprobe_F1 drucken (je < 1 h), Stufe/Bohrung notieren und im Skript nachführen; dann EG_Netzblende + EG_Klemmenabdeckung als Passproben; danach Startwerte im Skript anpassen, dann Wanne/Deckel. Noch offen aus der Liste: Ritzel-Nabe parametrisieren (Punkt 4), Abdeckung 24-V-Seite (Punkt 5, teils im Gehäuse erledigt).
## Dateien
Fusion «Claude Roboterarm v1» (J2); Repo github.com/Technoraily/KI-Integrierter-Roboter
