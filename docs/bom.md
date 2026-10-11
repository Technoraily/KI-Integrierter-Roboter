# Stückliste Kaufteile

Stand 11.10.2026, nach Gutachten Phase 1. Die Preise sind Schätzungen, keine geprüften Angebote. Bestellbar ist die Liste «Prüfstand»; die Stufen A und B sind vorläufig, weil ihre Mechanik vom Ergebnis des Prüfstands abhängt.

Vorhanden und eingeplant: 3× NEMA 17 (17CS04A-170E, für J1, J3, J4), Arduino Uno + CNC-Shield + A4988, Netzteil 12 V / 4 A (für erste Versuche), Küchenwaage, Kleinteile.

## Prüfstand: J2-Modul in Variante (a) Capstan

Der Prüfstand ist das spätere Schultergelenk im Massstab 1:1. Alle Teile ausser Messuhr und Thermometer werden im Arm weiterverwendet.

| Teil | Menge | AliExpress-Suchbegriff | ca. CHF |
|---|---|---|---|
| NEMA 17, 60 mm, ≥ 0,65 Nm, 5-mm-Welle (J2) | 1 | `Nema 17 stepper 60mm 65Ncm` | 12 |
| Netzteil 24 V, ≥ 6 A | 1 | `24V 6A power supply` | 15 |
| TMC2209-Treiber mit Kühlkörper | 1 | `TMC2209 V1.3 stepper driver` | 3 |
| GT2-Zahnriemenscheibe 16 Z, Bohrung 5 mm, für 10-mm-Riemen | 2 | `GT2 pulley 16 teeth bore 5mm width 10mm` | 3 |
| GT2-Riemen geschlossen, 10 mm breit, 280 mm | 2 | `GT2 closed loop belt 10mm 280mm` | 4 |
| GT2-Riemen geschlossen, 10 mm breit, 300 mm (Reserve für Achsabstand) | 1 | `GT2 closed loop belt 10mm 300mm` | 2 |
| Dyneema-Schnur 1,5 mm (UHMWPE), 10 m | 1 | `UHMWPE braided cord 1.5mm` | 4 |
| Dyneema-Schnur 2 mm, 10 m (Vergleich Steifigkeit) | 1 | `UHMWPE braided cord 2mm` | 3 |
| Präzisionswelle 8 mm × 100 mm | 2 | `linear shaft 8mm 100mm` | 4 |
| Rillenkugellager 608-2RS | 10 | `608 2RS bearing 10pcs` | 4 |
| Einschmelzgewinde M3 × 5 × 4, 100 Stk. | 1 | `M3 heat set insert brass 100pcs` | 4 |
| Schrauben-Sortiment M3 Innensechskant (falls nicht vorhanden) | 1 | `M3 hex socket screw assortment DIN912` | 6 |
| Messuhr 0,01 mm mit Magnetstativ | 1 | `dial indicator 0.01mm magnetic base` | 12 |
| Infrarot-Thermometer (Erwärmung Motor/Druckteile) | 1 | `infrared thermometer gun` | 7 |
| **Summe Prüfstand** | | | **~83** |

Zum Riemen: Für 16 Z → 96 Z ergibt 280 mm einen Achsabstand von rund 80 mm. Kürzere Riemen (158/200 mm) gehen geometrisch nicht. 10 mm Breite, weil die Trumkraft bei vollem Motormoment bis ca. 130 N erreicht. Gespannt wird über Langlöcher am Motor, eine Spannrolle braucht es nicht.

Vor dem Bestellen: Wicklungswiderstand der vorhandenen Motoren messen (`docs/motorvermessung.md`). Zeigt er einen Motor für kleinen Strom, lohnt es sich, Ersatzmotoren gleich mitzubestellen.

Varianten (b) Zykloid und (c) HTD-Riemen werden nur bestellt, falls (a) das Gate nicht besteht. Dann kämen dazu: für (b) Exzenterlager, Rollen und Stifte, für (c) HTD-3M-Riemen 15 mm mit Scheiben.

## Ausbaustufe A – Rest für die Achsen J1–J3 (vorläufig)

| Teil | Menge | AliExpress-Suchbegriff | ca. CHF |
|---|---|---|---|
| BTT Octopus mit STM32F446 (v1.1 oder Pro) | 1 | `BTT Octopus V1.1 F446` | 45 |
| TMC2209 + Kühlkörper | 2 weitere | wie oben | 6 |
| Lüfter 4010, 24 V | 1 | `4010 fan 24V` | 2 |
| Dünnringlager 6810-2RS (50 × 65 × 7) für J1 | 2 | `6810 2RS bearing` | 8 |
| Riemen, Ritzel, Welle für J1 und J3 | – | – | 10 |
| Zugfeder für Gewichtsausgleich J2 | 1 Satz | `extension spring assortment` | 4 |
| Endschalter (Mikroschalter mit Rolle) | 6 | `micro limit switch roller 10pcs` | 2 |
| Not-Aus-Taster, rastend | 1 | `emergency stop button 22mm` | 3 |
| Litze 0,5 mm², Stecker JST-XH, Geflechtschlauch | – | `JST XH connector kit`, `braided cable sleeve 8mm` | 10 |
| **Summe Rest Stufe A** | | | **~90** |

Prüfstand und Rest zusammen: rund 175 CHF. Das Board ist teurer als zuvor geplant, weil es 7 synchrone Achsen können muss.

## Ausbaustufe B – Hand J4–J6 und Greifer (vorläufig)

| Teil | Menge | ca. CHF |
|---|---|---|
| NEMA 17, 34 mm (J5) | 1 | 9 |
| NEMA 14 (J6) | 1 | 9 |
| TMC2209 | 3 | 9 |
| Lager, Riemen, Ritzel für die Hand | – | 15 |
| Servo für Greifer (MG996R oder DS3218) + 5-V-Wandler | 1 + 1 | 10 |
| Kabel, Stecker | – | 8 |
| **Summe Stufe B** | | **~60** |

## Ausbaustufe C – Schiene J0, 1000 mm Verfahrweg (Grobschätzung)

| Teil | Menge | ca. CHF |
|---|---|---|
| Linearführung MGN12 mit Wagen MGN12H, 1250 mm (oder gestossen) | 2 + 4 Wagen | 50 |
| Aluprofil 2040, 1250 mm | 2 | 30 |
| NEMA 17, 40 mm | 1 | 10 |
| GT2-Riemen offen 10 mm, 3 m, mit Ritzel und Umlenkrolle | 1 Satz | 8 |
| Schleppkette 10 × 15 mm, 1 m | 1 | 6 |
| Endschalter, Winkel, Nutensteine, Schrauben | – | 10 |
| **Summe Stufe C** | | **~115** |

Die Schiene läuft als siebte Achse auf dem Octopus; dazu kommt ein TMC2209 (~3 CHF). Lange Führungen und Profile sind auf AliExpress teuer im Versand; das wird vor Stufe C geklärt.

## Filament

- PLA: ca. 2–2,5 kg (Struktur und Verkleidung).
- PETG: ca. 0,5 kg (Motorplatten, Trommeln, Seilverankerungen, Teile am Motor).
