# Parameterliste

Zentrale Masse des Arms. Dieselben Namen werden als Benutzerparameter in Fusion 360 und als Konstanten im Python-Paket (`software/roboterarm/parameter.py`) verwendet.

Status: **Startwert** = aus dem Konzept, noch nicht geprüft · **gerechnet** = von der Lastrechnung getragen, aber mit angenommenen Motormomenten · **fix** = steht fest.

## Geometrie

| Name | Wert | Bedeutung | Status |
|---|---|---|---|
| `L_oberarm` | 200 mm | Achse J2 → Achse J3 | gerechnet |
| `L_unterarm` | 190 mm | Achse J3 → Handgelenkmitte (J5) | gerechnet |
| `L_hand` | 60 mm | Handgelenkmitte → Flanschfläche | gerechnet |
| `H_schulter` | 170 mm | Tischfläche → Achse J2 | Startwert |
| `D_flansch_lochkreis` | 31,5 mm | Werkzeugflansch ISO 9409-1, 4× M5 | fix |
| `Bauraum_max` | 240 mm | grösste Kantenlänge eines Druckteils | fix |

## Gelenke

| Gelenk | Bereich | Untersetzung | Motor | Status |
|---|---|---|---|---|
| J1 | ±170° | 20 | 17CS04A-170E (vorhanden) | Startwert (Statik unkritisch) |
| J2 | ±90° | 72 | NEMA 17, 60 mm | gerechnet |
| J3 | ±135° | 60 | 17CS04A-170E (vorhanden) | gerechnet |
| J4 | ±180° | 20 | 17CS04A-170E (vorhanden) | gerechnet |
| J5 | ±110° | 25 | NEMA 17, 34 mm | gerechnet |
| J6 | ±180° | 8 | NEMA 14 | gerechnet |

## Capstan-Modul J2

| Name | Wert | Bedeutung | Status |
|---|---|---|---|
| `z_ritzel` | 16 | Zähne Motorritzel GT2 | Startwert |
| `z_rad` | 96 | Zähne gedrucktes Rad (Ø ca. 61 mm) | Startwert |
| `b_riemen` | 10 mm | Riemenbreite | Startwert |
| `L_riemen` | 280 mm | Riemenlänge → Achsabstand ca. 80 mm | Startwert |
| `d_trommel` | 14 mm | Wickeldurchmesser der Seiltrommel | Startwert |
| `r_segment` | 84 mm | Wickelradius des Segments | Startwert |
| `w_segment` | ≥ 200° | überdeckter Winkel des Segments | Startwert |
| `d_seil` | 1,5 mm | Dyneema, doppelt geführt | Startwert |
| `d_achse` | 8 mm | mitdrehende Stahlachse als Kern von Rad + Trommel, in 608-Lagern | Startwert |

## Drucktoleranzen

Werden nach einem Toleranz-Testdruck auf dem A1 festgelegt (Phase 2).

| Name | Wert | Bedeutung |
|---|---|---|
| `tol_lagersitz` | offen | Übermass Bohrung für Kugellager-Aussenring |
| `tol_passung` | offen | Spiel zwischen zwei gedruckten Passflächen |
| `d_einschmelz_M3` | offen | Bohrung für M3-Einschmelzgewinde |
| `d_einschmelz_M4` | offen | Bohrung für M4-Einschmelzgewinde |
