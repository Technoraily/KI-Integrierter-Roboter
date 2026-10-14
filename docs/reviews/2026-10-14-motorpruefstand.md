# Gutachten: Motorprüfstand NEMA 17 (ohne Kaufteile)

Datum 14.10.2026. Geprüft: `cad/skripte/motorpruefstand.py`, `docs/motorvermessung.md`, `docs/stuecklisten/motorpruefstand.md`, Renderings. Unabhängiger Gutachter (Agent), Note 1–10.

## Runde 1: 6/10

Messprinzip (hängende Last, symmetrischer Waagebalken, Seilwinde) und Grundzahlen korrekt. Mängel:

1. Test B erreicht 240/360 U/min nicht (Beschleunigungsweg bei r = 20 mm und 200 mm Hub zu kurz).
2. Test C falsch parametriert ($100 von Test B übrig, $110 begrenzt, ohne Last aussagelos).
3. A4988 ohne Kühlung bei 1,2 A Dauerhalten: Thermoabschaltung täuscht Durchrutschen vor.
4. Netzteilspannung fehlt im Protokoll.
5. Schnur nur 4 mm vor der Tischkante; Kippmoment bei Test B grösser als Rückhaltemoment.
6. Last für r = 20 mm evtl. über 1,5 kg.
7. M3-Schraube ist nicht sicher vorhanden.
8. Mutterfalle 5,7 mm zu eng.
9. Klemmnabe der Trommel zu steif.
10. Messfehler (Schnurdicke, Rastmoment, Stösse, Sättigung, Reibung an der Stirnwand) nicht erwähnt.
11. Zapfen des Niederhalters mit 100 % Infill drucken.

**Umgesetzt:** gestufte Trommel r = 20/10 mm, Hub 300 mm, $120 = 1000; Test C neu unter Last; 1,0 A mit 5-min-Wärmetest; Spalte Spannung; Grundplatte bis y = -70 mit Zwingenlöchern, Platte 20 mm über der Kante; Last bis 3 kg; M3 ehrlich als «klären»; Mutterfalle 5,9; Nabe 10 mm mit Schlitz in den Kegel; Abschnitt Messfehler; Niederhalter 100 %.

## Runde 2: 8/10, fertig

Alle Punkte umgesetzt, Zahlen nachgerechnet und bestätigt. Restpunkte, danach ebenfalls umgesetzt:

1. Kippmoment bis 1,1 Nm statt 0,9 Nm → ohne Zwinge 4 kg Bücher.
2. Stufe r = 10 mm zu schmal für 300 mm einlagige Schnur → Kern 8,5 mm breit, Hinweis «einlagig wickeln».
3. Test C auch bei 360 U/min auf r = 10 mm.
4. Masse samt Tasche und Schnur wiegen.
5. Test C an der Bodenmarke der Flasche ablesen (±1 mm), nicht am Flansch (Parallaxe).
6. Stückliste: D-Profil-Variante «müsste noch konstruiert werden»; Schnur 2 m.
