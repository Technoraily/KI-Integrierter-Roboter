"""Auswertung der Messungen am J2-Prüfstand (Verfahren: docs/pruefstand-j2.md, Abschnitt Messen).

Aufruf:
  python software/j2_auswertung.py spiel --mm 1.20 1.45 1.32 1.07 --kg 1.13 2.20 1.13 0.06
  python software/j2_auswertung.py kriechen --punkte 0:0.00 10:0.02 60:0.05

Messuhrwerte in mm am Tastklotz, Waagenanzeigen in kg an der Lastbohrung.
"""

import argparse
import math
import sys

G = 9.81
L_HEBEL = 190.0  # mm, Achse -> Lastbohrung
R_TASTKLOTZ = 64.0  # mm, Achse -> Messuhr
GRENZE_SPIEL = 0.3  # Grad, Budget J2/J3 (docs/konzept.md, Fehlerbudget)
GRENZE_KRIECHEN = 0.1  # Grad im 24-h-Haltetest (docs/konzept.md, 3.8)
NULLMOMENT_TOLERANZ = 0.1  # Nm, so weit darf die Waage bei «Moment null» daneben liegen


def winkel(mm: float) -> float:
    """Messuhrweg am Tastklotz in Grad am Abtrieb."""
    return math.degrees(math.atan(mm / R_TASTKLOTZ))


def moment(anzeige_kg: float, gewicht_kg: float, hebel_kg: float) -> float:
    """Moment am Abtrieb in Nm; positiv = Hebel wird nach oben gezogen.

    hebel_kg: Waagenanzeige, bei der der unbelastete Hebel schwebt (Eigengewicht).
    """
    return (anzeige_kg - gewicht_kg - hebel_kg) * G * L_HEBEL / 1000


def spiel_und_steifigkeit(mm, kg, gewicht_kg=1.07, hebel_kg=0.0) -> dict:
    """mm und kg: die vier Ablesungen in der Reihenfolge Wert 1 bis Wert 4.

    Wert 1: Moment null von unten, Wert 2: +2 Nm, Wert 3: Moment null von oben, Wert 4: -2 Nm.
    """
    m = [moment(f, gewicht_kg, hebel_kg) for f in kg]
    spiel = winkel(abs(mm[2] - mm[0]))
    spanne = winkel(abs(mm[1] - mm[3]))
    hinweise = []
    for nr in (0, 2):
        if abs(m[nr]) > NULLMOMENT_TOLERANZ:
            hinweise.append(f"Wert {nr + 1}: Moment {m[nr]:+.2f} Nm statt 0 (Waage nachstellen oder Eigengewicht des Hebels eintragen)")
    if m[1] < 1.0 or m[3] > -1.0:
        hinweise.append(f"Wert 2 / Wert 4 liegen bei {m[1]:+.2f} / {m[3]:+.2f} Nm statt etwa +2 / -2 Nm")
    if spanne <= spiel:
        hinweise.append("Gesamtausschlag (Wert 2 bis 4) nicht grösser als das Spiel: Reihenfolge der Werte oder Messuhr prüfen")
        steifigkeit = None
    else:
        steifigkeit = (m[1] - m[3]) / (spanne - spiel)
    return {
        "momente_nm": m,
        "spiel_grad": spiel,
        "spiel_mm_lastbohrung": math.radians(spiel) * L_HEBEL,
        "spanne_grad": spanne,
        "steifigkeit_nm_pro_grad": steifigkeit,
        "spiel_ok": spiel <= GRENZE_SPIEL,
        "hinweise": hinweise,
    }


def kriechen(punkte) -> dict:
    """punkte: Liste (Minuten, mm); Drift zwischen erstem und letztem Punkt in Grad."""
    punkte = sorted(punkte)
    drift = winkel(punkte[-1][1] - punkte[0][1])
    dauer = punkte[-1][0] - punkte[0][0]
    return {"dauer_min": dauer, "drift_grad": drift, "feder_kriterium": abs(drift) > GRENZE_KRIECHEN}


def _bericht_spiel(e: dict) -> str:
    z = ["Momente (Nm): " + "  ".join(f"W{i + 1} {x:+.2f}" for i, x in enumerate(e["momente_nm"]))]
    z.append(f"Umkehrspiel (mit Reibung): {e['spiel_grad']:.3f} Grad = {e['spiel_mm_lastbohrung']:.2f} mm an der Lastbohrung"
             f" (Grenze {GRENZE_SPIEL} Grad: {'eingehalten' if e['spiel_ok'] else 'ÜBERSCHRITTEN'})")
    z.append(f"Gesamtausschlag Wert 2 bis 4: {e['spanne_grad']:.3f} Grad")
    k = e["steifigkeit_nm_pro_grad"]
    z.append("Steifigkeit: " + (f"{k:.1f} Nm/Grad (Schätzung des Gutachters 30 bis 100)" if k else "nicht auswertbar"))
    z += [f"Achtung: {h}" for h in e["hinweise"]]
    return "\n".join(z)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="befehl", required=True)
    s = sub.add_parser("spiel", help="Umkehrspiel und Steifigkeit aus den vier Ablesungen")
    s.add_argument("--mm", type=float, nargs=4, required=True, metavar=("W1", "W2", "W3", "W4"))
    s.add_argument("--kg", type=float, nargs=4, required=True, metavar=("F1", "F2", "F3", "F4"))
    s.add_argument("--gewicht", type=float, default=1.07, help="angehängtes Gewicht in kg (gewogen)")
    s.add_argument("--hebel", type=float, default=0.0, help="Waagenanzeige, bei der der leere Hebel schwebt, in kg")
    k = sub.add_parser("kriechen", help="Drift über die Zeit")
    k.add_argument("--punkte", nargs="+", required=True, metavar="MIN:MM")
    a = ap.parse_args()
    if a.befehl == "spiel":
        print(_bericht_spiel(spiel_und_steifigkeit(a.mm, a.kg, a.gewicht, a.hebel)))
    else:
        e = kriechen([(float(p.split(":")[0]), float(p.split(":")[1])) for p in a.punkte])
        if e["feder_kriterium"]:
            urteil = "ÜBERSCHRITTEN, Ausgleichsfeder prüfen"
        elif e["dauer_min"] < 24 * 60:
            urteil = f"bisher darunter, aber erst {e['dauer_min'] / 60:.1f} h gemessen: noch kein Urteil"
        else:
            urteil = "eingehalten"
        print(f"Drift {e['drift_grad']:+.3f} Grad in {e['dauer_min']:g} min (Grenze {GRENZE_KRIECHEN} Grad in 24 h: {urteil})")


if __name__ == "__main__":
    main()
