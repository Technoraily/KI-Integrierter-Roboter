import math
import random
import unittest

import numpy as np

from roboterarm import parameter as p
from roboterarm.kinematik import rueckwaerts, vorwaerts
from roboterarm.lastrechnung import G, gelenkmomente


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
    def test_rundlauf_fk_ik_fk(self):
        zufall = random.Random(1)
        for _ in range(500):
            q = [math.radians(zufall.uniform(lo, hi)) for lo, hi in p.GELENKBEREICH]
            ziel = vorwaerts(q)
            for ellbogen in (1, -1):
                for hand in (1, -1):
                    loesung = rueckwaerts(ziel, ellbogen, hand)
                    np.testing.assert_allclose(vorwaerts(loesung), ziel, atol=1e-9)

    def test_singularitaet_hand_gestreckt(self):
        ziel = vorwaerts([0.3, 0.5, 0.7, 0.0, 0.0, 1.1])
        np.testing.assert_allclose(vorwaerts(rueckwaerts(ziel)), ziel, atol=1e-9)

    def test_ausser_reichweite(self):
        ziel = np.eye(4)
        ziel[0, 3] = 2.0
        with self.assertRaises(ValueError):
            rueckwaerts(ziel)


class Lastrechnung(unittest.TestCase):
    def test_senkrecht_ohne_versatz_kein_moment(self):
        # Nutzlast ist seitlich versetzt, daher nur die Eigenmassen prüfen
        momente = gelenkmomente([0] * 6, nutzlast=0.0)
        np.testing.assert_allclose(momente, 0, atol=1e-12)

    def test_schulter_gestreckt_gegen_handrechnung(self):
        momente = gelenkmomente([0, math.pi / 2, 0, 0, 0, 0], nutzlast=0.0)
        hebel = {2: 0.0, 3: p.L_OBERARM, 4: p.L_OBERARM,
                 5: p.L_OBERARM + p.L_UNTERARM,
                 6: p.L_OBERARM + p.L_UNTERARM + p.L_HAND}
        erwartet = G * sum(m.kg * (hebel[m.glied] + m.ort[2]) for m in p.MASSEN)
        self.assertAlmostEqual(momente[1], erwartet, places=9)


if __name__ == "__main__":
    unittest.main()
