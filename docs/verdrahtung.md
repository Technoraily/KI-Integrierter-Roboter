# Verdrahtung (Vorstufe)

Stand 11.10.2026: Steuerung neu gewählt, weil Arm und Schiene koordiniert fahren müssen (7 synchrone Achsen). Board noch nicht bestellt. Der vollständige Verdrahtungsplan folgt in Phase 7.

## Board und Firmware

- **BTT Octopus mit STM32F446** (v1.1 oder Pro), 24 V, 8 Treibersockel.
- **grblHAL**, Treiber `STM32F4xx`, Board-Map [`btt_octopus_pro_map.h`](https://raw.githubusercontent.com/grblHAL/STM32F4xx/master/boards/btt_octopus_pro_map.h) («BTT Octopus Pro v1.1», für F429/F446 mit 12-MHz-Quarz). grblHAL unterstützt 3–8 Achsen ([`config.h`](https://raw.githubusercontent.com/grblHAL/core/master/config.h)).
- Rückfallebene: Marlin 2.1 (bis 9 Achsen; Servo dort auf PB6).

## Achszuordnung

| Achse | Buchstabe | Einheit | Treiber im Stillstand |
|---|---|---|---|
| J1 Basis | X | Grad | Absenkung |
| J2 Schulter | Y | Grad | voller Haltestrom |
| J3 Ellbogen | Z | Grad | voller Haltestrom |
| J4 Unterarm-Rolle | A | Grad | Absenkung |
| J5 Hand-Nicken | B | Grad | voller Haltestrom |
| J6 Flansch-Rolle | C | Grad | Absenkung |
| J0 Schiene | U | mm | Absenkung |
| – | (8. Sockel) | – | Reserve |

Die Zuordnung der Buchstaben zu den Sockeln Motor 0–7 wird beim Kompilieren festgelegt und mit dem Machbarkeitstest dokumentiert.

## Ein- und Ausgänge laut Board-Map

- 8 Endschalter-Eingänge (PG6, PG9–PG15), je einer pro Motor: einer je Achse für die Referenzfahrt. Die **beiden Endschalter der Schiene sind Öffner in Reihe auf dem einen U-Eingang**; die Richtung der Referenzfahrt unterscheidet die Enden. Der achte Eingang gehört zum achten Motor und bleibt Reserve.
- Reset/E-Stop, Feed Hold, Cycle Start: PF3–PF5. **Der Not-Aus trennt die Motorspannung und zieht zusätzlich den E-Stop-Eingang**, damit die Firmware den Positionsverlust kennt.
- Kein Servo-Ausgang in der Map. Der Greifer-Servo läuft über den vorhandenen Arduino Uno (USB, von Python angesprochen) mit eigenem 5-V-Wandler.
- Reserve für später (Greiferwechsler, Sensoren): PB6/PB7, PC0 und der achte Treibersockel.

## Vor der Bestellung zu prüfen

1. Angebot nennt ausdrücklich **STM32F446** (nicht H723).
2. Schaltplan des Octopus v1.1 gegen die Pro-Map vergleichen, falls das v1.1 gekauft wird (Marlin nutzt für beide dieselbe Pin-Datei, daher sehr wahrscheinlich gleich).

## Im Machbarkeitstest zu klären (sobald das Board da ist, ohne Mechanik)

Abbruchkriterium: Scheitert Punkt 1 oder 2, wird auf Marlin gewechselt.

1. grblHAL mit 7 Achsen kompilieren und flashen; alle 7 Sockel mit Treibern bestücken und die vorhandenen Motoren reihum umstecken. Alle 7 Achsen fahren in einem Satz synchron.
2. Sätze mit G93 aus Python streamen; Pufferverhalten und Durchsatz beobachten (Bedarf: 10–50 Sätze/s).
3. TMC2209 standalone: Stillstandsstrom-Absenkung je Sockel über den PDN-Pin ein- bzw. ausschalten.
4. Referenzfahrt: Reihenfolge und Einzelreferenzierung der 7 Achsen (z. B. J3 vor J2).
5. Not-Aus-Signal an PF3 und Wiederanlauf.
6. Servo-Weg über den Uno; Greiferbefehl erst nach Status «Idle» (Planerpuffer leer).

## Festgelegt

- Versorgung 24 V.
- Schrittraten liegen mit rund 20–30 kHz weit unter der Grenze des Boards.
- Jeder Bewegungssatz wird mit G93 (Zeitvorgabe) gesendet.
