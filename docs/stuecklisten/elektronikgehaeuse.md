# Vollständige Stückliste: Elektronikgehäuse J2-Prüfstand

Stand 28.10.2026, passend zum CAD `cad/skripte/elektronikgehaeuse.py` (Entwurf, Gutachten siehe `docs/reviews/`). Hier steht alles, was für Druck und Einbau des Gehäuses nötig ist. Elektrik, Kabel und Messmittel stehen in `docs/stuecklisten/pruefstand-j2.md` (Gruppe 4) und `docs/schema/verdrahtung-j2.md`; Beschreibung: `docs/elektronikgehaeuse.md`.

**Status:** *da* = vorhanden · *offen* = noch zu beschaffen · *klären* = unklar, ob vorhanden (bitte nachsehen). Preise sind Schätzungen.

## 1 Druckteile

Dateien in `cad/export/stl/Elektronikgehaeuse/`; Druckeinstellungen dort in `Druckeinstellungen.md`. Volumen als Vollkörper.

| Pos. | Teil (Datei `.stl`) | Menge | Material | cm³ | Drucklage |
|---|---|---|---|---|---|
| 1.1 | `EG_Wanne` (240 × 238 × 60) | 1 | PETG | 448 | Boden unten, offen nach oben |
| 1.2 | `EG_Deckel` (240 × 238 × 10, Platte 4 mm + Lippe 6 mm) | 1 | PETG | 230 | flach, Oberseite unten, Lippe nach oben |
| 1.3 | `EG_Netzblende` (134 × 57 × 5) | 1 | PETG | 34 | Aussenseite unten, Mutterntaschen oben |
| 1.4 | `EG_Klemmenabdeckung` (35 × 107 × 46) | 1 | PETG | 26 | Dach unten (auf dem Kopf), Stützen nur unter den zwei Laschen |
| 1.5 | `EG_Passprobe_C14` (56 × 100 × 5), Testteil | 1 | PETG | 19 | flach, Aussenseite unten, Mutterntaschen oben |
| 1.6 | `EG_Passprobe_F1` (114 × 26 × 5), Testteil | 1 | PETG | 12 | flach, wie exportiert |
| 1.7 | `EG_Netzteil_Schablone` (62 × 121 × 2,5), Testteil | 1 | PETG | 11 | flach, wie exportiert |
| 1.8 | `EG_Halter_24V` (80 × 26 × 12), Schale für F2 und Lüsterklemmen | 1 | PETG | 9 | flach, wie exportiert, Rand nach oben |

## 2 Kaufteile am Gehäuse

| Pos. | Teil | Menge | ca. CHF | Status |
|---|---|---|---|---|
| 2.1 | Netzteil Mean Well LRS-350-24 | 1 | – | da (Stückliste J2, 4.4) |
| 2.2 | Arduino Uno mit CNC-Shield V3 | 1 | – | da (4.3) |
| 2.3 | Einbau-Kaltgerätestecker C14, Schraubflansch | 1 | – | da (4.10) |
| 2.4 | Einbau-Sicherungshalter Bajonett (Gewinde etwas über 12 mm) mit Sicherung 5 × 20 mm T 3,15 A | 1 | – | da (4.11); Gewinde, Abflachung und Länge messen |
| 2.5 | Kfz-Flachsicherung 3 A im Halter (F2), Lüsterklemmen 24 V | 1 | – | da (4.13), liegen frei im Gehäuse |

## 3 Schrauben, Muttern, Gewindeeinsätze

| Pos. | Teil | Menge | Verwendung | Status |
|---|---|---|---|---|
| 3.1 | Einschmelzgewinde M3 (Messing Ø 5 × 4 mm) | 18 | Arduino-Dome (4), Deckeldome (10), Netzblendendome (4) | klären (Bestand nach den 41 für J2) |
| 3.2 | Schraube M3 × 6 | 4 | Uno auf die Dome (Eingriff in den Einsatz 4 mm, Spitze frei) | klären (Sortiment) |
| 3.3 | Schraube M3 × 10, Linsenkopf ISO 7380 (Zylinderkopf geht, steht dann 1 mm über dem Deckel) | 12 | Deckel (10), Klemmenabdeckung (2, Spitze bündig mit der Wannenunterseite) | klären (Sortiment), Menge prüfen |
| 3.4 | Schraube M3 × 16 (M3 × 14 geht) | 4 | Netzblende an die Wanne | klären |
| 3.5 | Schraube M3 × 12 | 2 | C14 an die Netzblende (mit dem C14 mitgelieferte Schrauben prüfen: Flansch + 5 mm Blende + 2,4 mm Mutter) | klären |
| 3.6 | Mutter M3 | 4 | C14 (2), Klemmenabdeckung (2) | da (Sortiment) |
| 3.7 | Zylinder- oder Linsenkopfschraube M4 × 6 | 4 | Netzteil von unten (Eindringtiefe im Netzteil höchstens 3 mm, nie länger) | offen (ca. 1 CHF) |
| 3.8 | Schraube M4 (Senkkopf, 16 bis 25 mm) oder Holzschraube 4 mm | 4 | Gehäuse auf ein Brett (nur falls gewünscht) | klären |
| 3.9 | Kabelbinder 2,5 bis 3,6 mm breit | 12 | F2 und Lüsterklemmen in der Schale (4), Schale am Boden (4), Netzkabel vorne (3), Reserve | klären |
| 3.10 | Schrumpfschlauch für Lötfahnen von F1 und die Hülsen am C14 (Isolation und Fixierung) | 1 Set | Netzseite | klären (Opa fragen) |
| 3.11 | **Zugentlastung / Knickschutz für das Netzkabel am C14** (Pflicht, Art mit Opa klären) | 1 | Netzseite | klären |

Kabelschuhe (Ring oder Gabel), Flachsteckhülsen und Aderendhülsen stehen in `pruefstand-j2.md` (Gruppe 4).

## 4 Messmittel und Werkzeug (zusätzlich zu Gruppe 5 und 7 der Stückliste J2)

| Pos. | Teil | Verwendung | Status |
|---|---|---|---|
| 4.1 | Schieblehre | Passproben, siehe «Zu messen» | da |
| 4.2 | Lötkolben mit Aufsatz für Einschmelzgewinde | 18 Einsätze | da (Test 20.10.) |
| 4.3 | Isolierter Schraubendreher (VDE) | Poti V ADJ durch den Deckelschlitz | klären (Opa) |
| 4.4 | Zwei Leisten (z. B. 20 mm hoch) | Wanne beim Anschrauben des Netzteils von unten | klären |

## 5 Verbrauchsmaterial

| Pos. | Material | Menge | Status |
|---|---|---|---|
| 5.1 | PETG-Filament | rund 790 cm³ Vollvolumen (448 + 230 + 34 + 26 + 19 + 12 + 11 + 9), mit üblicher Füllung geschätzt etwa 0,6 kg (Überschlag des Gutachters, Runde 3) | da (Nutzer 25.10.), Reichweite prüfen |
| 5.2 | Klebestift für die Druckplatte | nach Bedarf | klären |

## Was noch zu bestellen ist

Nur Kleinteile: Schrauben M4 × 6 (4 Stück), je nach Bestand Einschmelzgewinde M3 (18 Stück), Schrauben M3 × 6, × 10 (12 Stück) und × 16, Zugentlastung für das C14-Kabel. Alles zusammen unter 10 CHF. Das Gehäuse selbst kostet Filament (rund 10 CHF).

**Zu klären:** Bestand Einschmelzgewinde, Schrauben M3 × 6 / × 10 / × 16, Kabelbinder, isolierter Schraubendreher. **Kein Kauf nötig, bevor die Passproben (`EG_Passprobe_C14`, `EG_Passprobe_F1`, dann Netzblende und Klemmenabdeckung) gedruckt und probiert sind.**
