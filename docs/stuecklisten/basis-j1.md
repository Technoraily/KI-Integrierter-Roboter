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
| 2.8 | O-Ring NBR, Schnur 1,5 mm, **OD 52 (ID 49)**, gewählt 27.11.2026; OD 53 (ID 50) geht auch (2 Stück: Arm und Probe) | 1 (10 Stk.) | `NBR O-ring OD 52 CS 1.5` | 2 | offen, vom Nutzer ausgewählt |
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

## Abgleich mit dem AliExpress-Warenkorb (26.11.2026, abends)

Geprüft in Chrome, nur gelesen, nichts geändert oder bestellt. Preise mit Rabatt laut Warenkorb.

| Pos. | Teil laut Stückliste | Im Warenkorb (Variante, Preis) | Ergebnis |
|---|---|---|---|
| 2.1 | 2 × 6810ZZ | 6810ZZ 50 × 65 × 7, 2 Stück, CHF 6.97 | ok |
| 2.2 | 608ZZ | 608ZZ, 10 Stück, CHF 9.57 | ok |
| 2.3 | Welle Ø 8 | Linearwelle 8 mm × 150 mm, 2 Stück, CHF 5.14 | ok (auf 72 mm kürzen) |
| 2.4 | 3M-Ritzel 16 Z., 15 mm, Bohrung 8 | **fehlt** | ergänzen |
| 2.5 | GT2-Ritzel 20 Z., 10 mm, Bohrung 5 | **fehlt** | ergänzen |
| 2.6 | 3M-Riemen 318, **15 mm** breit | 3M 318 mm / 106 Z., aber **10 mm** breit, CHF 4.21 | **falsche Breite: 15 mm wählen** |
| 2.7 | GT2-Riemen 240, **10 mm** breit | 2GT 240 mm, aber **6 mm** breit, CHF 1.42 | **falsche Breite: 10 mm wählen** |
| 2.8 | O-Ring OD 53 × 1,5 (ID 50) | OD 53 / ID 50 / CS 1,5, 50 Stück, CHF 3.85 | ok |
| 2.9 | Zylinderstift 3 × 12 | GB119 M3 × 12, 20 Stück, CHF 1.79 | ok |
| 3.1 | Holzschraube 4 × 16 (11) | Rundkopf-Blechschraube M4 × 16, 20 Stück, CHF 1.72 | ok (selbstschneidend, hält in Holz) |
| 3.2 | Einschmelzgewinde M3 × 5 | M3, Länge 5, **Aussen-Ø 5**, 50 Stück, CHF 1.50 | ok (gleiche Sorte wie im Test vom 20.10.) |
| 3.3 | M3 × 10 ISO 4762 (19) | M3 × 10 Titan, **10 Stück**, CHF 2.62 | **zu wenig** (19 nötig), ausser du hast noch welche |
| 3.4 | M3 × 16 **Senkkopf** (2) | DIN 7991, aber **M4 × 16**, CHF 3.22 | **falsch: M3 × 16 wählen** |
| 3.5 | M3 × 16 ISO 4762 (1) | M3 × 16 Titan, 10 Stück, CHF 2.76 | ok |
| 3.6 | Mutter M3 (4) | **fehlt** (nur M2 und M5 im Korb) | ergänzen, ausser vorhanden |
| 3.7 / 3.7a | Scheiben M3 DIN 125 (7), **DIN 9021** (8) | **fehlen** | ergänzen |
| 3.8 | Madenschraube M3 × 6 | DIN 916 M3 × 6, 50 Stück, CHF 1.34 | ok |
| 3.9 / 3.10 | M2 × 12 + Mutter M2 | M2 × 12 (100), Mutter M2 (25), CHF 2.96 + 1.32 | ok |
| 3.11 | Mutter M5 (4) | Mutter M5, 25 Stück, CHF 1.69 | ok |
| 3.14 | Kabelverschraubung M16 | M16 weiss, 5 Stück, CHF 2.10 | ok |
| 3.15 | Sekundenkleber | 502-Kleber, 10 Stück, CHF 2.39 | ok |
| 4.2 | KW11 **mit Rolle** | «5pcs kw11» aus einem Angebot «KW12-3 und KW11-N» | **prüfen:** KW11-N hat meist einen Hebel **ohne** Rolle. Variante mit Rolle (z. B. KW11-3Z mit Rollenhebel) nehmen |
| – | (nicht für den Arm) | Hülle AirPods Pro 3, CHF 2.97 | – |

**Nachkontrolle (26.11.2026, später):** Der Nutzer hat den Warenkorb angepasst (20 Artikel, ca. CHF 61.79 inkl. Versand und Rabatt).
- 3M-Riemen jetzt **15 mm** / 318 mm / 106 Z. (CHF 4.87).
- GT2-Riemen jetzt **10 mm** / 240 mm (CHF 1.66).
- Senkkopf jetzt **M3 × 16** DIN 7991, 30 Stück (CHF 2.72).
- M3 × 10 jetzt **2 × 10 Stück**.
- Endschalter jetzt **KW11-3Z-N, 10 Stück, mit Rollenhebel** (laut Produktbild; Masszeichnung 20 × 10 mm, vor dem Druck des Halters trotzdem nachmessen).
- Ritzel 3M-16 und GT2-20, Scheiben M3 (DIN 125 und DIN 9021) und Muttern M3 hat der Nutzer schon, zum Teil vom J2-Prüfstand. Status: da.
- Einschmelzgewinde im Korb: M3, **Aussen-Ø 5 mm**, Länge 5. Das ist **genau die Sorte aus dem Test vom 20.10.** (Messing Ø 5, Bohrung Ø 4,0, `parameter.md`), also ok. Die Variante «M3 (OD 4,2 mm)» passt **nicht** zur Bohrung Ø 4,0.

## Warenkorb am 27.11.2026 (Bestellung noch nicht bestätigt)

Geprüft in Chrome und anhand von Bildschirmaufnahmen. Abweichungen zum Abgleich oben:
- O-Ring **OD 52 × 1,5** (10 Stk.), GT2 240 mm / 10 mm (anderer Händler).
- Endschalter: anderes Angebot (10 Stk. mit Rolle, 3 Anschlüsse), keine Masszeichnung gesehen: **vor dem Druck des Halters ausmessen**.
- Kabel: Silikon 2-adrig 26 AWG (Endschalter), JST-XH-Set 2 bis 5 Pole. 24 AWG entfällt, der Motor hat 1 m Kabel mit Stecker.
- Nicht in der Bestellung: Octopus, Pult-Teile, Not-Aus, Lüfter (Octopus und Pult ab 16.12. vorgesehen).
- J1-Test mit ESP32, CNC-Shield und TMC2209 vom J2-Prüfstand; Vref ca. 1,41 V für 1,0 A (aus dem J2-Wert umgerechnet, am Gerät messen).
