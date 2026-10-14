# Vollständige Stückliste: Motorprüfstand NEMA 17

Stand 14.10.2026, passend zum CAD `cad/skripte/motorpruefstand.py`. Ziel: **keine Kaufteile**. Ablauf der Messungen: [motorvermessung.md](../motorvermessung.md).

**Status:** *da* = vorhanden · *klären* = unklar, ob vorhanden (bitte nachsehen) · *Haushalt* = findet sich üblicherweise zu Hause.

## 1 Druckteile

Dateien in `cad/export/stl/Motorpruefstand/`. Zusammen rund 190 cm³ als Vollkörper, das sind ca. 90–110 g PLA bei den angegebenen Einstellungen.

| Pos. | Teil (Datei `.stl`) | Menge | Material | cm³ | Drucklage |
|---|---|---|---|---|---|
| 1.1 | `Motorhalter` (Grundplatte 200 × 110 mm mit Wiege) | 1 | PLA | 146 | Grundplatte unten |
| 1.2 | `Niederhalter` | 1 | PLA, 100 % Infill | 6 | umdrehen: Platte unten |
| 1.3 | `Waagebalken` (Löcher bei ±100 mm) | 1 | PLA | 18 | flach, Nabe oben |
| 1.4 | `Seiltrommel` (gestuft, Wickelradius 20 und 10 mm) | 1 | PLA | 22 | Aussenflansch unten |

## 2 Schrauben

| Pos. | Teil | Menge | Wofür | Status |
|---|---|---|---|---|
| 2.1 | Zylinderschraube M3 × 16 (× 14 bis × 20 geht) | 1, besser 2 | Klemmung Waagebalken bzw. Seiltrommel | da |
| 2.2 | Mutter M3 | 1, besser 2 | dazu | da |
| 2.3 | M3 × 8–10 | 0–4 | optional: Motor durch die Stirnwand schrauben | da (M3-Sortiment) |


## 3 Antrieb und Elektrik

| Pos. | Teil | Menge | Status |
|---|---|---|---|
| 3.1 | NEMA 17, 17CS04A-170E (Prüfling) | 3 | da |
| 3.2 | Arduino Uno mit GRBL | 1 | da |
| 3.3 | CNC-Shield mit A4988, Mikroschritt-Jumper | 1 | da |
| 3.4 | Netzteil 12 V / 4 A | 1 | da |
| 3.5 | Motorkabel, passend zum Stecker am Motor | 1 | klären |
| 3.6 | USB-Kabel zum Uno | 1 | klären |
| 3.7 | G-Code-Sender auf dem PC (z. B. Universal Gcode Sender oder Candle, kostenlos) | 1 | klären |

## 4 Messmittel und Lasten

| Pos. | Teil | Menge | Status |
|---|---|---|---|
| 4.1 | Küchenwaage | 1 | da |
| 4.2 | PET-Flaschen 1,5 l mit Wasser, dazu eine Tasche (Last bis ca. 3 kg) | 2 | Haushalt |
| 4.3 | Schnur ca. 1 mm, reissfest, ca. 2 m | 1 | Haushalt |
| 4.4 | Handy mit Wasserwaage-App | 1 | Haushalt |
| 4.5 | Klebeband als Marke (Test C) | 1 | Haushalt |
| 4.6 | Multimeter (Wicklungswiderstand, Vref) | 1 | klären |
| 4.7 | Schieblehre oder Lineal | 1 | klären |

## 5 Aufstellung und Werkzeug

| Pos. | Teil | Status |
|---|---|---|
| 5.1 | Tisch mit freier Kante, darunter Platz bis zum Boden | Haushalt |
| 5.2 | Schraubzwinge (besser) oder mind. 4 kg Bücher zum Beschweren | klären / Haushalt |
| 5.3 | Tuch oder Karton unter der Flasche | Haushalt |
| 5.4 | Innensechskant- bzw. Schraubendreher für M3, kleiner Schraubendreher für Vref | klären |
| 5.5 | PLA-Filament ca. 110 g | da |
| 5.6 | Kühlkörper oder Lüfter für den A4988, nur falls der Wärmetest es verlangt | klären |
