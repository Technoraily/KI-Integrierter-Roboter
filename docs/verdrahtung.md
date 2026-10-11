# Verdrahtung (Vorstufe)

Stand 11.10.2026: Pin-Belegung der Firmware geklärt, Board noch nicht bestellt. Der vollständige Verdrahtungsplan folgt in Phase 7.

## Pin-Belegung `grbl-Mega-5X` (RAMPS-Karte)

Quelle: [`cpu_map.h`](https://raw.githubusercontent.com/fra589/grbl-Mega-5X/edge/grbl/cpu_map.h), `CPU_MAP_2560_RAMPS_BOARD`; vom Gutachter gegengeprüft. Das MKS Gen L verwendet laut [Marlin-Pin-Datei](https://raw.githubusercontent.com/MarlinFirmware/Marlin/2.1.x/Marlin/src/pins/ramps/pins_MKS_GEN_L_V21.h) die RAMPS-Belegung, die Treibersockel passen also ohne Änderung.

| Achse | Gelenk | Sockel | Step | Dir | Enable | Endschalter Min | Endschalter Max |
|---|---|---|---|---|---|---|---|
| 1 (X) | J1 | X | A0 | A1 | D38 | D3 | D2 |
| 2 (Y) | J2 | Y | A6 | A7 | A2 | D14 | D15 |
| 3 (Z) | J3 | Z | D46 | D48 | A8 | D18 | D19 |
| 4 (A) | J4 | E0 | D26 | D28 | D24 | D42 | D40 |
| 5 (B) | J5 | E1 | D36 | D34 | D30 | D44 | D59 |
| 6 (C) | J6 | extern | D49 | D51 | D53 | D57 | D58 |

Pro Achse wird nur ein Endschalter gebraucht (Referenzfahrt); die Max-Eingänge bleiben frei. Spindel-PWM (D8/D6/D9 wählbar) ist für den Greifer-Servo vorgesehen.

## Besonderheiten des MKS Gen L V2.x

1. **Achse 6 (D49/D51/D53)** liegt am Display-/SD-Stecker EXP2 (RAMPS-Standard: SD-Detect, MOSI, SS). Ohne Display sind die Pins frei; dort wird der externe Treiberträger angeschlossen.
2. **Endschalter der Achsen 4–6.** Das Board hat laut Hersteller-PDF die Stecker EXP1, EXP2 und AUX-1, aber kein AUX-2. D42/D44 sind deshalb sehr wahrscheinlich nicht herausgeführt. Lösung: in `cpu_map.h` die Min-Endschalter der Achsen 4–6 auf die freien Max-Stecker von X/Y/Z legen (D2, D15, D19). Die Firmware wird ohnehin selbst kompiliert.
3. **DIAG-Jumper offen lassen.** D2 und D15 sind auf dem Board per Jumper mit den DIAG-Pins der Treibersockel E0/E1 verbunden. Für die Lösung aus Punkt 2 müssen diese Jumper offen sein.
4. **UART-Jumper offen lassen.** A9–A12 sind in der Firmware Reset, Feed Hold, Cycle Start und Safety Door, auf dem Board aber die UART/CS-Leitungen der Treibersockel. Die TMC2209 laufen standalone; mit gesteckten UART-Jumpern drohen Fehlauslösungen. Feed Hold, Cycle Start und Safety Door werden in `config.h` deaktiviert, soweit sie nicht gebraucht werden.

Vor der Board-Bestellung: das Hersteller-PDF ([makerbase-mks/MKS-GEN_L](https://github.com/makerbase-mks/MKS-GEN_L), Ordner `hardware`) optisch auf EXP2 und AUX-1 prüfen. Das ist ein Punkt für Phase 3/4, nicht für den Prüfstand – der läuft mit Uno und CNC-Shield.

## Festgelegt

- Versorgung 24 V; Not-Aus trennt die Motorspannung.
- J2, J3, J5: voller Haltestrom, Motoren dauernd bestromt (`$1=255`). J1, J4, J6: Stillstandsstrom-Absenkung.
- Greifer-Servo über eigenen 5-V-Wandler, nicht aus dem Board-Regler.
