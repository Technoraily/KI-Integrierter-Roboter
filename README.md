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

Stand vom 11.10.2026 (Ende des ersten Arbeitstags). Der vollständige Plan steht in [docs/konzept.md](docs/konzept.md).

**Abgeschlossen**
- Phase 0 (Projektgerüst) und Phase 1 (Detailkonzept): Kinematik und [Lastrechnung](docs/lastrechnung.md) stehen, 13 Tests grün.
- Gutachten: Gesamtkonzept 8/10, Detailkonzept 8/10, Steuerung für 7 Achsen 8/10 (Protokolle in `docs/reviews/`).
- Entscheide: 1 kg Nutzlast im ganzen Arbeitsraum; Schiene als 7. Achse, koordiniert mit dem Arm; alle Achsen nur über Zahnriemen (GT2 und HTD), kein Seiltrieb; Steuerung BTT Octopus + grblHAL.
- Messhebel für die [Motorvermessung](docs/motorvermessung.md): `cad/export/stl/Messhebel.stl`.

**Nächster Schritt**
- Phase 2: Schultergelenk J2 als Prüfstand in Fusion 360 konstruieren (drei Riemenstufen: GT2 20:72, HTD-3M 16:64, HTD-5M 18:90; Auslegung in `docs/konzept.md` 3.2 und `docs/parameter.md`), dann begutachten lassen und die Riemen-/Scheiben-/Wellenliste verbindlich machen.
- In Fusion existieren aus einem verworfenen Ansatz zwei Seitenwangen für das Seiltrieb-Layout; sie werden für das Riemen-Layout neu aufgebaut.

**Beschaffung für den Schulter-Test**
- Vorhanden bzw. bestellt: NEMA 17 mit 60 mm (ca. 0,7 Nm), Netzteil 24 V / 100 W mit Hohlstecker 5,5 × 2,5 mm, Delock-Adapter auf Schraubklemmen, M3-Schrauben; ausgewählt: Kugellager 608ZZ, Einschmelzgewinde M3 × 4 × 5.
- Noch offen: 2× TMC2209, Messuhr (Thermometer ist verzichtbar), Motorkabel prüfen. Riemen, Scheiben und 8-mm-Wellen erst nach dem CAD.
- Offene Rückfragen an den Nutzer: Wicklungswiderstand der drei vorhandenen Motoren (17CS04A-170E); Schultermotor mit Doppelwelle (-SZ) oder normal; Multimeter und Lötkolben vorhanden?

## Aufbau des Repos

| Ordner | Inhalt |
|---|---|
| `docs/` | Anforderungen, Konzept, Parameter, Lastrechnung, Stückliste, Bauanleitung, Prüfprotokolle |
| `cad/` | Exporte aus Fusion 360 (STL, STEP) und Renderings für die Anleitung |
| `firmware/` | Konfiguration für grblHAL |
| `software/` | Python-Paket für Kinematik, Simulation und Steuerung |

## Arbeitsweise

- Konstruiert wird in Fusion 360 auf dem lokalen PC; ins Repo kommen nur Exporte und Renderings.
- Jede Idee und jede Baugruppe wird von einem unabhängigen Gutachter mit 1–10 bewertet (höchstens 3 Runden). Die Protokolle liegen in `docs/reviews/`.
- Die Dokumentation wächst in jeder Phase mit.
