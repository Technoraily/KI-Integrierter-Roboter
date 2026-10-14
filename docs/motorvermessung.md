# Motorvermessung

Erster Schritt von Phase 2. Ziel: das Moment der drei vorhandenen Motoren (17CS04A-170E) messen, weil kein Datenblatt auffindbar ist und die Lastrechnung von diesem Wert abhängt. Alles geht **ohne Kaufteile**: gedruckter Motorprüfstand, Schnur, Wasserflaschen und die Küchenwaage. M3-Schrauben und Muttern sind vorhanden.

![Motorprüfstand](../cad/renders/Motorpruefstand_iso.png)

## Sofort möglich (ohne Druckteile)

| Messung | Wie | Erwartung |
|---|---|---|
| Gehäuselänge ohne Welle | Schieblehre oder Lineal | ca. 40 mm |
| Wicklungswiderstand | Multimeter zwischen den zwei Adern einer Wicklung (die Paare findest du per Durchgangsprüfung) | 1,5–2,5 Ω bei einem 1,7-A-Motor |
| Welle | Durchmesser, Länge ab Flansch, hat sie eine Abflachung? | 5 mm, ca. 22–24 mm |

Liegt der Widerstand deutlich höher (z. B. 30 Ω), ist es ein Motor für kleinen Strom und die Annahme 1,7 A falsch.

## Der Prüfstand

**Bauanleitung mit Bildern: [bauanleitung/motorpruefstand.md](bauanleitung/motorpruefstand.md).** Skript: `cad/skripte/motorpruefstand.py` (Fusion-Dokument «Nema 17 Prüfstand 40mm»). Teile und Material: [Stückliste](stuecklisten/motorpruefstand.md). Gutachten: `docs/reviews/2026-10-14-motorpruefstand.md`.

- **Motorhalter:** Grundplatte 200 × 110 mm mit Wiege. Der Motor wird von oben eingelegt, sein Bund steckt im Schlitz der Stirnwand. Die Wiege hält das Gegenmoment über die Kanten des Motors, es braucht keine Schrauben. Hast du vier M3 × 8–10, kannst du den Motor zusätzlich durch die Stirnwand anschrauben.
- **Niederhalter:** Er wird mit zwei Zapfen oben in die Wände gesteckt, damit der Motor nicht herausspringt.
- **Waagebalken (Test A):** Er ist symmetrisch, sein Eigengewicht erzeugt also kein Moment. Die Schnurlöcher liegen genau 100 mm von der Wellenmitte.
- **Seiltrommel (Tests B und C), gestuft:** Der äussere Kern hat Ø 39 mm, mit 1-mm-Schnur ergibt das **20 mm** Wickelradius, für 60 und 120 U/min. Der innere Kern hat Ø 19 mm, also **10 mm** Wickelradius, für 240 und 360 U/min. Mit dem kleinen Radius reicht der Hub für die Beschleunigung, und dieselbe Flasche ergibt das halbe Moment.
- Waagebalken und Seiltrommel werden mit je einer M3 × 16 (× 14 bis × 20 geht) und einer Mutter auf die Welle geklemmt. Hat die Welle eine Abflachung, kommt der Schlitz der Nabe über die Fläche. Zwischen Nabe und Stirnwand 1–2 mm Luft lassen, damit nichts schleift.

**Aufstellung:** Die Vorderkante der Grundplatte (die Seite mit Welle und Hebel) ragt **20 mm über die Tischkante**. Hebel, Trommel und Schnur hängen dann frei, und nichts streift an der Kante. Den hinteren Teil der Platte **mit einer Schraubzwinge** durch eines der zwei Löcher am Tisch festmachen. Ohne Zwinge mindestens **4 kg** Bücher hinten auf die Platte legen und zusätzlich mit der Hand drücken. Bei Test B zieht die Last bis zu 1,1 Nm Kippmoment über die Kante (3 kg an der Stufe r = 10 mm, 38 mm vor der Kante). Lege ein Tuch oder einen Karton unter die Flasche, weil sie beim Durchrutschen fällt.

**Elektrik:** Arduino Uno mit CNC-Shield und A4988 auf der X-Achse, Netzteil **12 V / 4 A** (vorhanden; für einen Motor bei 1,0 A reicht das mehrfach). Das Moment bei Drehzahl hängt stark von der Spannung ab, die Lastrechnung nimmt 24 V an. Test A (Haltemoment) ist von der Spannung unabhängig. Test B fällt an 12 V bei 240 und 360 U/min **tiefer** aus als später an 24 V. Ein schlechter Wert dort ist also eine sichere untere Grenze und noch kein Grund zur Sorge. Alle drei Mikroschritt-Jumper unter dem Treiber stecken (1/16). Treiberstrom einstellen: Vref = I × 8 × R_sense. Der Widerstand steht auf dem Treiberbrett: «R100» heisst 0,1 Ω, also Vref = 0,8 × I; «R050» heisst Vref = 0,4 × I; «R200» heisst Vref = 1,6 × I. Für den Test I = **1,0 A**, und **der eingestellte Strom wird notiert**.

**Erst ein Wärmetest:** Motor 5 Minuten ohne Last bestromt halten (`$1=255`). Wird der A4988 so heiss, dass man ihn nicht anfassen kann, oder lässt der Motor zwischendurch los, braucht es einen Kühlkörper oder Lüfter. Sonst schaltet der Treiber mitten in Test A kurz ab, und das sieht aus wie Durchrutschen.

## Zusammenbau

Schritt für Schritt mit Bildern: **[Bauanleitung Motorprüfstand](bauanleitung/motorpruefstand.md)**.

## Test A: Haltemoment

1. GRBL: `$1=255` (Motor bleibt bestromt), `$100=8.889` (dann bedeutet X = Grad an der Welle). Eine kleine Bewegung senden, z. B. `G91 G0 X1`, damit der Treiber aktiv ist.
2. Waagebalken waagrecht ausrichten, mit der Wasserwaage-App auf dem Handy prüfen.
3. Leere Flasche mit einer Schnurschlaufe in das Loch bei 100 mm hängen.
4. Wasser **langsam** in Schritten von 20–50 ml einfüllen, bis der Balken durchrutscht. Kurz vor dem erwarteten Wert kleinere Schritte nehmen. Stösse lösen das Rutschen zu früh aus.
5. Flasche mit Schnur auf der Küchenwaage wiegen: das ist m.
6. Dreimal messen, dann auf der anderen Seite (Gegenrichtung) wiederholen. Alle drei Motoren messen.

Auswertung: **M = m × 9,81 × 0,100**, also Nm = Gramm × 0,000981. Beispiel: 350 g ergeben 0,34 Nm.

## Test B: Moment bei Drehzahl (Seilwinde)

1. Seiltrommel statt Waagebalken aufklemmen. Die Schnur durch das radiale Loch der gewünschten Stufe und das axiale Loch nach aussen fädeln, unter dem Aussenflansch verknoten. Die Flasche steht am Boden.
2. Mit einer kurzen Fahrt prüfen, ob positive X-Werte die Flasche heben. Wenn nicht, die Schnur andersherum wickeln oder `$3=1` setzen.
3. Die Schnur **einlagig nebeneinander** auf den Kern wickeln. Läuft sie in eine zweite Lage oder auf den Kegel, wird der Radius grösser und das Moment falsch.
4. Bei jeder Drehzahl die Flasche **300 mm** hochziehen und wieder ablassen. Wasser zugeben, bis der Motor stehen bleibt (er brummt, die Flasche sinkt zurück). Die letzte Last, die noch sicher hochkam, **samt Tasche und Schnur wiegen**: das ist m. Als Last eignen sich bis zu zwei 1,5-l-Flaschen in einer Tasche (bis ca. 3 kg).

| Stufe | Einstellungen | U/min | Befehl |
|---|---|---|---|
| r = 20 mm | `$100=25.46 $110=30000 $120=1000` | 60 | `G91 G1 X300 F7540` |
| r = 20 mm | | 120 | `G91 G1 X300 F15080` |
| r = 10 mm | `$100=50.93 $110=30000 $120=1000` | 240 | `G91 G1 X300 F15080` |
| r = 10 mm | | 360 | `G91 G1 X300 F22620` |

Die Einheit ist mm Schnur. Mit 1000 mm/s² braucht die schnellste Fahrt 71 mm Weg zum Beschleunigen, die übrigen weniger. Es bleibt also eine Strecke mit konstanter Drehzahl.

Auswertung: **M = m × 9,81 × r** (r = 0,020 bzw. 0,010 m). Beispiel: 1,4 kg an r = 20 mm ergeben 0,27 Nm. So entsteht die Momentenkurve über der Drehzahl; die Lastrechnung arbeitet mit dem Wert bei Betriebsdrehzahl.

## Test C: Schritte gehen nicht verloren

Unter Last und bei Arbeitsdrehzahl, nicht im Leerlauf. Die Last hat jeweils **etwa die Hälfte** der Masse, die in Test B bei dieser Drehzahl gerade noch hochkam. Vor dem Start die Lage der Flasche am Boden mit Klebeband markieren.

| Stufe | Einstellungen | Fahrt, je 5-mal hin und zurück |
|---|---|---|
| r = 20 mm, 120 U/min | `$100=25.46 $110=30000 $120=1000` | `G91 G1 X300 F15080`, dann `G91 G1 X-300 F15080` |
| r = 10 mm, 360 U/min | `$100=50.93 $110=30000 $120=1000` | `G91 G1 X300 F22620`, dann `G91 G1 X-300 F22620` |

Danach muss die Flasche wieder auf der Bodenmarke stehen, auf ±1 mm genau. Ein verlorener Vollschritt verschiebt die Schnur um 0,63 mm (r = 20) bzw. 0,31 mm (r = 10). Mehrere verlorene Schritte sind also sichtbar.

## Messfehler, die man kennen sollte

- **Schnurdicke:** Das «+ 0,5» im Radius gilt für 1-mm-Schnur. Bei anderer Dicke d gilt r = 19,5 + d/2 bzw. 9,5 + d/2. 0,5 mm Fehler ergeben 2,5 % bzw. 5 %.
- **Beschleunigung:** Bleibt der Motor beim Anfahren stehen, war die Last um bis zu 10 % höher (a = 1 m/s² gegenüber g). m ist also eine sichere untere Grenze.
- **Rastmoment und Lagerreibung** verfälschen nur um wenige Prozent.
- **Stösse** beim Einfüllen lösen das Rutschen zu früh aus. Auch das ergibt eine untere Grenze.
- **Umrechnen auf einen anderen Strom:** Das Moment steigt etwa im Verhältnis zum Strom, bei hohem Strom wegen Sättigung etwas weniger. Von 1,0 A auf 1,7 A linear hochzurechnen überschätzt also leicht.

**Wichtig für die Auswertung:** Im Mikroschrittbetrieb liegt der gemessene Wert schon unter dem Datenblatt-Haltemoment (bei Nennstrom etwa 70 %). Ein so gemessener Wert wird in der Lastrechnung **direkt** als nutzbares Moment eingesetzt, umgerechnet auf den späteren Strom des TMC2209.

## Protokoll

| Motor | Länge (mm) | Widerstand (Ω) | Netzteil (V) | Strom (A) | Test A: m (g) / M (Nm) | Test B: m (g) bei 60 / 120 / 240 / 360 U/min | Test C ok? |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| J2 (60 mm) | | | | | | | |

Die Lastrechnung braucht für die vorhandenen Motoren 0,21 Nm nutzbares Moment, damit J3 mit 60:1 die Sicherheit 1,5 hält (angenommen sind 0,28 Nm). Liegt der Messwert darunter, wird J3 auf 70:1 erhöht (siehe `docs/lastrechnung.md`).

## Drucken

Druckeinstellungen und Lage auf dem Druckbett: [Bauanleitung, Schritt 1](bauanleitung/motorpruefstand.md#schritt-1-teile-drucken).

Der frühere Messhebel (`Messhebel.stl`, drückte auf die Waage) ist durch den Waagebalken ersetzt. Beim Drücken auf die Waage hebt die Gegenkraft den Halter an.
