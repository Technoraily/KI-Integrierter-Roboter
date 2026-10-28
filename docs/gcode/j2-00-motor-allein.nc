(J2 Test 0: Motor allein auf der Wange, ohne Riemen und Ritzelstufen)
(Einstellungen: $100=8.889 $110=45000 $120=500 [X = Grad an der Motorwelle])
(Markierung mit Klebeband auf die Welle; 1 Umdrehung = 360)
(Prueft Verdrahtung, Drehrichtung, Vref und dass keine Schritte fehlen)
G21 (mm bzw. Grad)
G91 (relativ)
G94 (Vorschub pro Minute)
(10 Umdrehungen vor, 10 zurueck, 60 U/min; Marke muss wieder am Start stehen)
G1 X3600 F21600
G1 X-3600 F21600
(5 Umdrehungen bei 120 U/min)
G1 X1800 F43200
G1 X-1800 F43200
M30
