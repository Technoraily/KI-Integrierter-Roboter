# Schiene J0: Kabelführung (Schleppkette)

Stand 04.11.2026 (nach Gutachten, Runde 2), **Entwurf für Stufe C** (Schiene wird erst nach dem Prüfstand gebaut). CAD: `cad/skripte/schiene_kette.py`, STL: `cad/export/stl/Schiene_Kette/`, Stückliste: [stuecklisten/schiene-kette.md](stuecklisten/schiene-kette.md). Nichts davon ist gedruckt oder erprobt. Gutachten: [reviews/2026-11-04-schiene-kette.md](reviews/2026-11-04-schiene-kette.md).

## Empfehlung zuerst

**Die Kette nur mit mitgelieferten Anschlussstücken (Endglieder mit Befestigungsflansch) bestellen.** Dann ist die gedruckte Klemme überflüssig; es braucht höchstens einen Adapter auf die Schraubenlöcher des Anschlussstücks. Die Klemme hier ist ein Notbehelf für den Fall, dass die Kette ohne Anschlussstücke kommt. Gebaut wird in Stufe C, nicht vorher.

## Was vorgesehen ist

`docs/konzept.md` 3.7: Der Roboter fährt auf einem Schlitten über rund 1000 mm; die Kabel laufen in einer Schleppkette 10 × 15 mm (Innenmass Höhe × Breite; so bezeichnen es die Händler, nicht einheitlich; in `docs/bom.md`: 1 m, ca. CHF 6). Die Endschalter der Schiene (zwei Öffner in Reihe) nehmen den vorhandenen `Endschalter_Halter` aus `standardteile.py`; für die Kabel am Kettenende gilt der vorhandene `Kabelhalter` (Platte mit Kabelbinder-Schlitzen).

## Kettenlänge (korrigiert)

Länge der Kette ≈ Verfahrweg/2 + π · R + Reserve. Bei 1000 mm Verfahrweg: 500 mm + π · 18 mm (= 57 mm) = **557 mm** bei Biegeradius 18 mm, bei Radius 28 mm 588 mm; mit einem Glied Reserve etwa 0,6 m. Die Kette von 1 m ist also deutlich zu lang und wird gekürzt (Ketten lassen sich an der Gliederung kürzen). Die Bogenhöhe beträgt etwa 2R + Aussenhöhe, also gut 50 bis 70 mm. Die untere Strecke von 500 mm trägt sich nicht selbst; sie braucht eine Gleitfläche oder einen Kanal, und der fehlt noch (Stufe C).

## Platz im Kettenquerschnitt (Schätzung)

Innenquerschnitt 10 × 15 = 150 mm². Zählt man grob die Adern: sechs Motoren mit je 4 Adern (24), sieben Endschalter mit je 2 (14), Greifer-Servo (3) und eine USB-Leitung der Kamera ergibt ungefähr 41 Adern von etwa 1,5 mm Durchmesser (je 2,25 mm² mit Luft) plus ein USB-Kabel (16 mm²), zusammen **etwa 110 mm², also rund 70 % der Fläche**. Das ist zu viel: üblich sind höchstens etwa 60 %, bei Wechselbiegung lieber 50 %. **Entweder eine grössere Kette (15 × 20 mm) einplanen, oder Leitungen bündeln** (gemeinsame Masse der Endschalter, eine Leitung je Motor mit 4 dünnen Adern, Flachbandkabel). Das ist vor der Bestellung der Kette zu klären; Anzahl und Durchmesser der Leitungen sind hier geschätzt.

## Teil: Kettenklemme (Sockel + Deckel, je 2 Stück)

Dasselbe Teil hält die Kette am festen Ende (am Profil) und am beweglichen Ende (am Schlitten). Fuss 76 × 49,4 × 5 mm mit zwei Langlöchern für M4 (Abstand 54 mm, Spiel ±4 mm; Schraubenkopf mit Scheibe Ø 9 liegt auf dem Fuss, keine Senkung), Block mit U-Tasche (Breite Kette + 0,4 mm, Höhe Kette + 0,2 mm), zwei Einschmelzgewinde M3 im Block (Wand 3 mm je Seite). Der Deckel (4 mm, zwei M3 × 8, Kopf 2 mm versenkt) hat **zwei Rippen**, die das Kettenglied um 0,8 mm pressen.

- **Reibklemme, kein Formschluss.** Die Haltekraft ist nicht berechnet, sie hängt vom Material des Glieds und vom Anzug ab. Der Zug der Kette beträgt wenige N. Beim ersten Satz mit einer Federwaage prüfen: Soll mindestens 20 N, sonst ist das Konzept falsch und die Anschlussstücke der Kette entscheiden.
- **Schrauben:** M3 × 8. Deckel 4 mm, Kopf 2 mm versenkt, darunter 2 mm Deckel plus 6 mm im Block; die Bohrung ist 8 mm tief (Spitze 2 mm über dem Grund).
- **Kettenmass ist nicht bekannt.** Händlerlisten nennen für 10 × 15 mm Innenmass Aussenmasse von 13 × 25 und 15 × 23 mm (Suchergebnisse vom 04.11.2026, Quelle nicht gesichert), Biegeradien von 18 bis 28 mm. Der Startwert im Skript (25 × 15 mm) ist ein Grösstwert aus beiden. **Endglied der gelieferten Kette mit der Schieblehre messen** (`KETTE_B`, `KETTE_H`) und STL neu exportieren, dann drucken. Die vorhandenen STL gelten nur für den Startwert und sind nicht zum Drucken gedacht.
- **Montage:** festes Ende auf Profil 2040, **auf der 20-mm-Seite** mit ihrer einen Nut in der Mitte: zwei T-Nutensteine M4 in der Nut, die Schraubenlinie liegt in Nutrichtung. Der Fuss ist 49,4 mm breit und ragt dort 14,7 mm je Seite über das Profil (Platz daneben klären). Auf der 40-mm-Seite liegen die Nuten bei ±10 mm; dort passt die Schraubenlinie in der Mitte nicht. Bewegliches Ende: Schlittenplatte noch nicht konstruiert, Lage und Höhe sind offen, **nur das feste Ende ist heute montierbar**.
- **Schraubenlänge M4:** Kopf mit Scheibe 0,8 mm, Fuss 5 mm, Nutenlippe etwa 2 mm, dazu mindestens 4 mm Eingriff im T-Nutenstein: **M4 × 14**.
- **Formschluss statt Reibung wäre besser:** Quer durch die Bolzenlöcher der Seitenlaschen des Endglieds eine M2 oder M3, oder ein Kabelbinder durch Schlitze. Das hängt vom Endglied der gelieferten Kette ab und ist erst dann sinnvoll zu konstruieren.
- PLA, weil die Klemme nicht warm wird (kein Motor in der Nähe).

Nicht gelöst: Schlittenplatte, Lage der Kette neben den Führungen, Gleitkanal, Kabelquerschnitt (siehe oben).
