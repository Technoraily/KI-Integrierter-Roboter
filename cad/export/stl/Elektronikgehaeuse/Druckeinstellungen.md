# Druckeinstellungen Elektronikgehäuse J2-Prüfstand

Drucker BambuLab A1, Düse 0,4 mm, Bambu Studio. Grundlage ist das Profil **«0.20mm Standard @BBL A1»**; geändert wird nur, was unten steht. Material **PETG** (Filamentprofil Bambu PETG Basic oder Generic PETG): Das Netzteil erwärmt das Gehäuse, PLA würde dort kriechen.

**Reihenfolge:** zuerst die beiden Testplatten `EG_Passprobe_C14` und `EG_Passprobe_F1` (je unter einer Stunde, passen zusammen auf eine Platte), dann `EG_Netzblende` und `EG_Klemmenabdeckung` (zusammen etwa 3 h), an den gekauften Teilen probieren, erst dann `EG_Wanne` und `EG_Deckel` (zusammen etwa ein bis zwei Tage Druckzeit, Schätzung, Anzeige im Slicer).

## Für alle Teile gleich

| Einstellung | Wert |
|---|---|
| Material | PETG |
| Schichthöhe | 0,20 mm |
| Obere / untere Schichten | 5 / 5 |
| Infill-Muster | Gyroid |
| Stützen | **aus**, ausser bei der Klemmenabdeckung (nur unter den zwei Laschen, siehe unten) |
| Druckplatte | Textured PEI, fettfrei; auf glatter PEI dünn Klebestift als Trennschicht (PETG haftet sonst zu stark) |
| Temperaturen, Geschwindigkeit, Lüfter | aus dem Filamentprofil (Bambu PETG Basic) übernehmen, nicht ändern |

## Je Teil

| Datei | Lage | Wände | Infill | Brim | Hinweis |
|---|---|---|---|---|---|
| `EG_Wanne.stl` | wie exportiert, Boden unten | 7 (Wand 3 mm voll) | 15 % | aussen 5 mm | 240 × 238 mm: mit Brim 250 × 248 mm, passt auf das 256-mm-Bett. Gegen Eckenablösung: Heizbett 70 °C, Lüfter in den ersten Schichten gering, Raum zugfrei |
| `EG_Deckel.stl` | wie exportiert: Oberseite unten auf dem Bett, Lippe nach oben | 5 | 20 % | aussen 5 mm | gleiche Hinweise wie die Wanne; Lippe 2 mm = 5 Linien; Lüftungsschlitze 3 mm und Zugangsschlitz brücken nicht |
| `EG_Passprobe_C14.stl` | wie exportiert, Aussenseite unten, Mutterntaschen oben | 5 | 50 % | aus | Testteil; gleiches Material wie die endgültigen Teile (PETG), damit das Spiel stimmt; Stufe = Anzahl Grübchen |
| `EG_Passprobe_F1.stl` | flach, wie exportiert | 5 | 50 % | aus | Testteil; Bohrungen 12,4 bis 13,2 mm aufsteigend, Grübchen = Nummer |
| `EG_Netzblende.stl` | Aussenseite unten, Mutterntaschen nach oben | 5 | 50 % | aus | Passprobe: Ausschnitt C14 und Bohrung F1 mit den Teilen probieren |
| `EG_Klemmenabdeckung.stl` | wie exportiert: Dach unten, Haube nach oben offen | 6 | 30 % | aus | **Stützen nur unter den zwei Laschen** (Baumstützen, sonst keine); Gang und Kabelschlitze sind nach oben offen. Seiten- und Rückwand enden frei in der Luft, das ist gewollt (Kante, kein Überhang) |

## Nachbearbeitung

- **Einschmelzgewinde M3** (18 Stück, Lötkolben, Bohrung 4,0 mm): 4 Arduino-Dome, 10 Deckeldome, 4 Netzblendendome. Die waagrechten Bohrungen der Netzblendendome sind tropfenförmig; Einsatz senkrecht zur Domenfläche eindrücken, bis er bündig ist. Die oberen Netzblendendome stehen 7 mm frei aus der Wand: Hängen sie durch, Baumstützen nur dort zulassen.
- Schlitze (Lüftung, Kabelaustritte, Kabelbinder) und Mutterntaschen entgraten. Bohrung F1 und Ausschnitt C14 nur mit Feile nacharbeiten, nie vergrössern, bevor die Passprobe gemessen ist.
- Sechskanttaschen für zwei Muttern M3 im Boden vor dem Netzteil: Muttern von oben einlegen; sitzen sie zu streng, mit dem Schraubendreher nachdrücken, nie die Tasche ausfeilen.
- Senkungen der Netzteilschrauben (Ø 8,2 × 4 mm) auf der Unterseite der Wanne: Kopf der Schraube M4 × 6 muss bündig oder tiefer liegen.

Filament gesamt: rund 0,6 kg PETG (Schätzung; die genaue Menge zeigt der Slicer).
