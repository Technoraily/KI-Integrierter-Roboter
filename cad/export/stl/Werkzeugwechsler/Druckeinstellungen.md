# Druckeinstellungen Werkzeugwechsler und Kamerahalter

Drucker BambuLab A1, Düse 0,4 mm, Bambu Studio. Grundlage ist das Profil **«0.20mm Standard @BBL A1»**; geändert wird nur, was unten steht. Beschreibung: `docs/werkzeugwechsler.md`, Stückliste: `docs/stuecklisten/werkzeugwechsler.md`. **Noch nichts gedruckt. Zuerst die Magnetprobe drucken und die Haltekraft messen, dann den Master allein für die Kugeltasche (Ø 6,15 mm) prüfen.**

## Für alle Teile gleich

| Einstellung | Wert |
|---|---|
| Material | PLA |
| Schichthöhe | 0,20 mm (bei den Platten 0,12 mm nur, wenn die Kugeln im Probedruck nicht gleichmässig aufliegen) |
| Obere / untere Schichten | 5 / 4 |
| Infill-Muster | Gyroid |
| Stützen | **aus** |
| Brim | aus |
| Druckplatte | Smooth PEI (glatte Rückseite der Platten) |

## Je Teil

| Datei | Lage auf dem Bett | Wände | Infill | Nachbearbeitung |
|---|---|---|---|---|
| `WF_Magnetprobe_A.stl`, `_B.stl` (je 34 × 30 × 12 mm) | flach, Magnettasche oben | 3 | 40 % | Magnet Ø 10 × 3 mm einkleben (bündig), Ringschraube M4 selbstschneidend in das Kernloch Ø 3,3 mm von hinten, Karton 0,4 mm dazwischen, Haltekraft mit Federwaage in der Magnetachse messen |
| `WF_Master.stl` (Ø 70 × 8 mm) | flach, Kupplungsseite oben (Taschen offen nach oben) | 4 | 50 % | Kugeln Ø 6 mm mit Sekundenkleber in die Taschen (halb eingesenkt), Magnete einkleben (bündig, alle drei mit dem Nordpol nach aussen), Stahlstift Ø 3 × 6 mm in die Aufnahme (Haltesitz), zwei Einschmelzgewinde M3 von der Rückseite, Pogo-Löcher nicht aufbohren (erst Pin probieren) |
| `WF_Werkzeug.stl` (Ø 70 × 8 mm) | flach, Kupplungsseite oben (Nuten offen nach oben) | 4 | 50 % | Magnete einkleben (alle drei mit dem Südpol nach aussen), sechs Schlitz-Zylinderschrauben M2 × 6 (DIN 84) von vorn mit Mutter in der Sechskanttasche hinten (mit einem Tropfen Kleber sichern), vier Einschmelzgewinde M3 auf der Rückseite (Ø 32 mm, Startwert); die V-Nuten mit einer Kugel prüfen |
| `WF_Kamerahalter.stl` (46 × 56 × 28 mm) | auf der Seite liegend (wie exportiert, der Z-Querschnitt liegt auf dem Bett) | 4 | 100 % | Löcher für M2 nicht aufbohren (die Löcher liegen im Druck waagrecht und werden leicht oval); Platine zuerst anlegen |

Filament gesamt etwa 75 bis 85 g PLA, Druckzeit etwa 5 Stunden (geschätzt, nicht gemessen).
