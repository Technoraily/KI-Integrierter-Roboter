# HANDOFF – KI-Integrierter Roboterarm (Stand 10.11.2026 Feierabend; Details: README.md, docs/konzept.md, index.md)
## Ziel
6-Achs-Desktop-Roboterarm (3D-Druck, NEMA 17, BTT Octopus + grblHAL) auf 1000-mm-Schiene, später Kamera-KI und Greiferwechsel. Aktuell: Prüfstand J2 testen, Motor vermessen, Elektronikgehäuse in Betrieb nehmen.
## Stand
- J2-Prüfstand mechanisch FERTIG und getestet (10.11.): Neudruck-Teile passten, alles perfekt, Getriebe lässt sich von Hand drehen (GT2 → 3M → 5M). Lösung der langen Ritzelnaben nur per Druck (j2_pruefstand.py, STL in cad/export/stl/J2_Pruefstand/, Doku docs/stuecklisten/pruefstand-j2.md). Bauanleitung (Seite mit 3D-Bildern + Einbau-Animation, https://claude.ai/artifact/Q2kJv1iygyFrLgLT2av9bt, privat; Bilder docs/bauanleitung/) ist am echten Teil bestätigt.
- Elektrik: Netzteil LRS-350-24, NEMA 17, Elektronikgehäuse gedruckt. 230-V-Seite verdrahtet (C14, N, PE), L noch mit Brücke statt F1. Noch NIE eingeschaltet. Haus-FI: zwei Kopp RCD 25-0,03; Steckdose noch nicht am FI getestet.
- 04.11. nur CAD, nichts gedruckt: Zubehör J2, Werkzeugwechsler + Kamerahalter, Kettenklemme Schiene (Gutachten 7–8/10). Magnet-STL (Ø 6 × 3) noch nicht neu exportiert.
- Git: alles committet und gepusht (Stand 00c56c0 plus Handoff-Commit). Projektseite index.md noch nicht auf den Stand 10.11. nachgeführt.
## Entscheidungen
- Kein Einschalten ohne F1 (5 × 20, T 3,15 A), ohne Klemmenabdeckung, ohne FI-Kontrolle, ohne Opa. 230-V-Seite nur Entwurf, Opa prüft/gibt frei. 24 V: Kfz-Sicherung 3 A nur für J2.
- Drehmoment-Vorrichtung J2 nicht gebaut; Querträger mit Schalter nur für Messungen ohne grosse Last.
## Offen
- F1: Opa lötet / Lötkolben / Halter mit Flachsteckfahnen. Belegung, Zugentlastung C14, Schalter: Opa. Messen: C14-Tiefe, F1-Gewinde, USB-Lage Uno, Shield-Höhe. Dann Motorkabel crimpen, Vref (max 1,77 A).
- Beobachten: 3M-Riemen läuft oben ab? Z72-Hülse Wand dünn (~0,9 mm); Distanzring A rechts nur falls Längsspiel > 0,3 mm.
## Nächster Schritt
MORGEN (11.11.): SOFTWARE-TEST mit ARDUINO UNO + CNC-Shield (GRBL), nicht Octopus. Der Nutzer will eine Testsoftware mit NOT-AUS und allen Sicherungen: Testablauf Schritt für Schritt, Soft-Not-Aus (Leertaste/Esc, Reset), Wegbegrenzung in Software (kein Referenzschalter im ersten Test, Start in Mitte), Strom-/Drehzahl-/Beschleunigungslimits, Abbruch bei Fehler, Log, kleinste Bewegung zuerst. Not-Aus für Test: Kfz-Sicherung 3 A in der 24-V-Leitung ziehen (ok ohne Last; mit Lasthebel besser Taster). Soft-Not-Aus + Erinnerung "Hand an Sicherung" in der Software. NEU: Nutzer baut morgen Endschalter ein, die er zu Hause hat (Typ/Anzahl/Anschluss erfragen, Referenzfahrt/Homing in GRBL einrichten; Limit-Pins am CNC-Shield, NC/NO klären). Fragen: USB-Port, GRBL auf dem Uno schon drauf? Davor klären: F1/Opa, Brücke, FI-Prüfung (Einschalttest 24 V ohne Last mit Opa; Motor am Netzteil erst nach Freigabe).
## Dateien
docs/schema/verdrahtung-j2.md, docs/elektronikgehaeuse.md, docs/stuecklisten/*.md, cad/skripte/j2_pruefstand.py, anleitung_bilder.py, anleitung_animation.py; Fusion «Claude Roboterarm v1» (J2); Repo github.com/Technoraily/KI-Integrierter-Roboter
