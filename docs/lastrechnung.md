# Lastrechnung

Statische Schwerkraftmomente aller Gelenke über den ganzen Arbeitsraum, gerechnet mit `software/roboterarm/lastrechnung.py`. Stand 11.10.2026, vor dem CAD.

Nachrechnen:

```
cd software
python -m roboterarm.lastrechnung
```

## Ergebnis

Geforderte Sicherheit: ≥ 1,5 (deckt Beschleunigung und Reibung ab). Beide Lastfälle erfüllen sie.

**0,5 kg im ganzen Arbeitsraum** (Ausladung bis 450 mm)

| Gelenk | Last (Nm) | verfügbar (Nm) | Sicherheit | Geschwindigkeit (°/s) |
|---|---|---|---|---|
| J1 | 0,00 | 4,76 | – | 120 |
| J2 | 8,10 | 16,38 | 2,0 | 27 |
| J3 | 3,50 | 9,10 | 2,6 | 48 |
| J4 | 0,96 | 3,06 | 3,2 | 120 |
| J5 | 0,97 | 3,06 | 3,2 | 120 |
| J6 | 0,15 | 0,58 | 3,9 | 300 |

**1,0 kg bis 300 mm Ausladung**

| Gelenk | Last (Nm) | verfügbar (Nm) | Sicherheit |
|---|---|---|---|
| J2 | 8,00 | 16,38 | 2,0 |
| J3 | 5,13 | 9,10 | 1,8 |
| J4 | 1,65 | 3,06 | 1,9 |
| J5 | 1,67 | 3,06 | 1,8 |
| J6 | 0,29 | 0,58 | 2,0 |

Bewegte Masse ab Schulter ohne Nutzlast: 2,30 kg.

## Was die Simulation geändert hat

Mit den Startwerten aus dem Konzept fiel der 1-kg-Fall an vier Gelenken durch (J3 1,4 · J4 1,1 · J5 0,9 · J6 1,5). Der Engpass für 1 kg ist also das Handgelenk, nicht die Schulter. Angepasst:

| Gelenk | vorher | neu | Grund |
|---|---|---|---|
| J3 | 40:1 | 50:1 | Sicherheit 1,4 → 1,8 |
| J4 | 12:1 | 20:1 | abgewinkelte Hand erzeugt bis 1,65 Nm um die Unterarmachse |
| J5 | 18:1, Pancake-Motor | 20:1, NEMA 17 34 mm | Pancake zu schwach; +70 g im Unterarm sind eingerechnet |
| J6 | 6:1 | 8:1 | Sicherheit 1,5 → 2,0 |

Alle Geschwindigkeitsziele bleiben erfüllt (J2/J3 ≥ 25°/s, Hand ≥ 90°/s).

## Annahmen

- **Motormomente sind angenommen**, nicht gemessen: 0,28 Nm nutzbar für einen 40-mm-NEMA-17 (J1–J3), 0,18 Nm für 34 mm (J4, J5), 0,08 Nm für NEMA 14 (J6), jeweils bis ca. 400 U/min an 24 V. Die Vermessung der drei vorhandenen Motoren steht aus.
- Wirkungsgrad: 0,65 für J2/J3 (vorsichtig; ein Capstan-Trieb liegt eher bei 0,85), 0,85–0,9 für Riemenstufen.
- Massenmodell geschätzt (Tabelle `MASSEN` in `parameter.py`); wird mit den Massen aus Fusion nachgeführt.
- Nutzlastschwerpunkt 80 mm vor dem Flansch und 30 mm seitlich versetzt.
- Die Ausgleichsfeder an J2 ist nicht eingerechnet; sie erhöht die Reserve zusätzlich.
- J1 trägt bei senkrechter Achse keine Schwerkraft. Sein Moment bestimmt die Beschleunigung, nicht die Statik.
