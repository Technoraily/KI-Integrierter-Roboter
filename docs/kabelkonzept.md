# Kabelkonzept (Entwurf 26.11.2026, Entscheide am selben Tag)

Ziel: Wer den Arm nachbaut, steckt alle Kabel ohne Löten, ohne Rätselraten und ohne Fummelei zusammen. Die Kabelführung ist Teil der Konstruktion (`docs/konzept.md`, Abschnitt «Kabelführung ist Teil der Tragstruktur»), nicht Nacharbeit. Das ist ein **Entwurf auf Basis von Annahmen**, nichts davon ist in Fusion geprüft; die offenen Punkte stehen unten.

## Regeln (gelten für jedes Teil, das konstruiert wird)

1. **Alles steckbar.** Jeder Kabelbaum endet an beiden Seiten in Steckern. Am Arm wird nicht gelötet und nicht gecrimpt.
2. **Unverwechselbar.** Jede Funktion hat eine eigene Steckerfamilie oder Polzahl, Gehäusefarbe und Kodierung; zwei Stecker, die auf dieselbe Buchse passen, dürfen nicht dieselbe Funktion haben. Motor: JST-XH 4-polig; Endschalter: JST-XH 2-polig; Bremse: JST-VH 2-polig (3,96 mm Teilung, passt mechanisch nicht auf XH); Servo: üblicher 3-poliger Servostecker. Motor- und Endschalterstecker sind verschieden lang beschriftet und farbig (Motor weiss, Endschalter blau, Bremse rot).
3. **Beschriftet.** Beide Enden jedes Kabels tragen dasselbe Etikett («J3 Motor»). Das Etikett steht auch in Anleitung und Stückliste.
4. **Länge nach Tabelle.** Jedes Kabel hat eine Länge: Weg durch den Arm plus Bewegungsreserve (Gelenkbereich) plus 20 % Montagereserve. Keine «lange genug»-Kabel.
5. **Führung durch das Teil.** Kanäle, Hohlwellen und Klemmpunkte sind im CAD modelliert (Querschnitt, Biegeradius, Zugentlastung am Teil). Kabel werden nicht gebogen, bis sie passen.
6. **Montierbar in einer Richtung.** Es gibt eine feste Reihenfolge, in der Kabel eingezogen und gesteckt werden, und sie steht in der Bauanleitung. Jeder Stecker ist von aussen erreichbar, ohne eine Baugruppe wieder abzubauen, die schon geschraubt ist.
7. **Prüfbar.** Jedes Kabel lässt sich mit dem Multimeter durchmessen (Durchgang je Ader). Eine Prüftabelle gehört in die Anleitung.

## Was durch den Arm läuft (Annahme: alle Motoren oberhalb von J1)

| Funktion | Adern | Querschnitt | Hinweis |
|---|---|---|---|
| Motor je Gelenk (J2 bis J6) | 4 | 0,25 mm² (AWG24) | je Spule ein verdrilltes Paar (Rot–Blau, Grün–Schwarz bei den 17CS04A-170E); Strom bis 1,77 A |
| Endschalter je Gelenk (J2 bis J6) | 2 | 0,14 mm² | mechanischer Mikroschalter als Öffner (Signal, Masse); Kabelbruch löst Alarm aus |
| Bremse J2 und J3 | 2 | 0,25 mm² | 24 V, Strom laut Datenblatt der Bremse (angenommen unter 0,5 A), Freilaufdiode am Verbraucher |
| Greifer-Servo | 3 | 0,25 mm² | 5 V, Signal, Masse; Ansteuerung offen (siehe unten) |
| Werkzeugwechsler | 4 | 0,14 mm² | Riegel-Servo-Signal, Riegel-Endlage, Werkzeug-ID (Codierwiderstand gegen Masse), 1 Reserve; Riegel-Servo teilt 5 V und Masse mit dem Greifer-Servo. Auf der Trennstelle nur Pogo-Kontakte: 5 V (geschaltet), Masse, Greifer-Signal, ID, 2 Reserve |
| Kamera | 1 USB-Kabel, geschirmt | – | zum Rechner, nicht zum Board |

Summe Adern ohne Kamera: 5×4 + 5×2 + 2×2 + 3 + 4 = **41 Adern**. Rechnung zum Platz: Ader mit Isolierung ca. 1,2 mm Durchmesser; 41 Adern mal 1,2 mm² Querschnitt ergibt ca. 49 mm², mit dem Faktor 0,6 für lose Packung ca. 82 mm², also ein Bündel von etwa **10 mm Durchmesser** plus das USB-Kabel (ca. 4 mm). Annahmen, nicht gemessen.

## Die kritischen Stellen

| Stelle | Anforderung | Offen |
|---|---|---|
| **J1-Hohlwelle** (Dünnringlager 6810/6813) | Bündel von ca. 10 mm plus USB-Kabel; freier Durchmesser **mindestens 25 mm**, damit Platz für Reserve und Stecker bleibt (Innendurchmesser 6810: 50 mm, Hohlwelle damit bis ca. 40 mm möglich) | Wandstärke und Steckerplatz im CAD prüfen |
| **J1 Verdrehung** ±170° | Kabel in der Hohlwelle verdrillen sich um bis zu 340° zwischen den Endlagen. Faustregel: freie Länge in der Hohlwelle mindestens 150 mm, Kabel nicht an der Wand klemmen | Faustregel ungeprüft; am Teststück messen oder aus der Literatur belegen |
| **Schulter J2** ±90° | Bündel schlaufenförmig um die Achse legen, Biegeradius mindestens das Zehnfache des Bündeldurchmessers (ca. 100 mm), sonst Kabelkanal mit Schleppkette im Gelenk | Biegeradius gegen Bauraum der Schale prüfen |
| **Ellbogen J3** ±135° | wie J2, grösserer Bereich | wie oben |
| **Hand J4 bis J6** | Nur noch Kamera, Greifer, Werkzeugwechsler und die Motor- und Endschalterkabel der Hand laufen im Unterarm; Kabelkanal bis zum Flansch mit mindestens 6 Adern plus USB (`konzept.md`, Handgelenk) | Lage der Motoren J4 bis J6 festlegen |

## Basis austauschbar (Anforderung des Nutzers, 7. Achse später)

Die Basis wird später auf den Schlitten der Schiene (J0) gesetzt oder gegen eine andere Basis getauscht. Darum gilt:
- **Mechanische Schnittstelle:** Lochbild 120 mm, 4× M5 im Quadrat, dazu ein Zentrierring (`parameter.md`, `a_lochbild_basis`). Jede Basis hat dasselbe Lochbild.
- **Elektrische Schnittstelle:** Alle Leitungen von der Basis zum Rest laufen über ein **Steckerfeld an einer festgelegten Stelle** (gleiche Lage und Belegung bei jeder Basis). Wird die Basis getauscht, werden nur diese Stecker gezogen und wieder gesteckt, nichts im Arm.
- **Zur Steuerung:** Ein Kabelbaum von der Basis zum Octopus; bei der Schiene führt er über die Schleppkette (J0). Länge und Stecker sind für beide Fälle gleich.

## Octopus (laut `docs/verdrahtung.md`)

7 Treiber (der 8. Sockel ist Reserve), 7 von 8 Endschalter-Eingängen (J0 bis J6; die zwei Schienen-Endschalter in Reihe auf einem Eingang), Not-Aus trennt die Motorspannung und zieht zusätzlich den E-Stop-Eingang. **Bremsen:** Für J2 und J3 braucht es je einen geschalteten 24-V-Ausgang. Das Konzept nennt dafür frei bleibende Pins (PB6, PB7, PC0). Vorgeschlagen: je ein kleines MOSFET-Modul mit Freilaufdiode, das vom Pin geschaltet wird. Ob grblHAL diese Pins als schaltbare Ausgänge zur Verfügung stellt, ist **nicht geprüft** und gehört in den Machbarkeitstest.

## Entscheide (26.11.2026: Nutzer hat die Wahl an Claude übergeben)

1. **Greifer-Servo:** Statt des Arduino Uno (nicht zur Hand) steuert ein **Raspberry Pi Pico** den Servo, im Elektronikgehäuse neben dem Octopus, per USB am Rechner. Er übernimmt dieselbe Rolle wie der Uno im Konzept («Greiferbefehl erst nach Status Idle»), kostet wenige Franken und lässt das Board und die Firmware des Octopus unberührt. Der Servo bekommt 5 V über einen eigenen Wandler; drei Adern laufen durch den Arm. Begründung: ein Eingriff in grblHAL für einen Servo-PWM-Ausgang wäre ungeprüft und für Nachbauer riskanter. Nicht geprüft: Pico-Programm (Servobibliothek in MicroPython oder Arduino), Stromaufnahme des Servos.
2. **Endschalter:** **mechanische Mikroschalter als Öffner** mit 2 Adern. Gründe: billig, bekannt, die vorhandenen CAD-Halter (`standardteile.py`) sind dafür gezeichnet, Kabelbruch führt zu Alarm statt zu einem ungefährlichen Fehlsignal. Die Wiederholgenauigkeit eines Mikroschalters liegt nach Erfahrung bei ca. 0,02 bis 0,05 mm am Auslöser (nicht für diese Schalter gemessen); bei einem Auslöser 50 mm von der Gelenkachse sind das unter 0,06°. Wiederholbarkeit am gebauten Arm messen; wenn sie nicht reicht, auf Hall-Sensoren mit 3 Adern wechseln.
3. **Steckerfamilie:** **JST-XH** für Motor (4-polig) und Endschalter (2-polig), **JST-VH** für die Bremse (2-polig, 3,96 mm Teilung, passt nicht auf XH). Vorkonfektionierte Kabelsets sparen das Crimpen, haben aber feste Längen; Länge je Kabel nach der Kabeltabelle der Bauanleitung. Nennstrom je Kontakt laut Hersteller ca. 3 A bei XH (genügt für 1,77 A, nicht geprüft).
4. **Wo die Motoren sitzen** (am Gelenk oder in der Säule): bestimmt, ob das Bündel in der J1-Hohlwelle 41 Adern oder weniger trägt. Wird bei der Konstruktion von Schulter und Oberarm festgelegt.

## Für die Konstruktion (Reihenfolge)

1. Basis und J1: Hohlwelle (mindestens Ø 25 mm frei), Steckerfeld, Kabelzugentlastung am Austritt zur Steuerung.
2. Schulter: Kabelschlaufe um J2, Klemmung, Bauraum für die Bremse.
3. Oberarm und Ellbogen: Kabelkanal, Biegeradius, Bremse J3.
4. Unterarm und Hand: Kabelkanal bis zum Flansch, Kamera, Greifer.
5. Zum Schluss ein Kabelplan mit Längen und Prüftabelle in die Bauanleitung.
