# HANDOFF – KI-Integrierter Roboterarm (Stand 25.11.2026 Feierabend; Details: README.md, docs/konzept.md, index.md)
## Ziel
6-Achs-Desktop-Roboterarm (3D-Druck, NEMA 17) auf 1000-mm-Schiene; Hobbyarm (aufheben, zeichnen, Kamera-KI). J2-Prüfstand: Messphase durch, Prüfstand kann weggestellt werden.
## Stand
- Messprotokoll docs/messprotokoll-j2.md ausgefüllt (Tests 1 bis 6). Gewichte gewogen: 0,995 / 3,56 / 6,13 kg; Hebelarm 190 mm, Tastklotz 64 mm.
- Spiel unter 0,01° (Test 1), Rütteln von Hand 0,125° (Budget ≤ 0,3° ok). Steifigkeit ca. 16,5 bis 18 Nm/° (nach 60 min Dauerlast ca. 15), Ziel 30 nicht erreicht. Kriechen 60 min bei 11,4 Nm: 0,06°, Motor kalt, Riemen/Scheiben ohne Schaden.
- Rücklauf ohne Strom: 1,9 Nm hält (max. 1 mm), 6,6 Nm (3,56 kg) und 11,4 Nm fallen in unter 1 s. Haltegrenze zwischen 1,9 und 6,6 Nm.
- konzept.md 3.8 (Feder, Kriterien) und NEU 3.9 (Parkposition, Haltebremse J2/J3, Dämpfung) nachgeführt. Hochrechnung: J3 fällt vermutlich auch, J4/J5 an der Grenze (nur aus einer Messung).
- software/j2_steuerung.html: Knopf «Motor aus» sendet `$MD`. docs/ruecklauftest-bild.html (auch als Artifact).
## Entscheidungen
- Nie Stecker bei 24 V ziehen/stecken (TMC2209 max ca. 28 V). Vref max 1,4 V.
- Kein 24-h-Test, 60 min genügen (Hobbyarm, Nutzer bei Strom dabei).
- Genauigkeit zuerst per Software-Vorsteuerung und Kamera; Closed-Loop/Encoder später, nichts kaufen.
- Bremse nur an J2 und J3 (Motor mit Bremse, ca. USD 47 bis 60, nicht geprüft); vorhandene Motoren 17CS04A-170E haben keine hintere Welle, Nachrüsten nicht sinnvoll. Vor dem Phase-2-Gate nichts bestellen.
## Offen
- Phase-2-Gate: Feder ja/nein, Bremse J2/J3, Scheiben PETG/PLA. Bauraum hinter dem Motor für Bremse prüfen (CAD).
- Parkposition-Befehl in Firmware, TPU-Dämpfungsteil als Testteil; Moment J3 am Gelenk prüfen; Nutzlastgewinn der Feder rechnen (grob +0,9 kg).
- Endschalter + Homing, Lizenz, grbl-j2.md noch auf Grbl, Verkaufsrepo Stand 11.11. nicht synchron.
## Nächster Schritt
Gutachter-Agent (1 bis 10, max. 3 Runden) für 3.8/3.9 (Feder, Bremse, Parkposition), dann Phase-2-Gate entscheiden.
## Dateien
docs/messprotokoll-j2.md, docs/konzept.md (3.8, 3.9), docs/lastrechnung.md, docs/ruecklauftest-bild.html, software/j2_steuerung.html, index.md; kein Fusion-Dokument in dieser Sitzung
