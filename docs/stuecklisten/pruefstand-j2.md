# Vollständige Stückliste: Prüfstand Schultergelenk J2

Stand 12.10.2026, passend zum CAD `cad/skripte/j2_pruefstand.py` (Gutachten 8/10). Hier steht **alles**, was es für Bau und Messung braucht: Druckteile, Kaufteile, jede Schraube, Elektrik, Messmittel, Werkzeug und Verbrauchsmaterial. Beschreibung und Montage: [pruefstand-j2.md](../pruefstand-j2.md).

**Status:** *da* = vorhanden oder bereits bestellt · *offen* = noch zu beschaffen · *klären* = unklar, ob vorhanden (bitte nachsehen). Die Preise sind Schätzungen, keine geprüften Angebote.

## Übersicht

| Gruppe | Positionen | Stück | noch offen, ca. CHF |
|---|---|---|---|
| 1 Druckteile | 22 | 22 | Filament |
| 2 Riemen, Scheiben, Lager, Wellen | 9 | 21 | 22 |
| 3 Schrauben, Muttern, Gewindeeinsätze | 13 | 92 | 2 |
| 4 Antrieb und Elektrik | 9 | 9 | 6 |
| 5 Messmittel und Lasten | 9 | – | 16 |
| 6 Aufstellung | 4 | – | 0–10 |
| 7 Werkzeug | 13 | – | je nach Bestand |
| 8 Verbrauchsmaterial | 4 | – | Filament |
| **Summe noch offen** | | | **rund 46 CHF**, dazu was unter *klären* fehlt, Filament und Werkzeug |

## 1 Druckteile

Dateien in `cad/export/stl/J2_Pruefstand/`. Volumen als Vollkörper; die Filamentmenge steht in Gruppe 8.

| Pos. | Teil (Datei `.stl`) | Menge | Material | cm³ | Drucklage |
|---|---|---|---|---|---|
| 1.1 | `Wange_Links` (Motorseite) | 1 | PETG | 266 | flach |
| 1.2 | `Wange_Rechts` | 1 | PLA | 266 | flach |
| 1.3 | `Quertraeger_unten_links` | 1 | PLA | 18 | liegend |
| 1.4 | `Quertraeger_unten_rechts` | 1 | PLA | 18 | liegend |
| 1.5 | `Quertraeger_oben_links` | 1 | PLA | 18 | liegend |
| 1.6 | `Quertraeger_oben_rechts` | 1 | PLA | 18 | liegend |
| 1.7 | `Scheibe_GT2_Z72` | 1 | PETG | 21 | Zahnkranz unten, Nabe oben |
| 1.8 | `Scheibe_3M_Z64` | 1 | PETG | 49 | Zahnkranz unten, Hülse oben |
| 1.9 | `Scheibe_5M_Z90` | 1 | PETG | 207 | Hebelseite unten |
| 1.10 | `Lasthebel` | 1 | PLA | 223 | flach, Nabenbund oben |
| 1.11 | `Messzeiger` | 1 | PLA | 15 | flach, Tastklotz oben |
| 1.12 | `Messuhrhalter` | 1 | PLA | 34 | auf dem Rücken |
| 1.13 | `Spannrolle_5M` | 1 | PETG | 7 | stehend |
| 1.14 | `Distanzring_A_links` | 1 | PETG | 0,4 | stehend |
| 1.15 | `Distanzring_A_rechts` | 1 | PETG | 0,1 | stehend |
| 1.16 | `Distanzring_B_links` | 1 | PETG | 0,1 | stehend |
| 1.17 | `Distanzring_B_rechts` | 1 | PETG | 0,5 | stehend |
| 1.18 | `Huelse_5M_links` | 1 | PETG | 0,2 | stehend |
| 1.19 | `Huelse_5M_mitte` | 1 | PETG | 0,1 | stehend |
| 1.20 | `Huelse_5M_rechts` | 1 | PETG | 5,2 | stehend |
| 1.21 | `Huelse_3M_links` | 1 | PETG | 1,9 | stehend |
| 1.22 | `Huelse_3M_rechts` | 1 | PETG | 1,5 | stehend |

Die Scheiben 1.7 bis 1.9 erst drucken, wenn die gekauften Ritzel nachgemessen sind. Vor allem anderen kommt der Toleranz-Testdruck (noch zu konstruieren).

## 2 Riemen, Scheiben, Lager, Wellen

| Pos. | Teil | Gebraucht | Bestellen | Suchbegriff AliExpress | ca. CHF | Status |
|---|---|---|---|---|---|---|
| 2.1 | Ritzel GT2, 20 Zähne, Bohrung 5 mm, für 10-mm-Riemen, **mit Nabe** (2 Gewindestifte), mit Bordscheiben | 1 | 2 | `GT2 pulley 20 teeth bore 5mm width 10mm` | 3 | offen |
| 2.2 | Ritzel HTD-3M, 16 Zähne, Bohrung 8 mm, für 15-mm-Riemen, mit Bordscheiben, **mit Nabe** (ca. 6 mm; ohne Nabe ginge auch, nur der Distanzring wird angepasst) | 1 | 1 | `HTD 3M pulley 16 teeth bore 8mm width 15mm` | 4 | offen |
| 2.3 | Ritzel HTD-5M, 18 Zähne, Bohrung 8 mm, für 15-mm-Riemen, mit Bordscheiben und **Nabe zwingend** (ca. Ø 20 × 8 mm, 2 Gewindestifte; die Hülse der 64er-Scheibe greift darüber) | 1 | 1 | `HTD 5M pulley 18 teeth bore 8mm width 15mm` | 5 | offen |
| 2.4 | Riemen GT2 geschlossen, 10 mm breit, 200 mm (100 Zähne) | 1 | – | – | – | da |
| 2.5 | Riemen HTD-3M geschlossen, 15 mm breit, 252 mm (84 Zähne) | 1 | – | – | – | da |
| 2.6 | Riemen HTD-5M geschlossen, 15 mm breit, 525 mm (105 Zähne) | 1 | – | – | – | da |
| 2.7 | Rillenkugellager 608 (8 × 22 × 7 mm): 6 in den Wangen, 2 in der 5M-Spannrolle, 2 als 3M-Spannrolle | 10 | 10–20 | `608 2RS bearing 10pcs` | 4–8 | da (ausgewählt: 608ZZ) |
| 2.8 | Präzisionswelle 8 mm, auf 70 mm abgelängt, mit angefeilten Flächen | 3 | 4 × 100 mm | `linear shaft 8mm 100mm` | 8 | offen |
| 2.9 | Sechskantschraube M8 × 90 mit Schaft (Teilgewinde) – Achse der Spannrollen | 2 | 2 | Baumarkt | 2 | offen |

## 3 Schrauben, Muttern, Gewindeeinsätze

Alle M3- und M4-Schrauben sind Zylinderschrauben mit Innensechskant (DIN 912).

| Pos. | Teil | Menge | Wofür | Status |
|---|---|---|---|---|
| 3.1 | M3 × 8 | 1 | Gewindestift in der Hebelnabe (auf die Abtriebswelle) | da (Sortiment) |
| 3.2 | M3 × 10 | 2 | Gewindestifte in der Nabe der 72er-Scheibe | da (Sortiment) |
| 3.3 | M3 × 12 | 4 | Motor an die linke Wange | da (Sortiment) |
| 3.4 | M3 × 16 | 26 | Querträger (16), Lasthebel (6), Messzeiger (2), Messuhrhalter (2) | klären |
| 3.5 | M3 × 20 | 4 | Prüfstand aufs Grundbrett | klären |
| 3.6 | M3 × 25 | 4 | Stellschrauben der 3M-Rolle (2), Blockierstift (1), Klemmung der Messuhr (1) | klären |
| 3.7 | M3 × 30 | 2 | Stellschrauben der 5M-Rolle | klären |
| 3.8 | M4 × 16 | 2 | Mitnahme an Welle B, ersetzen die Gewindestifte des 5M-Ritzels (am Ritzel prüfen: M4 oder M5) | offen, 1 CHF |
| 3.9 | Mutter M8, selbstsichernd | 2 | Spannrollen-Schrauben | offen, Baumarkt |
| 3.10 | Unterlegscheibe M8 (Aussen-Ø mindestens 16 mm) | 4 | unter Kopf und Mutter der M8, über den Langlöchern | offen, Baumarkt |
| 3.11 | Einschmelzgewinde M3 (Messing, Aussen-Ø 5 mm, 4 mm lang) | 41 | siehe unten | da (ausgewählt), 100er-Pack 4 CHF |
| 3.12 | Gewindestifte der gekauften Ritzel | – | liegen den Ritzeln bei (GT2 und 3M werden verwendet, 5M wird ersetzt) | mit 2.1–2.3 |
| 3.13 | M3-Sortiment als Ganzes, falls Längen fehlen | 1 | – | `M3 hex socket screw assortment DIN912`, 6 CHF |

**Wo die 41 Einschmelzgewinde sitzen:** Querträger 16 (je 2 pro Ende) · untere Querträger 4 (von unten, fürs Grundbrett) · 90er-Scheibe 8 (Hebel 6, Messzeiger 2) · 72er-Scheibe 2 · Hebelnabe 1 · linke Wange 3 (Blockierstift 1, Stellschrauben 2) · rechte Wange 6 (Stellschrauben 2, Messuhrhalter 4) · Messuhrhalter 1.

## 4 Antrieb und Elektrik

| Pos. | Teil | Menge | ca. CHF | Status |
|---|---|---|---|---|
| 4.1 | Schrittmotor NEMA 17, 60 mm lang, ca. 0,7 Nm, 5-mm-Welle | 1 | 12 | da |
| 4.2 | Treiber TMC2209 mit Kühlkörper (1 gebraucht, 1 Reserve) | 2 | 6 | offen |
| 4.3 | Arduino Uno mit CNC-Shield | 1 | – | da |
| 4.4 | Netzteil 24 V, mindestens 5 A (120 W), geschlossenes Tischnetzteil mit Hohlstecker 5,5 × 2,5 mm. Für die Messungen im Stillstand (Spiel, Steifigkeit, Haltetest) genügt auch das vorhandene Netzteil 12 V / 4 A | 1 | 30–35 | offen (laut Nutzer am 12.10.2026 nicht vorhanden) |
| 4.5 | Adapter Hohlstecker 5,5 × 2,5 mm auf Schraubklemmen | 1 | 2 | klären |
| 4.6 | Motorkabel, 4-polig, passend zum Stecker am Motor und zur Stiftleiste am Shield | 1 | 2 | klären |
| 4.7 | USB-Kabel zum Uno (USB-A auf USB-B) | 1 | 2 | klären |
| 4.8 | Litze 0,75 mm², rot und schwarz, je 0,5 m (Netzteil → Shield) | 1 | 1 | klären |
| 4.9 | PC mit GRBL-Sender oder Arduino-IDE | 1 | – | da |

Der Treiber läuft auf dem CNC-Shield an 24 V. Wie der Strom eingestellt wird, wird beim Aufbau dokumentiert; dafür braucht es das Multimeter (5.7).

## 5 Messmittel und Lasten

| Pos. | Teil | Wofür | ca. CHF | Status |
|---|---|---|---|---|
| 5.1 | Messuhr 0,01 mm, Schaft Ø 8 mm, Messweg 10 mm | Umkehrspiel, Steifigkeit, Haltetest | 12 mit Stativ | offen |
| 5.2 | Magnet- oder Tischstativ zur Messuhr | zweite Messstelle am Nabenbund (ohne Stativ bleibt eine Unsicherheit) | in 5.1 | offen |
| 5.3 | Koffer- oder Federwaage bis mindestens 10 kg | Wechsellast ±2 Nm; Gewichte abwiegen | 4 | offen |
| 5.4 | Küchenwaage | kleine Gewichte, Motorvermessung | – | da |
| 5.5 | Gewichte: 1,07 kg · 5,9 kg · 6,3 kg | Wechsellast, Haltetest, volles Moment – z. B. Wasserflaschen in einer Tragtasche, mit der Kofferwaage abgewogen | – | Haushalt |
| 5.6 | Schnur oder Schlaufe (trägt 10 kg) und ein Haken oder eine Schraube M8 für die Lastbohrung | Gewicht anhängen, Fangschnur | – | Haushalt |
| 5.7 | Multimeter | Treiberstrom einstellen, Wicklungswiderstand | 10–15 | klären |
| 5.8 | Schieblehre | Ritzel nachmessen, Testdruck prüfen | 8–10 | klären |
| 5.9 | Infrarot-Thermometer | Erwärmung von Motor und Wange im Haltetest (verzichtbar: Handprobe und Zeit notieren) | 7 | verzichtbar |

## 6 Aufstellung

| Pos. | Teil | Menge | Status |
|---|---|---|---|
| 6.1 | Brett 220 × 200 × 12 mm, Sperrholz oder MDF | 1 | Baumarkt oder Rest |
| 6.2 | Schraubzwinge, Spannweite mindestens 60 mm (Brett + Tischplatte) | 2 | klären |
| 6.3 | Weiche Unterlage unter dem Gewicht (Kiste, Hocker, Kissen) | 1 | Haushalt |
| 6.4 | Papierstreifen | – | zum Prüfen, dass der Hebel nicht auf dem Anschlag liegt |

Bohrbild und Befestigung: [Skizze](../bilder/pruefstand_befestigung.png).

## 7 Werkzeug

| Pos. | Werkzeug | Wofür | Status |
|---|---|---|---|
| 7.1 | Lötkolben (am besten mit Einschmelzspitze M3) | 41 Einschmelzgewinde setzen | klären |
| 7.2 | Innensechskant 2,5 mm, lang, mit Kugelkopf | alle M3-Schrauben; Motorschrauben und Blockierstift durch die rechte Wange | klären |
| 7.3 | Innensechskant 3 mm | M4 × 16 | klären |
| 7.4 | Innensechskant 1,5 und 2 mm | Gewindestifte der gekauften Ritzel | klären |
| 7.5 | Gabel- oder Ringschlüssel 13 mm, 2 Stück | M8-Schrauben der Spannrollen | klären |
| 7.6 | Metallsäge | Wellen auf 70 mm ablängen | klären |
| 7.7 | Feile (flach) | Wellenenden entgraten, Flächen für die Gewindestifte anfeilen | klären |
| 7.8 | Schraubstock oder Zwinge zum Einspannen der Wellen | Sägen und Feilen | klären |
| 7.9 | Bohrmaschine oder Akkuschrauber | Brett bohren, Bohrungen aufreiben | klären |
| 7.10 | Bohrer 3,0 · 3,5 · 4,0 · 6,5 · 8,0 · 10 mm | 3,0 Blockierbohrungen · 3,5 Brett · 4,0 Mitnahmebohrungen · 6,5 Senkung im Brett · 8,0 Naben und Messuhrhalter · 10 Löcher für die Stellschrauben | klären |
| 7.11 | Kreuzschlitz- oder Schlitzschraubendreher, klein | Klemmen am CNC-Shield und am Adapter | klären |
| 7.12 | Seitenschneider, Abisolierzange | Verkabelung | klären |
| 7.13 | 3D-Drucker BambuLab A1 | Druckteile | da |

## 8 Verbrauchsmaterial

| Pos. | Material | Menge | Status |
|---|---|---|---|
| 8.1 | PETG-Filament | rund 560 cm³ Vollvolumen, mit üblicher Füllung geschätzt 0,35–0,45 kg | klären |
| 8.2 | PLA-Filament | rund 610 cm³ Vollvolumen, geschätzt 0,35–0,45 kg | klären |
| 8.3 | Filament für Toleranz-Testdruck und Fehldrucke | Reserve 0,2 kg | – |
| 8.4 | Schraubensicherung mittelfest (verzichtbar) | 1 Tropfen je Gewindestift der Ritzel | verzichtbar |

Die genaue Filamentmenge zeigt der Slicer; sie hängt von Wandzahl und Füllung ab.

## Was noch zu bestellen ist

Aus den Gruppen 2 bis 5, alles mit Status *offen*:

| Teil | Menge | ca. CHF |
|---|---|---|
| Ritzel GT2 20 Z / HTD-3M 16 Z / HTD-5M 18 Z (alle mit Nabe und Bordscheiben) | 2 / 1 / 1 | 12 |
| Präzisionswelle 8 mm × 100 mm | 4 | 8 |
| M8 × 90 mit Schaft, selbstsichernde Mutter M8, Scheiben M8 | 2 / 2 / 4 | 3 |
| M4 × 16 | 2 | 1 |
| TMC2209 mit Kühlkörper | 2 | 6 |
| Messuhr 0,01 mm mit Stativ | 1 | 12 |
| Kofferwaage | 1 | 4 |
| **Summe** | | **rund 46** |

Dazu kommt, was sich beim Nachsehen als fehlend herausstellt (Status *klären*): M3-Schrauben in 16, 20, 25 und 30 mm, Motorkabel, USB-Kabel, Multimeter, Schieblehre, Zwingen, Werkzeug, Filament.
