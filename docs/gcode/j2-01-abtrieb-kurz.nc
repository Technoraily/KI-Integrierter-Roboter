(J2 Test 1: Abtrieb ohne Last, kurze Wege)
(Einstellungen: $100=640 $110=1800 $120=20)
(Hebel von Hand waagrecht stellen, BEVOR der Strom eingeschaltet wird: dort ist X0)
(Hebel ohne Gewicht. Richtung pruefen: X+ muss den Hebel nach oben bewegen,)
(sonst $3=1 setzen [nicht den Motorstecker umstecken].)
(Nach unten hoechstens 6.65 Grad [22 mm an der Lastbohrung]; hier nur -3)
G21 (mm bzw. Grad)
G91 (relativ)
G94 (Vorschub pro Minute)
G1 X2 F300 (2 Grad = 6,6 mm an der Lastbohrung, 5 Grad/s)
G4 P2
G1 X-2 F300
G1 X5 F300
G1 X-5 F300
G1 X-3 F300 (unter Waagrechte)
G1 X3 F300
M30
