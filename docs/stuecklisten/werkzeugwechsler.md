# Vollständige Stückliste: Werkzeugwechsler und Kamerahalter

Stand 04.11.2026 (nach Gutachten, Runde 2), passend zu `cad/skripte/werkzeugflansch.py`. Beschreibung: [../werkzeugwechsler.md](../werkzeugwechsler.md). Entwurf («nur vorsehen»), noch nichts bestellen ausser den Magneten für die Magnetprobe. **Status:** *klären* = bitte nachsehen · *offen* = noch zu kaufen · *nicht gewählt* = Entscheid fehlt. Masse der Kaufteile sind nicht bestätigt; Preise sind Schätzungen.

## 1 Druckteile (STL in `cad/export/stl/Werkzeugwechsler/`)

| Pos. | Teil (Datei `.stl`) | Menge | Material | cm³ | Drucklage |
|---|---|---|---|---|---|
| 1.1 | `WF_Magnetprobe_A` und `_B` (34 × 30 × 12 mm) | je 1 | PLA | je 11,9 | flach, Tasche oben |
| 1.2 | `WF_Master` (Ø 70 × 8 mm) | 1 | PLA | 27 | flach, Kupplungsseite oben |
| 1.3 | `WF_Werkzeug` (Ø 70 × 8 mm) | 1 | PLA | 28 | flach, Kupplungsseite oben |
| 1.4 | `WF_Kamerahalter` (46 × 56 × 28 mm) | 1 | PLA | 10 | auf der Seite liegend, wie exportiert |

Druckeinstellungen vollständig in `cad/export/stl/Werkzeugwechsler/Druckeinstellungen.md` (BambuLab A1, 0,4 mm, «0.20mm Standard @BBL A1», 0,20 mm, Gyroid, Stützen aus, Brim aus).

| Teil | Wände | Infill | Obere / untere | Stützen | Brim |
|---|---|---|---|---|---|
| Magnetprobe | 3 | 40 % | 5 / 4 | aus | aus |
| Master | 4 | 50 % | 5 / 4 | aus | aus |
| Werkzeug | 4 | 50 % | 5 / 4 | aus | aus |
| Kamerahalter | 4 | 100 % | 5 / 4 | aus | aus |

## 2 Kaufteile

| Pos. | Teil | Menge | Suchbegriff | ca. CHF | Status |
|---|---|---|---|---|---|
| 2.1 | Scheibenmagnet Ø 10 × 3 mm, N35 (Masse Startwert) | 10 (2 Probe, 6 Wechsler, 2 Reserve) | `neodymium disc magnet 10x3 N35` | 3 | offen |
| 2.2 | Stahlkugel Ø 6 mm (Lagerkugel, G10 oder besser) | 5 (3 + Reserve) | `steel ball 6mm bearing G10` | 2 | offen |
| 2.3 | Pogo-Pin (Federkontaktstift), Körper Ø ≤ 1,6 mm, Hub grösser als 0,4 mm; Haltesitz in der Bohrung Ø 1,7 mm (Typ und Durchmesser offen, `P75-E2` ist ungeprüft) | 6 + Reserve | `pogo pin spring loaded contact` | 3 | nicht gewählt |
| 2.3a | Stahlstift (Passstift oder Spannstift) Ø 3 × 6 mm als Codierstift | 1 | `dowel pin 3x6` | 1 | klären |
| 2.4 | Kameramodul 25 × 24 mm, Lochbild 21 × 12,5 mm, M2 (Startwert, z. B. Raspberry-Pi-Kameramodul) | 1 | | 28 | nicht gewählt |
| 2.5 | Einschmelzgewinde M3 (Länge ca. 5,7 mm) | 6 | | | klären |
| 2.6 | Kleber für Magnete und Kugeln: Sekundenkleber, besser 2-Komponenten-Kleber (Magnete halten die Zugkraft des Paares) | 1 | `2K epoxy 5 min` | 3 | klären |

## 3 Schrauben

| Pos. | Teil | Menge | Wofür | Status |
|---|---|---|---|---|
| 3.1 | niedrige Zylinderschraube M5 × 12, DIN 7984 (Kopfhöhe 3,5 mm; Länge hängt von der Gewindetiefe im Handgelenkflansch ab) | 4 | Master auf ISO-Flansch | klären |
| 3.1a | Scheibe M5, klein (Ø 9 × 1, DIN 433), Stahl | 4 | unter dem Kopf in der Senkung (Kopf 3,5 + Scheibe 1 = 4,5 mm in 5,5 mm tiefer Senkung; 2,5 mm PLA unter der Scheibe) | klären |
| 3.2 | Schraube M3 × 6 (Fuss 4 mm, Senkung 2,2 mm, Bohrung im Master 6 mm tief) | 2 | Kamerahalter auf Master | klären |
| 3.3 | Schlitz-Zylinderschraube M2 × 6, DIN 84 / ISO 1207 (Kopf Ø 3,8 × 1,3; **nicht** Inbus, dessen Kopf 2,0 mm hoch ist und vorsteht) | 6 | Kontaktflächen der Werkzeugplatte (Kopf bündig in der Senkung) | klären |
| 3.3a | Mutter M2, **Messing** (Edelstahl lässt sich kaum löten) | 6 | in der Sechskanttasche hinten. Löten nicht in der Tasche (Lötwärme erweicht PLA, Glasübergang rund 55–60 °C, und Kleber im Gewinde kann den Kontakt isolieren): Ader mit Kabelöse unter der Mutter klemmen oder vor dem Einbau an die Schraube löten | klären |
| 3.4 | Schraube M2 × 8 | 4 | Kameramodul auf Halter | klären |
| 3.4b | Ringschraube M4 (DIN 580 oder Schraube mit Öse), Länge etwa 12 mm; Gewindelänge am gelieferten Teil prüfen (Kernloch 8 mm tief) | 2 | Magnetprobe, Zugöse | offen (Suchbegriff `eye bolt M4`, ca. CHF 1) |
| 3.4a | Mutter M2 | 4 | dazu | klären |
| 3.5 | Schrauben M3 für den Greifer | 4 | Länge hängt vom Greifer ab | nicht gewählt |

## 4 Elektrik

| Pos. | Teil | Menge | Status |
|---|---|---|---|
| 4.1 | Litze 0,25 mm² für die Pogo-Pins, 6 Adern | etwa 1 m | klären |
| 4.2 | Flachbandkabel (CSI) für das Kameramodul, passende Länge | 1 | nicht gewählt |

## 5 Messmittel und Werkzeug

| Pos. | Teil | Status |
|---|---|---|
| 5.1 | Federwaage oder Küchenwaage mit Haken für die Magnetprobe (bis 5 kg) | da (Kofferwaage laut `pruefstand-j2.md`, Pos. 5.3) |
| 5.2 | Kompass oder zweiter Magnet für die Polung | klären |
| 5.3 | Lötkolben (Einschmelzgewinde, Pogo-Pins) | klären (HANDOFF: keiner vorhanden) |
| 5.4 | Schieblehre | klären |
| 5.5 | Karton 0,4 mm als Spaltlehre für die Magnetprobe | klären |

## 6 Verbrauchsmaterial

PLA etwa 75 bis 85 g (Master und Werkzeug je etwa 25 g, Kamerahalter etwa 13 g, Proben je 9 g).

## Was noch zu bestellen ist

- **Jetzt (nur für die Probe):** zwei Magnete Ø 10 × 3 mm, falls kein Magnet da ist, für unter CHF 2; und eine Kugel Ø 6 mm für den Test der Kugeltasche.
- **Nach der Magnetprobe:** Magnete (Grösse nach der gemessenen Kraft), Kugeln, Pogo-Pins. Kamera erst, wenn Modell und Lochbild gewählt sind.
