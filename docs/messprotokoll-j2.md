# Messprotokoll J2-Prüfstand

Zum Ausdrucken oder Abtippen. Verfahren und Begründung: `docs/pruefstand-j2.md` (Abschnitt Messen), Einstellungen und Testprogramme: `docs/grbl-j2.md`. Auswertung der Umkehrspiel- und Kriechmessung: `python software/j2_auswertung.py` (Aufrufe unten).

Messuhr: 0,01 mm, am Tastklotz 64 mm von der Achse. **0,1° am Abtrieb = 0,11 mm an der Messuhr = 0,33 mm an der Lastbohrung** (190 mm). Eine Ablesung (0,01 mm) ist also 0,009°.

## Kopf (einmal pro Messtag)

| Angabe | Eintrag |
|---|---|
| Datum / Uhrzeit | |
| Netzteil gemessen (V) | |
| Treiberstrom (A effektiv) / Vref (V) | |
| Materialien Scheiben (PETG/PLA) | |
| Spannung Riemen Stufe 1 / 2 / 3 (Spannweg, Anzugsart) | |
| Gewicht 1 gewogen (kg), Nennwert 1,07 | |
| Gewicht 2 gewogen (kg), Nennwert 5,9 | |
| Waage: Anzeige, bei der der leere Hebel schwebt (kg) | |
| Raumtemperatur (°C) | |

## Vor jeder Messung (Haken setzen)

- [ ] Spalt zwischen Hebel und oberem Querträger offen (liegt der Hebel auf, ist die Messung ungültig).
- [ ] Fangschnur gesetzt, Gewicht an kurzer Schlaufe, Hände nicht unter dem Hebel.
- [ ] Messuhr steht senkrecht auf der Tastfläche, Klemmschraube M3 nur leicht angezogen, Messweg reicht für den Hub (5° = 5,6 mm).
- [ ] Motor bestromt (`$1=255`) oder Blockierstift gesetzt (nur angelegt, nicht festgezogen).

## 1. Umkehrspiel und Steifigkeit unter Wechsellast ±2 Nm

Ablauf nach `pruefstand-j2.md`: Wert 1 = Moment null von unten, Wert 2 = +2 Nm, Wert 3 = Moment null von oben, Wert 4 = −2 Nm. Hebel waagrecht (Messuhrhalter in der passenden Lage). Pro Variante mindestens **3 Durchläufe**. Waagenanzeigen **ablesen und eintragen**, nicht die Sollwerte.

**Variante A: Blockierstift gesetzt** (misst nur Stufen 2 und 3) und **Variante B: Motor bestromt** (misst die ganze Kette, Motor hält). Beide in beiden Hebellagen (waagrecht nach rechts, waagrecht nach links).

| Variante | Lage | Lauf | W1 mm | W2 mm | W3 mm | W4 mm | F1 kg | F2 kg | F3 kg | F4 kg |
|---|---|---|---|---|---|---|---|---|---|---|
| A | rechts | 1 | | | | | | | | |
| A | rechts | 2 | | | | | | | | |
| A | rechts | 3 | | | | | | | | |
| A | links | 1 | | | | | | | | |
| A | links | 2 | | | | | | | | |
| A | links | 3 | | | | | | | | |
| B | rechts | 1 | | | | | | | | |
| B | rechts | 2 | | | | | | | | |
| B | rechts | 3 | | | | | | | | |
| B | links | 1 | | | | | | | | |
| B | links | 2 | | | | | | | | |
| B | links | 3 | | | | | | | | |

Auswertung je Zeile:

```
python software/j2_auswertung.py spiel --mm W1 W2 W3 W4 --kg F1 F2 F3 F4 --gewicht <gewogen> --hebel <Schwebe-Anzeige>
```

| Variante / Lage | Spiel (°) Mittel | Streuung der 3 Läufe | Steifigkeit (Nm/°) Mittel |
|---|---|---|---|
| A rechts | | | |
| A links | | | |
| B rechts | | | |
| B links | | | |

Beurteilung: Spiel **≤ 0,3°** (Budget J2). Gutachter erwartete 0,05 bis 0,15° und 30 bis 100 Nm/°. Streuen die drei Läufe stärker als das Spiel selbst, ist die Messung unbrauchbar (Messuhr lose, Hebel streift, Waage wackelt). Die Spiel-Differenz A gegen B zeigt, was auf Motor und Stufe 1 entfällt. Das Spiel enthält die Reibung und ist deshalb eine obere Grenze.

## 2. Steifigkeit und Setzen unter voller Last

Gewicht 2 (5,9 kg, 11 Nm) langsam anhängen, Ausschlag am Tastklotz ablesen. Der Anteil, den die Abtriebswelle im Lagersitz setzt, ist ohne zweite Messstelle nicht trennbar (0,05 mm Setzen entsprechen 0,045°): als Unsicherheit mitschreiben.

| Last (kg) | Messuhr vor (mm) | Messuhr nach (mm) | Ausschlag (mm) | Ausschlag (°) | Bemerkung |
|---|---|---|---|---|---|
| 3,56 (6,6 Nm), Lauf 1 | 0,29 | 1,00 | 0,71 | 0,64 | verworfen: Messuhr rutschte aus dem Halter, Null kam nicht zurück (60 statt 29 Striche) |
| 3,56 (6,6 Nm), Lauf 2 | 0,45 | 0,89 | 0,44 | 0,39 | Null kam zurück (45–46); ca. 17 Nm/° |
| 3,56 (6,6 Nm), Lauf 3 | 0,79 | 1,24 | 0,45 | 0,40 | Messuhr gesichert; nach Abhängen 0,82 (Rest 3 Striche); ca. 16,5 Nm/° |
| 6,13 (11,4 Nm) | 0,34 | 1,04 | 0,70 | 0,63 | nach 60 s 0,35 (Rest 1 Strich); nichts geknackt; ca. 18 Nm/°, zwischen den Stufen ca. 21 Nm/° |

Lastmoment mit Hebelarm 190 mm, Tastklotz 64 mm von der Achse (1 Strich = 0,01 mm = ca. 0,009°). Ablesung «mit Last» nach ca. 10 s, «nach» nach 60 s. Ohne zweite Messstelle bleibt das Setzen im Lagersitz als Unsicherheit (ca. ±5 %). Gewichte gewogen: 3,56 kg und 6,13 kg. Stufe 1,07 kg wurde nicht gemessen (Test 1 deckt ±2 Nm ab).

Nach dem Abhängen die Messuhr auf Null prüfen: bleibt eine Abweichung, hat sich etwas gesetzt oder ist gerutscht.

## 3. Kriechen im Haltetest unter 11 Nm (60 min, bewusst statt 24 h)

**Ergebnis 25.11.2026: bestanden.** Gesamtdrift 6,5 Striche in 60 min (ca. 0,06°), in den letzten 30 min nur 1,5 Striche, Rest nach dem Abhängen −3 Striche, Motor nicht warm. Ausschlag nach 60 min: 84 Striche (0,84 mm, ca. 0,75°) bei 11,4 Nm, also ca. 15 Nm/° mit Kriechen (kurz nach dem Anhängen ca. 18 Nm/°).

Entscheidung 25.11.2026: Für einen Hobbyarm genügt 1 h. Die Nutzlast trägt der Arm im Betrieb nur kurz, beim Lagern liegt er so, dass er kein Moment trägt. Ein 24-h-Test mit bestromtem Motor ohne Aufsicht entfällt; der Nutzer ist während der Messung anwesend. Das Kriechen läuft zuerst schnell und dann langsamer, die erste Stunde zeigt den Hauptteil.

Gewicht 6,13 kg (11,4 Nm) hängt, Motor bestromt, Hebel waagrecht, Messuhr bleibt stehen, Fangschnur gesetzt. Ablesezeiten: 0, 1, 5, 15, 30, 60 min. Motor und Wange jedes Mal mit der Hand prüfen. Messuhr-Null ohne Gewicht: **0,78 mm (Strich 78)**, Start 25.11.2026.

| Zeit (min) | Messuhr (mm) | Motor/Wange (°C oder Handprobe) | Bemerkung |
|---|---|---|---|
| 0 | 1,075 (7 bis 8 über 0, geschätzt) | – | Null ohne Gewicht 0,30 (Strich 30); Gewicht 6,13 kg |
| 1 | 1,09 | – | |
| 5 (gelesen bei 4) | 1,105 | – | |
| 15 | 1,12 | Motor nicht warm, Wange kälter | |
| 30 | 1,125 | – | +0,5 Striche seit 15 min |
| 60 | 1,14 | – | +1,5 Striche seit 30 min; Gesamtdrift +6,5 Striche (ca. 0,06°) |
| nach Abhängen, +60 s | 0,27 | – | Null war 0,30: Rest −3 Striche (unter 5, in Ordnung) |

```
python software/j2_auswertung.py kriechen --punkte 0:<mm> 30:<mm> 60:<mm>
```

Grenzen (eigene Festlegung für einen Hobbyarm, nicht normiert): in den letzten 30 min höchstens ca. 3 bis 5 Striche Weiterlauf (Warnzeichen ab ca. 10 Striche), Rest nach dem Abhängen unter ca. 5 Striche, Gehäuse des Motors **< 70 °C**. Das Auswerteskript nennt die Grenze 0,1° noch «24 h»; hier gilt die Striche-Grenze. Läuft die Uhr nach 60 min noch deutlich weiter: gezielt verlängern. Ausgleichsfeder siehe `konzept.md` 3.8.

## 4. Erwärmung

| Zeit (min) | Motorgehäuse (°C) | Treiber (°C) | Wange links (°C) | Bemerkung |
|---|---|---|---|---|
| 0 | | | | |
| 15 | | | | |
| 30 | | | | |
| 60 | | | | |

Ohne Infrarot-Thermometer: Handprobe («warm / kaum haltbar») und Zeit notieren.

## 5. Rücklauftest (Motor stromlos)

Hebel waagrecht, Fangschnur gesetzt, Messuhr abgenommen, Motor stromlos schalten.

| Gewicht | Hebel bleibt stehen? | Sinkt langsam (Zeit bis Anschlag, s) | Fällt (Zeit, s) | Bemerkung |
|---|---|---|---|---|
| 0,995 kg (ca. 1,9 Nm) | ja, nach kurzem Absinken um max. 1 mm an der Lastbohrung (ca. 0,3°) | – | – | 25.11.2026; Motor per `$MD` aus (Knopf «Motor aus» in j2_steuerung.html); Funktionsprobe ohne Gewicht vorher: Hebel von Hand leicht beweglich, Motor wirklich frei |
| 3,56 kg (6,6 Nm) | nein | – | in unter 1 s bis zum Anschlag, langsamer als mit 6,13 kg | 25.11.2026; Motor per `$MD` aus. Haltegrenze liegt zwischen 1,9 und 6,6 Nm |
| 6,13 kg (11,4 Nm) | nein | – | sofort (Zeit nicht gestoppt, Hebel schlug auf die Querstrebe) | 25.11.2026; Motor per `$MD` aus. Schwelle zwischen 1,9 und 11,4 Nm nicht untersucht |

Fällt der Hebel bis zum Anschlag, ist das ein Kriterium für die Ausgleichsfeder.

## 6. Riemen und Beobachtungen

| Frage | Ja / Nein / Bemerkung |
|---|---|
| Riemenstufe 3 (5M) springt über oder rutscht (einmal genügt für die Feder-Prüfung) | Nein, nirgends (25.11.2026, nach Tests 2, 3, 5) |
| Schritte fehlen (Test 2: Messuhr kehrt nach 20 Zyklen nicht auf X0 zurück) | Nein: Null kam in Läufen 2, 3 und der 6-kg-Stufe zurück (Rest 1 bis 3 Striche) |
| Gedruckte Scheibe verformt sich oder bekommt Risse (Foto) | Nein, nichts verformt oder gerissen (Sichtprüfung, kein Foto) |
| Geräusche, Schleifen, Hebel streift | Nichts Auffälliges, ausser beim Fall mit 6,13 kg: Hebel schlug auf die Querstrebe |
| Riemenspannung nach dem Versuch noch wie vorher | Ja, überall wie vorher |

## Ergebnis (nach den Messungen ausfüllen)

| Kriterium | Gemessen | Grenze | Erfüllt |
|---|---|---|---|
| Umkehrspiel J2 | | ≤ 0,3° | |
| Steifigkeit | | Schätzung 30 bis 100 Nm/° | |
| Kriechen 24 h bei 11 Nm | | ≤ 0,1° | |
| Motorgehäuse im Dauerhalten | | ≤ 70 °C | |
| Riemenstufe 3 springt nicht | | nie | |
| Hebel ohne Strom | bleibt bei 1,9 Nm stehen (max. 1 mm Absinken); fällt bei 11,4 Nm sofort | bleibt stehen (sonst Feder) | nein bei voller Last: Ausgleichsfeder oder Haltebremse nötig |
| Sicherheit J2 mit gemessenem Motormoment | | ≥ 1,5 (`lastrechnung.md`) | |

Aus diesen Zeilen folgt das Gate in Phase 2: Arm mit oder ohne Ausgleichsfeder, Scheiben aus PETG oder PLA, Stufe 3 so lassen oder ändern.
