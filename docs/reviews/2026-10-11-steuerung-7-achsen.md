# Prüfprotokoll: Steuerung für 7 synchrone Achsen

Anlass: Der Nutzer verlangt, dass Arm und Schiene koordiniert fahren (Greifer bleibt an einem Punkt, während der Arm auf der Schiene fährt). Die bisherige Planung (Mega-Board mit `grbl-Mega-5X`, Schiene separat am Uno) erfüllt das nicht. Unabhängiger Gutachter, Skala 0–4 unbrauchbar · 5–7 gut mit Verbesserungspotenzial · 8–10 nahezu perfekt.

**Ergebnis: 8/10 nach Runde 2 – kann so bleiben.** Runde 3 wurde nicht gebraucht.

| Punkt | Runde 1 | Runde 2 |
|---|---|---|
| Firmware | 6 | 8 |
| Board | 8 | 8 |
| Stückelung der Bewegung | 7 | 8 |
| Fehlendes (Servo, Referenzfahrt, Not-Aus) | 5 | 7 |
| **Gesamt** | **7** | **8** |

## Gewählt

BTT Octopus mit STM32F446, grblHAL mit 7 Achsen, TMC2209 standalone, 24 V. Marlin 2.1 als Rückfallebene. Details in `docs/konzept.md` 3.1 und `docs/verdrahtung.md`.

## Vom Gutachter an Primärquellen geprüft

- `grbl-Mega-5X` kann höchstens 6 Achsen ([Repo](https://github.com/fra589/grbl-Mega-5X)).
- grblHAL kann 3–8 Achsen ([config.h](https://raw.githubusercontent.com/grblHAL/core/master/config.h)) und hat eine Board-Map für den Octopus Pro v1.1 mit F429/F446, 8 Motoren und 8 Endschalter-Eingängen ([Map](https://raw.githubusercontent.com/grblHAL/STM32F4xx/master/boards/btt_octopus_pro_map.h)). TMC-UART ist dort als ungetestet markiert, Servo-Pins fehlen.
- grblHAL bezieht den Vorschub bei gemischten Linear- und Drehachsen nur auf die Linearachse ([planner.c](https://raw.githubusercontent.com/grblHAL/core/master/planner.c)) → jeder Satz mit G93.
- Marlin kann bis 9 Achsen ([Doku](https://marlinfw.org/docs/configuration/configuration.html)), der Mehrachs-Teil wird aber wenig genutzt.
- Klipper und LinuxCNC können es auch, brauchen aber einen Linux-Rechner.

Nicht belegt: dass FluidNC höchstens 6 Achsen kann; ein Erfahrungsbericht mit 7 Achsen unter grblHAL auf dem Octopus.

## Runde 1 (7/10) – Änderungen

| Befund | Änderung |
|---|---|
| Marlin als Erstwahl ist riskanter | grblHAL zuerst, Marlin als Rückfall |
| Vorschub bei gemischten Achsen mehrdeutig | G93 für jeden Satz; Achsen X/Y/Z, A/B/C, U |
| Feste Segmentlänge reicht nahe Singularitäten nicht | adaptive Stückelung: Start 5 mm, Fehler in der Segmentmitte < 0,05 mm |
| «Greifer steht» verlangt Absolutgenauigkeit | Ziel ehrlich ±0,5–1 mm; Schienenrichtung kalibrieren (0,1° = 1,7 mm über 1000 mm) |
| Kein Servo-Ausgang in der Board-Map | Greifer-Servo über den vorhandenen Uno |
| Not-Aus nur über die Motorspannung | zusätzlich Signal an die Firmware |

## Runde 2 (8/10) – Restpunkte, alle eingearbeitet

1. Machbarkeitstest gleich nach Eintreffen des Boards, mit allen 7 Treibern und Abbruchkriterium für den Wechsel auf Marlin.
2. Beide Endschalter der Schiene als Öffner in Reihe auf dem einen U-Eingang; der achte Eingang gehört zum achten Motor.
3. Greiferbefehl erst, wenn die Firmware «Idle» meldet.
4. Veraltete Budget- und Board-Angaben im Konzept bereinigt.

## Offen bis zum Machbarkeitstest

- 7 Achsen unter grblHAL auf diesem Board sind im Feld wenig erprobt.
- Stillstandsstrom-Absenkung der TMC2209 je Sockel im Standalone-Betrieb.
- Octopus v1.1 gegen die Pro-Map prüfen, falls das v1.1 gekauft wird.
