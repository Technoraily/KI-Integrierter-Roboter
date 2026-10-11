# Prüfprotokoll: Detailkonzept (Gate Phase 1)

Geprüft: Kinematik- und Lastrechnungs-Code, Annahmen, J2-Antrieb, Stückliste Prüfstand, Pin-Belegung. Unabhängiger Gutachter, Skala 0–4 unbrauchbar · 5–7 gut mit Verbesserungspotenzial · 8–10 nahezu perfekt. Höchstens 3 Runden.

**Ergebnis: 8/10 nach Runde 2 – die Konstruktion des J2-Prüfstands kann beginnen.** Runde 3 wurde nicht gebraucht.

| Punkt | Runde 1 | Runde 2 |
|---|---|---|
| Kinematik-Code | 7 | 8,5 |
| Lastrechnung | 8 | 9 |
| Annahmen / Realismus 1 kg | 6 | 7,5 |
| J2-Antrieb | 6 | 7 |
| Stückliste Prüfstand | 5,5 | 8 |
| Pin-Belegung | 7 | 8 |
| **Gesamt** | **6,5** | **8** |

## Vom Gutachter selbst nachgeprüft

- Tests und Lastrechnung ausgeführt; Ausgabe identisch mit `docs/lastrechnung.md`.
- J2, J3 und J5 von Hand nachgerechnet (11,76 / 5,41 / 1,68 Nm); eigene Suche nach dem ungünstigsten Fall liegt höchstens 0,4 % über dem Raster.
- Kinematik mit 2000 Zufallsstellungen: Ausgangsstellung immer unter den Lösungen, alle Lösungen treffen die Lage und liegen in den Gelenkgrenzen.
- Seilkraft J2: 140 N bei 11,76 Nm, 251 N bei vollem Antriebsmoment, 557 N bei blockiertem Motor; doppelt geführt je Seil die Hälfte.
- Riemen 16:96 mit 280 mm: Achsabstand 79,9 mm, 6,3 Zähne im Eingriff, Trumkraft bis 128 N.
- 8-mm-Stahlachse bei 60 mm Spannweite: 90 MPa und 0,03 mm Durchbiegung bei 300 N.
- Pin-Belegung gegen `cpu_map.h` und die Marlin-Pin-Datei des MKS Gen L geprüft.

## Runde 1 (6,5/10) – Befunde und Änderungen

| Befund | Änderung |
|---|---|
| IK nur 4 von 8 Zweigen, keine Grenzprüfung; Vorzeichenfehler bei q5 = π | `rueckwaerts` mit Schulter-Zweig, `loesungen`, `naechste_loesung`, `in_grenzen`; Fehler korrigiert; 13 Tests |
| Motormomente ungemessen, kein Datenblatt für 17CS04A-170E | Messung als erster Schritt von Phase 2 (`docs/motorvermessung.md`); Empfindlichkeit und Rückfallebene in der Lastrechnung |
| Massenmodell optimistisch (Verkleidung, Kabel fehlen) | +0,4 kg; J3 60:1, J5 25:1 |
| Riemen 158/200 mm geometrisch unbrauchbar, 6 mm Breite grenzwertig | 280 mm, 10 mm breit |
| Seil rutscht auf glatter Stahlwelle, keine drehmomentfeste Nabe | Rad und Trommel als ein Druckteil, Seil im Druckteil verankert |
| Segment 180° lässt keinen Platz für Verankerung und Anschlag | Segment ≥ 200° |
| Stückliste: Varianten (b)/(c) unvollständig, 24 V und J2-Motor fehlen | Varianten nacheinander statt parallel; Liste für (a) vollständig |
| MKS Gen L: kein AUX-2, Konflikt A9–A12 mit UART-Jumpern | `docs/verdrahtung.md` ergänzt |

## Runde 2 (8/10) – Restpunkte, alle eingearbeitet

1. Trommel nicht als frei tragendes PETG-Rohr um eine feststehende Achse (2 mm Wand, kriecht unter Seilvorspannung), sondern auf mitdrehender 8-mm-Stahlachse, Lager im Gehäuse.
2. Riemen über Langlöcher am Motor spannen; die F623ZZ-Lager passten nicht zum 10-mm-Riemen und sind gestrichen.
3. Messprotokoll: 60-mm-Motor mitmessen, Spitzenstrom notieren, 70-%-Abschlag nicht doppelt anwenden.
4. Restwidersprüche im Konzept bereinigt.

## Offen, nicht dringend

- `naechste_loesung` kennt keinen Umlauf bei ±180° an J4/J6 und setzt in der Handsingularität q4 = 0. Relevant erst für die Bahnplanung (Phase 8).
- Sichtprüfung des Hersteller-PDF des MKS Gen L auf EXP2 und AUX-1, vor der Board-Bestellung.
- Ob der Seiltrieb 30 Nm/° Steifigkeit erreicht, entscheidet der Prüfstand.
