# Stückliste: Toleranztest, Standardteile und Not-Aus-Gehäuse

Stand 17.10.2026, passend zu `cad/skripte/toleranztest.py` und `cad/skripte/standardteile.py` und `cad/skripte/notaus.py`. Ziel: Passungen messen, bevor Lager- und Gewindesitze im Arm gezeichnet werden; Endschalter und Kabel an allen Achsen einheitlich lösen.

**Status:** *da* = vorhanden · *klären* = bitte nachsehen · *offen* = noch zu kaufen.

## 1 Druckteile

| Pos. | Teil (Datei `.stl`) | Ordner | Menge | cm³ | Drucklage |
|---|---|---|---|---|---|
| 1.1 | `Toleranz_Platte` (186 × 90 × 8 mm) | `Toleranztest/` | 1 | 110 | flach |
| 1.2 | `Toleranz_Stehend` (100 × 8 × 42 mm) | `Toleranztest/` | 1 | 24 | stehend, Brim |
| 1.3 | `Passzapfen` (Ø 10 mm) | `Toleranztest/` | 1 | 2 | Bund unten |
| 1.4 | `Endschalter_Halter` | `Standardteile/` | 1 zum Testen, später 1 je Achse (8: J1–J6, Schiene 2) | 17 | Fuss unten |
| 1.6 | `NotAus_Gehaeuse` (66 × 66 × 61 mm plus Ohren) | `NotAus/` | 1 | 69 | Boden unten, offen |
| 1.7 | `NotAus_Deckel` (66 × 66 × 4 mm) | `NotAus/` | 1 | 16 | flach |
| 1.5 | `Kabelhalter` | `Standardteile/` | 4 zum Testen, später ca. 1 je Gelenk | 2 | flach |

Druckeinstellungen vollständig in `cad/export/stl/Toleranztest/`, `Standardteile/` und `NotAus/` je als `Druckeinstellungen.md` (BambuLab A1, 0,4-mm-Düse, «0.20mm Standard @BBL A1», PLA, 0,20 mm, Gyroid, Stützen aus).

| Teil | Wände | Infill | Obere / untere | Stützen | Brim |
|---|---|---|---|---|---|
| Toleranz_Platte | 3 | 15 % | 5 / 4 | aus | aus |
| Toleranz_Stehend | 3 | 15 % | 5 / 4 | aus | 5 mm |
| Passzapfen | 3 | 15 % | 5 / 4 | aus | aus |
| Endschalter_Halter | 4 | 40 % | 5 / 4 | aus | aus |
| Kabelhalter | 3 | 100 % | 5 / 4 | aus | aus |
| NotAus_Gehaeuse | 4 | 30 % | 5 / 4 | aus | aus |
| NotAus_Deckel | 4 | 50 % | 5 / 4 | aus | aus |

## 2 Schrauben und Kleinteile

| Pos. | Teil | Menge | Wofür | Status |
|---|---|---|---|---|
| 2.1 | Schraube M3 × 12 | 2 | Endschalter_Halter an den Prüfstand/Profil | da (M3-Sortiment) |
| 2.2 | Schraube M3 × 10 mit Senkkopf-Tasche (Zylinderkopf) | 1 je Kabelhalter | Kabelhalter | da |
| 2.3 | Schraube M2 × 10 (oder selbstschneidend 2,2 × 10) | 2 je Schalter | Mikroschalter am Halter | klären |
| 2.4 | Kabelbinder 2,5–3,6 mm breit | 1 je Kabelhalter | Zugentlastung | klären |
| 2.5 | Mutter M3 oder Einschmelzgewinde M3 | je nach Untergrund | Gegenstück der M3-Schrauben | klären |
| 2.6 | Einschmelzgewinde M3 (Länge ca. 5,7 mm) | 4 | Not-Aus-Gehäuse, Dome | klären |
| 2.7 | Zylinderschraube M3 × 10 | 4 | Deckel auf Gehäuse | da (M3-Sortiment) |
| 2.8 | Schraube M4 × 12 mit Mutter oder Holzschraube 4 × 20 | 2 | Gehäuseohren an Tisch/Profil | klären |
| 2.9 | Gummitülle oder Kabelbinder an den Kabelöffnungen Ø 9 mm | 2 | Zugentlastung Not-Aus | klären |

## 3 Elektrik

| Pos. | Teil | Menge | Status |
|---|---|---|---|
| 3.1 | Mikroschalter KW11-3Z oder KW12-3 (Hebel, 3 Pins) | 1 zum Testen, später 8 | offen |
| 3.2 | Not-Aus-Pilztaster Ø 22 mm, 1 Öffner + 1 Schliesser (Typ LAY37 / XB2), Pilz Ø 40 mm | 1 | offen |

Suchbegriff: «KW12-3 Mikroschalter 3 Pin» (AliExpress, ca. CHF 0,30–0,60 je Stück). **Vor dem Druck des Halters den Lochabstand der Schalterbohrungen am gekauften Teil messen** und `SW_LOCH` in `standardteile.py` anpassen (Startwert 9,5 mm).

## 4 Messmittel und Werkzeug

| Pos. | Teil | Status |
|---|---|---|
| 4.1 | Kugellager 608 (zum Testen der Reihe A) | klären (aus dem Prüfstand-J2-Bestellteil nehmen) |
| 4.2 | Einschmelzgewinde M3 und M4 (zum Testen der Reihe C) | klären |
| 4.3 | Schieblehre zum Messen der Lochmasse | klären |
| 4.4 | Lötkolben mit Spitze für Einschmelzgewinde | klären |
| 4.5 | Stahlachse 8 mm und M5-Schaft (Reihe B), Motorwelle 5 mm | da (Motoren) |
| 4.6 | Schraubendreher für M2/M3 | da |

## 5 Verbrauchsmaterial

PLA ca. 130 g gesamt (alle Teile, Testmenge).

## Was noch zu bestellen ist

- Mikroschalter KW12-3 (Test: 1 Stück; Bedarf später 8 Stück), unter CHF 5 inkl. Versand.
- Falls nicht vorhanden: Einschmelzgewinde M3 und M4 (Testsatz), Kugellager 608 (3 Stück).
- Not-Aus-Pilztaster 22 mm (ca. CHF 4–8). **Vor dem Druck die Gesamttiefe hinter der Lochplatte messen** (Kontaktblöcke, Startwert 58 mm Innentiefe in `notaus.py`).
- Kein Kauf nötig, bevor die Passungen gemessen sind.
