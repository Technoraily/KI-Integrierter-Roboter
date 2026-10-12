# KI-integrierter Roboterarm

Selbst konstruierter 6-Achs-Desktop-Roboterarm: 3D-gedruckt (PLA/PETG, BambuLab A1), NEMA-17-Schrittmotoren, Standardteile von AliExpress. Später mit Kamera-KI und automatischem Greiferwechsel.

## Eckdaten (Ziel)

| | |
|---|---|
| Achsen | 6 (Knickarm mit Zentralhand) + Schiene als 7. Achse, koordiniert |
| Reichweite | 450 mm (Schulter → Flansch) |
| Nutzlast | 1 kg im ganzen Arbeitsraum |
| Wiederholgenauigkeit | ≤ ±0,5 mm (unidirektional, nach Referenzfahrt, bei gleichbleibender Last) |
| Steuerung | BTT Octopus (STM32F446) + grblHAL, 7 synchrone Achsen, TMC2209, 24 V |
| Software | Python auf dem PC (Kinematik, Bahnplanung, später Kamera/KI) |

![Aufbau und Antriebe](docs/bilder/uebersicht.png)

Der Arm steht später auf einer angetriebenen Schiene mit 1000 mm Verfahrweg (Stufe C).

## Stand

Stand vom 12.10.2026. Der vollständige Plan steht in [docs/konzept.md](docs/konzept.md).

**Abgeschlossen**
- Phase 0 (Projektgerüst) und Phase 1 (Detailkonzept): Kinematik und [Lastrechnung](docs/lastrechnung.md) stehen, 13 Tests grün.
- Gutachten: Gesamtkonzept 8/10, Detailkonzept 8/10, Steuerung für 7 Achsen 8/10 (Protokolle in `docs/reviews/`).
- Entscheide: 1 kg Nutzlast im ganzen Arbeitsraum; Schiene als 7. Achse, koordiniert mit dem Arm; alle Achsen nur über Zahnriemen (GT2 und HTD), kein Seiltrieb; Steuerung BTT Octopus + grblHAL.
- Messhebel für die [Motorvermessung](docs/motorvermessung.md): `cad/export/stl/Messhebel.stl`.
- **CAD des Prüfstands für das Schultergelenk J2** ([Beschreibung](docs/pruefstand-j2.md)): drei Riemenstufen in zwei Ebenen, Spannrollen, Lasthebel, Messzeiger und Messuhrhalter. Gutachten nach drei Runden 8/10 (`docs/reviews/2026-10-12-pruefstand-j2.md`). Exporte in `cad/export/`, die Geometrie entsteht aus `cad/skripte/j2_pruefstand.py`.

![Prüfstand J2](cad/renders/J2_Pruefstand_Riementrieb.png)

**Nächster Schritt**
1. Ritzel, Riemen und Kleinteile des Prüfstands bestellen (`docs/bom.md`).
2. Motoren vermessen (`docs/motorvermessung.md`) – geht schon mit den vorhandenen Teilen.
3. Toleranz-Testdruck: Lagersitz, Einschmelzgewinde, Nabenbohrungen, je ein Zahnsegment der drei Riemenprofile.
4. Gelieferte Ritzel nachmessen, Masse im Skript anpassen, dann die Scheiben und den Rest drucken und den Prüfstand aufbauen.

**Beschaffung für den Schulter-Test**
- Vorhanden bzw. bestellt: NEMA 17 mit 60 mm (ca. 0,7 Nm), Netzteil 24 V / 100 W mit Hohlstecker 5,5 × 2,5 mm, Delock-Adapter auf Schraubklemmen, M3-Schrauben; ausgewählt: Kugellager 608ZZ, Einschmelzgewinde M3 × 4 × 5.
- Noch offen: 2× TMC2209, Messuhr (Thermometer ist verzichtbar), Motorkabel prüfen; dazu jetzt Riemen, Ritzel, 8-mm-Wellen, 2× M8 × 90, Kofferwaage.
- Offene Rückfragen an den Nutzer: Wicklungswiderstand der drei vorhandenen Motoren (17CS04A-170E); Schultermotor mit Doppelwelle (-SZ) oder normal; Multimeter und Lötkolben vorhanden? Sind Schrauben M3 × 16, × 25 und × 30 im Sortiment?
- In Fusion sind der verworfene Seiltrieb-Rahmen (`ALT_Rahmen_Seiltrieb`) und der Messhebel nur ausgeblendet.

## Aufbau des Repos

| Ordner | Inhalt |
|---|---|
| `docs/` | Anforderungen, Konzept, Parameter, Lastrechnung, Stückliste, Bauanleitung, Prüfprotokolle |
| `cad/` | Exporte aus Fusion 360 (STL, STEP), Renderings für die Anleitung, Skripte, die Baugruppen in Fusion aufbauen |
| `firmware/` | Konfiguration für grblHAL |
| `software/` | Python-Paket für Kinematik, Simulation und Steuerung |

## Arbeitsweise

- Konstruiert wird in Fusion 360 auf dem lokalen PC; ins Repo kommen nur Exporte und Renderings.
- Jede Idee und jede Baugruppe wird von einem unabhängigen Gutachter mit 1–10 bewertet (höchstens 3 Runden). Die Protokolle liegen in `docs/reviews/`.
- Die Dokumentation wächst in jeder Phase mit.
