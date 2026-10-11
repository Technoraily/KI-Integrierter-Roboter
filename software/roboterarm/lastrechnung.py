"""Statische Lastrechnung: Schwerkraftmomente aller Gelenke über den Arbeitsraum.

Aufruf:  python -m roboterarm.lastrechnung
Die Ausgleichsfeder an J2 ist nicht eingerechnet (konservativ), ebenso keine
Beschleunigungsmomente - dafür steht die geforderte Sicherheit.
"""

import itertools
import math

import numpy as np

from . import parameter as p
from .kinematik import ACHSEN, gliedlagen

G = 9.81
SICHERHEIT_SOLL = 1.5


def _gliedmassen(nutzlast: float) -> np.ndarray:
    """Je Glied eine Zeile (m·x, m·y, m·z, m) im Koordinatensystem des Glieds."""
    summen = np.zeros((6, 4))
    for glied, ort, kg in [(m.glied, m.ort, m.kg) for m in p.MASSEN] + [
        (6, p.ORT_NUTZLAST, nutzlast)
    ]:
        summen[glied - 1] += (*(kg * np.array(ort)), kg)
    return summen


def gelenkmomente(q, nutzlast: float, lagen=None, gliedmassen=None) -> np.ndarray:
    """Betrag des Schwerkraftmoments an jedem Gelenk (Nm) in Stellung q (rad)."""
    lagen = gliedlagen(q) if lagen is None else lagen
    gliedmassen = _gliedmassen(nutzlast) if gliedmassen is None else gliedmassen

    momente = np.zeros(6)
    moment_1, masse = np.zeros(3), 0.0  # Σ m·ort (Welt) und Σ m aller Glieder ab Gelenk i
    for i in reversed(range(6)):  # Gelenk i trägt alle Glieder ab i
        moment_1 += (lagen[i] @ gliedmassen[i])[:3]
        masse += gliedmassen[i, 3]
        achse = lagen[i][:3, 2 if ACHSEN[i] == "z" else 1]
        hebel_mal_masse = moment_1 - masse * lagen[i][:3, 3]
        momente[i] = achse @ np.cross(hebel_mal_masse, (0.0, 0.0, -G))
    return np.abs(momente)


def _raster():
    """Gelenkstellungen über den ganzen Bereich; q1 ist für die Schwerkraft egal."""
    def stufen(gelenk, schritt):
        lo, hi = p.GELENKBEREICH[gelenk]
        return np.radians(np.arange(lo, hi + 1e-6, schritt))

    q4 = np.radians((0.0, 90.0, 180.0, 270.0))
    return itertools.product(stufen(1, 10), stufen(2, 15), q4, stufen(4, 22), q4)


def maximalmomente(nutzlast: float, max_ausladung: float | None = None):
    """Grösstes Moment je Gelenk und grösste erreichte Ausladung des Flanschs."""
    groesste = np.zeros(6)
    reichweite = 0.0
    gliedmassen = _gliedmassen(nutzlast)
    for q2, q3, q4, q5, q6 in _raster():
        q = (0.0, q2, q3, q4, q5, q6)
        lagen = gliedlagen(q)
        flansch = lagen[-1][:3, 3]
        ausladung = math.hypot(flansch[0], flansch[1])
        if max_ausladung is not None and ausladung > max_ausladung:
            continue
        reichweite = max(reichweite, ausladung)
        groesste = np.maximum(groesste, gelenkmomente(q, nutzlast, lagen, gliedmassen))
    return groesste, reichweite


def bericht() -> bool:
    faelle = (
        ("1,0 kg im ganzen Arbeitsraum", 1.0, None),
        ("0,5 kg im ganzen Arbeitsraum", 0.5, None),
    )
    alles_ok = True
    for titel, nutzlast, grenze in faelle:
        momente, reichweite = maximalmomente(nutzlast, grenze)
        print(
            f"\n{titel}  (Flansch bis {reichweite * 1000:.0f} mm, "
            f"Lastschwerpunkt {p.ORT_NUTZLAST[2] * 1000:.0f} mm davor)"
        )
        print(f"{'Gelenk':<7}{'Last Nm':>9}{'verfügbar Nm':>14}{'Sicherheit':>12}{'°/s':>7}")
        for antrieb, last in zip(p.ANTRIEBE, momente):
            # J1 trägt bei senkrechter Achse keine Schwerkraft
            sicherheit = antrieb.abtriebsmoment / last if last > 1e-6 else math.inf
            ok = sicherheit >= SICHERHEIT_SOLL
            alles_ok &= ok
            print(
                f"{antrieb.name:<7}{last:>9.2f}{antrieb.abtriebsmoment:>14.2f}"
                f"{sicherheit:>12.1f}{antrieb.gelenkgeschwindigkeit:>7.0f}"
                f"{'' if ok else '  <-- zu knapp'}"
            )
    bewegt = sum(m.kg for m in p.MASSEN)
    print(f"\nBewegte Masse ab Schulter ohne Nutzlast: {bewegt:.2f} kg")
    return alles_ok


if __name__ == "__main__":
    raise SystemExit(0 if bericht() else 1)
