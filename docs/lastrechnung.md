# Lastrechnung

Statische Schwerkraftmomente aller Gelenke über den ganzen Arbeitsraum, gerechnet mit `software/roboterarm/lastrechnung.py`. Stand 11.10.2026, vor dem CAD, nach Gutachten Phase 1.

Nachrechnen (dauert rund eine halbe Minute):

```
cd software
python -m roboterarm.lastrechnung
```

## Ergebnis

Auslegungsziel: **1 kg im ganzen Arbeitsraum**, auch voll ausgestreckt. Der Flansch reicht bis 450 mm; der Schwerpunkt der Last ist 80 mm davor angenommen, also bei 530 mm. Geforderte Sicherheit ≥ 1,5 (deckt Beschleunigung und Reibung ab); sie ist an allen Gelenken erfüllt.

| Gelenk | Motor | Untersetzung | Last bei 1 kg (Nm) | verfügbar (Nm) | Sicherheit | Geschwindigkeit (°/s) |
|---|---|---|---|---|---|---|
| J1 | 17CS04A-170E (vorhanden) | 20 | 0,00 | 4,76 | – | 120 |
| J2 | NEMA 17, 60 mm (neu) | 72 | 11,76 | 21,06 | 1,8 | 33 |
| J3 | 17CS04A-170E (vorhanden) | 70 | 5,42 | 12,74 | 2,4 | 34 |
| J4 | 17CS04A-170E (vorhanden) | 20 | 1,66 | 4,76 | 2,9 | 120 |
| J5 | NEMA 17, 34 mm (neu) | 18,75 | 1,68 | 2,87 | 1,7 | 128 |
| J6 | NEMA 14 (neu) | 8 | 0,29 | 0,58 | 2,0 | 300 |

Mit 0,5 kg liegen alle Sicherheiten zwischen 2,3 und 4,9. Alle Achsen laufen über Zahnriemen; die Stufen stehen in `docs/parameter.md`. Bewegte Masse ab Schulter ohne Nutzlast: 2,78 kg (inklusive 0,4 kg für Verkleidung und Kabel).

Der unabhängige Gutachter hat J2, J3 und J5 von Hand nachgerechnet und den ungünstigsten Fall mit einer eigenen Suche bestätigt (Abweichung des Rasters ≤ 0,4 %).

## Empfindlichkeit

Die Rechnung steht und fällt mit dem Moment der vorhandenen Motoren, das noch nicht gemessen ist.

| Falls der 17CS04A-170E nur … nutzbar liefert | Sicherheit J3 | Folge |
|---|---|---|
| 0,28 Nm (Annahme) | 2,0 | passt |
| 0,22 Nm | 1,6 | passt knapp |
| 0,20 Nm | 1,4 | J3 auf 70:1 erhöhen (34°/s, Ziel ≥ 25°/s bleibt erfüllt) |

J2 ist mit Wirkungsgrad 0,65 für drei Riemenstufen vorsichtig gerechnet (drei Stufen zu je 0,9 ergäben 0,73 und Sicherheit 2,0).

## Änderungen gegenüber dem Konzept

| Gelenk | Konzept | jetzt | Grund |
|---|---|---|---|
| J2 | vorhandener Motor, 90:1 | NEMA 17 mit 60 mm, 72:1 | 1 kg ganz aussen; 72:1 = drei Riemenstufen 3,6 × 4 × 5 |
| J3 | 40:1 | 70:1 (Entscheid 26.11.2026, vorher 60:1) | Reserve für schwächere Motoren, schwerere Struktur und kleineren Treiberstrom |
| J4 | 34-mm-Motor, 12:1 | vorhandener Motor, 20:1 | abgewinkelte Hand erzeugt bis 1,66 Nm um die Unterarmachse |
| J5 | Pancake, 18:1 | NEMA 17 34 mm, 18,75:1 | Pancake zu schwach; 18,75:1 = zwei Riemenstufen 5 × 3,75 |
| J6 | 6:1 | 8:1 | Sicherheit 1,5 → 2,0 |

## Was 1 kg aussen kostet

Die Motoren schaffen es; die Grenze ist die Steifigkeit, nicht die Kraft.

- **Durchhang:** Zwischen leer und 1 kg ändert sich das Schultermoment um ca. 5 Nm. Bei der Zielsteifigkeit von 30 Nm/° (für den Riemenantrieb am unteren Rand der Schätzung) sind das 0,16° oder gut 1 mm am Flansch, dazu 0,3–1 mm Biegung der PLA-Struktur (Schätzung des Gutachters). Insgesamt 2–3 mm lastabhängiger Durchhang. Die ±0,5 mm gelten deshalb **bei gleichbleibender Last**.
- **Schwingen:** Eigenfrequenz um 10 Hz mit 1 kg ausgestreckt; der Arm schwingt nach dem Anhalten spürbar nach.
- **Kriechen:** 1 kg stundenlang ausgestreckt halten belastet PLA und Lagersitze dauerhaft. Der 24-h-Haltetest im Prüfstand läuft mit 11 Nm.

## Annahmen

- **Motormomente sind angenommen**, nicht gemessen: nutzbar ca. 70 % des Haltemoments bis etwa 400 U/min an 24 V. Für den 17CS04A-170E gibt es kein auffindbares Datenblatt; 1,7 A sind aus der Bezeichnung plausibel, das Haltemoment ist unbekannt. Gerechnet ist mit 0,28 Nm. Für 60 mm: 0,45 Nm, 34 mm: 0,18 Nm, NEMA 14: 0,08 Nm. Messung: `docs/motorvermessung.md`.
- Wirkungsgrad: 0,65 für J2/J3 (drei Stufen, vorsichtig), 0,85–0,9 für ein- und zweistufige Riemenantriebe.
- Massenmodell geschätzt (Tabelle `MASSEN` in `parameter.py`); wird mit den Massen aus Fusion nachgeführt.
- Nutzlastschwerpunkt 80 mm vor dem Flansch und 30 mm seitlich versetzt.
- Gerechnet ist **ohne** Ausgleichsfeder; das ist auch der geplante Bau. Die Feder ist eine Reserve, falls Motorvermessung oder Prüfstand es verlangen (Kriterien in `docs/konzept.md`, 3.8). Mit Teilausgleich von 4 Nm sänke das grösste J2-Moment von 11,8 auf 7,8 Nm.
- J1 trägt bei senkrechter Achse keine Schwerkraft. Sein Moment bestimmt die Beschleunigung, nicht die Statik.

## Nachrechnung 26.11.2026 (Datenblatt und Prüfstandmessung)

Neu seit der Rechnung vom 11.10.: Datenblatt des 17CS04A-170E gefunden (0,42 Nm, 1,7 A, 40 mm, Shopseite Cloudray), Motor J2 ist der 17HS24-2104S (0,76 Nm bei 2,1 A), Steifigkeit J2 gemessen (ca. 17 bis 18 Nm/°, nach 60 min ca. 15). Das Skript `lastrechnung.py` lief unverändert (Lasten und Sicherheiten wie in der Tabelle oben, bei Motormomenten 0,28 / 0,45 / 0,18 / 0,08 Nm). Die Rechnung unten ersetzt nur die Motormomente und hängt vom **eingestellten Treiberstrom** ab. Nutzbar = Haltemoment × Strom / Nennstrom × 0,7 (Mikroschritte, bis ca. 400 U/min, Annahme wie oben).

**Sicherheit mit Datenblattwerten** (Wirkungsgrad 0,65 für J2 und J3, 0,85 für J4; Last bei 1 kg aussen):

| Strom | J3 nutzbar (Nm) | J3 bei 60:1 | J3 bei 70:1 | J4 bei 20:1 | J2 nutzbar (Nm) | J2 bei 72:1 |
|---|---|---|---|---|---|---|
| 1,0 A | 0,173 | 1,24 | 1,45 | 1,77 | – | – |
| 1,2 A | 0,208 | **1,49** | 1,74 | 2,13 | 0,304 | 1,21 |
| 1,5 A | 0,259 | 1,87 | 2,18 | 2,66 | 0,380 | **1,51** |
| 1,7 A | 0,294 | 2,12 | 2,47 | 3,01 | – | – |
| 1,77 A (Modulgrenze) | – | – | – | – | 0,448 | 1,78 |

Gefordert ist Sicherheit ≥ 1,5. Ergebnis:
- **J3:** Mit 60:1 braucht es mindestens ca. 1,3 A Treiberstrom (bei 1,2 A 1,49, knapp unter dem Ziel). Mit **70:1 reicht schon 1,2 A (1,74)** und es bleibt Reserve für Wärme und Streuung. Geschwindigkeit bei 70:1 ca. 34 °/s (Ziel ≥ 25 °/s bleibt erfüllt). **Entschieden am 26.11.2026: J3 mit 70:1** (Parameter und Skript angepasst; die Tabelle oben zeigt jetzt J3 mit 12,74 Nm verfügbar, Sicherheit 2,4, 34 °/s). Grund: Die Übersetzung legt die Riemenstufen von J3 fest, und J3 ist noch nicht gezeichnet.
- **J2:** Die frühere Sicherheit 1,8 gilt nur bei **1,77 A**, der Obergrenze des Moduls. Bei 1,5 A sind es 1,51, bei 1,2 A nur 1,21. J2 muss also mit hohem Strom laufen (Kühlkörper, Lüfter). Die Haltemessung am Prüfstand (11,4 Nm bei ca. 0,9 A statisch gehalten, wo das Modell nur 0,91 ergibt) zeigt, dass das Modell fürs **statische Halten** konservativ ist; fürs Fahren (Beschleunigen, Drehzahl) bleibt es die vorsichtige Grundlage.
- **J4:** Auch bei 1,0 A Sicherheit 1,77, also unkritisch.
- J1, J5, J6 unverändert (J5 und J6 beruhen weiter auf angenommenen Momenten neuer Motoren).

**Durchhang mit gemessener Steifigkeit J2 von 17 Nm/°** (statt 30 Nm/°; 1 kg aussen, Flansch 450 mm von J2 entfernt):
- J2: Momentenänderung leer gegen 1 kg ca. 5,2 Nm, das ergibt 0,31° und ca. **2,4 mm** am Flansch (bei 30 Nm/° wären es 1,4 mm).
- J3 (Steifigkeit **nicht gemessen**, hier 17 Nm/° angenommen): ca. 3,2 Nm, 0,19°, ca. 0,8 mm am Flansch.
- Dazu kommen Biegung der gedruckten Struktur (0,3 bis 1 mm, Schätzung des Gutachters) und J4 bis J6. Insgesamt grob **3 bis 4 mm** lastabhängiger Durchhang bei 1 kg, statt 2 bis 3 mm in der Rechnung vom 11.10.
- Das ist statisch und wiederholbar. Mit Software-Vorsteuerung (Durchhang aus Stellung und Last vorrechnen) sollte sich der Grossteil ausgleichen lassen. Welcher Anteil übrig bleibt, ist nicht gemessen; als Arbeitsannahme 10 bis 20 % (0,3 bis 0,8 mm), zu bestätigen am gebauten Arm.
- Eigenfrequenz mit 1 kg ausgestreckt: ca. 7,5 Hz statt ca. 10 Hz (nach der Wurzel der Steifigkeit skaliert, grobe Rechnung).
