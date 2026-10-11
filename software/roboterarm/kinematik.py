"""Vorwärts- und Rückwärtskinematik des 6-Achs-Knickarms mit Zentralhand.

Kette (Nullstellung: Arm senkrecht nach oben, alle Winkel 0):
    Rz(q1) · T(H) · Ry(q2) · T(L1) · Ry(q3) · Rz(q4) · T(L2) · Ry(q5) · T(L3) · Rz(q6)
T(x) ist eine Verschiebung um x entlang z. Positives q2 neigt den Arm nach +x.
Winkel in Radiant, Längen in Metern.
"""

import math

import numpy as np

from . import parameter as p

ACHSEN = ("z", "y", "y", "z", "y", "z")
# Verschiebung entlang z vor dem jeweiligen Gelenk
VERSATZ = (0.0, p.H_SCHULTER, p.L_OBERARM, 0.0, p.L_UNTERARM, p.L_HAND)


def _rot(achse: str, winkel: float) -> np.ndarray:
    c, s = math.cos(winkel), math.sin(winkel)
    t = np.eye(4)
    if achse == "z":
        t[:2, :2] = ((c, -s), (s, c))
    else:  # y
        t[0, 0], t[0, 2], t[2, 0], t[2, 2] = c, s, -s, c
    return t


def _schub(z: float) -> np.ndarray:
    t = np.eye(4)
    t[2, 3] = z
    return t


def gliedlagen(q) -> list[np.ndarray]:
    """Lage (4x4) jedes Glieds 1..6 in Weltkoordinaten.

    Der Ursprung von Glied i liegt auf der Achse von Gelenk i; die Gelenkachse
    ist die y- bzw. z-Achse des Glieds laut ACHSEN. Glied 6 ist der Flansch.
    """
    t = np.eye(4)
    lagen = []
    for achse, versatz, winkel in zip(ACHSEN, VERSATZ, q):
        t = t @ _schub(versatz) @ _rot(achse, winkel)
        lagen.append(t)
    return lagen


def vorwaerts(q) -> np.ndarray:
    """Flanschlage (4x4) für sechs Gelenkwinkel."""
    return gliedlagen(q)[-1]


def rueckwaerts(ziel: np.ndarray, ellbogen: int = 1, hand: int = 1) -> np.ndarray:
    """Gelenkwinkel für eine Flanschlage (4x4).

    ellbogen = +1/-1 wählt das Vorzeichen von q3, hand = +1/-1 das von q5.
    Wirft ValueError, wenn das Ziel ausserhalb der Reichweite liegt.
    """
    r, pos = ziel[:3, :3], ziel[:3, 3]
    mitte = pos - p.L_HAND * r[:, 2]  # Handgelenkmitte

    q1 = math.atan2(mitte[1], mitte[0])
    radial = math.hypot(mitte[0], mitte[1])
    hoehe = mitte[2] - p.H_SCHULTER

    l1, l2 = p.L_OBERARM, p.L_UNTERARM
    c3 = (radial**2 + hoehe**2 - l1**2 - l2**2) / (2 * l1 * l2)
    if abs(c3) > 1 + 1e-9:
        raise ValueError("Ziel ausserhalb der Reichweite")
    q3 = ellbogen * math.acos(max(-1.0, min(1.0, c3)))
    q2 = math.atan2(radial, hoehe) - math.atan2(l2 * math.sin(q3), l1 + l2 * math.cos(q3))

    # Rest ist eine ZYZ-Zerlegung: R36 = Rz(q4) · Ry(q5) · Rz(q6)
    r03 = (_rot("z", q1) @ _rot("y", q2 + q3))[:3, :3]
    r36 = r03.T @ r
    s5 = math.hypot(r36[0, 2], r36[1, 2])
    if s5 < 1e-9:  # Singularität: J4 und J6 fluchten, q4 frei gewählt
        q4, q5, q6 = 0.0, math.atan2(0.0, r36[2, 2]), math.atan2(r36[1, 0], r36[0, 0])
        if r36[2, 2] < 0:
            q6 = math.atan2(-r36[1, 0], -r36[0, 0])
    else:
        q5 = hand * math.atan2(s5, r36[2, 2])
        q4 = math.atan2(hand * r36[1, 2], hand * r36[0, 2])
        q6 = math.atan2(hand * r36[2, 1], -hand * r36[2, 0])
    return np.array([q1, q2, q3, q4, q5, q6])
