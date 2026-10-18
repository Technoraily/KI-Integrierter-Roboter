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

Riemenlängen J2: GT2 200 mm, 3M 252 mm, 5M 525 mm; Achsabstände im Prüfstand 51,3 / 61,3 / 111,5 mm (Stufen 2 und 3 mit Spannrolle). Massgebend für alle Masse des Prüfstands sind die Konstanten in `cad/skripte/j2_pruefstand.py`; Beschreibung in `docs/pruefstand-j2.md`. Die übrigen Längen legt das CAD fest.

## Gemeinsam

| Name | Wert | Bedeutung | Status |
|---|---|---|---|
| `d_achse` | 8 mm | Stahlachsen der Zwischenwellen, in 608-Lagern | Startwert |

## Drucktoleranzen

Werden nach einem Toleranz-Testdruck auf dem A1 festgelegt (Phase 2). Testteil: `cad/skripte/toleranztest.py`, STL in `cad/export/stl/Toleranztest/`, Auswertung dort in `Druckeinstellungen.md`. Bis zur Messung gelten die Startwerte.

| Name | Wert | Bedeutung |
|---|---|---|
| `tol_lagersitz` | 0,20 mm (gemessen 18.10., liegend) | Übermass Bohrung für Kugellager-Aussenring. Test Reihe A: 22,20 mm sitzt besser als 22,25 mm und lässt sich noch gut eindrücken; kleinere Bohrungen waren zu eng |
| `tol_lagersitz_stehend` | > 0,30 mm (gemessen 18.10.) | waagrechte Bohrung (Druck hochkant, «Saggen» der Decke): 22,10 / 22,20 / 22,30 passten alle nicht |
| `tol_passung` | 0,20 mm (gemessen 18.10., Reihe D, Zapfen Ø 10) | Übermass Loch gegenüber gedrucktem Zapfen. 10,2 mm sass am besten mit wenig Widerstand, 10,3 mm fiel fast heraus (ganz wenig Widerstand). 10,25 mm vermutlich noch besser, nicht getestet |
| `d_einschmelz_M3` | 4,0 mm (Startwert) | Bohrung für M3-Einschmelzgewinde |
| `d_einschmelz_M4` | offen | Bohrung für M4-Einschmelzgewinde |
