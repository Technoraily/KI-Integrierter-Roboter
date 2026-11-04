# Gutachten: Werkzeugflansch, Greiferwechsler und Kamerahalter (04.11.2026)

Skala 0–4 unbrauchbar · 5–7 gut mit Potenzial · 8–10 fertig. Unabhängiger Gutachter (Agent), der Skript, Doku, Stückliste, Druckeinstellungen und Konzeptdateien gelesen und mit Python nachgerechnet hat; Fusion hat er nicht bedient.

## Runde 1: 6 von 10

Teile: Master 7, Werkzeug 5, Magnetprobe 6, Kamerahalter 6, Doku und Stückliste 6,5. Bestätigt: Nuttiefe 3,84 mm, Spiegelung der Winkel, Volumina, Senkung M5 gegen Taschen (engste Wand 1,4 mm), Mengen in der Stückliste.

| Nr. | Schwere | Mangel | Behandlung in Runde 2 |
|---|---|---|---|
| 1 | hoch | Kippmoment falsch (0,054 statt 0,0405 m × F_M; Bedarf 26 N statt 19,5 N) | neu gerechnet, Gegenprobe über die Plattenmitte, Bedarf 26 / 52 N |
| 2 | hoch | Kontaktkonzept (M2 × 6 in glattem Loch) nicht baubar | Senkung für den Kopf, M2 × 8 mit Mutter in Sechskanttasche hinten |
| 3 | mittel | Polung als Codierung nicht markiert, Pogo nicht verpolungssicher | mechanischer Codierstift Ø 3 × 6 mm (60° / r = 11 mm); Magnete alle gleich gepolt; im CAD geprüft: bei 120° Verdrehung blockiert der Stift |
| 4 | mittel | «Magnet zieht 2 bis 3 kg» zu optimistisch | als Schätzung mit 1 bis 1,5 kg gekennzeichnet, Erwartung benannt |
| 5 | mittel | Lastannahme 100 / 50 mm unbelegt, Dynamik und Schub fehlen | als Annahme benannt, Auslassungen aufgeführt |
| 6 | mittel | Magnetprobe: Öse 11 mm neben der Magnetachse (Schälzug) | zwei Ösen links und rechts des Magneten (Schnurbügel), Kippprobe an den fertigen Platten |
| 7 | mittel | Gewichte zu niedrig | Master 23–26 g, Kamerahalter 13 g, Roboterseite 55 g |
| 8 | mittel | Einschmelzgewinde 165° zu nah an Magnettasche (1,45 mm Wand) | Winkel 170° / 190°, Assert mit Taschenradius 5,1 mm und 2 mm Wand |
| 9 | mittel | M3 × 8 am Kamerahalter zu lang | M3 × 6 |
| 10 | mittel | Flachbandstecker und Schlitz | Schlitz 19 mm, Doku: hängt vom Modul ab |
| 11 | mittel | Spalttoleranz nicht beziffert | ±0,15 mm, Kugeltasche zuerst prüfen |
| 12 | niedrig | Kamera ohne Neigung, Sichtfeld | Neigung als Pflicht, 28,6° gerechnet |
| 13–16 | niedrig | M5-Scheibe, Kugelsitz Ø 6,15, Pogo-Aufnahme, Nutende | Scheibe in der Stückliste, Kugeltasche zuerst prüfen, Haltesitz benannt, Nut r = 22 bis 32 mm |

## Runde 2: 7 von 10

Bestätigt behoben: Kippmoment (0,0405 m × F_M, 26 / 52 N), Codierstift (60° / r = 11 mm, gespiegeltes Loch, blockiert bei ±120°), Einschmelzgewinde 170° / 190° (Wand ≥ 3,7 mm), M3 × 6, Spalttoleranz, Nutende, Gewichte, Annahmen benannt.

| Nr. | Schwere | Mangel | Behandlung |
|---|---|---|---|
| N1 | mittel | Magnetprobe nicht ausführbar: Ösen münden in der Kontaktfläche von Block A | Zug mittig über Kernloch Ø 3,3 mm von hinten für eine Ringschraube M4, Block 12 mm dick |
| N2 | mittel/hoch | M5-Kopf (5 mm) plus Scheibe (1 mm) steht aus der 5,5-mm-Senkung und kollidiert mit der Werkzeugplatte | niedriger Kopf DIN 7984 (3,5 mm) + Scheibe; Assert «Kopf + Scheibe + 0,5 ≤ Senkung» im Skript |
| N3 | mittel | M2 × 8 ragt 1,3 mm hinten heraus | M2 × 6, Eingriff 1,1 mm (mit Kleber sichern); Asserts: Spitze ≥ 0 und Eingriff ≥ 1 mm |
| N4 | niedrig | Kopfnorm der Kontaktschraube | DIN 84 genannt, Inbus ausdrücklich ausgeschlossen |
| N5 | niedrig/mittel | Codierloch zu nah am Greifer-Einschmelzgewinde 315° | Greiferlochbild auf Ø 32 mm, 0/90/180/270°; Asserts gegen Codierloch und Mutterntaschen |
| N6 | niedrig | Kontaktreibung, Pogo-Hub | in der Doku ergänzt |

Nach den Korrekturen im CAD erneut gebaut (alle Asserts bestanden, Platten ohne Überschneidung, Kugel Ø 3,0 tangential, ab 3,2 mm Überschneidung). Eine dritte Runde wurde nicht beauftragt; die Note 7 gilt für den Stand vor diesen Korrekturen.
