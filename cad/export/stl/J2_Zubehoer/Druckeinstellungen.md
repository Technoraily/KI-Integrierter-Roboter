# Druckeinstellungen J2-Zubehör

Drucker BambuLab A1, Düse 0,4 mm, Bambu Studio. Grundlage ist das Profil **«0.20mm Standard @BBL A1»**; geändert wird nur, was unten steht. Alle Dateien liegen schon in Druckorientierung. Beschreibung: `docs/zubehoer-j2.md`, Stückliste: `docs/stuecklisten/j2-zubehoer.md`. **Noch nichts gedruckt.**

## Für alle Teile gleich

| Einstellung | Wert |
|---|---|
| Schichthöhe | 0,20 mm |
| Obere / untere Schichten | 5 / 4 |
| Infill-Muster | Gyroid |
| Stützen | **aus** |
| Brim | aus |
| Druckplatte | Textured PEI oder Smooth PEI, vorher fettfrei |

## Je Teil

| Datei | Material | Lage auf dem Bett | Wände | Infill | Nachbearbeitung |
|---|---|---|---|---|---|
| `J2_Schalterprobe.stl` (14 × 46 × 16 mm) | PLA (Bambu PLA Basic) | wie exportiert, Tasche oben | 3 | 15 % | Mikroschalter einlegen, Masse messen (Tabelle in `docs/zubehoer-j2.md`); Löcher Ø 2,4 mm nicht aufbohren; Sechskanttasche der Mutter M2 an der Seite prüfen |
| `J2_Quertraeger_oben_Schalter.stl` (14 × 56 × 24 mm) | PLA (wie die übrigen Querträger) | liegend auf der 14 × 56-Fläche, Tasche oben, wie exportiert | 4 | 40 % | **erst nach der Schalterprobe drucken.** Vier Einschmelzgewinde M3 (Bohrung Ø 4,0 mm, 9 mm tief, mit Lötkolben) in die Enden; die waagrechten Bohrungen sind wie im bestehenden J2-Druck nicht als Tropfen ausgeführt (nur Ø 4 mm und Ø 2,4 mm, nicht getestet); M2-Löcher nicht aufbohren; Mutter M2 in die Sechskanttasche der Gegenwand legen |
| `J2_Motorkabelklemme.stl` (54 × 20 × 7 mm) | PETG (Bambu PETG Basic mit dem Standard-PETG-Profil von Bambu Studio für Düse 0,4 mm; Temperaturen vom Profil übernehmen) | flach, Unterseite (zum Motor) unten, Rille oben | 3 | 100 % | Grate in den Schlitzen entfernen, damit der Kabelbinder (3,6 × 1,4 mm) durchgeht |

Filament gesamt etwa 38 g (PLA 30 g, PETG 8 g), Druckzeit zusammen etwa 2 Stunden. Beides geschätzt, nicht gemessen.
