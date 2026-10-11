# Lastrechnung

Statische Schwerkraftmomente aller Gelenke über den ganzen Arbeitsraum, gerechnet mit `software/roboterarm/lastrechnung.py`. Stand 11.10.2026, vor dem CAD.

Nachrechnen:

```
cd software
python -m roboterarm.lastrechnung
```

## Ergebnis

Auslegungsziel seit 11.10.2026: **1 kg im ganzen Arbeitsraum**, auch voll ausgestreckt bei 450 mm. Geforderte Sicherheit ≥ 1,5 (deckt Beschleunigung und Reibung ab); sie ist an allen Gelenken erfüllt.

| Gelenk | Motor | Untersetzung | Last bei 1 kg (Nm) | verfügbar (Nm) | Sicherheit | Geschwindigkeit (°/s) |
|---|---|---|---|---|---|---|
| J1 | 17CS04A-170E (vorhanden) | 20 | 0,00 | 4,76 | – | 120 |
| J2 | NEMA 17, 60 mm (neu) | 90 | 10,88 | 26,32 | 2,4 | 27 |
| J3 | 17CS04A-170E (vorhanden) | 50 | 5,15 | 9,10 | 1,8 | 48 |
| J4 | 17CS04A-170E (vorhanden) | 20 | 1,65 | 4,76 | 2,9 | 120 |
| J5 | NEMA 17, 34 mm (neu) | 20 | 1,67 | 3,06 | 1,8 | 120 |
| J6 | NEMA 14 (neu) | 8 | 0,29 | 0,58 | 2,0 | 300 |

Mit 0,5 kg liegen alle Sicherheiten zwischen 2,6 und 4,9. Bewegte Masse ab Schulter ohne Nutzlast: 2,38 kg.

## Was sich gegenüber dem Konzept geändert hat

| Gelenk | Konzept | jetzt | Grund |
|---|---|---|---|
| J2 | vorhandener Motor, 90:1 | **NEMA 17 mit 60 mm**, 90:1 | 1 kg ganz aussen: vorhandener Motor käme nur auf Sicherheit 1,5 |
| J3 | 40:1 | 50:1 | Sicherheit 1,4 → 1,8 |
| J4 | 34-mm-Motor, 12:1 | **vorhandener Motor**, 20:1 | abgewinkelte Hand erzeugt bis 1,65 Nm; der dritte vorhandene Motor wird hier frei |
| J5 | Pancake, 18:1 | NEMA 17 34 mm, 20:1 | Pancake zu schwach |
| J6 | 6:1 | 8:1 | Sicherheit 1,5 → 2,0 |

Es bleiben drei Motoren zu kaufen, nur andere Typen.

## Was 1 kg aussen kostet

Die Motoren schaffen es; die Grenze ist die Steifigkeit, nicht die Kraft.

- **Durchbiegung:** Zwischen leer und 1 kg ändert sich das Schultermoment um ca. 5 Nm. Bei der Zielsteifigkeit von 30 Nm/° sind das 0,16° oder gut 1 mm am Flansch, zuzüglich Biegung der PLA-Struktur. Die Position ist wiederholbar, aber lastabhängig. Die ±0,5 mm gelten deshalb **bei gleichbleibender Last**.
- **Kriechen:** 1 kg stundenlang ausgestreckt halten belastet PLA und Seil dauerhaft. Der 24-h-Haltetest im Prüfstand wird auf 11 Nm angehoben.

## Annahmen

- **Motormomente sind angenommen**, nicht gemessen: nutzbar ca. 70 % des Haltemoments bis etwa 400 U/min an 24 V. Für den 17CS04A-170E habe ich kein Datenblatt gefunden; aus der Bezeichnung lese ich 0,4 Nm und 1,7 A (Vermutung). Gerechnet ist mit 0,28 Nm. Für 60 mm: 0,45 Nm, 34 mm: 0,18 Nm, NEMA 14: 0,08 Nm. Das Haltemoment wird am Prüfstand mit Hebel und Waage gemessen.
- Wirkungsgrad: 0,65 für J2/J3 (vorsichtig; ein Capstan-Trieb liegt eher bei 0,85), 0,85–0,9 für Riemenstufen.
- Massenmodell geschätzt (Tabelle `MASSEN` in `parameter.py`); wird mit den Massen aus Fusion nachgeführt.
- Nutzlastschwerpunkt 80 mm vor dem Flansch und 30 mm seitlich versetzt.
- Die Ausgleichsfeder an J2 ist nicht eingerechnet; sie erhöht die Reserve zusätzlich.
- J1 trägt bei senkrechter Achse keine Schwerkraft. Sein Moment bestimmt die Beschleunigung, nicht die Statik.
