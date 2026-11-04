# Gutachten: Schiene J0, Kettenklemme (04.11.2026)

Skala 0–4 unbrauchbar · 5–7 gut mit Potenzial · 8–10 fertig. Unabhängiger Gutachter (Agent), der nur Skript, Doku, Stückliste und Druckeinstellungen gelesen und von Hand gerechnet hat; keine Teile, kein Fusion.

## Runde 1: 4 von 10

Nachgerechnet und in Ordnung: Tasche, Block- und Fussmasse, Lage der Langlöcher (Senkung 2,75 mm vom Fussrand, 8,75 mm vom Block), Stückzahlen, Volumina.

| Nr. | Schwere | Mangel | Behandlung in Runde 2 |
|---|---|---|---|
| 1 | hoch | Deckel klemmt nichts: Tasche 0,4 mm Spiel, beidseitig offen, kein Formschluss | Deckel mit zwei Pressrippen (0,8 mm); als **Reibklemme** benannt, Haltekraft ≥ 20 N mit Federwaage zu prüfen; Empfehlung: Kette mit Anschlussstücken bestellen, dann entfällt die Klemme |
| 2 | hoch | Schraube M3 × 12 stösst auf den Bohrungsgrund | M3 × 8 (Spitze 2 mm über dem Grund) |
| 3 | hoch | Senkung 3 mm im 4-mm-Fuss; Scheibe Ø 9 passt nicht in Ø 8,5 | Senkung entfällt, Fuss 5 mm, Kopf mit Scheibe liegt auf |
| 4 | mittel | Wand um Einschmelzgewinde nur 1,5 mm je Seite | Wand 10 mm (3 mm je Seite), Assert im Skript |
| 5 | mittel | Bewährte Lösung (Anschlussstücke der Kette) nicht herausgestellt | oben in der Doku als Empfehlung |
| 6 | mittel | Konstruktion ohne belegte Kettenmasse; Startwert mischt zwei Funde | Doku sagt: Grösstwert aus zwei Händlerlisten ohne gesicherte Quelle; STL nur als Entwurf bezeichnet, vor dem Druck neu exportieren |
| 7 | mittel | Kettenlänge falsch formuliert (S/2 + π·R), Schlaufenhöhe und Gleitkanal fehlen | korrigiert (557 bis 588 mm), Bogenhöhe, Gleitkanal als offen |
| 8 | mittel | Platz im Querschnitt nicht gerechnet | grobe Rechnung: etwa 70 % Füllung, grössere Kette oder Bündelung nötig |
| 9 | niedrig | Docstring nannte Fuss 70 statt 76 mm | Docstring neu |
| 10 | niedrig | Montagefläche am Profil und bewegliches Ende unklar | 40-mm-Seite genannt; bewegliches Ende als nicht montierbar benannt |
| 11 | niedrig | Stückliste: Suchbegriffe, Preise, Zugentlastung am Kettenende, Endschalter-Halter fehlen | ergänzt |
| 12 | niedrig | Druckeinstellungen: Deckellage, Materialbegründung | ergänzt |

## Runde 2: 6 von 10

Bestätigt behoben: Schraubenlänge, Wand um die Einsätze, Fuss ohne Senkung, Kettenlängenformel, Aderzahl-Rechnung (108 mm², 72 %), Empfehlung Anschlussstücke zuerst. Haltekraft der Reibklemme bleibt unbelegt (Pressung biegt den dünnen Quersteg eher, als dass sie Normalkraft aufbaut).

| Nr. | Schwere | Mangel | Behandlung |
|---|---|---|---|
| 1 | hoch | Schraubenlinie bei y = 0 liegt auf dem Steg des Profils 2040 (40-mm-Seite hat Nuten bei ±10 mm) | Montage auf der 20-mm-Seite (eine Nut in der Mitte), Überstand 14,7 mm je Seite in der Doku |
| 2 | hoch/mittel | M4 × 10 zu kurz (2,2 mm Eingriff im T-Nutenstein) | M4 × 14 |
| 3 | mittel | Haltekraft nicht belegt, Formschluss besser | als Notbehelf belassen; Formschluss (Querschraube durch die Bolzenlöcher oder Kabelbinder) in der Doku als bessere Lösung, erst mit der gelieferten Kette konstruieren |
| 4 | niedrig | toter Verweis `werkstattteile.md`, Federwaage-Verweis | korrigiert |
| 5 | niedrig | Docstring Fuss 76 × 50 | 49,4 |
| 6 | niedrig | PRESS beim Nachmessen mitsetzen | Skript-Kommentar und Druckeinstellungen |
| 7 | niedrig | Quelle der Kettenmasse ungesichert | nicht lösbar ohne Kette |

Für ≥ 8 fehlt laut Gutachter: Formschluss-Lösung oder Zugtest, Lage zur Nut. Die Lage ist behoben; der Rest hängt an der gelieferten Kette (bei Anschlussstücken entfällt das ganze Teil). Runde 3 wird dafür nicht verbraucht.
