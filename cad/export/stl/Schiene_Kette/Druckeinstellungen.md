# Druckeinstellungen Schiene: Kettenklemme

Drucker BambuLab A1, Düse 0,4 mm, Bambu Studio. Grundlage ist das Profil **«0.20mm Standard @BBL A1»**; geändert wird nur, was unten steht. Beschreibung: `docs/schiene-kabelfuehrung.md`, Stückliste: `docs/stuecklisten/schiene-kette.md`. **Nicht drucken, bevor `KETTE_B`, `KETTE_H` und `PRESS` (Pressung der Rippen, sonst bei dünnerem Glied null) im Skript `cad/skripte/schiene_kette.py` an der gelieferten Kette nachgemessen und die STL neu exportiert sind;** die vorliegenden Dateien rechnen mit 25 × 15 mm (Startwert, ungeprüft). Noch nichts gedruckt.

## Für alle Teile gleich

| Einstellung | Wert |
|---|---|
| Material | PLA (die Klemme wird nicht warm) |
| Schichthöhe | 0,20 mm |
| Obere / untere Schichten | 5 / 4 |
| Infill-Muster | Gyroid |
| Stützen | **aus** |
| Brim | aus |
| Druckplatte | Textured PEI oder Smooth PEI, vorher fettfrei |

## Je Teil

| Datei | Lage auf dem Bett | Wände | Infill | Nachbearbeitung |
|---|---|---|---|---|
| `Kettenklemme_Sockel.stl` (76 × 49,4 × 20,2 mm) | Fuss unten, Tasche oben offen (wie exportiert) | 4 | 40 % | zwei Einschmelzgewinde M3 (Bohrung Ø 4,0 mm, 8 mm tief) von oben in den Block; Langlöcher Ø 4,5 mm nicht aufbohren; Schraubenköpfe M4 liegen mit Scheibe auf dem Fuss |
| `Kettenklemme_Deckel.stl` (20 × 45,4 × 5 mm) | flach, Kopfseite (Senkung für M3-Kopf) unten, die zwei Rippen zeigen nach oben (wie exportiert) | 4 | 100 % | keine |

Je Ende ein Sockel und ein Deckel, zusammen also 2 + 2. Filament für beide Sätze etwa 55 g, Druckzeit etwa 2 Stunden (geschätzt, nicht gemessen). Den ersten Satz allein drucken und die Haltekraft mit der Federwaage prüfen (Soll ≥ 20 N).
