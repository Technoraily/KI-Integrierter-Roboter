# Verdrahtung (Vorstufe)

Stand 11.10.2026: Pin-Belegung der Firmware geklärt, Board noch nicht bestellt. Der vollständige Verdrahtungsplan folgt in Phase 7.

## Pin-Belegung `grbl-Mega-5X` (RAMPS-Karte)

Quelle: [`cpu_map.h`](https://raw.githubusercontent.com/fra589/grbl-Mega-5X/edge/grbl/cpu_map.h), `CPU_MAP_2560_RAMPS_BOARD`. Das MKS Gen L verwendet laut Marlin-Pin-Datei die RAMPS-1.4-Belegung, die Treibersockel passen also ohne Änderung.

| Achse | Gelenk | Sockel | Step | Dir | Enable | Endschalter Min |
|---|---|---|---|---|---|---|
| 1 (X) | J1 | X | A0 | A1 | D38 | D3 |
| 2 (Y) | J2 | Y | A6 | A7 | A2 | D14 |
| 3 (Z) | J3 | Z | D46 | D48 | A8 | D18 |
| 4 (A) | J4 | E0 | D26 | D28 | D24 | D42 |
| 5 (B) | J5 | E1 | D36 | D34 | D30 | D44 |
| 6 (C) | J6 | extern | D49 | D51 | D53 | D57 |

Weitere Pins: Reset A9, Feed Hold A10, Cycle Start A11, Safety Door A12. Spindel-PWM (D8/D6/D9 wählbar) bleibt frei für den Greifer-Servo.

## Vor der Bestellung am Schaltplan des Boards zu prüfen

1. **Achse 6 (D49/D51/D53).** Auf RAMPS-artigen Boards liegen diese Pins am Display-/SD-Stecker (EXP2). Ohne Display sind sie frei; der externe Treiberträger wird dort angeschlossen. Am MKS-Gen-L-Schaltplan bestätigen.
2. **Endschalter der Achsen 4–6 (D42/D44/D57).** Auf dem RAMPS liegen sie an AUX-2/AUX-1. Falls das MKS Gen L sie nicht herausführt: in `cpu_map.h` auf die unbenutzten Max-Endschalter-Stecker X/Y/Z (D2, D15, D19) umlegen. Die Firmware wird ohnehin selbst kompiliert, das ist eine Änderung von sechs Zeilen.

## Festgelegt

- Versorgung 24 V; Not-Aus trennt die Motorspannung.
- J2, J3, J5: voller Haltestrom, Motoren dauernd bestromt (`$1=255`). J1, J4, J6: Stillstandsstrom-Absenkung.
- Greifer-Servo über eigenen 5-V-Wandler, nicht aus dem Board-Regler.
