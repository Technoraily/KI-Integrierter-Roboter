# Anforderungen

Quelle: Auftrag und Rückfragen vom 11.10.2026. Jede Anforderung hat eine Nummer, damit Prüfprotokolle und Tests darauf verweisen können.

## Muss

| Nr. | Anforderung |
|---|---|
| A1 | Roboterarm von Grund auf selbst konstruiert (Fusion 360), kein bestehender Bausatz |
| A2 | 6 Achsen |
| A3 | Reichweite ca. 400–450 mm, Nutzlast 0,5–1 kg |
| A4 | Strukturteile gedruckt auf BambuLab A1 (Bauraum 256 × 256 × 256 mm); PLA als Standard, PETG für wichtige Teile erlaubt |
| A5 | Kaufteile sind Standardteile und einfach über AliExpress beschaffbar |
| A6 | So wenige nicht druckbare Teile wie möglich, ohne Qualität und Präzision zu opfern |
| A7 | So präzise wie möglich; arbeitet zuverlässig |
| A8 | Vollständige, passende Verkleidung – nicht nur ein Gerüst |
| A9 | Bebilderte Bauanleitung und Dokumentation entstehen im Projekt |
| A10 | Vorgehen nach klarem Plan, Qualität vor Tempo |

## Soll

| Nr. | Anforderung |
|---|---|
| B1 | Kaufteile für den Anfang unter 150 CHF (Gesamtarm realistisch 175–250 CHF, daher zwei Ausbaustufen) |
| B2 | NEMA-17-Schrittmotoren; vorhandene Teile weiterverwenden (3× NEMA 17, Arduino Uno + CNC-Shield + A4988, Netzteil, Kleinteile) |
| B3 | Steuerung möglichst nah an Arduino/GRBL – Abweichung erlaubt, wenn begründet besser |

## Später (jetzt nur vorsehen)

| Nr. | Anforderung |
|---|---|
| C1 | KI-Integration per Kamera |
| C2 | Automatischer Greiferwechsel |

## Ausdrücklich nicht gewollt

- Ein auf das Minimum abgespeckter Baukasten-Arm, der nur einen kleinen Greifer bewegt.
- Ein möglichst schneller Bau ohne Plan.

## Messbare Ziele

Die Zahlenwerte (Wiederholgenauigkeit, Fehlerbudget pro Gelenk, Geschwindigkeiten) stehen in [konzept.md](konzept.md), Abschnitt 2.
