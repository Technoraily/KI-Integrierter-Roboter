# Lastrechnung

Statische Schwerkraftmomente aller Gelenke über den ganzen Arbeitsraum, gerechnet mit `software/roboterarm/lastrechnung.py`. Stand 11.10.2026, vor dem CAD, nach Gutachten Phase 1.

Nachrechnen (dauert rund 15 Sekunden):

```
cd software
python -m roboterarm.lastrechnung
```

## Ergebnis

Auslegungsziel: **1 kg im ganzen Arbeitsraum**, auch voll ausgestreckt. Der Flansch reicht bis 450 mm; der Schwerpunkt der Last ist 80 mm davor angenommen, also bei 530 mm. Geforderte Sicherheit ≥ 1,5 (deckt Beschleunigung und Reibung ab); sie ist an allen Gelenken erfüllt.

| Gelenk | Motor | Untersetzung | Last bei 1 kg (Nm) | verfügbar (Nm) | Sicherheit | Geschwindigkeit (°/s) |
|---|---|---|---|---|---|---|
| J1 | 17CS04A-170E (vorhanden) | 20 | 0,00 | 4,76 | – | 120 |
| J2 | NEMA 17, 60 mm (neu) | 72 | 11,76 | 21,06 | 1,8 | 33 |
| J3 | 17CS04A-170E (vorhanden) | 60 | 5,42 | 10,92 | 2,0 | 40 |
| J4 | 17CS04A-170E (vorhanden) | 20 | 1,66 | 4,76 | 2,9 | 120 |
| J5 | NEMA 17, 34 mm (neu) | 25 | 1,68 | 3,82 | 2,3 | 96 |
| J6 | NEMA 14 (neu) | 8 | 0,29 | 0,58 | 2,0 | 300 |

Mit 0,5 kg liegen alle Sicherheiten zwischen 2,3 und 4,9. Bewegte Masse ab Schulter ohne Nutzlast: 2,78 kg (inklusive 0,4 kg für Verkleidung und Kabel).

Der unabhängige Gutachter hat J2, J3 und J5 von Hand nachgerechnet und den ungünstigsten Fall mit einer eigenen Suche bestätigt (Abweichung des Rasters ≤ 0,4 %).

## Empfindlichkeit

Die Rechnung steht und fällt mit dem Moment der vorhandenen Motoren, das noch nicht gemessen ist.

| Falls der 17CS04A-170E nur … nutzbar liefert | Sicherheit J3 | Folge |
|---|---|---|
| 0,28 Nm (Annahme) | 2,0 | passt |
| 0,22 Nm | 1,6 | passt knapp |
| 0,20 Nm | 1,4 | J3 auf 70:1 erhöhen (34°/s, Ziel ≥ 25°/s bleibt erfüllt) |

J2 ist mit Wirkungsgrad 0,65 vorsichtig gerechnet; ein Seiltrieb liegt eher bei 0,85, dann wäre die Sicherheit 2,3.

## Änderungen gegenüber dem Konzept

| Gelenk | Konzept | jetzt | Grund |
|---|---|---|---|
| J2 | vorhandener Motor, 90:1 | NEMA 17 mit 60 mm, 72:1 | 1 kg ganz aussen; 72:1 ergibt sich aus Riemen 16:96 × Capstan 12:1 mit grösserer Trommel |
| J3 | 40:1 | 60:1 | Reserve für schwächere Motoren und schwerere Struktur |
| J4 | 34-mm-Motor, 12:1 | vorhandener Motor, 20:1 | abgewinkelte Hand erzeugt bis 1,66 Nm um die Unterarmachse |
| J5 | Pancake, 18:1 | NEMA 17 34 mm, 25:1 | Pancake zu schwach |
| J6 | 6:1 | 8:1 | Sicherheit 1,5 → 2,0 |

## Was 1 kg aussen kostet

Die Motoren schaffen es; die Grenze ist die Steifigkeit, nicht die Kraft.

- **Durchhang:** Zwischen leer und 1 kg ändert sich das Schultermoment um ca. 5 Nm. Bei der Zielsteifigkeit von 30 Nm/° sind das 0,16° oder gut 1 mm am Flansch, dazu 0,3–1 mm Biegung der PLA-Struktur (Schätzung des Gutachters). Insgesamt 2–3 mm lastabhängiger Durchhang. Die ±0,5 mm gelten deshalb **bei gleichbleibender Last**.
- **Schwingen:** Eigenfrequenz um 10 Hz mit 1 kg ausgestreckt; der Arm schwingt nach dem Anhalten spürbar nach.
- **Kriechen:** 1 kg stundenlang ausgestreckt halten belastet PLA und Seil dauerhaft. Der 24-h-Haltetest im Prüfstand läuft mit 11 Nm.

## Annahmen

- **Motormomente sind angenommen**, nicht gemessen: nutzbar ca. 70 % des Haltemoments bis etwa 400 U/min an 24 V. Für den 17CS04A-170E gibt es kein auffindbares Datenblatt; 1,7 A sind aus der Bezeichnung plausibel, das Haltemoment ist unbekannt. Gerechnet ist mit 0,28 Nm. Für 60 mm: 0,45 Nm, 34 mm: 0,18 Nm, NEMA 14: 0,08 Nm. Messung: `docs/motorvermessung.md`.
- Wirkungsgrad: 0,65 für J2/J3 (vorsichtig), 0,85–0,9 für Riemenstufen.
- Massenmodell geschätzt (Tabelle `MASSEN` in `parameter.py`); wird mit den Massen aus Fusion nachgeführt.
- Nutzlastschwerpunkt 80 mm vor dem Flansch und 30 mm seitlich versetzt.
- Die Ausgleichsfeder an J2 ist nicht eingerechnet; sie erhöht die Reserve zusätzlich.
- J1 trägt bei senkrechter Achse keine Schwerkraft. Sein Moment bestimmt die Beschleunigung, nicht die Statik.
