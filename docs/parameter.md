# Parameterliste

Zentrale Masse des Arms. Dieselben Namen werden als Benutzerparameter in Fusion 360 und als Konstanten im Python-Paket verwendet. Stand: Startwerte aus dem Konzept; Phase 1 (Simulation, Motorvermessung) und Phase 2 (Prüfstand) bestätigen oder ändern sie.

## Geometrie

| Name | Wert | Bedeutung | Status |
|---|---|---|---|
| `L_oberarm` | 200 mm | Achse J2 → Achse J3 | Startwert |
| `L_unterarm` | 190 mm | Achse J3 → Handgelenkmitte (J5) | Startwert |
| `L_hand` | 60 mm | Handgelenkmitte → Flanschfläche | Startwert |
| `H_schulter` | 170 mm | Tischfläche → Achse J2 | Startwert |
| `D_flansch_lochkreis` | 31,5 mm | Werkzeugflansch ISO 9409-1, 4× M5 | fix |
| `Bauraum_max` | 240 mm | grösste Kantenlänge eines Druckteils | fix |

## Untersetzungen

| Name | Wert | Status |
|---|---|---|
| `i_J1` | 20 | Startwert (Statik unkritisch) |
| `i_J2` | 90 (Bereich 80–100) | durch Lastrechnung bestätigt |
| `i_J3` | 50 | durch Lastrechnung bestätigt |
| `i_J4` | 20 | durch Lastrechnung bestätigt |
| `i_J5` | 20 | durch Lastrechnung bestätigt |
| `i_J6` | 8 | durch Lastrechnung bestätigt |

## Drucktoleranzen

Werden nach einem Toleranz-Testdruck auf dem A1 festgelegt (Phase 2).

| Name | Wert | Bedeutung |
|---|---|---|
| `tol_lagersitz` | offen | Übermass Bohrung für Kugellager-Aussenring |
| `tol_passung` | offen | Spiel zwischen zwei gedruckten Passflächen |
| `d_einschmelz_M3` | offen | Bohrung für M3-Einschmelzgewinde |
| `d_einschmelz_M4` | offen | Bohrung für M4-Einschmelzgewinde |
