import math
import unittest

import j2_auswertung as a


def mm(grad):
    return a.R_TASTKLOTZ * math.tan(math.radians(grad))


class Auswertung(unittest.TestCase):
    def test_modell_mit_lose_und_federung(self):
        # Obere Anlage bei 0, Lose s = 0,10 Grad, Steifigkeit k = 50 Nm/Grad
        s, k = 0.10, 50.0
        winkel = [-s, 2 / k, 0.0, -s - 2 / k]  # Wert 1 bis 4
        kg = [1.07, 2.15, 1.07, 0.0]  # Moment null / +2 / null / -2 Nm
        e = a.spiel_und_steifigkeit([mm(w) for w in winkel], kg)
        self.assertAlmostEqual(e["spiel_grad"], s, places=3)
        self.assertAlmostEqual(e["steifigkeit_nm_pro_grad"], k, delta=0.7)
        self.assertEqual(e["hinweise"], [])

    def test_momente(self):
        self.assertAlmostEqual(a.moment(1.07, 1.07, 0.0), 0.0)
        self.assertAlmostEqual(a.moment(2.15, 1.07, 0.0), 2.0, delta=0.02)
        self.assertAlmostEqual(a.moment(0.0, 1.07, 0.0), -2.0, delta=0.02)

    def test_eigengewicht_hebel_verschiebt_nullpunkt(self):
        self.assertAlmostEqual(a.moment(1.13, 1.07, 0.06), 0.0)

    def test_falsche_reihenfolge_wird_gemeldet(self):
        e = a.spiel_und_steifigkeit([0.0, 0.01, 0.5, 0.0], [1.07, 2.15, 1.07, 0.0])
        self.assertIsNone(e["steifigkeit_nm_pro_grad"])
        self.assertTrue(e["hinweise"])

    def test_waage_nicht_bei_moment_null(self):
        e = a.spiel_und_steifigkeit([0.0, 0.2, 0.1, -0.2], [1.5, 2.15, 1.07, 0.0])
        self.assertTrue(any("Wert 1" in h for h in e["hinweise"]))

    def test_kriechen(self):
        e = a.kriechen([(60, 0.20), (0, 0.0)])
        self.assertAlmostEqual(e["drift_grad"], a.winkel(0.20))
        self.assertTrue(e["feder_kriterium"])  # 0,20 mm = 0,18 Grad
        self.assertFalse(a.kriechen([(0, 0.0), (60, 0.05)])["feder_kriterium"])

    def test_zehntelgrad_entspricht_elf_hundertstel_mm(self):
        self.assertAlmostEqual(mm(0.1), 0.1117, places=3)  # docs/pruefstand-j2.md: 0,1 Grad = 0,11 mm


if __name__ == "__main__":
    unittest.main()
