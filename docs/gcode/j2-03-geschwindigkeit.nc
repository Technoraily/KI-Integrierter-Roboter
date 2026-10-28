(J2 Test 3: Drehzahlstufen wie Motorvermessung)
(Einstellungen: $100=640 $110=1800 $120=20)
(Hebel von Hand waagrecht stellen, BEVOR der Strom eingeschaltet wird: dort ist X0)
(Je 3 Zyklen 0 -> +15 -> 0 bei Motordrehzahl 60 / 120 / 240 / 360 U/min)
(Aufsteigend; stehen bleiben oder Brummen = Grenze gefunden, Programm mit Reset abbrechen)
(Messuhr vorher abnehmen: 15 Grad sind 17 mm am Tastklotz, mehr als ihr Messbereich)
(Hebel ohne Gewicht, dann mit 1,07 kg [2 Nm])
G21 (mm bzw. Grad)
G91 (relativ)
G94 (Vorschub pro Minute)
(60 U/min Motor = 5.0 Grad/s Abtrieb)
G1 X15 F300
G1 X-15 F300
G1 X15 F300
G1 X-15 F300
G1 X15 F300
G1 X-15 F300
(120 U/min Motor = 10.0 Grad/s Abtrieb)
G1 X15 F600
G1 X-15 F600
G1 X15 F600
G1 X-15 F600
G1 X15 F600
G1 X-15 F600
(240 U/min Motor = 20.0 Grad/s Abtrieb)
G1 X15 F1200
G1 X-15 F1200
G1 X15 F1200
G1 X-15 F1200
G1 X15 F1200
G1 X-15 F1200
(360 U/min Motor = 30.0 Grad/s Abtrieb)
G1 X15 F1800
G1 X-15 F1800
G1 X15 F1800
G1 X-15 F1800
G1 X15 F1800
G1 X-15 F1800
M30
