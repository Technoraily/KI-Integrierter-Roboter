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
| `a_lochbild_basis` | 120 mm | Lochbild Basis ↔ Schlitten/Grundplatte, 4× M5 im Quadrat | Startwert |
| `L_verfahrweg` | 1000 mm | Verfahrweg der Schiene J0 (Stufe C) | fix |
| `b_spur` | ≥ 150 mm | Abstand der beiden Linearführungen | Startwert |

## Gelenke

| Gelenk | Bereich | Untersetzung | Motor | Status |
|---|---|---|---|---|
| J1 | ±170° | 20 | 17CS04A-170E (vorhanden) | Startwert (Statik unkritisch) |
| J2 | ±90° | 72 | NEMA 17, 60 mm | gerechnet |
| J3 | ±135° | 60 | 17CS04A-170E (vorhanden) | gerechnet |
| J4 | ±180° | 20 | 17CS04A-170E (vorhanden) | gerechnet |
| J5 | ±110° | 25 | NEMA 17, 34 mm | gerechnet |
| J6 | ±180° | 8 | NEMA 14 | gerechnet |

## Prüfstand J2, Variante S (Seiltrieb)

| Name | Wert | Bedeutung | Status |
|---|---|---|---|
| `S_z_ritzel` | 20 | Zähne Motorritzel GT2 | Startwert |
| `S_z_rad` | 120 | Zähne gedrucktes Rad (Ø 76,4 mm) | Startwert |
| `S_b_riemen` | 10 mm | Riemenbreite GT2 | Startwert |
| `S_L_riemen` | 300 mm | Riemenlänge → Achsabstand ca. 73 mm | Startwert |
| `S_d_trommel` | 12,5 mm | Rillengrund der Seiltrommel (Seilmitte Ø 14 mm) | Startwert |
| `S_r_segment` | 83,25 mm | Rillengrund des Segments (Seilmitte R 84 mm) | Startwert |
| `S_p_rille` | 1,8 mm | Steigung der Schraubenrille auf der Trommel | Startwert |
| `S_L_trommel` | 32 mm | Länge der Trommel | Startwert |
| `S_w_segment` | ≥ 200° | überdeckter Winkel des Segments | Startwert |
| `d_seil` | 1,5 mm | Dyneema, doppelt geführt | Startwert |

## Prüfstand J2, Variante R (nur Zahnriemen)

| Name | Wert | Bedeutung | Status |
|---|---|---|---|
| `R_z1` | 20 : 72 | Stufe 1, GT2 10 mm, Riemen 200 mm | Startwert |
| `R_z2` | 16 : 64 | Stufe 2, HTD-3M 15 mm, Riemen 252 mm | Startwert |
| `R_z3` | 18 : 90 | Stufe 3, HTD-5M 15 mm, Riemen 525 mm | Startwert |

## Gemeinsam

| Name | Wert | Bedeutung | Status |
|---|---|---|---|
| `d_achse` | 8 mm | Stahlachsen (Zwischenwellen, Trommelachse), in 608-Lagern | Startwert |

## Drucktoleranzen

Werden nach einem Toleranz-Testdruck auf dem A1 festgelegt (Phase 2).

| Name | Wert | Bedeutung |
|---|---|---|
| `tol_lagersitz` | offen | Übermass Bohrung für Kugellager-Aussenring |
| `tol_passung` | offen | Spiel zwischen zwei gedruckten Passflächen |
| `d_einschmelz_M3` | offen | Bohrung für M3-Einschmelzgewinde |
| `d_einschmelz_M4` | offen | Bohrung für M4-Einschmelzgewinde |
