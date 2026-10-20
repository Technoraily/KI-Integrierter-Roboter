# Druckeinstellungen Prüfstand J2

Drucker BambuLab A1, Düse 0,4 mm, Bambu Studio. Grundlage ist das Profil **«0.20mm Standard @BBL A1»**; geändert wird nur, was unten steht. Alle Werte sind Startwerte; sie werden nach dem ersten Druck nachgeführt.

## Für alle Teile gleich

| Einstellung | Wert |
|---|---|
| Material | je Teil PLA oder PETG (Tabelle unten), Temperaturen laut Filamentprofil (Bambu PLA Basic / PETG Basic oder Generic) |
| Schichthöhe | 0,20 mm |
| Obere / untere Schichten | 5 / 4 |
| Infill-Muster | Gyroid |
| Stützen | **aus** (alle Teile sind ohne Stützen konstruiert) |
| Brim | aus, ausser in der Tabelle angegeben |
| Druckplatte | Textured PEI; bei Smooth PEI mit Klebestift als Trennschicht (PETG) |
| Elefantenfuss-Kompensation | bei den Scheiben prüfen: Die untersten Zähne dürfen nicht aufquellen, sonst klemmt der Riemen |

## Je Teil

| Pos. | Datei | Material | Lage auf dem Druckbett | Wände | Infill | Brim | Hinweis |
|---|---|---|---|---|---|---|---|
| 1.1 | `Wange_Links_Lager22-20.stl` | PETG | flach, Lagertaschen (Innenseite) **oben** | 4 | 30 % | 5 mm | grösstes Teil, 195 × 196 mm; Motor sitzt aussen, deshalb PETG |
| 1.2 | `Wange_Rechts_Lager22-20.stl` | PLA | flach, Lagertaschen (Innenseite) **oben** | 4 | 30 % | aus | wie links |
| 1.3–1.6 | `Quertraeger_unten_links / _unten_rechts / _oben_links / _oben_rechts.stl` | PLA | liegend (wie exportiert) | 4 | 40 % | aus | Einschmelzbohrungen Ø 4,0 liegen waagrecht, nach dem Druck mit 4-mm-Bohrer von Hand säubern |
| 1.7 | `Scheibe_GT2_Z72.stl` | PETG | Zahnkranz unten, Nabe oben | 4 | 40 % | aus | Zähne unten nicht zerdrücken lassen; Blockierbohrungen mit 3-mm-Bohrer aufreiben |
| 1.8 | `Scheibe_3M_Z64.stl` | PETG | Zahnkranz unten, Hülse oben | 5 | 40 % | aus | Hülse nimmt die M4-Mitnahme auf, daher 5 Wände |
| 1.9 | `Scheibe_5M_Z90.stl` | PETG | Hebelseite unten | 4 | 30 % | aus | Zahnflanken wirken direkt auf das Spiel: erst ein Zahnsegment als Test drucken |
| 1.10 | `Lasthebel.stl` | PLA | flach, Nabenbund oben | 5 | 40 % | aus | 240 mm lang, passt diagonal oder gerade aufs Bett (256 mm) |
| 1.11 | `Messzeiger.stl` | PLA | flach, Tastklotz oben | 4 | 40 % | aus | Tastflächen nach dem Druck mit Schleifpapier K400 plan abziehen |
| 1.12 | `Messuhrhalter.stl` | PLA | auf dem Rücken | 4 | 40 % | aus | Schaftbohrung Ø 8 mm stramm gedruckt, mit 8-mm-Bohrer aufreiben |
| 1.13 | `Spannrolle_5M_Lager22-20.stl` | PETG | stehend | 4 | 100 % | aus | Lagersitze mit der Achse senkrecht gedruckt: Ø 22,20 gilt |
| 1.14–1.17 | `Distanzring_A_links / _A_rechts / _B_links / _B_rechts.stl` | PETG | stehend | 3 | 100 % | aus | stehen unter Klemmkraft, deshalb voll |
| 1.18–1.22 | `Huelse_5M_links / _mitte / _rechts`, `Huelse_3M_links / _rechts.stl` | PETG | stehend | 3 | 100 % | aus | Bohrung Ø 8,3 für die M8-Schraube, nicht aufbohren |

Nachbearbeitung: Fäden und Reste aus Bohrungen, Langlöchern und Zahnlücken entfernen; Einschmelzgewinde erst setzen, wenn die Teile kalt sind. Aufreibmasse und Orte der 41 Einschmelzgewinde stehen in `docs/bauanleitung/Bauanleitung_J2_Pruefstand.pdf` und in der Stückliste.

Filament gesamt (Schätzung mit üblicher Füllung): PETG 0,35–0,45 kg, PLA 0,35–0,45 kg, dazu 0,2 kg Reserve (siehe `docs/stuecklisten/pruefstand-j2.md`, Gruppe 8).

Druckreihenfolge: zuerst die kleinen Teile (Spannrolle, Hülsen, Distanzringe) und das Zahnsegment der 90er-Scheibe zur Passprobe; die Scheiben 1.7 bis 1.9 erst drucken, wenn die gekauften Ritzel nachgemessen sind.
