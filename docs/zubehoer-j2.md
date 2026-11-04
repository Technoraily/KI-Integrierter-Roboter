# Zubehör J2-Prüfstand

Stand 04.11.2026 (nach Gutachten, Runde 2). CAD: `cad/skripte/j2_zubehoer.py`, STL: `cad/export/stl/J2_Zubehoer/` (mit `Druckeinstellungen.md`), Stückliste: [stuecklisten/j2-zubehoer.md](stuecklisten/j2-zubehoer.md), Gutachten: [reviews/2026-11-04-j2-zubehoer.md](reviews/2026-11-04-j2-zubehoer.md). Kein Teil ist am Prüfstand erprobt oder gedruckt. Es gibt noch keine Bilder (Fusion hatte beim Bauen keinen aktiven Viewport); die Geometrie steht im Skript. **Alle Masse des Schalters KW12-3 sind Startwerte und im Netz nicht bestätigt** (Händlerangaben widersprechen sich); deshalb gibt es eine Probe, die vor den Querträgern gedruckt wird.

## Was gebaut wurde und was nicht

| Idee | Ergebnis |
|---|---|
| Referenzschalter J2 | **gebaut**: Querträger mit Schaltertasche, dazu eine Probe |
| Motorkabel-Zugentlastung | **gebaut**: Klemme auf dem Motorgehäuse |
| Test für die Ritzelnabe | **gestrichen** (siehe unten): Die Schieblehre leistet dasselbe |
| Drehmoment-Messvorrichtung | **nicht gebaut**: Der Motorprüfstand (`docs/motorvermessung.md`, Wiege «passt für 34–60 mm» laut `motorpruefstand.py`) misst auch den J2-Motor (Zeile «J2 (60 mm)» im Protokoll); am Prüfstand misst der Lasthebel mit Waage das Moment am Abtrieb (`docs/pruefstand-j2.md`). Eine dritte Vorrichtung wäre doppelt |

## Referenzschalter im Querträger (`J2_Quertraeger_oben_Schalter`, `J2_Schalterprobe`)

Der Prüfstand hat laut `docs/grbl-j2.md` bewusst keine Referenzfahrt. Der Schalter ist **sinnvoll, aber nicht nötig**: `docs/konzept.md` verlangt, die Wiederholbarkeit der Referenzsensoren separat zu messen, weil sie die Genauigkeit des späteren Arms direkt begrenzt. Das lässt sich am Prüfstand mit der Messuhr am Tastklotz tun.

- Ersatz für einen der oberen Querträger, gleiche Aussenmasse (14 × 24 × 56 mm), gleiche Einschmelzbohrungen. Die Tasche liegt oben und nimmt den Mikroschalter mit Rollenhebel auf. Dasselbe Teil passt links wie rechts (die Mutterntasche liegt auf einer Seite, die Schrauben kommen also von der anderen).
- **Befestigung:** Schrauben M2 × 16 (M2 × 14 reicht nur knapp: 3,55 mm Wand + 6,9 mm Tasche + 1,75 mm Gegenwand + 1,6 mm Mutter = 13,8 mm) durch die Wand, den Schalter und die Gegenwand, dort Mutter M2 in einer Sechskanttasche (3,55 mm Wand, 1,75 mm bleiben unter der Mutter).
- **Rollenhöhe:** Die Rolle steht 2,2 mm über der Querträgerkante; die Tasche ist 1,0 mm tiefer als nötig, damit Beilagen (Pappe, Folie) unter dem Schalter die Höhe einstellen. Mit den Startwerten sind höchstens 0,4 mm Beilage möglich, sonst fehlt die Reserve.
- **Auslösewinkel (gerechnet, aber abhängig von drei Annahmen):** Hebelkontur aus dem J2-Skript; Anschlag des Hebels am Querträger bei 96,7° aus der Senkrechten (6,7° unter der Waagrechten, so im Skript). Annahmen: Rolle 2,2 mm über der Kante, Vorlauf 1,5 mm, Restweg 1,6 mm.

| Seite | Schalter löst aus bei | Restweg aufgebraucht bei | Hebel liegt auf bei |
|---|---|---|---|
| rechts (x = 88 mm) | 96,3° (X = −6,3°) | 97,4° | 96,8° |
| links (x = −85 mm) | 96,4° | 97,4° | 96,8° |

  Der Schalter löst also etwa 0,4° vor dem Anschlag aus. Die Rolle hat bis zum Aufliegen des Hebels rund 0,7° Reserve (am Hebelarm von etwa 93 mm Radius rund 1 mm). 1° entspricht an der Rolle etwa 1,5 mm Weg. Gerechnet für den rechten Querträger: Bei Vorlauf 1,0 mm löst der Schalter bei 96,0° aus, bei 1,5 mm bei 96,3°, bei 2,5 mm erst bei 97,0°, also **nach** dem Aufliegen des Hebels bei 96,8° (dann schaltet er nie vor dem Anschlag; Abhilfe: Beilage, die die Rolle höher stellt, oder ein anderer Schalter). **Das sind Eingabewerte, keine Messergebnisse.** Mit Druck- und Schaltertoleranzen (0,2 bis 0,3 mm) bleibt die Reserve klein.
- **Rolle und Hebel:** Der Hebel ist 20 bis 40 mm dick. Die Rolle (Durchmesser 5 mm angenommen, Mitte bei z = 37 mm, Rollenhebel nach +z) liegt damit bei z = 34,5 bis 39,5 mm: 0,5 mm Rand zur Hebelkante, 14,5 mm zur anderen. Das ist knapp. Das Skript bricht ab, wenn die Rolle näher als 0,5 mm an die Hebelkante kommt. Ob der Rollenhebel nach +z oder über den Körper zeigt, hängt vom gekauften Schalter ab; das ist die Messung mit der grössten Wirkung.
- **Anschlagwand und Last:** Der Hebel trifft die Querträgerkante zuerst an der äusseren Ecke (x ≈ 95 mm), also auf der Seitenwand der Tasche (3,55 mm × 20 mm Hebeldicke = 71 mm² statt 280 mm² beim Vollquerträger). Statisch (11,8 Nm, Kontaktradius 101 mm) sind das rund 117 N und 1,6 MPa. Bei einem Fall des 6,3-kg-Gewichts aus 30 mm (1,85 J) wäre die Spitzenlast um ein Vielfaches höher und für 71 mm² PLA nicht belegt. **Deshalb: Der Querträger mit Schalter wird nur für Messungen ohne oder mit kleiner Last benutzt (Referenzfahrt, Wiederholbarkeit). Für Haltetest und Rücklauftest mit 5,9 und 6,3 kg wird wieder der Original-Querträger eingesetzt.**

**Reihenfolge:** Schalter kaufen (`micro limit switch roller 10pcs`, steht in `docs/bom.md`). `J2_Schalterprobe` drucken (ca. 20 min; ihre Längskante entspricht der Kante z = 0 des Querträgers, die Masse z gelten also für beide Teile). Am Schalter und an der Probe messen und im Skript nachführen:

| Mass | Startwert | Wie messen |
|---|---|---|
| Körper Länge × Höhe × Dicke | 20 × 10,5 × 6,5 mm | Schieblehre; muss in die Tasche (6,9 mm breit) passen |
| Lochabstand | 9,5 mm | Schieblehre; Löcher der Probe müssen fluchten |
| Rollendurchmesser | 5 mm | Schieblehre |
| Rollenmitte, Abstand vom Körperende | 6 mm (Hebel nach +z) | Schieblehre; auf der Probe ist z direkt ablesbar |
| Höhe der freien Rolle über dem Körper | 5,5 mm | Schieblehre, Schalter auf ebener Fläche |
| Vorlauf bis zum Schalten, Restweg | 1,5 / 1,6 mm | Schalter auf der Probe mit Durchgangsprüfer, Rolle mit dem Tiefenmass der Schieblehre niederdrücken |

Erst dann den Querträger drucken. Stimmt der Rollenhebel nicht (Richtung, Länge), Skript ändern oder die Idee verwerfen.

**Messablauf Wiederholbarkeit (Entwurf, nicht erprobt):** Querträger mit Schalter rechts einbauen, Messuhrhalter in der Lage «links» (Halter steht dem Hebel gegenüber; `docs/pruefstand-j2.md`), Messuhr mit höchstens 1 mm Vorspannung auf den Tastklotz (7,5 mm Weg bis zum Anschlag plus Vorspannung müssen in die 10 mm Messbereich passen). Motor bestromt. Hebel stets von oben zum Schalter fahren, **langsam** (0,05°/s, `G1 F3`, das sind etwa 0,06 mm/s am Tastklotz: eine Ablesezeit von 0,3 s kostet dann nur 0,02 mm), bei Schalten (Durchgangsprüfer am Schalter, Multimeter ohne Summer: Anzeige springt) die Messuhr ablesen, danach 5° zurück. 20 Wiederholungen; die Streuung der Ablesungen in mm geteilt durch 64 mm (Radius des Tastklotzes) ergibt die Wiederholbarkeit im Bogenmass. Der Messbereich 10 mm der Messuhr deckt die 7,5 mm Weg am Tastklotz bis zum Anschlag ab. Der Schaltereingang an der Steuerung ist für den Uno-Aufbau nicht vorgesehen (`docs/grbl-j2.md`: keine Endschalter): Die Messung geschieht mit dem Durchgangsprüfer, ohne Firmware.

## Motorkabelklemme (`J2_Motorkabelklemme`)

Ein Sattel (54 × 20 × 7 mm) auf dem Motorgehäuse (42,3 mm), an den Flügeln mit zwei Kabelbindern um den Motor gespannt. Die Rille (Ø 6,4 mm, in Achsrichtung des Motors) nimmt das Kabel auf, zwei Kabelbinder-Schlitze darüber halten es (Zugentlastung). PETG, weil der Motor warm wird (`docs/konzept.md` 3.3). Es braucht kein Loch im Prüfstand. Die Klemme liegt auf einer ebenen Motorseite; die Motorecken sind abgeschrägt, die Fläche ist etwas schmaler als 42,3 mm, das Teil ist aber flach und sitzt auf der Mitte. Kabel und Austrittsstelle am Motor sind nicht geprüft: Rille passt für vier Adern im Mantel, sonst `KL_RILLE_D` im Skript ändern. Die Seite des Motors (oben, unten) ist frei; das Kabel soll nicht über die Riemen laufen. Am anderen Ende der vorhandene `Kabelhalter` auf dem Grundbrett.

Nicht gelöst: die Zugentlastung der drei Motorkabel an der Rückwand des Elektronikgehäuses. Die Wanne ist gedruckt und hat dort keine Schlitze (offene Idee 5 in `docs/offene-ideen.md`).

## Kollision und Bauraum

Alle Teile liegen weit unter 240 mm (grösstes 56 mm). Der Querträger mit Schalter ändert die Aussenmasse des Originals nicht und nimmt nur Material weg, kann also keinen anderen Körper des Prüfstands berühren; die Rolle (nicht modelliert) steht im Hebelraum z 34,5 bis 39,5 mm über der Kante und wird nur vom Hebel erreicht (gerechnet, nicht im CAD mit dem Hebel in Schräglage geprüft). Die Motorkabelklemme wurde nicht gegen den Prüfstand geprüft; sie liegt an einer Motorseite, die zum Riemen hin frei bleiben muss.

## Nabenlehre für die gekauften Ritzel: gestrichen

Eine gedruckte Lehre prüft Nabenlänge und -durchmesser nicht besser als die Schieblehre (ihr gedrucktes Mass hat selbst ±0,1 mm), und die Grenzwerte aus dem Prüfstandsskript decken nicht alles ab. Stattdessen **Sollwerte zum Nachmessen** (Annahmen aus `cad/skripte/j2_pruefstand.py`, Bordscheiben und Naben ungeprüft):

| Ritzel | Messen | Soll |
|---|---|---|
| 3M Z16 auf Welle A | Gesamtlänge vom linken Bordrand bis zum Nabenende | höchstens 26,0 mm (Skript-Annahme 24,5 mm); sonst weniger als 1 mm Luft zur rechten Wange (56 mm). Der Distanzring A rechts ist dafür parametriert; bei Nabe 7,5 statt 6 mm schrumpft er auf etwa 0,7 mm, also Dicke prüfen |
| 3M Z16 | Nabendurchmesser | Annahme 14 mm; kleiner als die Bordscheibe Ø 18 mm |
| 5M Z18 auf Welle B | Nabenlänge ab Rückseite der Bordscheibe | höchstens 8,1 mm (Skript-Annahme 8,0 mm, Bohrung der Z64-Scheibe reicht bis 29,6 mm) |
| 5M Z18 | Nabendurchmesser | höchstens 20,3 mm (Bohrung der Scheibe); Annahme 20 mm |

Ist die Nabe zu lang, hilft kein Druckteil: Nabe an der Drehbank kürzen (Opa) oder anderes Ritzel bestellen.
