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

Dateien in `cad/export/stl/J2_Pruefstand/`. Teile mit Zusatz `_Lager22-20` sind mit dem gemessenen Lagersitz Ø 22,20 mm (18.10.2026) neu exportiert. Volumen als Vollkörper; die Filamentmenge steht in Gruppe 8.

| Pos. | Teil (Datei `.stl`) | Menge | Material | cm³ | Drucklage |
|---|---|---|---|---|---|
| 1.1 | `Wange_Links_Lager22-20` (Motorseite) | 1 | PETG | 266 | flach |
| 1.2 | `Wange_Rechts_Lager22-20` | 1 | PLA | 266 | flach |
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
| 1.13 | `Spannrolle_5M_Lager22-20` | 1 | PETG | 7 | stehend |
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
| 2.1 | Ritzel GT2, 20 Zähne, Bohrung 5 mm, für 10-mm-Riemen, **mit Nabe** (2 Gewindestifte), mit Bordscheiben | 1 | 2 | `GT2 pulley 20 teeth bore 5mm width 10mm` | 3 | im Warenkorb (XIAOXI 3D, 2,93 CHF, 1 Stück; Variante Bohrung 5 mm / Breite 10 mm auf der Produktseite geprüft und lieferbar; Bild zeigt Nabe mit Gewindestift und Bordscheibe). Die erste Wahl (Creality, nur 6 mm breit) wurde ersetzt. Keine Reserve im Warenkorb. |
| 2.2 | Ritzel HTD-3M, 16 Zähne, Bohrung 8 mm, für 15-mm-Riemen, mit Bordscheiben, **mit Nabe** (ca. 6 mm; ohne Nabe ginge auch, nur der Distanzring wird angepasst) | 1 | 1 | `HTD 3M pulley 16 teeth bore 8mm width 15mm` | 4 | im Warenkorb (Wanco Motor, «K-Typ» mit Nabe, Variante 8 mm / 16 mm / 16 Z auf Produktseite lieferbar). Zeichnung: Nabe Ø 18 mm, Gesamtlänge 29 mm bei 15-mm-Riemen, 2 Gewindestifte M4. Die Nabe ist also etwa 13 mm lang, nicht «ca. 6 mm»: Distanzring und Bauraum im CAD prüfen. |
| 2.3 | Ritzel HTD-5M, 18 Zähne, Bohrung 8 mm, für 15-mm-Riemen, mit Bordscheiben und **Nabe zwingend** (ca. Ø 20 × 8 mm, 2 Gewindestifte; die Hülse der 64er-Scheibe greift darüber) | 1 | 1 | `HTD 5M pulley 18 teeth bore 8mm width 15mm` | 5 | im Warenkorb (JHong Transmission Store, 7,12 CHF; Variante 8 mm glatte Bohrung / Riemenbreite 15 mm / 18 Zähne auf der Produktseite vorhanden). Bilder zeigen Nabe mit 2 Gewindestiften und Bordscheibe; **Masse der Nabe nennt der Händler nicht** → beim Eintreffen mit der Schieblehre messen (verlangt: ca. Ø 20 × 8 mm). |
| 2.4 | Riemen GT2 geschlossen, 10 mm breit, 200 mm (100 Zähne) | 1 | 1 | – | 2,32 | im Warenkorb (XIAOXI 3D, Variante 10 mm / 200 mm geprüft) |
| 2.5 | Riemen HTD-3M geschlossen, 15 mm breit, 252 mm (84 Zähne) | 1 | 1 | – | 6,09 | im Warenkorb (Carol Store, Variante 15 mm / 252 mm) |
| 2.6 | Riemen HTD-5M geschlossen, 15 mm breit, 525 mm (105 Zähne) | 1 | 1 | – | 2,76 | im Warenkorb (Variante 15 mm / 5M-525 mm geprüft) |
| 2.7 | Rillenkugellager 608 (8 × 22 × 7 mm): 6 in den Wangen, 2 in der 5M-Spannrolle, 2 als 3M-Spannrolle | 10 | 10–20 | `608 2RS bearing 10pcs` | 4–8 | da (ausgewählt: 608ZZ; 25.10.: Kugellager vorhanden) |
| 2.8 | Präzisionswelle 8 mm, auf 70 mm abgelängt, mit angefeilten Flächen | 3 | 4 × 100 mm | `linear shaft 8mm 100mm` | 8 | da (Wellen vom Opa, Nutzer 25.10.; Länge und Durchmesser mit der Schieblehre prüfen) |
| 2.9 | Sechskantschraube M8 × 90 mit Schaft (Teilgewinde) – Achse der Spannrollen | 2 | 2 | Baumarkt | 2 | im Warenkorb (DIN 931, Edelstahl 316, M8, 90 mm, 2 Stück, 3,83 CHF) |

## 3 Schrauben, Muttern, Gewindeeinsätze

Alle M3- und M4-Schrauben sind Zylinderschrauben mit Innensechskant (DIN 912).

| Pos. | Teil | Menge | Wofür | Status |
|---|---|---|---|---|
| 3.1 | M3 × 8 | 1 | Gewindestift in der Hebelnabe (auf die Abtriebswelle) | da (Sortiment) |
| 3.2 | M3 × 10 | 2 | Gewindestifte in der Nabe der 72er-Scheibe | da (Sortiment) |
| 3.3 | M3 × 12 | 4 | Motor an die linke Wange | da (Sortiment) |
| 3.4 | M3 × 16 | 26 | Querträger (16), Lasthebel (6), Messzeiger (2), Messuhrhalter (2) | da (laut Nutzer 25.10.: alle Schrauben vorhanden) |
| 3.5 | M3 × 20 | 4 | Prüfstand aufs Grundbrett | da (wie 3.4) |
| 3.6 | M3 × 25 | 4 | Stellschrauben der 3M-Rolle (2), Blockierstift (1), Klemmung der Messuhr (1) | da (wie 3.4) |
| 3.7 | M3 × 30 | 2 | Stellschrauben der 5M-Rolle | da (wie 3.4) |
| 3.8 | M4 × 16 | 2 | Mitnahme an Welle B, ersetzen die Gewindestifte des 5M-Ritzels (am Ritzel prüfen: M4 oder M5) | da (wie 3.4) |
| 3.9 | Mutter M8, selbstsichernd | 2 | Spannrollen-Schrauben | Nutzer hat normale M8-Muttern (nicht selbstsichernd); im Warenkorb: DIN 6926 Flansch-Nylock M8, 5 Stück, 0,91 CHF |
| 3.10 | Unterlegscheibe M8 (Aussen-Ø mindestens 16 mm) | 4 | unter Kopf und Mutter der M8, über den Langlöchern | da (Aussen-Ø nachmessen, mind. 16 mm) |
| 3.11 | Einschmelzgewinde M3 (Messing, Aussen-Ø 5 mm; Längen 5 / 4 / 3 mm gemischt, siehe unten) | 41 | siehe unten | da, alle 41 am 20.10.2026 gesetzt (Bohrung Ø 4,0 mm, mit Lötkolben bestätigt) |
| 3.12 | Gewindestifte der gekauften Ritzel | – | liegen den Ritzeln bei (GT2 und 3M werden verwendet, 5M wird ersetzt) | mit 2.1–2.3 |
| 3.13 | M3-Sortiment als Ganzes, falls Längen fehlen | 1 | – | `M3 hex socket screw assortment DIN912`, 6 CHF |

**Verwendete Längen (20.10.2026; nach der Z90 blieben 9 × 5 mm, 11 × 4 mm, 26 × 3 mm):** 5 mm: obere Querträger (8) und ein Stirnloch der unteren (1); 4 mm: Z72-Nabe (2), Hebelnabe (1), Stellschrauben in den Wangenkanten (4), Grundbrett-Löcher der unteren Querträger (4); 3 mm: übrige untere Querträger (7), Blockierstift (1), Messuhrhalter an der Wange (4) und Klemmschraube (1). Z90: Hebelkreis (6) mit 5 mm, Zeiger (2) mit 4 mm. Übrig: 13 × 3 mm. Die Bohrtiefen im CAD sind für 4 mm ausgelegt; das 4-mm-Loch der Z72-Nabe ist nur 5,5 mm tief.

**Wo die 41 Einschmelzgewinde sitzen:** Querträger 16 (je 2 pro Ende) · untere Querträger 4 (von unten, fürs Grundbrett) · 90er-Scheibe 8 (Hebel 6, Messzeiger 2) · 72er-Scheibe 2 · Hebelnabe 1 · linke Wange 3 (Blockierstift 1, Stellschrauben 2) · rechte Wange 6 (Stellschrauben 2, Messuhrhalter 4) · Messuhrhalter 1.

## 4 Antrieb und Elektrik

| Pos. | Teil | Menge | ca. CHF | Status |
|---|---|---|---|---|
| 4.1 | Schrittmotor NEMA 17, 60 mm lang, ca. 0,7 Nm, 5-mm-Welle. Laut Link des Nutzers (25.10.) StepperOnline 17HS24-2104S: 76 Ncm, 2,1 A je Phase, 1,6 Ω, 3 mH, Welle Ø 5 mm mit D-Fläche, 4 fest angebrachte Leiter UL1007 AWG24 (ca. 0,2 mm²), 500 mm lang; Farben A+ schwarz, A− grün, B+ rot, B− blau (Motor-Typ am Aufdruck prüfen) | 1 | 12 | da |
| 4.2 | Treiber TMC2209 mit Kühlkörper (1 gebraucht, 1 Reserve) | 2 | 6 | im Warenkorb (2 Stück, Variante «TMC2209», blauer Kühlkörper laut Bildern, 2,23 CHF/Stück; Händler verkauft auch TMC2208/ATD5833, richtige Variante beim Eintreffen prüfen) |
| 4.3 | Arduino Uno mit CNC-Shield | 1 | – | da |
| 4.4 | Netzteil 24 V: **Mean Well LRS-350-24** (24 V, 14,6 A, 350 W, offenes Netzteil mit Schraubklemmen, Datenblatt `docs/LRS-350.pdf`). Ersetzt das Tischnetzteil; Umschalter 115/230 V auf 230 V, Ausgang auf 24,0 V einstellen | 1 | – | da (25.10.2026), Typenschild bestätigen |
| 4.5 | Adapter Hohlstecker auf Schraubklemmen | – | – | entfällt (Netzteil hat Schraubklemmen) |
| 4.6 | Motorkabel: Der Motor hat 4 fest angebrachte Kabel, an deren Enden kommen Dupont-Buchsenkontakte in ein 4-poliges Dupont-Gehäuse, das auf die Stiftleiste am Shield passt. Leiter AWG24 (ca. 0,2 mm²) passt in die Backe 24 AWG / 0,25 mm² der SN-58B und in die Dupont-Backe SN-2549 (0,08–1,0 mm²) | 1 | – | Dupont-Set und Zange SN-58B im Warenkorb |
| 4.7 | USB-Kabel zum Uno (USB-A auf USB-B) | 1 | 2 | da |
| 4.8 | Litze 1,00 mm² (Aufdruck: Huber+Suhner Radox 155), rot und schwarz, je 0,5 m (Netzteil → Shield) | 1 | – | da |
| 4.9 | PC mit GRBL-Sender oder Arduino-IDE | 1 | – | da |
| 4.10 | Einbaukaltgerätestecker C14 (Netzeingang) mit Flachsteckhülsen (6,3 mm, vollisoliert) | 1 | – | da (Hülsen aufgesteckt) |
| 4.11 | Feinsicherung 5 × 20 mm T 3,15 A 250 V (träge) mit Halter (F1) | 1 | – | da |
| 4.12 | Gabelkabelschuhe an Litze 1,00 mm² für die Netzteilklemmen (Schraubengrösse nachmessen) | 3 | – | da |
| 4.13 | Kfz-Flachsicherung 3 A (F2) mit Halter (mind. 32 V DC; Standard oder Mini klären) | 1 | – | da, Halter klären |
| 4.14 | Aderendhülsen 1,0 mm² für die Schraubklemmen am CNC-Shield (+24 V, GND) und passende Zange | 2 | 2–5 | klären (Opa fragen) |
| 4.15 | Kaltgerätekabel C13 (Netzkabel zum C14) | 1 | – | klären (Opa fragen) |
| 4.16 | Gehäuse und Schalter für die 230-V-Seite | 1 | – | klären (mit Opa; Schema nur Entwurf) |

Der Treiber läuft auf dem CNC-Shield an 24 V. Wie der Strom eingestellt wird, wird beim Aufbau dokumentiert; dafür braucht es das Multimeter (5.7).

## 5 Messmittel und Lasten

| Pos. | Teil | Wofür | ca. CHF | Status |
|---|---|---|---|---|
| 5.1 | Messuhr 0,01 mm, Schaft Ø 8 mm, Messweg 10 mm | Umkehrspiel, Steifigkeit, Haltetest | 12 mit Stativ | da (Messuhr, 25.10.) |
| 5.2 | Magnet- oder Tischstativ zur Messuhr | zweite Messstelle am Nabenbund (ohne Stativ bleibt eine Unsicherheit) | in 5.1 | da (gedruckter Messuhrhalter, Messuhr steht darauf; Nutzer 25.10.) |
| 5.3 | Koffer- oder Federwaage bis mindestens 10 kg | Wechsellast ±2 Nm; Gewichte abwiegen | 4 | da (Kofferwaage, 25.10.) |
| 5.4 | Küchenwaage | kleine Gewichte, Motorvermessung | – | da |
| 5.5 | Gewichte: 1,07 kg · 5,9 kg · 6,3 kg | Wechsellast, Haltetest, volles Moment – z. B. Wasserflaschen in einer Tragtasche, mit der Kofferwaage abgewogen | – | Haushalt |
| 5.6 | Schnur oder Schlaufe (trägt 10 kg) und ein Haken oder eine Schraube M8 für die Lastbohrung | Gewicht anhängen, Fangschnur | – | Haushalt |
| 5.7 | Multimeter | Treiberstrom einstellen, Wicklungswiderstand | 10–15 | da (Nutzer 25.10.) |
| 5.8 | Schieblehre | Ritzel nachmessen, Testdruck prüfen | 8–10 | da (Nutzer 25.10.) |
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

Stand 25.10.2026, nach Abgleich mit dem AliExpress-Warenkorb (Produktseiten gelesen):

| Teil | Menge | Stand |
|---|---|---|
| Ritzel HTD-3M 16 Z, 8 mm, 15 mm | 1 | im Warenkorb |
| M8 × 90 Teilgewinde, DIN 931 Edelstahl | 2 | im Warenkorb |
| Mutter M8 selbstsichernd (Flansch-Nylock) | 2 (5 im Paket) | im Warenkorb |
| TMC2209 mit Kühlkörper | 2 | im Warenkorb |
| Ritzel GT2 20 Z, Bohrung 5 mm, 10 mm breit, mit Nabe | 1 | im Warenkorb |
| **Ritzel HTD-5M 18 Z, Bohrung 8 mm glatt, 15 mm breit, mit Nabe** | 1 | im Warenkorb |
| Riemen GT2 10 × 200 / HTD-3M 15 × 252 / HTD-5M 15 × 525 | je 1 | im Warenkorb |
| Präzisionswelle 8 mm, 3 × 70 mm | 3 | da (vom Opa) |

Im Warenkorb, aber nicht in der Stückliste: Dupont-Set 310 Stück (2,90 CHF), Zange SN-58B (5,68 CHF; Produktbild: Backen für 0,25–1,5 mm² / AWG 24–16, crimpt offene Kontakte wie Dupont, Kfz-Stecker, Flachsteckhülsen und Ringschuhe; für Aderendhülsen vermutlich ungeeignet, dafür gibt es Zangen mit eckigen Backen), Wärme-Einsatzmuttern M3 × 4 × 5 (100 Stück, 3,54 CHF; alle 41 Einsätze des Prüfstands sind schon gesetzt, also Reserve für spätere Teile), iPhone-Hülle und AirPods-Hülle (nicht fürs Projekt).

Dazu kommt, was sich beim Nachsehen als fehlend herausstellt (Status *klären*): Motorkabel (Dupont-Set und SN-58B im Warenkorb), Aderendhülsen mit passender Zange (Opa fragen), Kaltgerätekabel C13, Zwingen, Werkzeug, Filament.
