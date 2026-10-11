# Parameterliste

Zentrale Masse des Arms. Dieselben Namen werden als Benutzerparameter in Fusion 360 und als Konstanten im Python-Paket (`software/roboterarm/parameter.py`) verwendet.

Status: **Startwert** = aus dem Konzept, noch nicht geprüft · **gerechnet** = von Lastrechnung bzw. Gutachten getragen, aber mit angenommenen Motormomenten und Riemenwerten · **fix** = steht fest.

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

## Gelenke und Riemenstufen

Zähnezahlen als Ritzel : Rad. GT2 = 2-mm-Teilung, 10 mm breit; 3M/5M = HTD mit 3- bzw. 5-mm-Teilung, 15 mm breit.

| Gelenk | Bereich | Untersetzung | Motor | Stufe 1 | Stufe 2 | Stufe 3 | Status |
|---|---|---|---|---|---|---|---|
| J0 Schiene | 1000 mm | – | NEMA 17, 40 mm (neu) | GT2, Ritzel 20, offen | – | – | Startwert |
| J1 | ±170° | 20 | 17CS04A-170E (vorhanden) | GT2 20 : 80 | 3M 16 : 80 | – | Startwert |
| J2 | ±90° | 72 | NEMA 17, 60 mm (neu) | GT2 20 : 72 | 3M 16 : 64 | 5M 18 : 90 | gerechnet |
| J3 | ±135° | 60 | 17CS04A-170E (vorhanden) | GT2 16 : 60 | 3M 16 : 64 | 5M 15 : 60 | gerechnet |
| J4 | ±180° | 20 | 17CS04A-170E (vorhanden) | GT2 20 : 100 | 3M 16 : 64 | – | Startwert |
| J5 | ±110° | 18,75 | NEMA 17, 34 mm (neu) | GT2 16 : 80 | 3M 16 : 60 | – | Startwert |
| J6 | ±180° | 8 | NEMA 14 (neu) | GT2 16 : 40 | GT2 16 : 50 | – | Startwert |

Riemenlängen J2: GT2 200 mm, 3M 252 mm, 5M 525 mm. Die übrigen Längen legt das CAD fest.

## Gemeinsam

| Name | Wert | Bedeutung | Status |
|---|---|---|---|
| `d_achse` | 8 mm | Stahlachsen der Zwischenwellen, in 608-Lagern | Startwert |

## Drucktoleranzen

Werden nach einem Toleranz-Testdruck auf dem A1 festgelegt (Phase 2).

| Name | Wert | Bedeutung |
|---|---|---|
| `tol_lagersitz` | offen | Übermass Bohrung für Kugellager-Aussenring |
| `tol_passung` | offen | Spiel zwischen zwei gedruckten Passflächen |
| `d_einschmelz_M3` | offen | Bohrung für M3-Einschmelzgewinde |
| `d_einschmelz_M4` | offen | Bohrung für M4-Einschmelzgewinde |
