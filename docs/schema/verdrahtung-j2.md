# Verdrahtungsliste J2-Prüfstand (Entwurf, Stand 25.10.2026)

Grundlage für das KiCad-Schema (Lernen) und den QElectroTech-Plan (Opa). Beide müssen mit dieser Liste übereinstimmen.

**Farben 24-V-Seite:** rot = +24 V, schwarz = 0 V. Litze 1,00 mm² (Aufdruck: Huber+Suhner Radox 155 1.00mm2). Anschlüsse: am Netzteil Gabelkabelschuhe unter die Klemmschrauben (fest anziehen, Schraubengrösse nachmessen), am C14 vollisolierte Flachsteckhülsen 6,3 mm aufstecken (nichts anschrauben), am CNC-Shield Aderendhülsen 1,0 mm² in die Schraubklemmen.

## Bauteile (Kennzeichen)

| Kz. | Teil | Daten | Status |
|---|---|---|---|
| T1 | Schaltnetzteil Mean Well LRS-350-24 (Datenblatt `docs/LRS-350.pdf`) | 24 V, 14,6 A, 350 W; Ausgang einstellbar 21,6–28,8 V; Eingang 180–264 V AC (Umschalter auf 230 V); Eingangsstrom 3,4 A bei Volllast; Einschaltstrom 60 A; Ableitstrom < 2 mA (Schutzleiter Pflicht) | da, Typenschild bestätigen (-24?) |
| F1 | Feinsicherung 5 × 20 mm, T 3,15 A, 250 V (träge) mit Halter | 230-V-Seite, Netzleiter L | da |
| X1 | Einbaukaltgerätestecker (Netzeingang) | L, N, PE | da |
| F2 | Kfz-Flachsicherung 3 A im Halter (≥ 32 V DC) | 24-V-Seite, in +24 V (rot) | da, Halter klären (Standard oder Mini) |
| A1 | Arduino Uno | Strom über USB | da |
| A2 | CNC-Shield V3 (auf A1) | Motorspannung an Schraubklemme | da |
| U1 | Treiber TMC2209 im X-Steckplatz | Strom über Vref einstellen | offen (bestellen) |
| M1 | Schrittmotor NEMA 17, 60 mm | 4 Drähte, 2 Spulen | da |
| X2 | USB-A auf USB-B | A1 ↔ PC | da |

## Leitungen 24-V-Seite und Motor

| Nr. | Von | Nach | Farbe / Querschnitt | Bemerkung |
|---|---|---|---|---|
| W1 | T1 Klemme +V | F2 Eingang | rot 1,00 mm² | möglichst kurz |
| W2 | F2 Ausgang | A2 Klemme +24 V (VIN) | rot 1,00 mm² | |
| W3 | T1 Klemme −V | A2 Klemme GND | schwarz 1,00 mm² | nicht gesichert |
| W4 | A2 X-Stiftleiste (1B, 1A, 2A, 2B) | M1 (Spule A / Spule B) | Motorkabel 4-polig | Spulen laut Hersteller: A = schwarz (A+) + grün (A−), B = rot (B+) + blau (B−); mit Multimeter prüfen (je Spule ca. 1,6 Ω, zwischen den Spulen unendlich). Reihenfolge an der Stiftleiste 1B, 1A, 2A, 2B: Spule A auf 1B/1A, Spule B auf 2A/2B. Vertauschen innerhalb einer Spule kehrt nur die Drehrichtung um. Nie unter Spannung ein- oder ausstecken |
| W5 | X2 | A1 USB-B-Buchse | USB-Kabel | Logik und PC-Verbindung |

## Leitungen 230-V-Seite (nur Entwurf, Opa prüft und gibt frei)

| Nr. | Von | Nach | Bemerkung |
|---|---|---|---|
| W10 | X1 L | F1 | Leiterfarbe nach Vorgabe Opa |
| W11 | F1 | T1 Klemme L | |
| W12 | X1 N | T1 Klemme N | |
| W13 | X1 PE | T1 Schutzleiter-/Erdklemme (FG) | Gabelkabelschuh; Opa entscheidet, ob für den Schutzleiter ein geschlossener Ringschuh nötig ist |

Klemmen T1 laut Datenblatt (Case 207A): 1 = AC/L, 2 = AC/N, 3 = FG (Schutzleiter), 4–6 = −V, 7–9 = +V (je drei Klemmen parallel).
Hinweise: Der Lüfter läuft erst ab ca. 50 °C Gehäusetemperatur. Bei Überlast schaltet das Netzteil im «Hiccup»-Modus und erholt sich selbst. Vor dem Anschluss des Shields die Ausgangsspannung mit dem Multimeter auf 24,0 V einstellen (Poti «V ADJ», Bereich bis 28,8 V). Der TMC2209 verträgt höchstens ca. 28 V, nicht höher drehen.

Offen: Schalter vor F1 (ja/nein), Umschalter 115/230 V am Netzteil auf 230 V, Klemmenbeschriftung nach Typenschild, Einbau in Gehäuse (berührungssicher).

## Offene Fragen
1. Typenschild T1 bestätigt LRS-350-24? (PDF gilt für die ganze Serie.) F1 T 3,15 A genügt für den Prüfstand (Last ca. 30 W); bei Volllast zieht das Netzteil 3,4 A, für den ganzen Roboterarm wäre F1 zu klein. Einschaltstrom 60 A: Opa beurteilt, ob T 3,15 A dafür passt.
2. Halter F2: Standard (ATO, 19 mm) oder Mini (ATM, 11 mm). Aderendhülsen und Kaltgerätekabel C13: vorhanden? (Opa fragen)
3. Schalter und Gehäuse für die 230-V-Seite: Entscheid mit Opa.
4. Vref und Mikroschritt-Jumper des TMC2209 beim Aufbau festlegen und hier eintragen.
