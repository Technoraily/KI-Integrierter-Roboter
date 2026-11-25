# Designvorgabe Roboterarm (Stand 25.11.2026)

Vorgabe des Nutzers: Der Arm wird **von unten nach oben** nach einer Bildvorlage gestaltet (6-Achs-Industrieroboter, weisse Schalen, dunkler Sockel). Das Bild liegt nur lokal beim Nutzer und ist **nicht im Repo** (fremde Produktabbildung, Repo ist öffentlich). Diese Datei hält fest, was aus dem Bild übernommen wird. Masse kommen nur aus `docs/parameter.md` und den CAD-Skripten, nicht aus dem Bild.

## Was auf dem Bild zu sehen ist

- **Sockel:** dunkelgrauer, kantiger Block, breiter als die Säule. Hier: Basis auf dem Schienenschlitten (Lochbild 120 mm, 4× M5).
- **Säule (J1):** weisse, facettierte Schale, drehbar auf dem Sockel, oben der runde Schulterkopf mit der waagrechten Achse J2.
- **Oberarm:** nach vorn und oben geneigt, weisse Schale mit kantigen Flächen. J2 (±90°) erlaubt das.
- **Ellbogen (J3):** runde Nabe an beiden Seiten, Unterarm waagrecht.
- **Unterarm und Hand:** Unterarm schlank, am Ende ein kantiger Handgelenkblock (J4 bis J6) mit Werkzeugflansch.
- **Gesamteindruck:** glatte weisse Flächen, wenige sichtbare Schrauben, keine Kabel aussen, dunkelgraue Teile an Sockel und Gelenknaben.

## Übersetzung in unser Konzept

| Bildteil | Unser Bauteil | Masse aus | Druck |
|---|---|---|---|
| Sockel | Basis auf Schlitten | `a_lochbild_basis` 120 mm, Bauraum 240 mm | dunkelgrau (PETG), Antrieb J1 darin |
| Säule | J1-Drehteil mit Schulterbock | `H_schulter` 200 mm (Entscheid 26.11.2026) | tragende Teile PETG, Schale PLA weiss |
| Oberarm | J2 → J3 | `L_oberarm` 200 mm | Schale PLA weiss |
| Unterarm | J3 → J5 | `L_unterarm` 190 mm | Schale PLA weiss |
| Hand | J4 bis J6, Flansch | `L_hand` 60 mm, `D_flansch_lochkreis` 31,5 mm | Schale PLA weiss |

## Regeln für die Gestaltung

- Tragende Teile (Lager, Riemen, Motoren) und Schalen werden getrennt konstruiert: Die Schale ist Verkleidung (laut Lastrechnung 0,4 kg für Verkleidung und Kabel eingerechnet) und darf nichts tragen.
- Jedes Teil muss auf den A1 (240 mm Kantenlänge) passen und ohne Stützen oder mit einfachen Stützen druckbar sein. Facettierte Flächen (wie im Bild) sind ideal für den Druck.
- Bauraum freihalten: **Bremse an J2** (hinter dem Motor ca. 30 mm, `konzept.md` 3.9), **Teilausgleichsfeder J2** (Anlenkpunkte 50 bis 80 mm von der Achse, 3.8), Parkposition mit Anschlag und weicher Dämpfung (3.9).
- Kabel innen führen (Hohlräume in Säule und Oberarm), Zugentlastung an jedem Gelenk.
- Reihenfolge: Basis, Säule J1, Schulter J2, Oberarm, Ellbogen J3, Unterarm, Hand J4 bis J6, Greifer. Jedes Teil: Kollision, Bauraum A1, Montierbarkeit, Lastrechnung, Gutachten (max. 3 Runden); Kritisches zuerst als Testteil, ausser J2-Prüfstand (neu drucken nur nach Rücksprache).

## Basis austauschbar (Anforderung des Nutzers, 26.11.2026)

Die 7. Achse (Schiene J0) kommt erst später. Die Basis muss darum **gegen eine andere getauscht** werden können, ohne den Arm umzubauen: gleiches Lochbild (120 mm, 4× M5, Zentrierring) und ein Steckerfeld an fester Stelle für alle Leitungen (Einzelheiten in `docs/kabelkonzept.md`). Die Basis ist die untere Teilbaugruppe: Dunkler Sockel mit Antrieb J1, darüber die Säule als eigene Baugruppe.

## Steuerung (Entscheid 26.11.2026)

Geplant wird mit dem **BTT Octopus** (STM32F446) und grblHAL, wie in `docs/verdrahtung.md`. FluidNC auf dem ESP32 war nur für die Tests am Prüfstand. FluidNC läuft nicht auf dem Octopus (anderer Prozessor).

## Proportionen: Bildvorlage gegen unsere Masse (grobe Schätzung am Bild, ±20 %)

Am Bild geschätzt (Pixelabstände, nicht gemessen am Original): Unterarm einschliesslich Hand ist etwa 1,2-mal so lang wie der Oberarm; unsere Masse (190 + 60 mm gegen 200 mm) ergeben 1,25. Das passt. Anders ist die **Höhe der Schulterachse über dem Tisch**: Auf dem Bild liegt sie etwa 1,0 bis 1,1 Oberarmlängen über dem Tisch (ca. 200 bis 220 mm bei 200 mm Oberarm); unser `H_schulter` ist 170 mm (0,85). Die Vorlage hat also einen höheren Sockel und eine höhere Säule als unser Startwert.

Folgen einer höheren Schulter: mehr Platz für die Basis, das Steckerfeld und die Bremse hinter dem Motor; der Arm kommt weiter nach unten; die Säule wird länger (mehr Hebel auf J1-Lager, mehr Biegung der Säule). `H_schulter` ist als **Startwert** geführt, also änderbar. **Entschieden am 26.11.2026: 200 mm.** Die Säule wird steif ausgelegt; bei Bauraumproblemen ist 170 mm der Rückfall. Ob die Optik damit der Vorlage entspricht, zeigt ein Render des Layouts, sobald Fusion läuft.

## Werkzeugwechsler (Entscheid 26.11.2026)

Der Greifer wird automatisch gewechselt, ohne dass ein Kabel mitgerissen werden kann. Grundlage ist der Entwurf in `docs/werkzeugwechsler.md` (kinematische Kupplung mit drei Kugeln und V-Nuten, Kontakte in der Kupplungsfläche). Festgelegt:
- **Kein Kabel über die Trennstelle.** Alle Leitungen enden fest auf der Roboterseite (Master) mit Zugentlastung und Stecker; die Werkzeugseite hat nur flache Gegenkontakte und kein eigenes Kabel. Bei einer Kollision löst sich das Werkzeug, statt Kabel oder Getriebe zu beschädigen.
- **Mechanische Verriegelung:** Ein Riegel, von einem kleinen Servo auf der Roboterseite bewegt, hält das Werkzeug. Die Magnete zentrieren und spannen nur vor (die vorhandenen Magnete Ø 6 × 3 mm reichen als Halt nicht, siehe Haltekraft-Rechnung dort). Riegelstellung wird zurückgemeldet (Endlage).
- **Werkzeugerkennung:** Jedes Werkzeug trägt einen Codierwiderstand über zwei Kontakte; die Steuerung (Pico) misst ihn und weiss, welches Werkzeug dransteckt.
- **Strom erst nach Erkennung und Verriegelung:** Die Versorgung des Greifer-Servos wird erst eingeschaltet, wenn ein gültiges Werkzeug erkannt und der Riegel zu ist (MOSFET), damit ein falsch sitzendes Werkzeug keinen Kurzschluss auf den Kontakten macht.
- Kamera hat ein eigenes Kabel am Handgelenk und läuft nicht über den Wechsler. Werkzeugablage am Schienenende (im Rohbau gezeichnet).
- Konstruktion: wird mit dem Handgelenk konstruiert (oberstes Teil der Reihenfolge). Claude konstruiert, der Nutzer druckt und baut.

## Offene Punkte

- Steifigkeit J2 gemessen ca. 17 Nm/° statt Ziel 30: Durchhang wird per Software ausgeglichen, Wert für die Auslegung: 17 Nm/° (`konzept.md` 3.8).
- Grösse und Lage des Handgelenkblocks (die Vorlage zeigt einen kantigen Block): erst nach Auslegung J4 bis J6.
- Fusion 360 war beim Start dieser Datei nicht verbunden (Add-in starten).
