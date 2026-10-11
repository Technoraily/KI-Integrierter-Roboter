# Motorvermessung

Erster Schritt von Phase 2. Ziel: das Haltemoment der drei vorhandenen Motoren (17CS04A-170E) messen, weil kein Datenblatt auffindbar ist und die Lastrechnung von diesem Wert abhängt.

## Sofort möglich (ohne Druckteile)

| Messung | Wie | Erwartung |
|---|---|---|
| Gehäuselänge ohne Welle | Schieblehre oder Lineal | ca. 40 mm |
| Wicklungswiderstand | Multimeter zwischen den zwei Adern einer Wicklung (die Paare findest du per Durchgangsprüfung) | 1,5–2,5 Ω bei einem 1,7-A-Motor |

Liegt der Widerstand deutlich höher (z. B. 30 Ω), ist es ein Motor für kleinen Strom und die Annahme 1,7 A falsch.

## Haltemoment (braucht den gedruckten Messhebel)

Aufbau: Motor liegend festgeschraubt, Messhebel auf die Welle geklemmt, das Hebelende drückt in 100 mm Abstand von der Wellenmitte auf die Küchenwaage.

1. Motor am Uno + CNC-Shield mit A4988 an 12 V anschliessen, Strom am Treiber einstellen (Vref, wird mit dem Prüfstand dokumentiert).
2. Motor bestromen, ohne ihn zu drehen (GRBL: `$1=255`, dann eine kleine Bewegung senden, damit die Treiber aktiv bleiben).
3. Hebel waagrecht auf die Waage legen, Waage auf null stellen.
4. Motor in kleinen Schritten gegen die Waage fahren, bis er durchrutscht. Den höchsten Wert vor dem Durchrutschen notieren.
5. Dreimal wiederholen, bei allen drei Motoren.

Auswertung: Moment (Nm) = Anzeige (g) × 0,000981. Beispiel: 400 g am 100-mm-Hebel = 0,39 Nm.

## Protokoll

| Motor | Länge (mm) | Widerstand (Ω) | Strom (A) | Anzeige (g) | Haltemoment (Nm) |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

Die Lastrechnung rechnet mit 70 % des Haltemoments als nutzbarem Moment. Ab 0,30 Nm Haltemoment hält J3 die Sicherheit 1,5 mit 60:1; darunter wird J3 auf 70:1 erhöht (siehe `docs/lastrechnung.md`).
