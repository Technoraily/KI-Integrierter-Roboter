# Druckeinstellungen Basis J1

Stand 26.11.2026, Bauraummodell V2.2 (`cad/skripte/basis_j1.py`). Die STL-Dateien liegen **so, wie das Teil im Arm sitzt**. Wo «umdrehen» steht, das Teil im Slicer um 180° kippen («Auf Fläche legen»).

Gemeinsam: BambuLab A1, Düse 0,4 mm, Basis «0.20mm Standard @BBL A1», Schichthöhe 0,20 mm, texturiertes PEI, kein Brim, **keine Stützen** (ausser wo angegeben).

## Jetzt druckbar (hängt nicht von der 6810-Passprobe ab)

| Datei | Menge | Material | Wände | oben / unten | Infill | Lage auf dem Bett | Nacharbeit |
|---|---|---|---|---|---|---|---|
| `Passprobe_6810_Sitz_Magnet.stl` | 1 | PLA grau | 4 | 5 / 4 | 15 % Gyroid | wie exportiert (Bund unten) | – |
| `Passprobe_6810_Zapfen.stl` | 1 | PLA grau | 4 | 5 / 4 | 15 % Gyroid | wie exportiert (Fuss unten) | **zuerst** 3 Einschmelzgewinde oben setzen |
| `Spannring_fuer_Probe.stl` | 1 | PLA grau | 4 | 5 / 5 | 100 % | **umdrehen** (Nut oben) | O-Ring OD 53 × 1,5 einlegen |
| `Motorkasten.stl` | 1 | PLA grau | 3 | 4 / 4 | 15 % Gyroid | wie exportiert (Boden unten) | 4 Einschmelzgewinde in den Auflagen, 4 Magnete oben |
| `Motorplatte.stl` | 1 | **PETG weiss** | 4 | 5 / 5 | 40 % Gyroid | flach | – |
| `Sockelgehaeuse_links.stl`, `_rechts.stl` | je 1 | PLA grau | 3 | 4 / 4 | 15 % Gyroid | **umdrehen** (Deckel unten) | Magnete, 1 Zylinderstift 3 × 12 je Hälfte einkleben |
| `Farbring_J1_links.stl`, `_rechts.stl` | je 1 | PLA rot | 3 | 4 / 4 | 15 % Gyroid | wie exportiert (Magnettaschen unten) | Magnete |
| `Kastenkappe.stl` | 1 | PLA weiss | 3 | 4 / 4 | 15 % Gyroid | wie exportiert (Rand unten) | Magnete |
| `Bock_unten.stl` | 1 | PLA grau | 5 | 5 / 5 | 40 % Gyroid | wie exportiert (Laschen unten) | 3 Einschmelzgewinde, unteres 608 einpressen |
| `Bock_Deckel.stl` | 1 | PLA grau | 5 | 5 / 5 | 40 % Gyroid | **umdrehen** (Lagersitz oben) | oberes 608 einpressen |
| `Distanzring_unten.stl`, `_oben.stl` | je 1 | PLA grau | 3 | – | 100 % | flach | – |
| `Scheibe_GT2_80Z.stl` | 1 | PLA grau | 4 | 5 / 5 | 40 % Gyroid | **umdrehen** (obere Bordscheibe unten, Nabe oben) | 2 Einschmelzgewinde radial |

**Magnete:** Sekundenkleber in die Tasche, **Polung mit dem Gegenstück prüfen** (müssen sich anziehen).

## Erst nach der Passprobe 6810 (folgen als STL)

- `Grundplatte` (Lagerzapfen Ø 49,9)
- `Nabe_Drehteller` (Lagersitze Ø 65,2)
- `Spannring` (für den Arm, gleich wie die Probe)

## Erst nach dem Ausmessen des gekauften KW11

- `Schalterhalter`

## Passprobe: was prüfen und melden

1. **Ring (Ø 65,2):** Das 6810 von oben bis auf den Bund drücken. Fällt es hinein, geht es von Hand mit Druck (so soll es sein), oder klemmt es?
2. **Zapfen (Ø 49,9):** Nach dem Setzen der Einsätze das 6810 aufschieben. Ist es lose oder kippelt es, ist es leicht schiebbar ohne Spiel (so soll es sein), oder klemmt es? Hat sich der Zapfen ausgebeult?
3. **Spannring:** Mit O-Ring und 3 × M3 × 10 bis auf Block anziehen. Dreht das Lager danach noch leicht, aber ohne Spiel?
4. **Magnete:** Fallen sie heraus, halten sie ohne Kleber, oder passen sie nicht hinein?
5. Wenn möglich mit dem Messschieber an 2 Stellen messen: Innen-Ø Ring, Aussen-Ø Zapfen.
