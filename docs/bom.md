# Stückliste Kaufteile

Stand 11.10.2026, nach den Gutachten zu Antrieb und Steuerung. Die Preise sind Schätzungen, keine geprüften Angebote. **Noch nicht bestellen:** Die Prüfstand-Liste wird erst mit dem fertigen CAD der beiden Varianten verbindlich (Riemenlängen und Lagerzahl können sich dabei noch ändern).

Vorhanden und eingeplant: 3× NEMA 17 (17CS04A-170E, für J1, J3, J4), Arduino Uno + CNC-Shield + A4988, Netzteil 12 V / 4 A (für erste Versuche), Küchenwaage, Kleinteile.

## Prüfstand: Schultergelenk J2 in zwei Varianten

Beide Varianten werden gebaut und gegeneinander gemessen: S = Zahnriemen + Seiltrieb, R = nur Zahnriemen. Sie teilen sich Motor, Treiber, Netzteil, Achsen, Lager und Messmittel.

### Gemeinsame Teile

| Teil | Menge | AliExpress-Suchbegriff | ca. CHF |
|---|---|---|---|
| NEMA 17, 60 mm, ≥ 0,65 Nm, 5-mm-Welle (J2) | 1 | `Nema 17 stepper 60mm 65Ncm` | 12 |
| Netzteil 24 V, ≥ 6 A | 1 | `24V 6A power supply` | 15 |
| TMC2209-Treiber mit Kühlkörper | 1 | `TMC2209 V1.3 stepper driver` | 3 |
| GT2-Zahnriemenscheibe 20 Z, Bohrung 5 mm, für 10-mm-Riemen | 2 | `GT2 pulley 20 teeth bore 5mm width 10mm` | 3 |
| Präzisionswelle 8 mm × 100 mm | 4 | `linear shaft 8mm 100mm` | 8 |
| Rillenkugellager 608-2RS | 10 | `608 2RS bearing 10pcs` | 4 |
| Einschmelzgewinde M3 × 5 × 4, 100 Stk. | 1 | `M3 heat set insert brass 100pcs` | 4 |
| Schrauben-Sortiment M3 Innensechskant (falls nicht vorhanden) | 1 | `M3 hex socket screw assortment DIN912` | 6 |
| Messuhr 0,01 mm mit Magnetstativ | 1 | `dial indicator 0.01mm magnetic base` | 12 |
| Infrarot-Thermometer (Erwärmung Motor/Druckteile) | 1 | `infrared thermometer gun` | 7 |
| **Summe gemeinsam** | | | **~74** |

### Nur Variante S (Seiltrieb)

| Teil | Menge | AliExpress-Suchbegriff | ca. CHF |
|---|---|---|---|
| GT2-Riemen geschlossen, 10 mm breit, 300 mm | 2 | `GT2 closed loop belt 10mm 300mm` | 4 |
| Dyneema-Schnur 1,5 mm (UHMWPE), 10 m | 1 | `UHMWPE braided cord 1.5mm` | 4 |
| Dyneema-Schnur 2 mm, 10 m (Vergleich Steifigkeit) | 1 | `UHMWPE braided cord 2mm` | 3 |
| **Summe S** | | | **~11** |

Die AliExpress-Schnur wird vor dem Einbau 24 h vorgereckt. Echtes Dyneema SK78/DM20 aus dem Segel- oder Kletterhandel kriecht weniger und wäre die bessere Wahl, falls der Haltetest nicht besteht.

### Nur Variante R (nur Zahnriemen)

| Teil | Menge | AliExpress-Suchbegriff | ca. CHF |
|---|---|---|---|
| GT2-Riemen geschlossen, 10 mm breit, 200 mm | 2 | `GT2 closed loop belt 10mm 200mm` | 3 |
| HTD-3M-Scheibe 16 Z, Bohrung 8 mm, für 15-mm-Riemen | 1 | `HTD 3M pulley 16 teeth bore 8mm width 15mm` | 4 |
| HTD-3M-Riemen geschlossen, 15 mm breit, 252 mm | 1 | `HTD 3M 252 belt 15mm` | 3 |
| HTD-5M-Scheibe 18 Z, Bohrung 8 mm, für 15-mm-Riemen | 1 | `HTD 5M pulley 18 teeth bore 8mm width 15mm` | 5 |
| HTD-5M-Riemen geschlossen, 15 mm breit, 525 mm | 1 | `HTD 5M 525 belt 15mm` | 5 |
| **Summe R** | | | **~20** |

Die grossen Scheiben (72 Z, 64 Z, 90 Z und das 120-Z-Rad von Variante S) werden gedruckt.

**Prüfstand insgesamt: rund 105 CHF.**

Vor dem Bestellen: Wicklungswiderstand der vorhandenen Motoren messen (`docs/motorvermessung.md`). Zeigt er einen Motor für kleinen Strom, lohnt es sich, Ersatzmotoren gleich mitzubestellen.

## Ausbaustufe A – Rest für die Achsen J1–J3 (vorläufig)

| Teil | Menge | AliExpress-Suchbegriff | ca. CHF |
|---|---|---|---|
| BTT Octopus mit STM32F446 (v1.1 oder Pro) | 1 | `BTT Octopus V1.1 F446` | 45 |
| TMC2209 + Kühlkörper (alle 7 Achsen, für den Machbarkeitstest) | 6 weitere | wie oben | 18 |
| Lüfter 4010, 24 V | 1 | `4010 fan 24V` | 2 |
| Dünnringlager 6810-2RS (50 × 65 × 7) für J1 | 2 | `6810 2RS bearing` | 8 |
| Riemen, Ritzel, Welle für J1 und J3 | – | – | 10 |
| Zugfeder für Gewichtsausgleich J2 | 1 Satz | `extension spring assortment` | 4 |
| Endschalter (Mikroschalter mit Rolle) | 10 | `micro limit switch roller 10pcs` | 2 |
| Not-Aus-Taster, rastend, mit zwei Kontakten | 1 | `emergency stop button 22mm` | 3 |
| Litze 0,5 mm², Stecker JST-XH, Geflechtschlauch | – | `JST XH connector kit`, `braided cable sleeve 8mm` | 10 |
| **Summe Rest Stufe A** | | | **~102** |

Prüfstand und Rest zusammen: rund 210 CHF. Board und Treiber können früh bestellt werden, weil der Machbarkeitstest der Steuerung keine Mechanik braucht.

## Ausbaustufe B – Hand J4–J6 und Greifer (vorläufig)

| Teil | Menge | ca. CHF |
|---|---|---|
| NEMA 17, 34 mm (J5) | 1 | 9 |
| NEMA 14 (J6) | 1 | 9 |
| Lager, Riemen, Ritzel für die Hand | – | 15 |
| Servo für Greifer (MG996R oder DS3218) + 5-V-Wandler | 1 + 1 | 10 |
| Kabel, Stecker | – | 8 |
| **Summe Stufe B** | | **~51** |

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

Die Schiene läuft als siebte Achse auf dem Octopus; der Treiber dafür ist in Stufe A enthalten. Lange Führungen und Profile sind auf AliExpress teuer im Versand; das wird vor Stufe C geklärt.

## Gesamt

| | ca. CHF |
|---|---|
| Prüfstand | 105 |
| Rest Stufe A | 102 |
| Stufe B | 51 |
| Reserve 15 % | 40 |
| **Arm** | **~300** |
| Stufe C, Schiene | 115 |
| **Arm mit Schiene** | **~415** |

## Filament

- PLA: ca. 2–2,5 kg (Struktur und Verkleidung).
- PETG: ca. 0,5 kg (Motorplatten, Trommeln, Seilverankerungen, Teile am Motor).
