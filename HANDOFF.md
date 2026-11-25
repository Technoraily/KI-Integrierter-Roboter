# HANDOFF – KI-Integrierter Roboterarm (Stand 26.11.2026; Details: README.md, docs/konzept.md, index.md)
## Ziel
6-Achs-Desktop-Roboterarm (3D-Druck, NEMA 17) auf 1000-mm-Schiene (später); Hobbyarm (aufheben, zeichnen, Kamera-KI), Nachbau durch Dritte muss ohne Fummelei gehen. Gestaltung nach Bildvorlage des Nutzers (liegt nur lokal, nicht im Repo): weisse Schalen, dunkler Sockel (docs/design-vorgabe.md).
## Stand
- J2-Messphase durch (docs/messprotokoll-j2.md). Steifigkeit J2 ca. 17 bis 18 Nm/° (Gate wollte 30), Spiel klein, Kriechen 60 min unkritisch. Rücklauf ohne Strom: 1,9 Nm hält, ab 6,6 Nm fällt der Hebel.
- Motoren: J2 = 17HS24-2104S (60 mm, 0,76 Nm, 2,1 A, ohne hintere Welle); J1/J3/J4 = Cloudray 17CS04A-170E (40 mm, 0,42 Nm, 1,7 A, 2,6 Ω; gemessen 3,3 bis 3,4 Ω). Kandidat Bremsmotor: Doppelwelle 60 mm, 0,76 Nm, 2,1 A (Link/Titel beim Nutzer). Nichts bestellen vor dem Phase-2-Gate.
- Gutachten Feder/Bremse (docs/reviews/2026-11-25-feder-bremse-parkposition.md): 3.8 = 8/10, 3.9 = 7/10 (Runde 3 offen). konzept.md 3.8/3.9: Feder allein reicht nicht; Parkposition, Haltebremse J2 (J3 erst nach Rücklauftest dort), Dämpfung am Anschlag.
- NEU 26.11.: Lastrechnung neu (docs/lastrechnung.md): J2 Sicherheit 1,8 nur bei 1,77 A; J3 mit 70:1 ab 1,2 A ok (70:1 entschieden). Durchhang ca. 3 bis 4 mm pro kg, per Software ausgleichen.
- NEU docs/kabelkonzept.md (Regeln, 41 Adern, Hohlwelle mind. Ø 25 mm, Basis-Steckerfeld), docs/design-vorgabe.md (Basis austauschbar, Proportionen, H_schulter 200).
## Entscheidungen
- Steuerung: Standard-BTT-Octopus mit grblHAL für den Arm; ESP32/FluidNC nur Prüfstand. Basis austauschbar (Lochbild 120 mm, 4× M5, Steckerfeld).
- Werkzeugwechsler: mechanischer Servo-Riegel, Werkzeugerkennung per Codierwiderstand, kein Kabel über die Trennstelle (design-vorgabe.md). Claude konstruiert alles, Nutzer druckt/baut. Master-Pult (alle Taster, Not-Aus) gewünscht, Umfang offen (offene-ideen.md Nr. 8).
- Nie Stecker bei 24 V ziehen/stecken (TMC2209 max ca. 28 V). Vref nur bei 24 V AN einstellen, Modulgrenze 1,77 A (Vref 2,5 V).
- Kein 24-h-Test; Genauigkeit zuerst Software-Ausgleich und Kamera.
- Entschieden 26.11.: H_schulter 200 mm, J3 mit 70:1 (parameter.py, parameter.md, Lastrechnung angepasst, 20 Tests ok). Von Claude entschieden (Nutzer: «Rest entscheide du»): Greifer-Servo über Raspberry Pi Pico (statt Uno), Endschalter mechanisch als Öffner (2 Adern, Halter KW11/KW12 in standardteile.py), Stecker JST-XH (Motor 4P, Endschalter 2P) und JST-VH (Bremse 2P); 41 Adern, Bündel ca. 10 mm (docs/kabelkonzept.md).
## Offen
- Fusion 360 war nicht verbunden (Add-in starten), dann Design: Gesamtlayout, Basis/J1, Schulter J2 (Bauraum Bremse ca. 30 mm hinter Motor, Feder), Oberarm J3, Hand.
- Offene Detailentscheide bei der Konstruktion: Lage der Motoren (Gelenk oder Säule), Verfügbarkeit der 70er GT2-Scheibe für J3 (Stufe 20:70 ist Vorschlag).
- Gutachten 3.9 Runde 3, Rücklauf mit gezogenem Netzteil, Rücklauf an J3, Aufprallenergie.
## Nächster Schritt
Fusion starten, dann Gesamtlayout und Basis mit J1 konstruieren (Hohlwelle, Steckerfeld).
## Dateien
docs/kabelkonzept.md, docs/design-vorgabe.md, docs/lastrechnung.md, docs/konzept.md (3.8, 3.9), docs/messprotokoll-j2.md, docs/motorvermessung.md, docs/reviews/2026-11-25-feder-bremse-parkposition.md; kein Fusion-Dokument in dieser Sitzung
