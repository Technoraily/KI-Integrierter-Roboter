# HANDOFF – KI-Integrierter Roboterarm (Stand 22.11.2026 Feierabend; Details: README.md, docs/konzept.md, index.md)
## Ziel
6-Achs-Desktop-Roboterarm (3D-Druck, NEMA 17) auf 1000-mm-Schiene. Aktuell: Prüfstand J2, Messphase mit 24 V (Netzteil laut Nutzer geklärt; Not-Aus/Freigabe nicht im Detail nachgefragt).
## Stand
- Steuerung: ESP32 (FluidNC v4.1.1, COM9), TMC2209 nur STEP/DIR/EN. Uno-Klon stürzt ab, neuer Uno defekt → Prüfstand bleibt beim ESP32. config idle_ms 255 (Motor bleibt bestromt).
- Vref hängt auf diesem Modul von VM ab: 24 V AUS ca. 0,45 V max, 24 V AN 1,274 V (≈0,9 A, Annahme 0,71 A/V). Nur bei 24 V AN messen/einstellen. Tempo-Grenze am Hebel: 23 °/s ok, 24 °/s Schrittverlust (nicht an Welle/accel gelegen; Vermutung Drehmoment bei Drehzahl). Sicher bis ca. 20 °/s. Pendeltest ohne Last 8× bei 20 °/s: Messuhr kam auf ±1 Strich zurück.
- Welle ersetzt, Prüfstand per Brett (Bohrbild docs/bohrbild-brett.html, 4× Ø3,5 + 2× Ø10) am Tisch angeschraubt.
- software/j2_steuerung.html: Pendeln jetzt Von/Bis/Wiederholungen/Pause (für Messuhr an der Nullstellung, Arm schwenkt von der Messuhr weg).
- NEU docs/messung-anleitung.html: bebilderte Anleitung Test 1 Variante A (Blockierstift M3×25 an Welle A, Loch Ø6 in rechter Wange ca. x 54 / y 46 mm), Rechner mit Eingabe in Teilstrichen (Überlauf: 71 → −29).
- Erste Messung (Federwaage, grob; Gewicht 0,995 kg, ca. ±1,85 Nm): Lauf 1 Spiel 0,009°, 6,9 Nm/°; Lauf 2 (Riemen nachgezogen) Spiel 0,000°, 7,7 Nm/°. Spiel unter 0,01° (nicht auflösbar), Steifigkeit weit unter Schätzung 30–100 Nm/° (Ziel 30). Waagenwerte nur ganzzahlig → ca. ±13 % Unsicherheit; Nachspannen brachte kaum etwas. Bei 1 kg Nutzlast ca. 6–7 mm lastabhängiger Durchhang am Flansch (450 mm), Eigenfrequenz ca. 5 Hz (grobe Rechnung).
## Entscheidungen
- Nie Stecker bei 24 V ziehen/stecken (TMC2209 max ca. 28 V). Vref max 1,4 V ohne Kühlkörper.
- Steifigkeit zuerst mit echten Gewichten messen (Test 2), nicht mit Federwaage; erst dann verbessern (günstig zuerst: Riemen, Scheiben PLA/mehr Wände, Software-Ausgleich).
## Offen
- Lauf 3 und Test 2 (Gewichte 1/2/3 kg oder 1,07/3,5/5,9 kg, Küchenwaage); Variante B (Motor bestromt), andere Hebellage, Tests 3–6 (Haltetest 24 h, Erwärmung, Rücklauf). Messprotokoll/grbl-j2.md noch auf Grbl. SPREAD-Pad/Vref 1,4 V optional. Endschalter + Homing. Lizenz wählen. Verkaufsrepo Stand 11.11. nicht synchron.
## Nächster Schritt
Gewichte besorgen und wiegen, Test 2 (Messprotokoll Punkt 2), Messuhr vor/nach, Null prüfen. Messwerte in Messprotokoll eintragen, dann entscheiden ob Verbesserung nötig.
## Dateien
docs/messung-anleitung.html, docs/bohrbild-brett.html, docs/messprotokoll-j2.md, docs/pruefstand-j2.md, software/j2_steuerung.html, j2_auswertung.py, fluidnc/config_j2.yaml, index.md; Repo github.com/Technoraily/KI-Integrierter-Roboter (kein Fusion-Dokument in dieser Sitzung)
