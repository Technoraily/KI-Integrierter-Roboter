# Vollständige Stückliste: Basis mit J1

Stand 26.11.2026, passend zum CAD `cad/skripte/basis_j1.py` (**Bauraummodell V2.2**, Gutachten Runde 1: 5/10, Runde 2: 6/10, Runde 3: 7/10, alle eingearbeitet, Nachprüfung 8/10). Beschreibung und Montage: [basis-j1.md](../basis-j1.md). Die Stückzahlen sind gegen das Skript gezählt (Listen `HOLZ_SCHR`, `BOCK_SCHR`, `AUFLAGE`, `SPANN_SCHR`, `DECKEL_SCHR`, Magnetpositionen).

**Status:** *da* = vorhanden · *offen* = noch zu beschaffen · *klären* = bitte nachsehen. Preise sind Schätzungen, keine geprüften Angebote.

## Übersicht

| Gruppe | Positionen | noch offen, ca. CHF |
|---|---|---|
| 1 Druckteile | 17 | Filament (vorhanden) |
| 2 Lager, Welle, Riemen, Scheiben, O-Ring | 9 | 35 |
| 3 Schrauben, Muttern, Einsätze, Magnete | 15 | ca. 6 |
| 4 Antrieb und Elektrik | 4 | ca. 3 (Stecker folgen mit dem Steckerfeld) |
| 5 Aufstellung | 2 | 0–10 |
| 6 Werkzeug | – | je nach Bestand |
| 7 Verbrauchsmaterial | 2 | 0 |
| **Summe noch offen** | | **rund 45 CHF**, dazu was unter *klären* fehlt |

## 1 Druckteile

Allgemein: BambuLab A1, Düse 0,4 mm, Basis «0.20mm Standard @BBL A1», Schichthöhe 0,20 mm, texturiertes PEI, kein Brim (ausser wo angegeben). STL nach dem Gutachten in `cad/export/stl/Basis_J1/` mit eigener `Druckeinstellungen.md`. Gramm geschätzt (Vollvolumen aus dem CAD × Füllung).

| Pos. | Teil | Menge | Material | Wände | oben/unten | Infill | Stützen | Lage auf dem Bett | Nacharbeit |
|---|---|---|---|---|---|---|---|---|---|
| 1.1 | Passprobe_6810_Sitz_Magnet | 1 | PLA grau | 4 | 5/4 | 15 % Gyroid | keine | Bund unten | 6810 einpressen, 3 Magnete probieren |
| 1.2 | Passprobe_6810_Zapfen | 1 | PLA grau | 4 | 5/4 | 15 % Gyroid | keine | Fuss unten | **zuerst** 3 Einsätze setzen, dann 6810 aufschieben |
| 1.2a | Spannring_fuer_Probe (gleich wie 1.5) | 1 | PLA grau | 4 | 5/5 | 100 % | keine | Nut oben | O-Ring einlegen, auf die Probe schrauben |
| 1.3 | Grundplatte | 1 | PLA grau | 4 | 5/4 | 25 % Gyroid | keine | Platte unten | Einsätze, Muttern M3 (unten), Magnete |
| 1.4 | Nabe_Drehteller | 1 | PLA grau | **6** | 6/6 | 40 % Gyroid | keine | **Teller unten** (Oberseite aufs Bett) | 4 × M5-Mutter; Sitze nicht nacharbeiten |
| 1.5 | Spannring | 1 | PLA grau | 4 | 5/5 | 100 % | keine | Nut oben | O-Ring einlegen |
| 1.6 | Bock_unten | 1 | PLA grau | 5 | 5/5 | 40 % Gyroid | keine | Laschen unten | 3 Einsätze, 608 unten einpressen |
| 1.7 | Bock_Deckel | 1 | PLA grau | 5 | 5/5 | 40 % Gyroid | keine | **Lagersitz oben** (umgedreht, flach) | 608 einpressen |
| 1.8 | Distanzring_unten / _oben | je 1 | PLA grau | 3 | – | 100 % | keine | flach | – |
| 1.9 | Scheibe_GT2_80Z | 1 | PLA grau | 4 | 5/5 | 40 % Gyroid | keine | **obere Bordscheibe unten**, Nabe oben | 2 Einsätze radial |
| 1.10 | Motorplatte | 1 | **PETG weiss** | 4 | 5/5 | 40 % Gyroid | keine | flach | – |
| 1.11 | Motorkasten | 1 | PLA grau | 3 | 4/4 | 15 % Gyroid | keine (Auflagen und Buckel mit 45°-Stütze) | Boden unten | 4 Einsätze, 4 Magnete |
| 1.12 | Sockelgehaeuse_links / _rechts | je 1 | PLA grau | 3 | 4/4 | 15 % Gyroid | keine (Buckel mit Kegel) | **Deckel unten** (umgedreht) | Magnete |
| 1.13 | Farbring_J1_links / _rechts | je 1 | PLA rot | 3 | 4/4 | 15 % Gyroid | keine | Taschen unten | Magnete |
| 1.15 | Schalterhalter | 1 | PLA grau | 4 | 5/5 | 40 % Gyroid | keine | **Schalterauflage unten**, Lasche zeigt nach oben (Muttertaschen oben offen) | 2 M2-Muttern einlegen |
| 1.14 | Kastenkappe (massiv) | 1 | PLA weiss | 3 | 4/4 | 15 % Gyroid | keine | Rand unten | Magnete |

Gramm und Volumen pro Teil: siehe Tabelle am Schluss («Volumen aus dem CAD»). Geschätzt zusammen: **PLA grau ca. 600 g, PLA weiss ca. 60 g, PLA rot ca. 45 g, PETG weiss ca. 30 g.**

**Warum PETG für die Motorplatte:** Sie liegt direkt auf dem Motorflansch. Der Motor wird bis ca. 50–60 °C warm, und PLA wird ab ca. 55–60 °C weich. Unter der Riemenspannung würde sie sich langsam verziehen. Alle anderen Teile sind weit genug vom Motor weg.

**Magnete:** einen Tropfen Sekundenkleber in die Tasche. **Polung vor dem Kleben prüfen:** Gegenstück aufsetzen, die Magnete müssen sich anziehen.

## 2 Lager, Welle, Riemen, Scheiben, O-Ring

| Pos. | Teil | Menge | Suchbegriff | ca. CHF | Status |
|---|---|---|---|---|---|
| 2.1 | Dünnringlager **6810ZZ** oder 6810-2RS (50 × 65 × 7), nicht offen | 2 | `6810ZZ bearing` | 8 | offen (zuerst, für die Passprobe) |
| 2.2 | Kugellager **608ZZ** oder 608-2RS (8 × 22 × 7) | 2 | `608ZZ bearing 10pcs` | 6 | offen |
| 2.3 | Welle Ø 8 mm, auf 72 mm gekürzt, 2 D-Flächen anfeilen | 1 | `8mm linear shaft 100mm` | 3 | offen |
| 2.4 | Zahnscheibe HTD 3M, 16 Zähne, für 15 mm Riemen, Bohrung 8 | 1 | `HTD 3M 16T 15mm bore 8` | 5 | offen |
| 2.5 | Zahnscheibe GT2, 20 Zähne, für 10 mm Riemen, Bohrung 5 | 1 | `GT2 20T 10mm bore 5` | 3 | offen |
| 2.6 | Riemen HTD 3M, geschlossen, **318 mm (106 Zähne)**, 15 mm (Ersatz: 315 mm, dann Lasche anpassen) | 1 | `HTD 3M 318 15mm closed belt` | 5 | offen, Lieferbarkeit prüfen |
| 2.7 | Riemen GT2, geschlossen, **240 mm (120 Zähne)**, 10 mm | 1 | `GT2 240mm closed loop 10mm` | 3 | offen |
| 2.8 | O-Ring 50 × 1,5 mm, NBR (2 Stück: Arm und Probe) | 1 (Set) | `O-ring 50x1.5 NBR` | 2 | offen |
| 2.9 | Zylinderstift 3 × 12 mm, Stahl | 4 | Gehäuse 2, Bockdeckel 2; `dowel pin 3x12` | 2 (Set) | klären |

## 3 Schrauben, Muttern, Einsätze, Magnete

| Pos. | Teil | Menge | Verwendung | ca. CHF | Status |
|---|---|---|---|---|---|
| 3.1 | Holzschraube 4,0 × 16, Halbrundkopf | 11 | Grundplatte 8, Kasten 3 | 1 | klären |
| 3.2 | Einschmelzgewinde M3, 5 mm lang | 16 | Zapfen 3, Bock 3, Kasten 4, GT2-80 2, Schalterhalter 1, Passprobe 3 | – | da |
| 3.3 | Zylinderschraube M3 × 10, ISO 4762 | 19 | Spannring 3, Spannring der Probe 3, Bock 4, Motor 4, Motorplatte 4, Schalterhalter 1 | 2 | klären |
| 3.4 | Senkschraube M3 × 16, ISO 10642 | 2 | Bockdeckel | 1 (Set) | klären |
| 3.5 | Zylinderschraube M3 × 16, ISO 4762 | 1 | Spannschraube Bock | (Set) | klären |
| 3.6 | Mutter M3, ISO 4032 | 4 | unten in der Lasche (Bock) | – | klären |
| 3.7 | Unterlegscheibe M3, DIN 125 | 7 | Motor 4, Spannschraube 1, Einstellscheiben Schalterhalter 2 | 1 | klären |
| 3.7a | Unterlegscheibe M3 gross, **DIN 9021** (Langlöcher) | 8 | Bock 4, Motorplatte 4 | 1 | offen |
| 3.8 | Madenschraube M3 × 6, ISO 4029 | 2 | GT2-80 auf der Welle (die Kaufritzel bringen eigene mit) | 1 (Set) | klären |
| 3.9 | Zylinderschraube M2 × 12 (und M2 × 10 als Reserve) | 2 | Endschalter auf dem Halter (Schalter 6,4 + Halter 4) | 1 (Set) | klären |
| 3.10 | Mutter M2 | 2 | Endschalter, unten im Halter | (Set) | klären |
| 3.11 | Mutter M5, ISO 4032 | 4 | Schnittstelle Säule, im Teller | – | klären |
| 3.12 | M5-Schrauben zur Säule | 4 | Länge folgt mit der Säule (voraussichtlich M5 × 20) | – | da |
| 3.13 | Neodym-Magnet 6 × 3 mm | 31 | Grundplatte 4, Gehäuse 4 + Fuge 4, Deckel 4, Ring 4, Kasten 4, Kappe 4, Passprobe 3 | – | da (ca. 120) |
| 3.14 | Kabelverschraubung M16 (Kabel ca. 5–10 mm) mit Mutter | 1 | Kabelaustritt hinten | 1 | klären |
| 3.16 | Kabelbinder 2,5 mm | 2 | Niederhalter Kabel auf der Grundplatte | – | klären |
| 3.15 | Sekundenkleber | – | Magnete, Muttern | – | klären |

## 4 Antrieb und Elektrik

| Pos. | Teil | Menge | Suchbegriff | ca. CHF | Status |
|---|---|---|---|---|---|
| 4.1 | Schrittmotor 17CS04A-170E | 1 | – | – | da |
| 4.2 | Mikroschalter KW11 **mit Rolle** (vor dem Druck ausmessen) | 1 | `KW11 micro switch roller lever` | 2 | klären |
| 4.3 | Kabel Motor (JST-XH 4-polig) und Endschalter (JST-XH 2-polig) bis zum Steckerfeld | je 1 | laut `kabelkonzept.md` | folgt | folgt mit dem Steckerfeld |
| 4.4 | Einstellung im Octopus/grblHAL: **Motorstrom J1 1,0 A** | – | Begründung in `basis-j1.md` | – | – |

## 5 Aufstellung

| Pos. | Teil | Menge | ca. CHF | Status |
|---|---|---|---|---|
| 5.1 | Holzplatte mindestens 300 × 250 × 18 mm (Basis ca. 282 mm lang mit Kasten) | 1 | 0–5 | klären |
| 5.2 | **Schraubzwinge** (Holzplatte am Regal festmachen, sonst kippt der Arm) | 2 | – | da |

## 6 Werkzeug

Lötkolben mit Einsatzspitze, Inbusschlüssel 1,5 / 2 / 2,5 mm (ein kurzer Winkelschlüssel 2,5 für die Spannschraube), Kreuzschraubendreher, Metallsäge oder Trennscheibe und Flachfeile (Welle kürzen, D-Flächen), Messschieber, Seitenschneider, Spitzzange, Akkubohrer mit 2,5-mm-Bohrer (Holz vorbohren), Handy-App für die Riemenfrequenz.

## 7 Verbrauchsmaterial

Filament PLA grau/weiss/rot, PETG weiss (alles vorhanden), Sekundenkleber.

## Was noch zu bestellen ist

**Noch nichts.** Erst das Gutachten Runde 2. Danach in dieser Reihenfolge:
1. **2 × 6810** (ca. 8 CHF) bestellen und die Passproben drucken (`cad/export/stl/Basis_J1/`).
2. Nach der Passprobe: 2.2 bis 2.8, also 608, Welle, Scheiben, Riemen und O-Ring (ca. 27 CHF).
3. Dazu, was bei den *klären*-Positionen fehlt.
