# Vollständige Stückliste: Schiene, Kettenklemme

Stand 04.11.2026 (nach Gutachten, Runde 2), passend zu `cad/skripte/schiene_kette.py`. Beschreibung: [../schiene-kabelfuehrung.md](../schiene-kabelfuehrung.md). Stufe C, noch nicht aktuell: nichts bestellen. **Status:** *klären* = bitte nachsehen · *offen* = noch zu kaufen. Preise sind Schätzungen, nicht geprüft.

## 1 Druckteile (STL in `cad/export/stl/Schiene_Kette/`)

| Pos. | Teil (Datei `.stl`) | Menge | Material | cm³ | Drucklage |
|---|---|---|---|---|---|
| 1.1 | `Kettenklemme_Sockel` (76 × 49,4 × 20,2 mm) | 2 (festes und bewegliches Ende) | PLA | je 24 | Fuss unten, Tasche oben |
| 1.2 | `Kettenklemme_Deckel` (20 × 45,4 × 5 mm) | 2 | PLA | je 3,5 | Kopfseite (Senkung) unten, Rippen oben |

Druckeinstellungen vollständig in `cad/export/stl/Schiene_Kette/Druckeinstellungen.md` (BambuLab A1, 0,4 mm, «0.20mm Standard @BBL A1», 0,20 mm, Gyroid, Stützen aus, Brim aus).

| Teil | Wände | Infill | Obere / untere | Stützen | Brim |
|---|---|---|---|---|---|
| Sockel | 4 | 40 % | 5 / 4 | aus | aus |
| Deckel | 4 | 100 % | 5 / 4 | aus | aus |

## 2 Kaufteile

| Pos. | Teil | Menge | Suchbegriff | ca. CHF | Status |
|---|---|---|---|---|---|
| 2.1 | **Schleppkette 10 × 15 mm mit Anschlussstücken** (bevorzugt; dann entfällt die Klemme), Aussenmass beim Händler erfragen; ob 10 × 15 reicht, ist offen (siehe Doku: Platz im Querschnitt) | 1 | `drag chain 10x15 1m with mounting brackets` (steht in `docs/bom.md`) | 6 | offen |
| 2.2 | T-Nutenstein M4 für Profil 2040 (Nut 6 mm) | 2 | `T-slot nut M4 2040 profile` | 1 | offen |
| 2.3 | Einschmelzgewinde M3 (Länge ca. 5,7 mm) | 4 | `M3 heat set insert` | 2 | klären |

## 3 Schrauben

| Pos. | Teil | Menge | Wofür | Status |
|---|---|---|---|---|
| 3.1 | Zylinderschraube M3 × 8 | 4 | Deckel auf Sockel (2 je Klemme) | klären |
| 3.2 | Zylinderschraube M4 × 14 | 2 | festes Ende: Sockel auf Profil, 20-mm-Seite (Scheibe 0,8 + Fuss 5 + Nutenlippe ca. 2 + mindestens 4 mm im T-Nutenstein) | klären |
| 3.3 | Scheibe M4, Aussen-Ø 9 (DIN 125) | 2 | unter dem Kopf, liegt auf dem Fuss (keine Senkung) | klären |
| 3.4 | Schrauben M4 für das bewegliche Ende | 2 | Länge hängt von der Schlittenplatte ab | offen (Schlitten nicht konstruiert) |

## 4 Elektrik, Zubehör

| Pos. | Teil | Menge | Status |
|---|---|---|---|
| 4.1 | `Kabelhalter` (aus `cad/skripte/standardteile.py`, STL in `cad/export/stl/Standardteile/`) | 2 | Zugentlastung der Kabel am Kettenende, drucken |
| 4.2 | `Endschalter_Halter` (aus `standardteile.py`) | 2 | Endschalter an beiden Enden der Schiene |
| 4.3 | Kabelbinder 2,5 mm breit | 2 | am Kabelhalter |

## 5 Messmittel und Werkzeug

Schieblehre zum Messen des Kettenendglieds (klären). Federwaage zum Prüfen der Haltekraft (Koffer- oder Federwaage, Pos. 5.3 in `pruefstand-j2.md`; vorhanden laut dieser Stückliste). Lötkolben für die Einschmelzgewinde (klären).

## 6 Verbrauchsmaterial

PLA etwa 55 g für zwei Sätze (4 Teile), Druckzeit etwa 2 Stunden (geschätzt).

## Was noch zu bestellen ist

Erst in Stufe C: Schleppkette **mit Anschlussstücken** und T-Nutensteine. Vorher klären: Aussenmass und Anschlussstücke der Kette, Aderzahl gegen Querschnitt (eventuell Kette 15 × 20 mm). Hat die Kette passende Anschlussstücke, entfallen die gedruckten Klemmen.
