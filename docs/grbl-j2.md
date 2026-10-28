# GRBL-Einstellungen und Testprogramme J2-Prüfstand

Grundlage: Arduino Uno mit CNC-Shield V3, ein TMC2209 im X-Steckplatz, Netzteil 24 V (siehe `docs/schema/verdrahtung-j2.md`). Die Zahlen rechnet `software/j2_testprogramme.py`, das auch die Programme in `docs/gcode/` erzeugt (Endung `.nc`, weil `*.gcode` in der `.gitignore` steht). Der spätere BTT Octopus mit grblHAL nimmt dieselben `$`-Werte.

**X bedeutet Grad am Abtrieb (Hebel).** X = 0 ist der Hebel waagrecht, positiv ist der Hebel nach oben. Die Nullstellung entsteht beim Einschalten: Hebel **von Hand waagrecht stellen, bevor der Strom kommt**. Es gibt keine Referenzfahrt und keine Endschalter; die Anschläge sind mechanisch (Querträger).

## Rechnung

| Grösse | Wert | Herleitung |
|---|---|---|
| Untersetzung | 72 | GT2 20:72 (3,6) × 3M 16:64 (4) × 5M 18:90 (5) |
| Motorschritt | 1,8° | 200 Vollschritte |
| Mikroschritt | 1/16 | alle drei Jumper am Shield gesteckt (TMC2209: MS1 und MS2 gesetzt = 1/16, intern auf 256 interpoliert) |
| Schritte pro Grad am Abtrieb | **640** | 200 × 16 × 72 / 360 |
| Winkel pro Mikroschritt | 0,0016° | an der Lastbohrung (190 mm vom Drehpunkt) 0,005 mm Weg |
| Grenze Arduino | 30 000 Schritte/s | = 46,9°/s am Abtrieb = 562 U/min am Motor |

Die Prüfdrehzahlen sind dieselben wie in `docs/motorvermessung.md`:

| Motor U/min | Abtrieb | Schritte/s |
|---|---|---|
| 60 | 5°/s (300°/min) | 3 200 |
| 120 | 10°/s (600°/min) | 6 400 |
| 240 | 20°/s (1 200°/min) | 12 800 |
| 360 | 30°/s (1 800°/min) | 19 200 |

## `$`-Einstellungen (einmal eintippen, Stand zum Test 1 bis 4)

```
$0=10  $1=255  $2=0  $3=0  $4=0  $5=0  $6=0
$10=1  $11=0.010  $12=0.002  $13=0
$20=0  $21=0  $22=0  $30=1000  $31=0  $32=0
$100=640  $101=250  $102=250
$110=1800  $111=500  $112=500
$120=20    $121=10   $122=10
$130=360   $131=200  $132=200
```

- `$1=255`: Motor bleibt immer bestromt. Das braucht der Haltetest, sonst fällt der Hebel.
- `$110=1800` (°/min) begrenzt auf 30°/s und damit auf 19 200 Schritte/s. Das ist die oberste Prüfstufe und liegt unter der Arduino-Grenze.
- `$120=20` (°/s²): 0,35 rad/s². Mit 6,3 kg an 190 mm sind das etwa 0,08 Nm am Abtrieb, also gegenüber 11,8 Nm vernachlässigbar.
- `$3`: dreht der Hebel bei `X+` nach unten, `$3=1` setzen. Motorstecker nie unter Spannung umstecken.
- Y und Z sind unbelegt (nur ein Treiber), die Werte stehen nur der Vollständigkeit halber da.
- **Nur `G1` verwenden, nie `G0`:** Eilgang fährt mit `$110`, ohne dass man ihn über F kürzen kann.
- Für **Test 0 (Motor allein)** stattdessen `$100=8.889 $110=45000 $120=500` (X = Grad an der Welle). Danach auf die Werte oben zurückstellen.

## Treiberstrom (Vref)

Der Motor 17HS24-2104S ist mit 2,1 A je Phase angegeben. Ein TMC2209-Modul mit 0,11 Ω Messwiderstand erreicht bei der höchsten Vref (2,5 V) nur etwa 1,77 A effektiv, das ist gleichzeitig die Obergrenze des Moduls. Formel (aus dem TMC2209-Datenblatt abgeleitet):

**Vref = I (effektiv) × 1,41** bei 0,11 Ω Messwiderstand.

| Strom effektiv | Vref | Verwendung |
|---|---|---|
| 0,8 A | 1,13 V | erster Lauf, Test 0 |
| 1,2 A | 1,69 V | Tests 1 bis 4 ohne und mit Wechsellast ±2 Nm |
| 1,5 A | 2,12 V | Haltetest 11 Nm (Hebel 5,9 kg) |
| 1,77 A | 2,50 V | Modulgrenze, nicht darüber |

Erforderliches Motormoment bei 11,8 Nm am Abtrieb: 11,8 / 72 / 0,65 = 0,25 Nm (Wirkungsgrad 0,65 wie in `software/roboterarm/parameter.py`; das ist angenommen, nicht gemessen). Das Haltemoment des Motors beträgt 0,76 Nm bei 2,1 A (Hersteller); bei 1,5 A sind es linear gerechnet etwa 0,54 Nm, im Mikroschrittbetrieb noch etwa 70 % davon, also ungefähr 0,38 Nm. Das ergibt Sicherheit um 1,5; knapp, aber für einen Test brauchbar.

**Vor dem Einsatz am Modul prüfen (ungeprüft):**
1. Aufdruck des Messwiderstands (R110 = 0,11 Ω). Steht dort etwas anderes, ändert sich der Faktor.
2. Vref messen: Multimeter zwischen Poti-Gehäuse (Metall) und GND, mit dem kleinen Schraubendreher langsam am Poti drehen. Mit USB allein (ohne 24 V) ist die Vref schon einstellbar.
3. Nach dem Einstellen den Wert in `docs/schema/verdrahtung-j2.md` (Offene Frage 4) eintragen.
4. Das Modul wird bei 1,5 A heiss: Kühlkörper gehört dazu, ein Lüfter ist Reserve. Nach 5 Minuten Haltebetrieb mit dem Finger prüfen.

## Inbetriebnahme in dieser Reihenfolge

1. **Ohne Motor:** Shield, Treiber (Einbaurichtung nach der Pinbeschriftung von Modul und Shield, nicht nach Gefühl), Jumper. Nur USB. GRBL aufspielen, `$$` zeigt die Werte.
2. **Vref 0,8 A (1,13 V)** einstellen. Netzteil auf 24,0 V gestellt und gemessen, dann an das Shield.
3. **Test 0:** Motor allein, ohne Riemen und ohne Ritzel auf der Welle. Klebeband als Marke. `j2-00-motor-allein.nc` (10 Umdrehungen vor und zurück, danach 5 bei 120 U/min). Die Marke muss auf dem Anfangspunkt stehen.
4. Vref auf 1,2 A, Motor und Ritzel einbauen, Hebel waagrecht stellen, Strom ein, `$`-Werte von oben.
5. **Test 1** (`j2-01-abtrieb-kurz.nc`): Richtung prüfen, ohne Gewicht, höchstens 2 bis 5° in die Höhe, 3° nach unten. Nach unten gibt der Anschlag nur 6,65° frei (22 mm an der Lastbohrung).
6. **Test 2 bis 4**, danach Messungen laut `docs/pruefstand-j2.md`.

## Testprogramme (`docs/gcode/`)

| Datei | Zweck | Dauer |
|---|---|---|
| `j2-00-motor-allein.nc` | Verdrahtung, Drehrichtung, Vref, Schrittverlust des Motors allein | ca. 40 s |
| `j2-01-abtrieb-kurz.nc` | Erste Bewegungen am Abtrieb, Richtung | ca. 20 s |
| `j2-02-schrittverlust.nc` | 20 Zyklen ±5° (5,6 mm am Tastklotz), Messuhr vor und nach vergleichen | ca. 30 s |
| `j2-03-geschwindigkeit.nc` | 15° bei 60 / 120 / 240 / 360 U/min, je 3 Zyklen | ca. 1 min |
| `j2-04-dauerlauf.nc` | 100 Zyklen 15° bei 120 U/min, Erwärmung | ca. 5 min |

- **Messuhr bei Test 3 und 4 abnehmen:** 15° sind am Tastklotz (64 mm Radius) 17 mm, mehr als der Messbereich von 10 mm. Test 2 bleibt bei 5° = 5,6 mm.
- **Last stufenweise:** zuerst alle Tests ohne Gewicht, dann mit 1,07 kg (2 Nm), erst danach mit 5,9 kg (11 Nm). Test 3 mit Last hört bei der ersten Stufe auf, in der der Motor brummt oder stehen bleibt (Reset oder Strg+X im Sender).
- **Fallende Last:** Gewicht an kurzer Schlaufe, Fangschnur, Hände nicht unter den Hebel (`docs/pruefstand-j2.md`, «Lasthebel und Sicherheit»).
- Die Programme sind in GRBL-Schreibweise geprüft (ASCII, Kommentare ohne verschachtelte Klammern), aber **noch nicht auf einem Arduino ausgeführt**.

## Ungeprüft / offen

- Mikroschritt 1/16 bei der gelieferten TMC2209-Variante (MS1/MS2-Tabelle des Datenblatts); sonst ändert sich `$100`.
- Aufdruck des Messwiderstands und damit der Vref-Faktor.
- Wirkungsgrad 0,65 und Haltemoment unter Last: ergeben sich erst aus den Messungen.
- Richtung des Treibersteckers beim Aufstecken auf das Shield: Beschriftung auf dem Modul gegen das Shield prüfen, ein falsch herum aufgestecktes Modul ist defekt.
