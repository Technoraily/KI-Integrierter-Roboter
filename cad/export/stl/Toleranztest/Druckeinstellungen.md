# Druckeinstellungen Toleranztest

Drucker BambuLab A1, Düse 0,4 mm, Bambu Studio. Grundlage ist das Profil **«0.20mm Standard @BBL A1»**; geändert wird nur, was unten steht. Alle drei Teile passen zusammen auf **ein** Druckbett (Platte 186 × 90 mm).

**Wichtig:** gleiches Filament, gleiche Temperatur und gleiche Druckplatte wie später für die Arm-Teile. Sonst gelten die Toleranzen nicht.

## Für alle Teile gleich

| Einstellung | Wert |
|---|---|
| Material | PLA (Bambu PLA Basic oder Generic PLA), Temperaturen laut Filamentprofil |
| Schichthöhe | 0,20 mm |
| Wände | 3 |
| Obere / untere Schichten | 5 / 4 |
| Infill-Muster / Dichte | Gyroid, 15 % |
| Stützen | **aus** (auch bei Toleranz_Stehend: die Löcher sind Teil der Messung) |
| Brim | aus; bei Toleranz_Stehend **ein** (Brim 5 mm), sonst kippt das Teil |
| Druckplatte | Textured PEI oder Smooth PEI, vorher fettfrei |
| Nachbearbeitung | keine: Löcher nicht aufbohren, Fäden nur mit dem Fingernagel entfernen |

## Je Teil

| Datei | Lage auf dem Druckbett | Hinweis |
|---|---|---|
| `Toleranz_Platte.stl` | flach (wie exportiert), Kerben oben links | Reihe A bis D von vorn nach hinten, kleinstes Mass links |
| `Toleranz_Stehend.stl` | **stehend**: 100 × 8 mm unten, 42 mm hoch (wie exportiert) | Löcher waagrecht, Brim ein |
| `Passzapfen.stl` | Bund unten (wie exportiert) | Messstift für Reihe D |

Filament gesamt: ca. 45–60 g PLA, Druckzeit ca. 3–4 h.

## Auswerten

Pro Reihe das Mass notieren, bei dem das Gegenstück **von Hand ohne Hammer saugend** sitzt, und in `docs/parameter.md` eintragen:

| Reihe | Gegenstück | Ergebnis |
|---|---|---|
| A, Stehend | Kugellager 608 (Aussen 22 mm) | `tol_lagersitz` = Lochmass − 22,00 |
| B | Motorwelle 5 mm, Stahlachse 8 mm | Bohrung für Wellen mit Spiel |
| C | Einschmelzgewinde M3 / M4 | `d_einschmelz_M3`, `d_einschmelz_M4` |
| D | Passzapfen Ø 10 mm; M3-Schraube | `tol_passung` = Lochmass − 10,00 |

Liegend und stehend vergleichen: Ist das Stehend-Loch merklich kleiner oder oval, gilt für waagrechte Lagersitze im Arm ein Zuschlag.
