# Offene Ideen (noch nicht gemacht, ohne Teile möglich)

Stand 04.11.2026. Reihenfolge nach Nutzen.

| Nr. | Idee | Nutzen | Aufwand |
|---|---|---|---|
| ~~1~~ | ERLEDIGT 28.10. (`EG_Netzteil_Schablone`) – **Prüfplatte Netzteil** (175 × 65 mm): Ausschnitt für Klemmleiste, Montageohren, Poti | Man sieht am Netzteil, ob Klemmleiste, Ohren und Poti stimmen, bevor die 3 h für Netzblende und Haube gedruckt werden | klein |
| ~~2~~ | ERLEDIGT 28.10. (`EG_Halter_24V`, allgemeine Schale, Masse ungeprüft) – **Halter für F2, Lüsterklemmen und 24-V-Klemmen am Shield** (Rest von Punkt 5) | Berührschutz auch auf der 24-V-Seite; weniger dringend als 230 V | mittel |
| ~~3~~ | ERLEDIGT 28.10. (`docs/aufbauanleitung-j2.md`) – **Aufbauanleitung Prüfstand** auf einer Seite: von der Lieferung bis zum ersten GRBL-Test | Ablauf beim Eintreffen der Teile (ca. 1.–9.11.) | klein |
| 4 | Prüfplatte Uno-USB (Lage der Buchse); vom Nutzer abgelehnt, nur falls das Gehäuse hier Probleme macht | – | klein |

Erledigt: Punkt 4 der ersten Liste (Ritzel-Nabe parametrisiert, 28.10.).

## 04.11.2026: neue Liste und was daraus wurde

| Idee | Ergebnis |
|---|---|
| F1-Halter ohne Löten | **nicht gebaut**: Reihenklemme zu gross (57 mm tief), Schraub-Einbauhalter nicht gefunden. Befund und Optionen in `docs/elektronikgehaeuse.md` (Abschnitt «Sicherung F1 ohne Löten») |
| Drehmoment-Messvorrichtung J2 | **nicht gebaut**: Motorprüfstand (bis 60 mm Motorlänge) und Lasthebel am J2-Prüfstand decken es ab, siehe `docs/zubehoer-j2.md` |
| Endschalter J2 | gebaut: Querträger mit Schaltertasche und Probe, `docs/zubehoer-j2.md` |
| Motorkabel-Zugentlastung | gebaut (Klemme am Motor); die Zugentlastung an der Gehäuserückwand bleibt offen |
| Ritzel-Test | als Nabenlehre gebaut, im Gutachten gestrichen (die Schieblehre reicht); stattdessen Sollwerte-Tabelle in `docs/zubehoer-j2.md` |
| Schiene: Kabelführung | Entwurf der Kettenklemme für Stufe C, `docs/schiene-kabelfuehrung.md` |
| Kamerahalter, Greiferwechsler | Entwurf, `docs/werkzeugwechsler.md` |

Neu offen aus dieser Runde:

| Nr. | Idee | Nutzen | Aufwand |
|---|---|---|---|
| 5 | Zugentlastung für die drei Motorkabel an der Rückwand des Elektronikgehäuses (Wanne ist gedruckt: Klemme zum Aufstecken oder Kabelbinder-Brücke aussen) | Kabelzug geht nicht in den Stecker des Shields | klein |
| 6 | Mechanische Verriegelung (Riegel mit Servo) für den Greiferwechsler, falls die Magnetprobe zu wenig Kraft zeigt | 1 kg bei waagrechtem Werkzeug | mittel |
| 7 | Handgelenk konstruieren (ISO-Flansch, Kabelkanal, Kamera-Schraubpunkte), dann Wechsler und Kamerahalter daran anpassen | Voraussetzung für die Passung dieser Entwürfe | gross |
