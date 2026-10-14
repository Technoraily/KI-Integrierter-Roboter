# Druckeinstellungen Motorprüfstand

Drucker BambuLab A1, Düse 0,4 mm, Bambu Studio. Grundlage ist das Profil **«0.20mm Standard @BBL A1»**; geändert wird nur, was unten steht.

## Für alle Teile gleich

| Einstellung | Wert |
|---|---|
| Material | PLA (Bambu PLA Basic oder Generic PLA), Temperaturen laut Filamentprofil |
| Schichthöhe | 0,20 mm |
| Wände | siehe Tabelle unten |
| Obere / untere Schichten | 5 / 4 |
| Infill-Muster | Gyroid |
| Stützen | **aus** |
| Brim | aus (beim Motorhalter einschalten, falls die Ecken sich lösen) |
| Druckplatte | Textured PEI oder Smooth PEI, vorher fettfrei |

## Je Teil

| Datei | Lage auf dem Druckbett | Wände | Infill | Hinweis |
|---|---|---|---|---|
| `Motorhalter.stl` | Grundplatte unten (wie exportiert) | 3 | 30 % | grösstes Teil, 200 × 110 mm |
| `Niederhalter.stl` | **umdrehen**: Platte unten, Zapfen oben | 3 | **100 %** | die Zapfen müssen fest sein |
| `Waagebalken.stl` | flach, Nabe oben (wie exportiert) | 4 | 40 % | |
| `Seiltrommel.stl` | Aussenflansch unten (wie exportiert) | 4 | 40 % | die Kegel sind 45°, keine Stützen nötig |

Danach Fäden aus Schlitzen, Mutterfallen und Bohrungen entfernen. Die 5,1-mm-Bohrungen müssen sich leicht auf die Motorwelle schieben lassen, sonst mit einem 5-mm-Bohrer von Hand nachdrehen.

Filament gesamt: ca. 110 g PLA.
