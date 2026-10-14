# Stückliste Kaufteile

Stand 12.10.2026. Die Preise sind Schätzungen, keine geprüften Angebote. **Die Prüfstand-Liste ist verbindlich:** Das CAD des Schultergelenks ist begutachtet (8/10, `docs/reviews/2026-10-12-pruefstand-j2.md`); Zähnezahlen, Riemenlängen, Bohrungen und Stückzahlen stehen fest. Die vollständige Teileliste mit allen Schraubenlängen steht in `docs/pruefstand-j2.md`.

Zu jeder Baugruppe gibt es eine vollständige Stückliste in `docs/stuecklisten/` (alle Teile, nicht nur Kaufteile). Dieses Dokument ist die Kostenübersicht über das ganze Projekt.

Vorhanden und eingeplant: 3× NEMA 17 (17CS04A-170E, für J1, J3, J4), Arduino Uno + CNC-Shield + A4988, Netzteil 12 V / 4 A (für erste Versuche), Küchenwaage, Kleinteile.

## Was jetzt bestellt werden kann und was nicht

Massgebend für «jetzt»: Das Teil hängt nicht vom CAD ab und wird für den Schulter-Test oder den Steuerungstest gebraucht. Diese Liste geht den Tabellen weiter unten vor, wo sie abweicht (grösseres Netzteil, Reserve bei Treibern und Lagern).

**Jetzt bestellen – für den Schulter-Test (ca. 100 CHF):**

| Teil | Menge | ca. CHF |
|---|---|---|
| NEMA 17, 60 mm, ≥ 0,65 Nm, 1,5–2,0 A, 5-mm-Welle | 1 | 12 |
| Tischnetzteil 24 V, 10 A, geschlossen + Adapter Hohlstecker auf Schraubklemmen | 1 | 23 |
| TMC2209 mit Kühlkörper | 10 (7 gebraucht, 3 Reserve) | 30 |
| Rillenkugellager 608-2RS | 20 | 8 |
| Einschmelzgewinde M3, 100 Stk. | 1 | 4 |
| Schrauben-Sortiment M3 Innensechskant | 1 | 6 |
| Messuhr 0,01 mm mit Magnetstativ | 1 | 12 |
| Infrarot-Thermometer | 1 | 7 |

**Jetzt sinnvoll mitzubestellen – für den Steuerungstest, braucht keine Mechanik (ca. 70 CHF):**

| Teil | Menge | ca. CHF |
|---|---|---|
| BTT Octopus mit **STM32F446** (nicht H723) | 1 | 45 |
| USB-C-Kabel | 1 | 3 |
| NEMA 17, 40 mm, ca. 0,4 Nm (später Schiene; bis dahin vierter Testmotor und Ersatz) | 1 | 10 |
| Lüfter 4010, 24 V | 1 | 2 |
| Not-Aus-Taster, rastend, zwei Kontakte | 1 | 3 |
| Endschalter mit Rolle | 10 | 2 |
| Sicherungshalter mit 10-A-Sicherung | 1 | 2 |

**Jetzt bestellen – Riemen, Scheiben und Kleinteile des Prüfstands (ca. 35 CHF, Tabellen unten):** Die Ritzel kommen zuerst an die Reihe: Sie werden nach der Lieferung nachgemessen, erst dann werden die gedruckten Scheiben gedruckt.

**Warten:**

| Teil | Warum warten |
|---|---|
| Riemen, Scheiben und Wellen für J1 und J3 | erst nach dem Prüfstand-Ergebnis und dem CAD dieser Baugruppen |
| Dünnringlager 6810, Zugfeder | Basis und Gewichtsausgleich sind noch nicht konstruiert |
| Motoren für J5 und J6 | erst Stufe B; die Hand kann sich nach dem Schulter-Test noch ändern |
| Greifer-Servo, 5-V-Wandler | Stufe B |
| Kabel, Stecker, Crimpzange, Geflechtschlauch | erst beim Zusammenbau von Stufe A nötig; Längen dann bekannt |
| Schiene (Führungen, Profile, Schleppkette) | Stufe C; Bezugsquelle für die langen Teile ist noch offen |

## Prüfstand: Schultergelenk J2 (drei Riemenstufen)

Der Prüfstand ist das spätere Schultergelenk in Originalgrösse; alle Teile ausser Messuhr und Thermometer werden im Arm weiterverwendet.

**Die vollständige Stückliste mit jedem Druckteil, jeder Schraube, Elektrik, Messmitteln, Werkzeug und Verbrauchsmaterial steht in [stuecklisten/pruefstand-j2.md](stuecklisten/pruefstand-j2.md).** Die Tabellen hier zeigen nur die Kaufteile mit Preisen.

### Motor, Elektrik, Lager, Messmittel

| Teil | Menge | AliExpress-Suchbegriff | ca. CHF |
|---|---|---|---|
| NEMA 17, 60 mm, ≥ 0,65 Nm, 5-mm-Welle (J2) | 1 | `Nema 17 stepper 60mm 65Ncm` | 12 |
| Netzteil 24 V, ≥ 6 A | 1 | `24V 6A power supply` | 15 |
| TMC2209-Treiber mit Kühlkörper | 1 | `TMC2209 V1.3 stepper driver` | 3 |
| GT2-Zahnriemenscheibe 20 Z, Bohrung 5 mm, für 10-mm-Riemen (1 gebraucht, 1 Reserve) | 2 | `GT2 pulley 20 teeth bore 5mm width 10mm` | 3 |
| Präzisionswelle 8 mm × 100 mm (3 gebraucht, auf 70 mm ablängen und anfeilen; 1 Reserve) | 4 | `linear shaft 8mm 100mm` | 8 |
| Sechskantschraube M8 × 90 mit Schaft, selbstsichernde Mutter, 2 Scheiben (Baumarkt) | 2 | – | 3 |
| Schrauben M4 × 16 Innensechskant (Gewinde am 5M-Ritzel prüfen: M4 oder M5) | 2 | – | 1 |
| Schrauben M3 × 30 Innensechskant, falls nicht im Sortiment | 2 | – | 1 |
| Koffer- oder Federwaage bis mindestens 10 kg (Wechsellast, Gewichte abwiegen) | 1 | `luggage scale` | 4 |
| Brett 220 × 200 × 12 mm (Sperrholz oder MDF), 2 Schraubzwingen | 1 | – | vorhanden / Baumarkt |
| Rillenkugellager 608-2RS (10 gebraucht: 6 Wellenlager, 4 in den Spannrollen) | 10 | `608 2RS bearing 10pcs` | 4 |
| Einschmelzgewinde M3 × 5 × 4, 100 Stk. (41 gebraucht) | 1 | `M3 heat set insert brass 100pcs` | 4 |
| Schrauben-Sortiment M3 Innensechskant (falls nicht vorhanden) | 1 | `M3 hex socket screw assortment DIN912` | 6 |
| Messuhr 0,01 mm mit Magnetstativ | 1 | `dial indicator 0.01mm magnetic base` | 12 |
| Infrarot-Thermometer (Erwärmung Motor/Druckteile) | 1 | `infrared thermometer gun` | 7 |
| **Zwischensumme** | | | **~83** |

### Riemen und Scheiben

| Teil | Menge | AliExpress-Suchbegriff | ca. CHF |
|---|---|---|---|
| GT2-Riemen geschlossen, 10 mm breit, 200 mm (1 gebraucht, 1 Reserve) | 2 | `GT2 closed loop belt 10mm 200mm` | 3 |
| HTD-3M-Scheibe 16 Z, Bohrung 8 mm, für 15-mm-Riemen, mit Bordscheiben | 1 | `HTD 3M pulley 16 teeth bore 8mm width 15mm` | 4 |
| HTD-3M-Riemen geschlossen, 15 mm breit, 252 mm | 1 | `HTD 3M 252 belt 15mm` | 3 |
| HTD-5M-Scheibe 18 Z, Bohrung 8 mm, für 15-mm-Riemen, mit Bordscheiben und Nabe (2 Gewindestifte) | 1 | `HTD 5M pulley 18 teeth bore 8mm width 15mm` | 5 |
| HTD-5M-Riemen geschlossen, 15 mm breit, 525 mm | 1 | `HTD 5M 525 belt 15mm` | 5 |
| **Zwischensumme** | | | **~20** |

Die grossen Scheiben (72 Z, 64 Z, 90 Z) werden gedruckt.

**Prüfstand insgesamt: rund 105 CHF.** Filament für die 22 Druckteile: rund 1,1 Liter Vollvolumen, mit üblicher Füllung grob 0,5–0,7 kg.

Vor dem Bestellen: Wicklungswiderstand der vorhandenen Motoren messen (`docs/motorvermessung.md`). Zeigt er einen Motor für kleinen Strom, lohnt es sich, Ersatzmotoren gleich mitzubestellen.

## Ausbaustufe A – Rest für die Achsen J1–J3 (vorläufig)

| Teil | Menge | AliExpress-Suchbegriff | ca. CHF |
|---|---|---|---|
| BTT Octopus mit STM32F446 (v1.1 oder Pro) | 1 | `BTT Octopus V1.1 F446` | 45 |
| TMC2209 + Kühlkörper (alle 7 Achsen, für den Machbarkeitstest) | 6 weitere | wie oben | 18 |
| Lüfter 4010, 24 V | 1 | `4010 fan 24V` | 2 |
| Dünnringlager 6810-2RS (50 × 65 × 7) für J1 | 2 | `6810 2RS bearing` | 8 |
| Riemen (GT2, HTD-3M, HTD-5M), Aluscheiben, Wellen für J1 und J3 | – | – | 20 |
| Zugfeder für Gewichtsausgleich J2 – **nur bei Bedarf** (Konzept 3.8), erst nach dem Prüfstand bestellen | 1 Satz | `extension spring assortment` | 4 |
| Endschalter (Mikroschalter mit Rolle) | 10 | `micro limit switch roller 10pcs` | 2 |
| Not-Aus-Taster, rastend, mit zwei Kontakten | 1 | `emergency stop button 22mm` | 3 |
| Litze 0,5 mm², Stecker JST-XH, Geflechtschlauch | – | `JST XH connector kit`, `braided cable sleeve 8mm` | 10 |
| **Summe Rest Stufe A** | | | **~112** |

Prüfstand und Rest zusammen: rund 215 CHF. Board und Treiber können früh bestellt werden, weil der Machbarkeitstest der Steuerung keine Mechanik braucht.

## Ausbaustufe B – Hand J4–J6 und Greifer (vorläufig)

| Teil | Menge | ca. CHF |
|---|---|---|
| NEMA 17, 34 mm (J5) | 1 | 9 |
| NEMA 14 (J6) | 1 | 9 |
| Lager, Riemen (GT2, HTD-3M), Aluscheiben für J4–J6 | – | 29 |
| Servo für Greifer (MG996R oder DS3218) + 5-V-Wandler | 1 + 1 | 10 |
| Kabel, Stecker | – | 8 |
| **Summe Stufe B** | | **~65** |

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
| Rest Stufe A | 112 |
| Stufe B | 65 |
| Reserve 15 % | 40 |
| **Arm** | **~320** |
| Stufe C, Schiene | 115 |
| **Arm mit Schiene** | **~435** |

## Filament

- PLA: ca. 2–2,5 kg (Struktur und Verkleidung).
- PETG: ca. 0,5 kg (Motorplatten, Riemenscheiben, Teile am Motor).
