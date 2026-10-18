\## Übergabe (HANDOFF.md)

\- Halte HANDOFF.md im Projektordner aktuell: max. 25 Zeilen, Inhalt ersetzen statt anhängen.

\- Aktualisiere sie nach jedem abgeschlossenen größeren Arbeitsschritt und sofort, wenn ich "Feierabend", "Schluss" oder "Übergabe" sage.

\- Inhalt: Ziel, Stand, Entscheidungen, Offen, Nächster Schritt, wichtige Dateien und Fusion-Dokument.

\- Keine Passwörter oder Tokens in die Datei.

\- Beim Start nur HANDOFF.md lesen. Weitere Dateien nur öffnen, wenn der nächste Schritt sie braucht.

\- Wurde HANDOFF.md beim Start geladen: kurz bestätigen und beim "Nächsten Schritt" weitermachen.


## Arbeitsregeln (aus dem Claude-Gedächtnis übernommen, damit sie auf jedem Computer gelten)

- Sprache Deutsch (Schweiz: «ss» statt «ß», CHF). Abstände und Spiel in **mm**; bei Winkeln immer den Weg in mm an einer benannten Stelle dazuschreiben.
- Repo ist **öffentlich** (github.com/Technoraily/KI-Integrierter-Roboter, Projektseite über GitHub Pages: `index.md`). Commits nur mit `275000754+Technoraily@users.noreply.github.com`; nie eine private Mailadresse in Dateien oder Commits. Vor jedem Push prüfen, dass nichts Privates drinsteht.
- Projektseite pflegen: bei jedem neuen Stand `index.md` (Stand, Phasentabelle, Bilder) nachführen, committen, pushen.
- Prüfverfahren: Ideen/Baugruppen von einem unabhängigen Agenten mit 1–10 bewerten lassen (0–4 unbrauchbar, 5–7 gut mit Potenzial, 8–10 fertig). Max. 3 Runden, ab 8 keine weitere. Protokoll in `docs/reviews/`.
- Stückliste je Baugruppe in `docs/stuecklisten/<baugruppe>.md` mit ALLEN Teilen (Vorlage `pruefstand-j2.md`): Positionsnummern, Druckteile, Kaufteile mit Suchbegriff und Preis, jede Schraube mit Länge/Menge/Verwendung, Elektrik, Messmittel, Werkzeug, Verbrauchsmaterial, Status (da/offen/klären), am Schluss «Was noch zu bestellen ist». Stückzahlen gegen CAD-Skript nachzählen.
- Druckeinstellungen immer vollständig zu jedem Druckteil (STL-Ordner `Druckeinstellungen.md`, Bauanleitung, Stückliste): BambuLab A1, 0,4-mm-Düse, Basis «0.20mm Standard @BBL A1», Material, Schichthöhe, Wände, obere/untere Schichten, Infill-Muster und -Dichte, Stützen, Brim, Lage auf dem Bett, Nachbearbeitung.
- Versionen: mehrere sind ok, aber jede durchdacht und schnell. Masse nur aus `docs/parameter.md` bzw. CAD-Skripten, nie aus dem Gedächtnis. Vorher prüfen, ob eine Idee schon verworfen wurde (`docs/konzept.md`, `docs/reviews/`). Vor jeder Version: Kollision, Bauraum A1, Montierbarkeit, Lastrechnung, Gutachten. Kritisches zuerst als kleines Testteil.
- Gemessene Drucktoleranz (A1, Toleranztest 18.10.2026): Kugellagersitz 608 liegend gedruckt = Bohrung Ø 22,20 mm (Übermass 0,20 mm), gilt als Standard für alle Skripte. Waagrechte (stehend gedruckte) Lagersitze: 22,10 bis 22,30 passten nicht (Saggen der Decke), dort Tropfenform/Stützen statt nur grösseres Mass. Passung gedruckter Zapfen Ø 10 mm: Loch Ø 10,20 mm (Übermass 0,20 mm). Weitere Werte in `docs/parameter.md`.
- Budget knapp: zuerst die günstigste sichere Lösung nennen und prüfen, ob der Kauf jetzt nötig ist. Bestand beim Nutzer erfragen, nicht aus den Dokumenten ableiten.
- Verbreitete, bewährte Technik (wie bei kommerziellen Produkten) vor ungewohnten Lösungen. Fachbegriffe der Antriebstechnik kurz erklären.

## Synchronisation zwischen Computern

Hooks in `.claude/settings.json` holen beim Start den Stand von GitHub (`.claude/hooks/sync-start.sh`) und pushen beim Beenden automatisch (`.claude/hooks/sync-end.sh`). Einrichtung: `docs/sync-zweiter-computer.md`. Immer nur an einem Computer gleichzeitig arbeiten.
