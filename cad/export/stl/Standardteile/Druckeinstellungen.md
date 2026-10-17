# Druckeinstellungen Standardteile

Drucker BambuLab A1, Düse 0,4 mm, Bambu Studio. Grundlage ist das Profil **«0.20mm Standard @BBL A1»**; geändert wird nur, was unten steht. Beide Teile passen zusammen auf ein Druckbett.

## Für alle Teile gleich

| Einstellung | Wert |
|---|---|
| Material | PLA (Bambu PLA Basic oder Generic PLA); später für Teile nahe am Motor PETG |
| Schichthöhe | 0,20 mm |
| Obere / untere Schichten | 5 / 4 |
| Infill-Muster | Gyroid |
| Stützen | **aus** |
| Brim | aus |
| Druckplatte | Textured PEI oder Smooth PEI, vorher fettfrei |

## Je Teil

| Datei | Lage auf dem Druckbett | Wände | Infill | Hinweis |
|---|---|---|---|---|
| `Endschalter_Halter.stl` | Fuss unten (wie exportiert) | 4 | 40 % | die Wand wird durch Rippen gestützt; Langlöcher nicht aufbohren |
| `Kabelhalter.stl` | flach (wie exportiert) | 3 | 100 % | klein, 100 % ist schneller als Wände zählen |

Filament gesamt: ca. 20–25 g PLA. Die Teile werden bei Bedarf mehrfach gedruckt, Menge siehe `docs/stuecklisten/werkstattteile.md`.
