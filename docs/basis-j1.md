# Basis mit J1 (Bauraummodell V2.2, Stand 26.11.2026)

CAD: `cad/skripte/basis_j1.py` (Fusion, Komponente `Basis_J1`; V1 in `basis_j1_v1.py`). Prüfungen: `montage_basis.py` (Endzustand, Drehung ±170°, alle Einschiebewege, Werkzeugzugang) und `kollision.py`. Stückliste: [stuecklisten/basis-j1.md](stuecklisten/basis-j1.md). Gutachten: [reviews/2026-11-26-basis-j1.md](reviews/2026-11-26-basis-j1.md). Renders: `cad/renders/basis_j1_v2_*.png`.

## Aufbau

- **Grundplatte** (ein Druckteil):
  - Achteck Ø 184 mit **fest stehendem, hohlem Lagerzapfen** (Ø 30 mm frei für die Kabel, Vorgabe ≥ 25) und 7 Rippen (5 × 10 mm).
  - Nach hinten eine Lasche für den Bock der Zwischenwelle.
  - Sie wird mit **8 Holzschrauben** auf die Holzplatte geschraubt: 4 bei r 70 und 4 bei r 40. Die bei r 40 liegen unter der Nabe und kommen vor ihr hinein.
  - Kabelfenster nach +y (24 × 10,5 mm, z 5,5–16).
- **J1-Lagerung:** zwei Dünnringlager **6810** (50 × 65 × 7) mit 40 mm Abstand in **O-Anordnung**.
  - Die Innenringe werden zusammengedrückt: unten durch den Bund (Ø 53), oben durch den Spannring.
  - Die Aussenringe liegen an den Schultern der Nabe (Ø 62, berühren die Dichtungen nicht).
  - **Vorspannung über einen O-Ring 50 × 1,5 (NBR)** in einer Nut 2,0 × 0,6 mm im Spannring (aussen Ø 56).
  - Der Spannring wird mit 3 × M3 × 10 **auf Block** gegen die Zapfenoberkante gezogen. Über dem Lager hat er 0,5 mm Freistich und berührt das Lager nur über den O-Ring (ca. 27 % verpresst).
  - Die Kraft ist damit wiederholbar und nicht «nach Gefühl». Der Spannring ist Teil der Passprobe.
- **Nabe = Drehteller** (ein Druckteil, grau):
  - Unten die **3M-Scheibe mit 80 Zähnen** (echtes Zahnprofil, Borde als 45°-Kegel), oben der 12-eckige Teller r 72.
  - Halbmond, Mitnehmer und oberer Bord haben 45°-Kegel bzw. -Keile. Die Nabe wird kopfüber ohne Stützen gedruckt.
  - Das untere Lager wird **von unten** eingepresst (Bohrung darunter Ø 66), das obere von oben.
  - Dazu der **Halbmond** (halber Ring r 37–44) für den Endschalter und ein **Mitnehmer** für den festen Anschlag.
- **Schnittstelle zur Säule** (gleich bei jeder späteren Basis):
  - Lochbild 120 mm, 4 × M5, die Muttern sitzen unten im Teller.
  - Zentrierzapfen der Säule **Ø 65,0 in der Nabenbohrung Ø 65,2, höchstens 8 mm tief, innen ≥ Ø 58 frei**. Darunter steht der feste Spannring (Schraubenköpfe bis z 94), und die drehende Säule darf ihn nicht berühren.
- **Antrieb 20:1:**
  - Stufe 1: **GT2 20:80**, Riemen 240 mm, Achsabstand 67,3.
  - Stufe 2: **3M 16:80**, Riemen **318 mm (106 Zähne)**, 15 mm breit, Achsabstand 81,3. Damit liegt die Zwischenwelle ausserhalb des Tellers und kann von oben eingeschoben werden. Am 16er-Ritzel greifen 6,0 Zähne.
  - Der Motor **17CS04A-170E** hängt im Kasten unter der Motorplatte (PETG), 1 mm über dem Boden.
- **Zwischenwelle:**
  - 8 mm mit D-Flächen für die Madenschrauben, zwei 608.
  - Sie sitzt in einem **zweiteiligen Bock**: Der untere Teil mit Rücken steht auf der Lasche, der obere Arm wird flach gedruckt und mit 2 × M3-Senkschrauben und 2 Stiften aufgesetzt.
  - Befestigt mit 4 Langlöchern und M3-Muttern unten in der Lasche.
- **Spannen:**
  - **Stufe 2:** Bock **nach hinten (−x)** ziehen, mit der Spannschraube M3 × 16 aus dem festen Klotz hinter dem Bockrücken (bei y 35). Die Spannung bleibt so stehen und kriecht nicht zurück.
  - **Stufe 1:** Motorplatte nach hinten schieben (7 mm Weg, Langlöcher 12 mm).
  - Sollspannung (Richtwert, gerechnet mit geschätzter Riemenmasse, nicht geprüft):
    - 3M ca. **70 N**: freie Länge 75 mm schwingt mit ca. **270 Hz**. Bei 50 N könnte der Riemen überspringen, bevor der Motor Schritte verliert (Gutachten Runde 2).
    - GT2 ca. **20 N**: freie Länge 64,5 mm schwingt mit ca. **300 Hz**.
    - Messen mit einer Handy-App («belt tension», Gitarrenstimmer).
- **Endschalter J1:**
  - KW11 mit Rolle, **liegend** auf einem kleinen **Schalterhalter** vorne (+x). Der Schalter wird am Tisch mit 2 × M2 × 12 aufgeschraubt (Muttern unten im Halter).
  - Der Halter wird von vorne auf den Absatz der Grundplatte geschoben und mit 1 × M3 × 10 waagrecht festgeschraubt. Unter dem Teller kommt man von oben nicht an den Schalter, von vorne schon (Gehäuse ab).
  - Die Rolle steht frei bei r 42,7. Der Halbmond (r 44) drückt sie 1,3 mm, und Rampen an seinen Enden fahren die Rolle sanft an.
  - **Den gekauften KW11 vor dem Druck ausmessen.** Die Masse im Modell sind angenommen.
  - Der **Halbmond** drückt ihn, solange J1 auf der einen Seite steht (0° bis 180°). Aus dem Schalterzustand ist sofort klar, auf welcher Seite der Arm steht. Die **Referenz ist die Flanke bei 0°**, also in der Mitte des Bereichs. Die Referenzfahrt geht nie an den Rand.
  - **Fester Anschlag:** Der Mitnehmer an der Nabe trifft einen Finger bei 25°, seitlich vom Schalter.
    - Er greift zwischen ±171° (noch frei) und ±176° (greift), im CAD geprüft.
    - Der Pfosten ist massiv (r 52–70, 16 mm breit). Bei 1,0 A Motorstrom (ca. 104 N am Finger) ergibt das ca. 6 MPa Biegung, PLA hält quer zu den Schichten 15–25 MPa.
    - Fällt der Schalter aus, reisst so trotzdem kein Kabel ab.
  - **Seitenerkennung im CAD geprüft:** Der Schalter ist gedrückt für J1 +5° bis +175° und frei für −5° bis −175°.
  - **Schaltweg einstellen:** Zwischen der Halterlasche und dem Absatz liegt 1 Scheibe M3 (0,5 mm). Mit 0 oder 2 Scheiben verschiebt sich die Rolle um ±0,5 mm.
- **Kabelweg:**
  - Aus dem Zapfen durch das Fenster nach +y, unter der Nabe (11 mm frei bis zur Scheibe, das Bündel ist 10 mm), entlang y 40–50 nach hinten.
  - Mit **2 Kabelbindern durch die Ösen** in der Grundplatte flach niederhalten, damit nichts an der drehenden Nabe streift.
  - Über die Bocklasche (z 15–26) in den Kasten zum Steckerfeld.
  - Im CAD als Platzhalterkörper geprüft: Er wird bei keiner Drehlage berührt.
- **Steckerfeld:** Platzhalter im Kasten (+y-Seite). Das Kabel zum Octopus führt hinten durch eine **Kabelverschraubung M16** (bei y 30).
- **Schalen** (tragen nichts):
  - **Sockelgehäuse** und **Farbring** sind zweiteilig (links/rechts), weil der Teller grösser ist als ihr Loch.
  - Halt mit Magneten an der Grundplatte und an der vorderen Fuge, 2 Zylinderstifte richten aus.
  - Die **Kastenkappe** (weiss, massiv modelliert, mit 15 % Füllung gedruckt) sitzt mit 4 Magneten.
  - Die Zylinderstifte werden **im Gehäuse festgeklebt**, nicht in der Grundplatte.
  - Alle Magnete 6 × 3 (28 Stück), Buckel mit Stützkegeln (druckbar ohne Stützen).

## Rechnung

- **Kippmoment auf die Lager:**
  - Höchstens ca. 12–15 Nm (grösstes J2-Moment 11,8 Nm laut `lastrechnung.md` plus Säule).
  - Das gibt bei 40 mm Abstand ca. **375 N radial je Lager**.
  - Ein 6810 trägt laut Katalog ca. 6 kN (nicht im Datenblatt geprüft), also grosse Reserve. Flächenpressung im PLA-Sitz ca. 0,8 N/mm².
- **Riemenkräfte J1:**
  - Mit vollem Motorstrom wären beide Riemen überlastet: 8,4 Nm am Gelenk ergeben 3M 220 N (zulässig 168 N) und GT2 66 N (zulässig 44 N).
  - J1 braucht nur Beschleunigung, ca. **1,5 Nm** (0,4 kg·m² × 2 rad/s² + Reibung).
  - **Darum Motorstrom J1 auf 1,0 A begrenzen** (ca. 5 Nm am Gelenk): 3M 131 N, GT2 39 N, beide unter der Grenze. Bei einem Zusammenstoss verliert der Motor Schritte, bevor ein Riemen Schaden nimmt.
  - Die 608 der Zwischenwelle liegen nur mit dem Aussenring auf (Freigang Ø 13 im Bock), der drehende Innenring schleift nicht.
- **Kippsicherheit des ganzen Roboters:**
  - Mit 1 kg ausgestreckt kippt er um die Vorderkante einer 300 × 250-Platte mit ca. 7,8 Nm.
  - Basis, Motor und Platte halten nur ca. 3–4 Nm dagegen.
  - **Die Holzplatte muss mit 2 Schraubzwingen am Regal festgemacht oder angeschraubt werden.** Lose aufgestellt kippt der Arm.
- **Spiel J1:** gleich gebaut wie J2 (vorgespannte Riemen, gemessen unter 0,01°). Für J1 ist das erwartet, aber **nicht gemessen**.

## Montage (Reihenfolge einhalten, sonst passen die geschlossenen Riemen nicht)

1. **Einsätze und Muttern vor dem Anschrauben:**
   - Einschmelzgewinde: Zapfen 3, Bock 3 (2 oben im Rücken, 1 hinten im Rücken für die Spannschraube), Kasten 4, GT2-80-Scheibe 2.
   - Absatz vorne: 1 Einschmelzgewinde waagrecht für den Schalterhalter.
   - **4 M3-Muttern** von unten in die Lasche (Tropfen Kleber).
   - 4 M5-Muttern unten in den Teller.
   - Welle: 2 D-Flächen 0,5 mm tief anfeilen, an den Stellen der beiden Scheiben.
2. Grundplatte (8 Holzschrauben) und Kasten (3 Holzschrauben) auf die Holzplatte schrauben, Holzplatte am Regal festmachen.
3. Unteren Bockteil mit 608 auf die Lasche setzen (4 × M3 × 10 mit Scheibe, locker), Spannschraube M3 × 16 mit Scheibe durch den Klotz in den Rücken drehen.
4. Unteres 6810 **von unten** in die Nabe drücken.
5. **3M-Riemen um die Nabenscheibe legen**, Nabe mit dem Mitnehmer nach hinten (−x) von oben auf den Zapfen setzen. Den Riemen dabei nach hinten zum Bock führen.
6. Oberes 6810 von oben in die Nabe und auf den Zapfen drücken. O-Ring in den Spannring legen, Spannring mit 3 × M3 × 10 **bis auf Block** anziehen.
7. Den oberen Bockarm (mit 608) **ca. 11 mm über dem Bock von hinten einschieben** und dann auf die 2 Stifte absenken. Von oben geht es nicht, weil der Teller darüber liegt. Mit 2 × M3 × 16 Senkkopf festschrauben.
8. Die Welle von oben durch das obere 608 schieben und dabei der Reihe nach aufreihen:
   - Distanzring oben.
   - GT2-80-Scheibe, **den GT2-Riemen vorher umlegen**.
   - 3M-Ritzel, **es muss im 3M-Riemen liegen**.
   - Distanzring unten, dann ins untere 608.

   Danach die Madenschrauben auf die D-Flächen anziehen.
9. Stufe 2 spannen: Spannschraube anziehen, bis die Sollspannung erreicht ist, dann die 4 Bockschrauben festziehen.
10. Motor unter die Motorplatte (4 × M3 × 10 mit Scheibe), GT2-20-Ritzel auf die Welle, Platte mit Motor in den Kasten. GT2-Riemen auflegen, nach hinten spannen, 4 × M3 × 10 festziehen.
11. Endschalter am Tisch auf den Halter schrauben (2 × M2 × 12, Muttern unten). Den Halter mit der Rolle voran von vorne auf den Absatz schieben und mit M3 × 10 festschrauben. Kabel anstecken.
12. Gehäusehälften aufsetzen (Stifte, Magnete), Farbring aufsetzen, Kappe aufsetzen.

**Abnehmen der Schalen** (für Service): zuerst die Kappe, dann den Farbring, dann jede Gehäusehälfte 4 mm anheben (Stifte), 3 mm nach vorne und seitlich wegziehen. **Riemenwechsel 3M:** Der Riemen umschliesst den Zapfen. Dafür müssen Arm und Nabe herunter, das ist bei dieser Bauart normal.

## Offen

- **Passprobe 6810** zuerst:
  - Sitz Ø 65,2 und Zapfen Ø 49,9 mit 3 Einsätzen, dazu 3 Magnettaschen und der echte Spannring mit O-Ring.
  - Die Einsätze vor dem Messen setzen.
  - Danach die Masse im Skript nachführen.
- Kaufritzel (3M-16, GT2-20) nach dem Kauf messen. Die Zähne müssen mit den gedruckten Scheiben fluchten, sonst mit Distanzringen ausgleichen.
- Steckerfeld konstruieren (mit der Säule, wenn die Kabelzahl feststeht). Kabelschlaufe für ±170° in der Säule.
- Gutachten Runde 2.
