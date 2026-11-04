# Vollständige Stückliste: Zubehör J2-Prüfstand

Stand 04.11.2026 (nach Gutachten, Runde 2), passend zu `cad/skripte/j2_zubehoer.py`. Beschreibung: [../zubehoer-j2.md](../zubehoer-j2.md). **Status:** *da* = vorhanden (laut früheren Stücklisten) · *klären* = bitte nachsehen · *offen* = noch zu kaufen. Bestand habe ich nicht bei dir erfragt; «da» steht nur dort, wo ein anderes Dokument es schon so führt. Preise sind Schätzungen, nicht geprüft.

## 1 Druckteile (STL in `cad/export/stl/J2_Zubehoer/`)

| Pos. | Teil (Datei `.stl`) | Menge | Material | cm³ | Drucklage |
|---|---|---|---|---|---|
| 1.1 | `J2_Schalterprobe` (14 × 46 × 16 mm) | 1 | PLA | 8 | Tasche oben |
| 1.2 | `J2_Quertraeger_oben_Schalter` (14 × 56 × 24 mm) | 1 (zweiter für die andere Seite freiwillig) | PLA | 16 | liegend, Tasche oben |
| 1.3 | `J2_Motorkabelklemme` (54 × 20 × 7 mm) | 1 | PETG | 7 | flach, Rille oben |

Druckeinstellungen vollständig in `cad/export/stl/J2_Zubehoer/Druckeinstellungen.md` (BambuLab A1, 0,4 mm, «0.20mm Standard @BBL A1», 0,20 mm, Gyroid, Stützen aus, Brim aus).

| Teil | Wände | Infill | Obere / untere | Stützen | Brim |
|---|---|---|---|---|---|
| Schalterprobe | 3 | 15 % | 5 / 4 | aus | aus |
| Querträger mit Schalter | 4 | 40 % | 5 / 4 | aus | aus |
| Motorkabelklemme | 3 | 100 % | 5 / 4 | aus | aus |

## 2 Kaufteile

| Pos. | Teil | Menge | Suchbegriff | ca. CHF | Status |
|---|---|---|---|---|---|
| 2.1 | Mikroschalter KW12-3 mit Rollenhebel, 3 Pins (Masse nicht bestätigt) | 2 (1 zum Messen und Probieren, 1 Reserve; nach dem Messen kommt der Probe-Schalter in den Querträger) | `micro limit switch roller 10pcs` / `KW12-3` (10 Stück stehen schon in `docs/bom.md`) | 2 | offen |
| 2.2 | Einschmelzgewinde M3 (Länge ca. 5,7 mm) | 4 (8 mit zweitem Querträger) | `M3 heat set insert` | 2 | klären |

## 3 Schrauben und Kleinteile

| Pos. | Teil | Menge | Wofür | Status |
|---|---|---|---|---|
| 3.1 | Schraube M2 × 16 (× 14 ist das Minimum) | 2 je Schalter | Schalter durch den Querträger | klären |
| 3.2 | Mutter M2 | 2 je Schalter | in der Sechskanttasche der Gegenwand | klären |
| 3.3 | Kabelbinder 3,6 mm breit, 250–300 mm lang | 2 | Klemme um den Motor | klären |
| 3.4 | Kabelbinder 2,5 mm breit, 100 mm lang | 1 | Kabel in der Rille halten | klären |
| 3.5 | Zylinderschraube M3 × 16 | 0 zusätzlich | die Querträger werden gegen die alten getauscht, es gelten dieselben 4 Schrauben | da |
| 3.6 | Pappe oder Folie 0,1–0,4 mm | wenige Streifen | Beilagen unter dem Schalter | klären |

## 4 Elektrik

| Pos. | Teil | Menge | Status |
|---|---|---|---|
| 4.1 | Litze 0,5 mm², ca. 1 m, für den Schalter | 1 | klären |
| 4.2 | Schrumpfschlauch für die Lötfahnen | 1 Satz | klären |
| 4.3 | Durchgangsprüfer (Multimeter HC-303TN, ohne Summer; Anzeige springt) | 1 | da (laut HANDOFF) |

## 5 Messmittel und Werkzeug

| Pos. | Teil | Status |
|---|---|---|
| 5.1 | Schieblehre mit Tiefenmass (Schalter, Ritzel) | klären |
| 5.2 | Lötkolben mit Spitze für Einschmelzgewinde und Schalter-Lötfahnen | klären (HANDOFF: keiner vorhanden; in CLAUDE.md steht ein Test vom 20.10. mit Lötkolben, also vielleicht geliehen) |
| 5.3 | Messuhr (Prüfstand-Bestellung) für die Wiederholbarkeit | offen (Teil der Prüfstand-Bestellung) |
| 5.4 | Schraubendreher klein für M2 | klären |

## 6 Verbrauchsmaterial

PLA etwa 30 g, PETG etwa 8 g (aus den Volumina geschätzt).

## Was noch zu bestellen ist

- Mikroschalter KW12-3, zwei Stück (liegt schon in der Sammelbestellung `docs/bom.md`); **den Schalter vor dem Druck des Querträgers an der Schalterprobe messen.**
- Nichts weiter, bevor die Probe gemessen ist.
