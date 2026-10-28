# Prüfprotokoll: Elektronikgehäuse J2-Prüfstand

Geprüft wird der Entwurf (`cad/skripte/elektronikgehaeuse.py`, `docs/elektronikgehaeuse.md`, Stückliste, Druckeinstellungen) von unabhängigen Gutachtern. Skala 0–4 unbrauchbar · 5–7 gut mit Potenzial · 8–10 fertig. Die Gutachter haben nur Skript, STL, Doku und die Datenblatt-Zeichnung gelesen und von Hand gerechnet; echte Teile (C14, F1, Uno, Netzteil) hatten sie nicht.

| Runde | Note | Kern |
|---|---|---|
| 1 | 6/10 | Kabelweg der Ringschuh-Kabel, Haube nicht druckbar, drei Schraubenlängen, Poti- und Lüfterlage |
| 2 | 6/10 | Korrekturen aus Runde 1 überwiegend richtig, aber drei neue Fehler (Tropfenbohrung, Haubenstreifen, Muttern) und Deckelrand |
| 3 | **7/10** | Korrekturen bestätigt, keine kritischen Fehler; offen blieben falsche Deckel-Behauptung und Haubenlänge |

**Ziel «über 8» wurde nicht erreicht.** Nach Runde 3 sieht das Prüfverfahren keine weitere Runde vor. Die unten markierten Korrekturen nach Runde 3 sind **nicht** erneut begutachtet.

## Runde 1: 6/10

| Nr. | Mangel | Massnahme |
|---|---|---|
| K1 | Der Kabelkanal links der Haube war 2,6 mm breit; die Ringschuh-Kabel hätten nirgends hingekonnt | Kabelgang 10 mm links vom Netzteil unter der Haube, Kabel treten durch unten offene Schlitze (10 × 14 mm) in den Stirnwänden aus |
| K2 | Haube nur mit Stützen druckbar: rechte Wand hing über dem Netzteil-Freischnitt frei | Haube auf dem Kopf gedruckt (Dach unten) |
| W1 | Deckelschrauben M3 × 10 stiessen im Dom an (Bohrung 7 mm) | Bohrung 10 mm tief |
| W2 | Arduino M3 × 8 stiess an | M3 × 6, Dome Ø 8; Uno zuerst allein, dann Shield |
| W3 | Haubenschrauben M3 × 10 standen 1 mm unter den Boden | Lasche 5 mm dick, Spitze bündig |
| W4 | Poti V ADJ näher an der Haube als angenommen; Lüftungsschlitze nicht über dem Lüfter | Lagen aus der Zeichnung ausgemessen und korrigiert |
| W5 | Nur 17 mm hinter dem C14 für die Flachsteckhülsen | Netzteil 10 mm nach hinten (27 mm) |
| W6 | Deckel nur an 6 Schrauben | 9, später 10 Dome |
| W7 | Umschalter 115/230 V fehlte im Montageplan | Schritt 2 |
| W8 | 230-V-Leitungen ohne Fixierpunkte | Kabelbinderschlitze vorne |

## Runde 2: 6/10

| Nr. | Mangel | Massnahme |
|---|---|---|
| W1 | Tropfenbohrung der waagrechten Einsatzbohrungen 5,66 mm breit statt Ø 4,0 | Raute erst ab den Tangentenpunkten; im STL ±2,0 mm bestätigt |
| W2 | Haube: freier Streifen an Seiten- und Rückwand | Freischnitt bis zum Boden |
| W3 | Muttern in den nach unten offenen Taschen fallen heraus | Taschen von oben, die Laschen halten die Muttern |
| W4 | Deckelrand vorne ungeschraubt | Wandsteg mit Dom bei x = 100 |
| W5 | Kabelbinderschlitze auf der falschen Seite, Kommentare veraltet, Deckelschrauben 1 mm über Deckel | Schlitze verlegt, Kommentare angepasst, Linsenkopf ISO 7380 |

## Runde 3: 7/10

Alle Korrekturen aus Runde 2 wurden im STL nachgemessen und bestätigt. Neue Befunde und die Massnahmen (**danach nicht mehr begutachtet**):

| Nr. | Mangel | Massnahme |
|---|---|---|
| W1 | Doku behauptete «kein Schraubenabstand am Rand über 100 mm»; seitlich sind es 146 und 186 mm (rechts und links keine Dome wegen Netzteil und Haube) | Behauptung gestrichen. Lippe 2 × 6 mm unter dem Deckelrand links, rechts und hinten; Deckel druckt mit der Oberseite unten. **Wirkung unbestätigt, zeigt erst der Druck** |
| W2 | Haube innen 90 mm lang: Rückwand schneidet den Ringschuh der Klemme 9 (reicht bis etwa 90 mm) | Innenlänge 91,5 mm, Rückwand 1,2 mm (Aussenfläche 92,7 mm, Poti ab 93,2 mm). 0,5 mm Luft zum Poti nur aus der Zeichnung, Passprobe nötig |
| W3 | Wanddome berührten die Wand nur tangential | Mittelpunkt 3,5 mm von der Innenwand (0,5 mm Überlappung) |
| W4 | Über der Tropfenspitze der Netzblendendome nur 1,17 mm Material | Dome Ø 9 (1,7 mm) |
| K1 | Doku und Skript widersprachen sich (Kabelbinderschlitze, «Mutter unter dem Boden», Haubenmass, Tabellenzeile 3.11) | angeglichen |
| K2 | Filamentschätzung zu tief | etwa 0,6 kg PETG |

Nach den Änderungen: Fusion-Kollisionsprüfung erneut ausgeführt, keine Durchdringung der Druckteile mit den Referenzquadern; STL neu exportiert und nachgemessen (Wanne 240 × 238 × 60, Deckel 240 × 238 × 10, Blende 134 × 57 × 5, Haube 35 × 107 × 46; Tropfenbohrung ±2,0 mm).

## Was ohne echte Teile nicht geprüft werden konnte

- Klemmleiste des Netzteils (Länge bis 90,8 oder etwa 92 mm, Breite), Montageohren (in der Zeichnung strichliert), Lage von Umschalter und Poti: nur aus dem Bild gelesen.
- C14 (Ausschnitt 28 × 20, Lochabstand, Tiefe mit Hülsen), F1 (Gewindelänge bei 5 mm Blende, Abflachung), USB-Lage am Uno (Gutachter erinnerte eher 30 bis 40 mm), Höhe des Shield-Stapels.
- Verzug und Haftung der 240-mm-Teile, Wirkung der Deckellippe, Slicer-Lauf (Zeit, Gewicht, Stützen).
- Lüftung und Temperatur im geschlossenen Gehäuse, Kriech- und Luftstrecken, Normen, Brandverhalten (PETG nicht V-0), Freigabe der 230-V-Seite durch Opa.

## Empfehlung

Als Nächstes die zwei Testplatten `EG_Passprobe_C14` und `EG_Passprobe_F1` drucken (nach der Begutachtung ergänzt, nicht begutachtet), dann die **Passproben** `EG_Netzblende` und `EG_Klemmenabdeckung` (zusammen etwa 3 h) und mit C14, F1 und dem Netzteil probieren. Wanne und Deckel erst danach drucken, nach Anpassung der Startwerte im Skript.
