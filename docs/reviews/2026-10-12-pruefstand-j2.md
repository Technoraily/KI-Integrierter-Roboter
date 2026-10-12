# Prüfprotokoll: CAD des Prüfstands Schultergelenk J2

Geprüft wird, ob man mit dem CAD-Stand (`cad/skripte/j2_pruefstand.py`, `docs/pruefstand-j2.md`) die Kaufteile bestellen und drucken kann. Unabhängige Gutachter, Skala 0–4 unbrauchbar · 5–7 gut mit Verbesserungspotenzial · 8–10 nahezu perfekt.

## Runde 1: 5/10

Der Gutachter hat die Geometrie des Skripts in Python nachgerechnet und die Bilder geprüft.

| Nr. | Mangel | Massnahme |
|---|---|---|
| K1 | Die Spannrolle der Stufe 2 drückte den 3M-Riemen auf die 64er-Scheibe (Abstand Rolle–Welle B 42,16 mm, nötig > 42,41 mm); der 252er-Riemen wäre nie straff geworden. Das Skript hatte den Fehler verschluckt, und die Kollisionsmeldung war im Dokument fälschlich als Darstellungsfehler abgetan. | Achsabstand Stufe 2 auf 61,3 mm, Rolle bei x = 8 mm. Das Skript bricht jetzt ab, wenn eine Rolle näher als 1,5 mm an eine Scheibe kommt oder ein freies Trum kürzer als 8 mm wird. Kollisionsprüfung danach ohne Meldung. |
| K2 | Der Lasthebel (30 × 20 mm) gibt mit etwa 57 Nm/° so viel nach wie der Antrieb (erwartet 30–100 Nm/°) und kriecht im Haltetest. Ein guter Antrieb wäre fälschlich durchgefallen. | Eigener, unbelasteter Messzeiger auf der 90er-Scheibe und ein Messuhrhalter am Rahmen. Hebel von 60 auf 30 mm verjüngt. |
| W1 | Spannrolle 5M: nur 2,6 mm Luft zur 90er-Scheibe, etwa 4 mm Spannweg nutzbar. | Rolle auf y = 90 mm; Luft 10 mm, Reserve 4,8 mm Riemenlänge. |
| W2 | Motorschrauben im fertigen Rahmen nicht erreichbar. | Langlöcher 7 × 13 mm in der rechten Wange; Zugangsbohrungen für Hebel-, Zeiger- und Blockierschraube. |
| W3 | Die Mitnahmeschrauben an Welle B erreichten die Welle nicht; Ritzel und Welle waren lose. | M4 × 16 in 3,9-mm-Bohrungen (schneiden sich spielfrei ein), Spitze auf der angefeilten Welle. |
| W4 | Gewindestifte an Welle A (M3 × 8) erreichten die angefeilte Fläche nicht. | M3 × 10. |
| W5 | Schrauben fürs Grundbrett standen auf Grund. | Bohrung 12 mm tief. |
| W6 | Keine Anschläge, kein Fallschutz, Kippen ungeklärt. | Obere Querträger dienen als Anschläge bei 93°; Aufstellung an der Tischkante mit Zwingen und Fallschutz beschrieben. |
| W7 | Kein Messuhrhalter, keine Möglichkeit, den Antrieb zu blockieren. | Messuhrhalter, Blockierstift durch die 72er-Scheibe (alle 4,5° am Abtrieb). |
| W8 | Material der linken Wange offen; Spannrollen nur durch Reibung gehalten. | Linke Wange und Hülsen in PETG; je Wange und Rolle eine M3-Stellschraube. |
| klein | Anlagebunde im Bereich der Lagerdichtung, Radialspiel am Abtrieb, dünner Kranz über den Fenstern, M8 × 90 unnötig lang, falsche Zahlen im Dokument. | Anlagebund Ø 12 mm, Bohrung Abtrieb 8,05 mm, Fenster Ø 24 mm, M8 × 80, Dokument korrigiert. |
| klein | Lagerbund 1 mm, 3M-Rolle ohne Bord, Zahnform ohne Kopfkantenradius. | Belassen und begründet; Zahnsegment-Testdruck vor dem Druck der Scheiben. |

Empfehlung des Gutachters, übernommen: Ritzel zuerst bestellen und nachmessen, dann die Scheiben drucken.

## Runde 2: 7/10

Ein zweiter, unabhängiger Gutachter hat den Stand nach Runde 1 neu nachgerechnet. Kein kritischer Mangel; alle Mängel der Runde 1 behoben oder teilweise behoben. Antrieb (Achslagen, Riemenlängen, Rollenlagen, axiale Stapel, Schwenkbereich) in Ordnung. Offen waren der Messaufbau und Einzelheiten der Spannrollen.

| Nr. | Mangel | Massnahme |
|---|---|---|
| W-A | Die Stellschrauben der 3M-Rolle ragen 6–13 mm unten aus den Wangen, dort liegt das Grundbrett. | Zwei Löcher Ø 10 mm im Brett; gespannt wird, bevor das Brett am Tisch festgezwungen ist. In Skizze und Beschreibung aufgenommen. |
| W-B | Die Klemmschraube der Messuhr (M3 × 8) erreichte den Schaft nicht; eine Punktschraube kann die Pinole klemmen. | Geschlitzte Klemmbohrung mit M3 × 25 quer zum Schlitz. |
| W-C | Das Gehäuse der Messuhr wäre an Scheibe und Riemen gestossen, bevor der Taster den Zeiger erreicht. | Messuhr-Achse von 26 auf 38 mm neben die linke Wange verlegt; Zeiger mit Tastklotz (30 mm breit, bis 46 mm), Tastfläche 8 mm höher. |
| W-D | «Hebel einmal rechts, einmal links» misst kein Umkehrspiel, weil dazwischen 180° gedreht und die Messuhr umgesetzt wird. | Messablauf neu: Gewicht anhängen (−2 Nm), dann mit einer Kofferwaage nach oben ziehen (+2 Nm); die Messuhr bleibt stehen. |
| K-1 | M8 × 80 mit zwei Scheiben zu kurz. | M8 × 90 mit Schaft. |
| K-2 | Hülsen Ø 12 mm würden beim Anziehen der M8 zerdrückt. | Hülsen auf Ø 16 mm, wo Platz ist; M8 nur handfest mit selbstsichernder Mutter, die Lage halten die Stellschrauben. |
| K-3 | Spannreserve 3M mit 1,7 mm knapp. | Rolle auf x = 10 mm: Reserve 2,9 mm. |
| K-4 | Blockierstift nur 0,3 mm neben einem Gewindestift der Nabe; 0,3 mm Lochspiel. | Bohrungen um 45° gedreht (1,9 mm Abstand), Ø 3,0 mm, Stift fest anziehen. |
| K-5 | Zwei Motorschrauben liegen dicht am GT2-Riemen. | Montagefolge: Motor vor dem Auflegen des Riemens lose anschrauben. |
| K-6 | Die Messuhr sieht auch das Setzen der Abtriebswelle im Lagersitz. | Zusätzlich auf dem Nabenbund des Hebels tasten und abziehen. |
| K-7 | Aufstellung unklar. | Skizze `docs/bilder/pruefstand_befestigung.png`: Brett bündig an der Tischkante, Wangen quer zur Kante. |
| K-8 | Ein in den Kunststoff geschnittenes Gewinde hat eine zufällige Phase zum Gewinde der Ritzelnabe. | Bohrung als saugende Passung beschrieben, kein Gewinde. |

## Runde 3: 8/10 – Tor erreicht

Ein dritter, unabhängiger Gutachter: «Der Antrieb, der Rahmen und die Stückliste stimmen rechnerisch; die Kaufteile können bestellt und die Hauptteile nach Nachmessen und Testdruck gedruckt werden. Kein kritischer Mangel.» Alle Mängel der Runde 2 behoben, zwei davon teilweise (Auswertung der Wechsellast, Tasten auf dem Nabenbund).

Mit der Note 8 ist die Prüfung abgeschlossen. Die Anmerkungen der Runde 3 sind eingearbeitet, aber **nicht mehr begutachtet**:

| Nr. | Anmerkung | Massnahme |
|---|---|---|
| W1 | Mit dem 300-mm-Brett hing die Last nach dem Umdrehen 2 mm innerhalb der Tischkante. | Brett 220 × 200 mm, Prüfstand mittig; Last in beiden Lagen 78,5 mm ausserhalb. |
| W2 | Die Auswertung des Umkehrspiels war unterbestimmt (Spiel und elastischer Anteil nicht trennbar). | Ablesung zweimal bei Moment null, von unten und von oben kommend; Steifigkeit aus den Endpunkten. |
| W3 | Klemmung der Messuhr zu steif (rund 670 N nötig). | Schlitz durch die Bohrung hindurch (rund 170 N), Bohrung 8,0 mm, Schraube 1 mm weiter von der Armstirn. |
| W4 | Ein fest angezogener Blockierstift zieht die 72er-Scheibe schief gegen den 1-mm-Lagerbund. | Stift nur anlegen; Restspiel höchstens 0,017° am Abtrieb, im Dokument vermerkt. |
| klein | Hülse der 3M-Rolle kommt am Ende des Spannwegs dem GT2-Riemen auf 1 mm nahe; Zahlen im Dokument; Senkung im Brett ohne Reserve; Querträgerschrauben greifen nur 4 mm; Nabenbund nur mit Stativ antastbar; Schlüssel für den Blockierstift. | Nutzbare 3M-Reserve mit 2,1 mm angegeben; Zahlen korrigiert; Senkung 3,5 mm; Querträger mit M3 × 16; Stativ und Schlüssel im Dokument. Nicht umgesetzt: die Hülsenabstände in der Abbruchprüfung des Skripts. |

## Nach dem Gutachten, auf Wunsch des Nutzers

Die oberen Querträger sitzen 5 mm tiefer (y = 124 statt 129 mm). Bei waagrechtem Hebel bleiben damit rund 10 mm Spalt statt 5 mm; der Hebel fällt im Störfall bis 96,7° statt 93,3° (Lastbohrung 22 mm statt 11 mm). Kollisionsprüfung danach ohne Meldung; Abstände der Querträger zu Riemen, Scheibe, Spannrolle und Motor mindestens 12 mm.
