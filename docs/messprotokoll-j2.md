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
| 1,07 | | | | | |
| 3,5 | | | | | |
| 5,9 | | | | | |
| 6,3 (11,8 Nm) | | | | | |

Nach dem Abhängen die Messuhr auf Null prüfen: bleibt eine Abweichung, hat sich etwas gesetzt oder ist gerutscht.

## 3. Kriechen im Haltetest unter 11 Nm

Gewicht 2 hängt, Motor bestromt, Hebel waagrecht, Messuhr bleibt stehen. Ablesezeiten: 0, 1, 5, 15, 30, 60 min, dann stündlich, am Ende nach 24 h. Der Kriechtest ist erst nach **24 h** aussagekräftig.

| Zeit (min) | Messuhr (mm) | Motor/Wange (°C oder Handprobe) | Bemerkung |
|---|---|---|---|
| 0 | | | |
| 1 | | | |
| 5 | | | |
| 15 | | | |
| 30 | | | |
| 60 | | | |
| 1440 (24 h) | | | |

```
python software/j2_auswertung.py kriechen --punkte 0:<mm> 60:<mm> 1440:<mm>
```

Grenzen (Ausgleichsfeder wird eingebaut, siehe `konzept.md` 3.8): Drift **> 0,1°** in 24 h, Gehäuse des Motors **> 70 °C**.

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
| 1,07 kg (2 Nm) | | | | |
| 5,9 kg (11 Nm) | | | | |

Fällt der Hebel bis zum Anschlag, ist das ein Kriterium für die Ausgleichsfeder.

## 6. Riemen und Beobachtungen

| Frage | Ja / Nein / Bemerkung |
|---|---|
| Riemenstufe 3 (5M) springt über oder rutscht (einmal genügt für die Feder-Prüfung) | |
| Schritte fehlen (Test 2: Messuhr kehrt nach 20 Zyklen nicht auf X0 zurück) | |
| Gedruckte Scheibe verformt sich oder bekommt Risse (Foto) | |
| Geräusche, Schleifen, Hebel streift | |
| Riemenspannung nach dem Versuch noch wie vorher | |

## Ergebnis (nach den Messungen ausfüllen)

| Kriterium | Gemessen | Grenze | Erfüllt |
|---|---|---|---|
| Umkehrspiel J2 | | ≤ 0,3° | |
| Steifigkeit | | Schätzung 30 bis 100 Nm/° | |
| Kriechen 24 h bei 11 Nm | | ≤ 0,1° | |
| Motorgehäuse im Dauerhalten | | ≤ 70 °C | |
| Riemenstufe 3 springt nicht | | nie | |
| Hebel ohne Strom | | bleibt stehen (sonst Feder) | |
| Sicherheit J2 mit gemessenem Motormoment | | ≥ 1,5 (`lastrechnung.md`) | |

Aus diesen Zeilen folgt das Gate in Phase 2: Arm mit oder ohne Ausgleichsfeder, Scheiben aus PETG oder PLA, Stufe 3 so lassen oder ändern.
