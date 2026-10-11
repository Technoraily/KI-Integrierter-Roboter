import contextlib
import io
import math
import random
import unittest

import numpy as np

from roboterarm import parameter as p
from roboterarm.kinematik import (
    in_grenzen,
    loesungen,
    naechste_loesung,
    rueckwaerts,
    vorwaerts,
)
from roboterarm.lastrechnung import G, bericht, gelenkmomente


def zufallsstellung(zufall):
    return [math.radians(zufall.uniform(lo, hi)) for lo, hi in p.GELENKBEREICH]


class Vorwaerts(unittest.TestCase):
    def test_nullstellung_zeigt_senkrecht_nach_oben(self):
        lage = vorwaerts([0] * 6)
        hoehe = p.H_SCHULTER + p.L_OBERARM + p.L_UNTERARM + p.L_HAND
        np.testing.assert_allclose(lage[:3, 3], (0, 0, hoehe), atol=1e-12)
        np.testing.assert_allclose(lage[:3, :3], np.eye(3), atol=1e-12)

    def test_schulter_90_grad_streckt_arm_nach_x(self):
        lage = vorwaerts([0, math.pi / 2, 0, 0, 0, 0])
        reichweite = p.L_OBERARM + p.L_UNTERARM + p.L_HAND
        np.testing.assert_allclose(lage[:3, 3], (reichweite, 0, p.H_SCHULTER), atol=1e-12)


class Rueckwaerts(unittest.TestCase):
    def test_alle_acht_zweige_treffen_die_lage(self):
        zufall = random.Random(1)
        for _ in range(300):
            ziel = vorwaerts(zufallsstellung(zufall))
            for schulter in (1, -1):
                for ellbogen in (1, -1):
                    for hand in (1, -1):
                        q = rueckwaerts(ziel, ellbogen, hand, schulter)
                        np.testing.assert_allclose(vorwaerts(q), ziel, atol=1e-9)

    def test_zweigwahl_bestimmt_vorzeichen(self):
        ziel = vorwaerts([0.2, 0.6, 0.9, 0.4, 0.8, -0.3])
        for ellbogen in (1, -1):
            for hand in (1, -1):
                q = rueckwaerts(ziel, ellbogen, hand)
                self.assertEqual(math.copysign(1, q[2]), ellbogen)
                self.assertEqual(math.copysign(1, q[4]), hand)
        vorne, hinten = rueckwaerts(ziel), rueckwaerts(ziel, schulter=-1)
        self.assertAlmostEqual(abs(vorne[0] - hinten[0]), math.pi)

    def test_ausgangsstellung_ist_unter_den_loesungen(self):
        zufall = random.Random(2)
        for _ in range(300):
            q = np.array(zufallsstellung(zufall))
            gefunden = loesungen(vorwaerts(q))
            self.assertTrue(all(in_grenzen(l) for l in gefunden))
            self.assertTrue(
                any(np.allclose(l, q, atol=1e-7) for l in gefunden),
                f"Stellung {np.degrees(q).round(1)} nicht wiedergefunden",
            )

    def test_naechste_loesung_bleibt_bei_kleiner_bewegung_im_zweig(self):
        zufall = random.Random(3)
        for _ in range(100):
            q = np.array(zufallsstellung(zufall)) * 0.9  # Abstand zu den Grenzen
            if abs(q[4]) < 0.05 or abs(q[2]) < 0.05:
                continue  # an einer Singularität ist der Zweig nicht eindeutig
            np.testing.assert_allclose(naechste_loesung(vorwaerts(q), q), q, atol=1e-7)

    def test_singularitaet_hand_gestreckt(self):
        ziel = vorwaerts([0.3, 0.5, 0.7, 0.0, 0.0, 1.1])
        np.testing.assert_allclose(vorwaerts(rueckwaerts(ziel)), ziel, atol=1e-9)

    def test_singularitaet_hand_zurueckgeklappt(self):
        ziel = vorwaerts([0.3, 0.5, 0.7, 0.0, math.pi, 1.1])
        np.testing.assert_allclose(vorwaerts(rueckwaerts(ziel)), ziel, atol=1e-9)

    def test_ausser_reichweite(self):
        ziel = np.eye(4)
        ziel[0, 3] = 2.0
        with self.assertRaises(ValueError):
            rueckwaerts(ziel)
        self.assertEqual(loesungen(ziel), [])
        with self.assertRaises(ValueError):
            naechste_loesung(ziel, [0] * 6)


class Lastrechnung(unittest.TestCase):
    def test_senkrecht_ohne_versatz_kein_moment(self):
        # Nutzlast ist seitlich versetzt, daher nur die Eigenmassen prüfen
        momente = gelenkmomente([0] * 6, nutzlast=0.0)
        np.testing.assert_allclose(momente, 0, atol=1e-12)

    def test_gestreckt_gegen_handrechnung(self):
        """Arm waagrecht: Moment an J2, J3 und J5 = g · Σ m · Abstand zur Achse."""
        momente = gelenkmomente([0, math.pi / 2, 0, 0, 0, 0], nutzlast=0.0)
        ursprung = {2: 0.0, 3: p.L_OBERARM, 4: p.L_OBERARM,
                    5: p.L_OBERARM + p.L_UNTERARM,
                    6: p.L_OBERARM + p.L_UNTERARM + p.L_HAND}
        for gelenk in (2, 3, 5):
            erwartet = G * sum(
                m.kg * (ursprung[m.glied] + m.ort[2] - ursprung[gelenk])
                for m in p.MASSEN if m.glied >= gelenk
            )
            self.assertAlmostEqual(momente[gelenk - 1], erwartet, places=9)

    def test_seitlich_versetzte_nutzlast_belastet_j4_und_j6(self):
        # Arm waagrecht, Versatz der Nutzlast per J6 in die Waagrechte gedreht
        momente = gelenkmomente([0, math.pi / 2, 0, 0, 0, math.pi / 2], nutzlast=1.0)
        erwartet = G * 1.0 * p.ORT_NUTZLAST[0]
        self.assertAlmostEqual(momente[3], erwartet, places=9)
        self.assertAlmostEqual(momente[5], erwartet, places=9)

    def test_auslegung_erfuellt_die_sicherheit(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(bericht())


if __name__ == "__main__":
    unittest.main()
