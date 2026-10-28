# Aufbau Prüfstand J2: von der Lieferung bis zum ersten Test

Eine Seite als Ablauf. Die Einzelheiten stehen in den verlinkten Dateien. **Elektrik an der 230-V-Seite nur mit Freigabe von Opa** (`docs/schema/verdrahtung-j2.md`, `docs/elektronikgehaeuse.md`). Zeitpunkt: Lieferung ca. 1.–9.11.2026.

## 0. Vor der Lieferung (schon möglich)

- Passproben und Haube probieren: `EG_Netzteil_Schablone` auf das Netzteil legen, danach `EG_Netzblende` und `EG_Klemmenabdeckung` (`docs/elektronikgehaeuse.md`).
- Gehäuse-Konstanten nachführen, Wanne und Deckel drucken.

## 1. Wareneingang

1. Alles gegen `docs/stuecklisten/pruefstand-j2.md` abhaken, Status in der Liste von «offen» auf «da» setzen.
2. Sichtprüfung: Riemen, Ritzel (Zähne, Nabe), Lager, Motor (Typenschild 17HS24-2104S).
3. **Ritzel messen** (Schieblehre): Bord, Nabenlänge und Nabendurchmesser des 3M-Ritzels (16 Zähne) und des 5M-Ritzels (18 Zähne). Werte in `cad/skripte/j2_pruefstand.py` oben eintragen (`BORD_*`, `NABE_*`), Skript ausführen. Meldet es weniger als 1 mm Luft zur rechten Wange, ist die Nabe zu lang: kürzen lassen oder das Ritzel umdrehen. Betroffene Teile (Distanzring, 64-Zahn-Scheibe) neu drucken.
4. **TMC2209-Modul:** Aufdruck des Messwiderstands lesen (R110 = 0,11 Ω?), Jumper MS1/MS2 notieren.

## 2. Mechanik

1. Bohrungen der Ritzel und gedruckten Scheiben aufreiben, wo das CAD es verlangt (`docs/pruefstand-j2.md`).
2. Wellen, Ritzel und Scheiben einbauen, Riemen auflegen, Spannrollen einstellen. Reihenfolge und Bilder: `docs/bauanleitung/Bauanleitung_J2_Pruefstand.pdf`.
3. Blockierstift einsetzen (trennt Motor und Stufe 1 von der Messung), Hebel waagrecht prüfen.
4. Messuhrhalter montieren (Tastradius 64 mm), Messuhr noch nicht.

## 3. Elektronik (ohne Netzspannung)

1. Gehäuse auf das Grundbrett schrauben, Netzteil, Uno und Shield einbauen (`docs/elektronikgehaeuse.md`, Montage Schritt 1 bis 6).
2. TMC2209 mit Kühlkörper einsetzen, **Einbaurichtung nach der Beschriftung**.
3. Motorkabel crimpen, Stecker nicht unter Spannung umstecken.
4. F2 und Lüsterklemmen in den Halter (`EG_Halter_24V`), nur auf der 24-V-Seite.

## 4. Netz und 24 V (mit Opa)

1. Verdrahten nach `docs/schema/verdrahtung-j2.md`, Schutzleiter zuerst. Zugentlastung am C14 ist Pflicht.
2. Opa prüft, bevor das erste Mal Netzspannung anliegt.
3. Netzteil einschalten, über das Poti im Deckelschlitz auf **24,0 V** stellen und mit dem Multimeter messen, erst dann an das Shield.

## 5. Erster Lauf (`docs/grbl-j2.md`)

1. Nur USB: GRBL aufspielen, `$$` prüfen, `$`-Werte eintippen (`$100=640`).
2. Vref auf 0,8 A (1,13 V), Motor allein: `j2-00-motor-allein.nc`, Klebebandmarke vergleichen.
3. Vref 1,2 A, Motor und Ritzel einbauen, Hebel von Hand waagrecht, dann Strom. `j2-01-abtrieb-kurz.nc`: Richtung prüfen (`$3`), höchstens 2 bis 5° nach oben, 3° nach unten.
4. `j2-02` bis `j2-04`, erst ohne Last, dann 1,07 kg, erst danach 5,9 kg.

## 6. Messen

`docs/messprotokoll-j2.md` ausfüllen, mit `software/j2_auswertung.py` auswerten. Grenzen: Spiel ≤ 0,3°, Kriechen ≤ 0,1°/24 h, Motorgehäuse ≤ 70 °C. Ergebnis in `index.md` und `HANDOFF.md` nachführen.
