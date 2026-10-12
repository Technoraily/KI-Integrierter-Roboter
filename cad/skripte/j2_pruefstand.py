"""J2-Pruefstand (Schultergelenk, drei Riemenstufen) in Fusion 360 aufbauen.

Wird im Fusion-Python ausgefuehrt (z. B. ueber das MCP-Add-in mit
exec(open(pfad, encoding="utf-8").read())). Das Skript loescht eine vorhandene
Baugruppe "J2_Pruefstand" und baut sie aus den Massen unten neu auf.
Alle Masse in mm; Ursprung: Tischflaeche unter der Abtriebsachse, z = 0 an der
Innenflaeche der linken Wange (Motorseite), z waechst zur rechten Wange.
"""
import math
from math import pi, sin, cos, atan2, hypot, asin, sqrt, radians

import adsk.core
import adsk.fusion

MM = 0.1  # Fusion rechnet intern in cm

# ---------------------------------------------------------------- Masse
W = 56.0            # lichte Weite zwischen den Wangen
T_WANGE = 8.0
D_WELLE = 8.0
L_WELLE = 70.0
D_LAGER, B_LAGER = 22.0, 7.0      # 608
TOL_LAGERSITZ = 0.15              # Uebermass Bohrung, nach Testdruck anpassen
D_EINSCHMELZ_M3 = 4.0             # Bohrung fuer M3-Einschmelzgewinde, nach Testdruck anpassen
T_EINSCHMELZ = 7.0                # Bohrungstiefe in Wangen (1 mm Restwand)
T_EINSCHMELZ_TIEF = 9.0           # Bohrungstiefe, wo M3 x 16 eingeschraubt wird
D_M3_DURCH = 3.4
D_BOHRUNG_WELLE = 8.15            # gedruckte Nabe auf 8-mm-Welle (Wellen A und B)
D_BOHRUNG_ABTRIEB = 8.05          # stramm: Radialspiel am Abtrieb ginge in die Messung ein
D_ANLAGE = 12.0                   # Anlagebund am Lager-Innenring (unter der Dichtung bleiben)
D_MITNAHME_M4 = 3.9               # Bohrung, in die sich die M4-Mitnahmeschraube spielfrei einschneidet

# Achsen (x, y)
Y_ABTRIEB = 170.0
C1, C2, C3 = 51.3, 61.3, 111.5    # Achsabstaende Stufe 1..3 (Stufe 2/3 kuerzer als Nennmass, Spannrolle gleicht aus)
W_OB, W_BA, W_AM = radians(-100), radians(-20), radians(60)
O = (0.0, Y_ABTRIEB)
B = (O[0] + C3 * cos(W_OB), O[1] + C3 * sin(W_OB))
A = (B[0] + C2 * cos(W_BA), B[1] + C2 * sin(W_BA))
M = (A[0] + C1 * cos(W_AM), A[1] + C1 * sin(W_AM))
U_MOTOR = (cos(W_AM), sin(W_AM))  # Spannrichtung Motor
HUB_MOTOR = 3.0                   # Langloch +-

# Riemen: Teilung, Zaehne, Laenge
def pd(z, p):
    return z * p / pi

PD20, PD72 = pd(20, 2), pd(72, 2)
PD16, PD64 = pd(16, 3), pd(64, 3)
PD18, PD90 = pd(18, 5), pd(90, 5)
L_GT2, L_3M, L_5M = 200.0, 252.0, 525.0
# Zahnluecke gedruckte Scheiben: (Kopfkreis = Teilkreis - 2u, Lueckenradius, Lueckentiefe)
PROFIL = {
    "GT2": dict(u2=0.508, r=0.65, h=0.80, t_in=0.25, t_out=0.75),
    "3M": dict(u2=0.762, r=0.95, h=1.27, t_in=0.38, t_out=0.85),
    "5M": dict(u2=1.143, r=1.60, h=2.16, t_in=0.57, t_out=1.17),
}

# Spannrollen
R_ROLLE_5M = 16.0                 # gedruckte Rolle ueber 2x 608
R_ROLLE_3M = 11.0                 # 2x 608 blank
Y_ROLLE_5M = 90.0                 # Langloch waagrecht auf dieser Hoehe
X_ROLLE_3M = 10.0                 # Langloch senkrecht an dieser Stelle
HUB_ROLLE = 8.0                   # Langloch +-

# Axiale Lage (z)
Z_5M = (3.5, 20.0)                # Zahnbreite Z90 / Ritzel Z18
Z_GT2 = (7.5, 19.5)               # Zahnbreite Z72
Z_3M = (30.0, 46.5)               # Zahnbreite Z64 / Ritzel Z16
Z_HEBEL = (20.0, 40.0)

# Rahmen
X_STELL_5M = -80.0               # Grund der Nische fuer die Stellschraube der 5M-Rolle
UMRISS = [(-95, 0), (100, 0), (100, 145), (45, 196), (-45, 196), (-95, 150),
          (-95, Y_ROLLE_5M + 7), (X_STELL_5M, Y_ROLLE_5M + 7), (X_STELL_5M, Y_ROLLE_5M - 7), (-95, Y_ROLLE_5M - 7)]
TRAEGER = {  # Name: (x, y) Mitte, Querschnitt 14 x 24. Die oberen sind zugleich Endanschlaege des Hebels.
    "Quertraeger_unten_links": (-85, 12),
    "Quertraeger_unten_rechts": (88, 12),
    "Quertraeger_oben_links": (-85, 124),
    "Quertraeger_oben_rechts": (88, 124),
}
TRAEGER_B, TRAEGER_H, TRAEGER_LOCH = 14.0, 24.0, 6.0

# Lasthebel
R_HEBELNABE = 35.0
R_LOCHKREIS = 27.0
L_HEBEL = 190.0                   # Achse -> Lastbohrung
B_HEBEL_NABE, B_HEBEL_ENDE = 60.0, 30.0   # Arm verjuengt sich

# Messzeiger (unbelastet, auf der Z90-Scheibe) und Messuhrhalter
R_ZEIGER = (37.0, 72.0)           # radiale Erstreckung
B_ZEIGER = 14.0
Z_ZEIGER = (20.0, 32.0)
R_ZEIGER_SCHRAUBEN = (44.0, 60.0)
R_MESS = 64.0                     # Radius, an dem die Messuhr antastet
D_MESSUHR_SCHAFT = 8.0            # stramm drucken, auf den Schaft der Messuhr aufreiben
R_TASTKLOTZ = (56.0, 72.0)        # Tastklotz am Zeigerende
B_TASTKLOTZ = 30.0                # Tastflaechen 15 mm ueber der Zeigermitte
Z_TASTKLOTZ = (20.0, 46.0)
Z_MESSUHR = 38.0                  # Messuhr-Achse: Gehaeuse bleibt neben Scheibe und 5M-Riemen (z <= 20)

# Blockierstift: M3 x 25 durch die Z72-Scheibe in die linke Wange (trennt Motor und Stufe 1 von der Messung)
R_BLOCKIER = 17.0


# ---------------------------------------------------------------- Riemengeometrie
def tangente(c1, r1, s1, c2, r2, s2):
    dx, dy = c2[0] - c1[0], c2[1] - c1[1]
    d = hypot(dx, dy)
    th = atan2(dy, dx) + asin(max(-1.0, min(1.0, (s1 * r1 - s2 * r2) / d)))
    n = (-sin(th), cos(th))
    return ((c1[0] - s1 * r1 * n[0], c1[1] - s1 * r1 * n[1]),
            (c2[0] - s2 * r2 * n[0], c2[1] - s2 * r2 * n[1]), th)


def riemenlaenge(kreise):
    """kreise: [(Mitte, Radius, s)] in Laufrichtung; s=+1 Scheibe innen (Gegenuhrzeigersinn), -1 Rueckenrolle."""
    n = len(kreise)
    tang = [tangente(*kreise[i], *kreise[(i + 1) % n]) for i in range(n)]
    L, wraps = 0.0, []
    for i in range(n):
        p1, p2, th = tang[i]
        L += hypot(p2[0] - p1[0], p2[1] - p1[1])
        w = ((th - tang[i - 1][2]) * kreise[i][2]) % (2 * pi)
        wraps.append(w)
        L += kreise[i][1] * w
    return L, wraps, tang


def rolle_suchen(c1, r1, c2, r2, Lsoll, ri, start, richtung, smax):
    """Rollenmitte auf der Geraden start + s*richtung, bei der der Riemen genau Lsoll lang ist."""
    best = None
    for i in range(int(smax * 50) + 1):
        s = i / 50
        ci = (start[0] + s * richtung[0], start[1] + s * richtung[1])
        # Rolle darf den Riemen nicht auf eine Scheibe druecken
        if min(hypot(ci[0] - c1[0], ci[1] - c1[1]) - r1, hypot(ci[0] - c2[0], ci[1] - c2[1]) - r2) < ri + 1.5:
            continue
        L, wraps, tang = riemenlaenge([(c1, r1, 1), (c2, r2, 1), (ci, ri, -1)])
        if not (0.003 < wraps[2] < 3.0):
            continue
        trume = [hypot(t[1][0] - t[0][0], t[1][1] - t[0][1]) for t in tang]
        if min(trume) < 8.0:
            continue
        if best is None or abs(L - Lsoll) < abs(best[1] - Lsoll):
            best = (ci, L, wraps, trume)
    if best is None or abs(best[1] - Lsoll) > 0.05:
        raise RuntimeError("Spannrolle: keine gueltige Lage fuer Riemenlaenge %.1f gefunden" % Lsoll)
    return best


I3, L3_ist, WRAP3, TRUME3 = rolle_suchen(B, PD18 / 2, O, PD90 / 2, L_5M, R_ROLLE_5M + PROFIL["5M"]["t_out"],
                                 (-95, Y_ROLLE_5M), (1, 0), 70)
I2, L2_ist, WRAP2, TRUME2 = rolle_suchen(A, PD16 / 2, B, PD64 / 2, L_3M, R_ROLLE_3M + PROFIL["3M"]["t_out"],
                                 (X_ROLLE_3M, 0), (0, 1), 50)
I3 = (round(I3[0], 1), I3[1])
I2 = (I2[0], round(I2[1], 1))


def spannreserve(c1, r1, c2, r2, ri, ci, u, Lsoll):
    """Wie viel Riemenlaenge die Rolle bis zum Ende des Langlochs bzw. bis zur naechsten Scheibe noch aufnimmt."""
    L_max = Lsoll
    for i in range(1, int(HUB_ROLLE * 10) + 1):
        c = (ci[0] + u[0] * i / 10, ci[1] + u[1] * i / 10)
        if min(hypot(c[0] - c1[0], c[1] - c1[1]) - r1, hypot(c[0] - c2[0], c[1] - c2[1]) - r2) < ri + 1.0:
            break
        L_max = riemenlaenge([(c1, r1, 1), (c2, r2, 1), (c, ri, -1)])[0]
    return L_max - Lsoll


RESERVE3 = spannreserve(B, PD18 / 2, O, PD90 / 2, R_ROLLE_5M + PROFIL["5M"]["t_out"], I3, (1, 0), L_5M)
RESERVE2 = spannreserve(A, PD16 / 2, B, PD64 / 2, R_ROLLE_3M + PROFIL["3M"]["t_out"], I2, (0, 1), L_3M)

# Hebelkontur (Grundstellung: Arm nach oben) und Anschlagwinkel an den oberen Quertraegern
HEBEL_KONTUR = [(-B_HEBEL_NABE / 2, 15.0), (B_HEBEL_NABE / 2, 15.0), (B_HEBEL_ENDE / 2, L_HEBEL), (-B_HEBEL_ENDE / 2, L_HEBEL)]


def anschlagwinkel(traeger, richtung):
    """Winkel aus der Senkrechten, bei dem der Hebelarm den Quertraeger beruehrt (richtung +1: nach links)."""
    cx, cy = traeger
    for i in range(0, 1300):
        w = radians(i / 10) * richtung
        for k in range(4):
            a, b = HEBEL_KONTUR[k], HEBEL_KONTUR[(k + 1) % 4]
            for j in range(101):
                x, y = a[0] + (b[0] - a[0]) * j / 100, a[1] + (b[1] - a[1]) * j / 100
                X = O[0] + x * cos(w) - y * sin(w)
                Y = O[1] + x * sin(w) + y * cos(w)
                if abs(X - cx) <= TRAEGER_B / 2 and abs(Y - cy) <= TRAEGER_H / 2:
                    return i / 10
    return None


ANSCHLAG_LINKS = anschlagwinkel(TRAEGER["Quertraeger_oben_links"], 1)
ANSCHLAG_RECHTS = anschlagwinkel(TRAEGER["Quertraeger_oben_rechts"], -1)
W_BLOCKIER = W_BA + radians(45)   # 25 Grad neben den Gewindestiften der Nabe, auf der vom 3M-Riemen abgewandten Seite
BLOCKIER = [(A[0] + R_BLOCKIER * cos(W_BLOCKIER + i * pi / 2), A[1] + R_BLOCKIER * sin(W_BLOCKIER + i * pi / 2)) for i in range(4)]
MESSHALTER = {"links": -R_MESS, "rechts": R_MESS}   # x der Messuhr; der Halter sitzt aussen an der rechten Wange


# ---------------------------------------------------------------- Fusion-Helfer
app = adsk.core.Application.get()
des = adsk.fusion.Design.cast(app.activeProduct)
root = des.rootComponent
VI = adsk.core.ValueInput
P3 = adsk.core.Point3D
NEU = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
JOIN = adsk.fusion.FeatureOperations.JoinFeatureOperation
CUT = adsk.fusion.FeatureOperations.CutFeatureOperation


def p(x, y):
    return P3.create(x * MM, y * MM, 0)


def alle_profile(sk):
    col = adsk.core.ObjectCollection.create()
    for pr in sk.profiles:
        col.add(pr)
    return col


def extrudiere(comp, profile, z0, z1, op, body=None):
    inp = comp.features.extrudeFeatures.createInput(profile, op)
    inp.startExtent = adsk.fusion.OffsetStartDefinition.create(VI.createByReal(z0 * MM))
    inp.setDistanceExtent(False, VI.createByReal((z1 - z0) * MM))
    if body is not None:
        inp.participantBodies = [body]
    return comp.features.extrudeFeatures.add(inp)


def skizze(comp, name):
    sk = comp.sketches.add(comp.xYConstructionPlane)
    sk.name = name
    return sk


def zylinder(comp, c, d, z0, z1, body=None, name=None):
    """Vollzylinder; mit body wird angefuegt."""
    sk = skizze(comp, (name or "Zyl") + "_Skizze")
    sk.sketchCurves.sketchCircles.addByCenterRadius(p(*c), d / 2 * MM)
    f = extrudiere(comp, alle_profile(sk), z0, z1, JOIN if body else NEU, body)
    b = body or f.bodies.item(0)
    if name and not body:
        b.name = name
    return b


def bohrung(comp, body, punkte, d, z0, z1, name="Bohrung"):
    sk = skizze(comp, name)
    for c in punkte:
        sk.sketchCurves.sketchCircles.addByCenterRadius(p(*c), d / 2 * MM)
    extrudiere(comp, alle_profile(sk), z0, z1, CUT, body)


def langloch_kurven(sk, c, u, a, r):
    """Langloch: Mitte c, Richtung u (Einheitsvektor), halbe Laenge a, Radius r."""
    n = (-u[1], u[0])
    c1 = (c[0] - a * u[0], c[1] - a * u[1])
    c2 = (c[0] + a * u[0], c[1] + a * u[1])
    L = sk.sketchCurves.sketchLines
    Ar = sk.sketchCurves.sketchArcs
    L.addByTwoPoints(p(c1[0] + r * n[0], c1[1] + r * n[1]), p(c2[0] + r * n[0], c2[1] + r * n[1]))
    L.addByTwoPoints(p(c1[0] - r * n[0], c1[1] - r * n[1]), p(c2[0] - r * n[0], c2[1] - r * n[1]))
    Ar.addByThreePoints(p(c2[0] + r * n[0], c2[1] + r * n[1]), p(c2[0] + r * u[0], c2[1] + r * u[1]),
                        p(c2[0] - r * n[0], c2[1] - r * n[1]))
    Ar.addByThreePoints(p(c1[0] + r * n[0], c1[1] + r * n[1]), p(c1[0] - r * u[0], c1[1] - r * u[1]),
                        p(c1[0] - r * n[0], c1[1] - r * n[1]))


def langloecher(comp, body, liste, z0, z1, name="Langloch"):
    """liste: [(Mitte, Richtung, halbe Laenge, Durchmesser)]"""
    sk = skizze(comp, name)
    sk.isComputeDeferred = True
    for c, u, a, d in liste:
        langloch_kurven(sk, c, u, a, d / 2)
    sk.isComputeDeferred = False
    extrudiere(comp, alle_profile(sk), z0, z1, CUT, body)


def polygon(comp, punkte, z0, z1, name):
    sk = skizze(comp, name + "_Umriss")
    L = sk.sketchCurves.sketchLines
    for i in range(len(punkte)):
        L.addByTwoPoints(p(*punkte[i]), p(*punkte[(i + 1) % len(punkte)]))
    b = extrudiere(comp, alle_profile(sk), z0, z1, NEU).bodies.item(0)
    b.name = name
    return b


def zahnscheibe(comp, c, zaehne, teilung, profil, z0, z1, name):
    """Gedruckte Zahnscheibe mit vereinfachter U-Luecke (Radius r, Tiefe h)."""
    pr = PROFIL[profil]
    Ro = zaehne * teilung / pi / 2 - pr["u2"] / 2
    r, h = pr["r"], pr["h"]
    rc = Ro - h + r
    ya = sqrt(Ro * Ro - r * r)
    sk = skizze(comp, name + "_Zahnkontur")
    sk.isComputeDeferred = True
    L = sk.sketchCurves.sketchLines
    Ar = sk.sketchCurves.sketchArcs

    def pt(phi, rad, tang):
        return p(c[0] + rad * cos(phi) - tang * sin(phi), c[1] + rad * sin(phi) + tang * cos(phi))

    for i in range(zaehne):
        phi = 2 * pi * i / zaehne
        phi2 = 2 * pi * (i + 1) / zaehne
        L.addByTwoPoints(pt(phi, ya, -r), pt(phi, rc, -r))
        Ar.addByThreePoints(pt(phi, rc, -r), pt(phi, rc - r, 0), pt(phi, rc, r))
        L.addByTwoPoints(pt(phi, rc, r), pt(phi, ya, r))
        Ar.addByThreePoints(pt(phi, ya, r), pt((phi + phi2) / 2, Ro, 0), pt(phi2, ya, -r))
    sk.isComputeDeferred = False
    if sk.profiles.count != 1:
        raise RuntimeError("%s: Zahnkontur ergibt %d Profile" % (name, sk.profiles.count))
    b = extrudiere(comp, alle_profile(sk), z0, z1, NEU).bodies.item(0)
    b.name = name
    return b


def radialbohrung(comp, body, c, richtung, r_aussen, z, stufen, name="Radialbohrung"):
    """Bohrung von aussen radial zur Achse. richtung: 'x' oder 'y' (positive Seite).
    stufen: [(Durchmesser, Tiefe ab r_aussen)]."""
    basis = comp.yZConstructionPlane if richtung == "x" else comp.xZConstructionPlane
    soll = (c[0] if richtung == "x" else c[1]) + r_aussen
    planes = comp.constructionPlanes
    ebene = None
    for vz in (1, -1):
        inp = planes.createInput()
        inp.setByOffset(basis, VI.createByReal(vz * soll * MM))
        ebene = planes.add(inp)
        o = ebene.geometry.origin
        ist = (o.x if richtung == "x" else o.y) / MM
        if abs(ist - soll) < 1e-6:
            break
        ebene.deleteMe()
    ebene.name = name + "_Ebene"
    for d, tiefe in stufen:
        sk = comp.sketches.add(ebene)
        sk.name = name
        m = P3.create(soll * MM, c[1] * MM, z * MM) if richtung == "x" else P3.create(c[0] * MM, soll * MM, z * MM)
        sk.sketchCurves.sketchCircles.addByCenterRadius(sk.modelToSketchSpace(m), d / 2 * MM)
        inp = comp.features.extrudeFeatures.createInput(alle_profile(sk), CUT)
        inp.setSymmetricExtent(VI.createByReal(2 * tiefe * MM), True)
        inp.participantBodies = [body]
        comp.features.extrudeFeatures.add(inp)


def riemen(comp, kreise, profil, z0, z1, name):
    """Riemen als Band um die Teilkreise (nur zur Darstellung und Kollisionspruefung)."""
    pr = PROFIL[profil]
    sk = skizze(comp, name + "_Verlauf")
    sk.isComputeDeferred = True
    for delta, vz in ((pr["u2"] / 2 - 0.03, -1), (pr["t_out"] - 0.03, 1)):
        ks = [(c, r + vz * s * delta, s) for c, r, s in kreise]
        _, wraps, tang = riemenlaenge(ks)
        n = len(ks)
        for i in range(n):
            p1, p2, th = tang[i]
            sk.sketchCurves.sketchLines.addByTwoPoints(p(*p1), p(*p2))
            c, r, s = ks[i]
            pin = tang[i - 1][1]
            a0 = atan2(pin[1] - c[1], pin[0] - c[0])
            am = a0 + s * wraps[i] / 2
            sk.sketchCurves.sketchArcs.addByThreePoints(p(*pin), p(c[0] + r * cos(am), c[1] + r * sin(am)), p(*p1))
    sk.isComputeDeferred = False
    col = adsk.core.ObjectCollection.create()
    for prf in sk.profiles:
        if prf.profileLoops.count == 2:
            col.add(prf)
    if col.count != 1:
        raise RuntimeError("%s: Riemenprofil nicht eindeutig (%d)" % (name, col.count))
    b = extrudiere(comp, col, z0, z1, NEU).bodies.item(0)
    b.name = name
    return b


_farben = {}


def farbe(body, name, rgb):
    """Einfache Einfaerbung; scheitert still, wenn die Bibliothek anders aufgebaut ist."""
    try:
        if name not in _farben:
            ap = des.appearances.itemByName(name)
            if ap is None:
                basis = None
                for lib in app.materialLibraries:
                    if lib.appearances.count == 0:
                        continue
                    for i in range(lib.appearances.count):
                        a = lib.appearances.item(i)
                        if "Plastic - Matte" in a.name or "Kunststoff - Matt" in a.name:
                            basis = a
                            break
                    if basis:
                        break
                ap = des.appearances.addByCopy(basis, name)
                for pr in ap.appearanceProperties:
                    cp = adsk.core.ColorProperty.cast(pr)
                    if cp:
                        cp.value = adsk.core.Color.create(rgb[0], rgb[1], rgb[2], 255)
                        break
            _farben[name] = ap
        body.appearance = _farben[name]
    except Exception:
        pass


DRUCK = ("Druck_Orange", (235, 130, 30))
RAHMEN = ("Druck_Hellgrau", (200, 200, 205))
KAUF = ("Kaufteil_Stahl", (110, 115, 125))
ALU = ("Kaufteil_Alu", (170, 175, 185))
GUMMI = ("Riemen_Schwarz", (25, 25, 25))
MOTOR = ("Motor_Dunkel", (45, 45, 50))

# ---------------------------------------------------------------- Aufbau
for occ in list(root.occurrences):
    if occ.component.name == "J2_Pruefstand":
        occ.deleteMe()
haupt_occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
haupt = haupt_occ.component
haupt.name = "J2_Pruefstand"


def teil(name):
    occ = haupt.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = name
    return occ.component


ACHSEN = {"A": A, "B": B, "O": O}
LOCHKREIS = [(O[0] + R_LOCHKREIS * cos(radians(30 + 60 * i)), O[1] + R_LOCHKREIS * sin(radians(30 + 60 * i))) for i in range(6)]

# --- Wangen
for seite, z_aussen, z_innen in (("Links", -T_WANGE, 0.0), ("Rechts", W + T_WANGE, W)):
    k = teil("Wange_" + seite)
    za, zb = min(z_aussen, z_innen), max(z_aussen, z_innen)
    w = polygon(k, UMRISS, za, zb, "Wange_" + seite)
    # Lagersitze: Tasche von innen, Durchgang 15 mm (Aussenring liegt auf dem Bund)
    bohrung(k, w, ACHSEN.values(), 15.0, za, zb, "Durchgang_Lager")
    tz = (z_innen - B_LAGER, z_innen) if seite == "Links" else (z_innen, z_innen + B_LAGER)
    bohrung(k, w, ACHSEN.values(), D_LAGER + TOL_LAGERSITZ, tz[0], tz[1], "Lagersitz_608")
    # Quertraeger-Schrauben
    loecher = []
    for cx, cy in TRAEGER.values():
        loecher += [(cx, cy - TRAEGER_LOCH), (cx, cy + TRAEGER_LOCH)]
    bohrung(k, w, loecher, D_M3_DURCH, za, zb, "Schrauben_Quertraeger")
    # Spannrollen-Langloecher (M8)
    ll = [((I3[0], I3[1]), (1, 0), HUB_ROLLE, 8.4), ((I2[0], I2[1]), (0, 1), HUB_ROLLE, 8.4)]
    if seite == "Links":
        n = (-U_MOTOR[1], U_MOTOR[0])
        ll.append((M, U_MOTOR, HUB_MOTOR, 23.0))
        for a in (-15.5, 15.5):
            for b in (-15.5, 15.5):
                ll.append(((M[0] + a * U_MOTOR[0] + b * n[0], M[1] + a * U_MOTOR[1] + b * n[1]), U_MOTOR, HUB_MOTOR, D_M3_DURCH))
    else:
        # Zugang von rechts zu den Motorschrauben
        n = (-U_MOTOR[1], U_MOTOR[0])
        for a in (-15.5, 15.5):
            for b in (-15.5, 15.5):
                ll.append(((M[0] + a * U_MOTOR[0] + b * n[0], M[1] + a * U_MOTOR[1] + b * n[1]), U_MOTOR, HUB_MOTOR, 7.0))
    langloecher(k, w, ll, za, zb, "Langloecher")
    zm = (za + zb) / 2
    # Stellschrauben M3 fuer die Spannrollen (stuetzen die M8-Schraube formschluessig gegen den Riemenzug)
    radialbohrung(k, w, (0, I3[1]), "x", X_STELL_5M, zm,
                  [(D_EINSCHMELZ_M3, 6.0), (3.2, -X_STELL_5M + I3[0] - HUB_ROLLE)], "Stellschraube_5M")
    radialbohrung(k, w, (I2[0], 0), "y", 0.0, zm, [(D_EINSCHMELZ_M3, 6.0), (3.2, I2[1] - HUB_ROLLE)], "Stellschraube_3M")
    if seite == "Links":
        bohrung(k, w, [BLOCKIER[0]], D_EINSCHMELZ_M3, zb - T_EINSCHMELZ, zb, "Einschmelz_Blockierstift")
    else:
        # Zugang von rechts: Hebel- und Zeigerschrauben, Blockierstift
        zugang = list(LOCHKREIS) + [(O[0], O[1] - r) for r in R_ZEIGER_SCHRAUBEN] + [BLOCKIER[0]]
        bohrung(k, w, zugang, 6.0, za, zb, "Zugangsbohrungen")
        halter = [(x + dx, 160.0) for x in MESSHALTER.values() for dx in (-8.0, 8.0)]
        bohrung(k, w, halter, D_EINSCHMELZ_M3, zb - T_EINSCHMELZ, zb, "Einschmelz_Messuhrhalter")
    farbe(w, *RAHMEN)

# --- Quertraeger
for name, (cx, cy) in TRAEGER.items():
    k = teil(name)
    b = polygon(k, [(cx - TRAEGER_B / 2, cy - TRAEGER_H / 2), (cx + TRAEGER_B / 2, cy - TRAEGER_H / 2),
                    (cx + TRAEGER_B / 2, cy + TRAEGER_H / 2), (cx - TRAEGER_B / 2, cy + TRAEGER_H / 2)], 0, W, name)
    pts = [(cx, cy - TRAEGER_LOCH), (cx, cy + TRAEGER_LOCH)]
    bohrung(k, b, pts, D_EINSCHMELZ_M3, 0, T_EINSCHMELZ_TIEF, "Einschmelz_links")
    bohrung(k, b, pts, D_EINSCHMELZ_M3, W - T_EINSCHMELZ_TIEF, W, "Einschmelz_rechts")
    if "unten" in name:
        # zwei Einschmelzgewinde von unten fuer die Verschraubung auf dem Grundbrett
        for z in (14.0, W - 14.0):
            radialbohrung(k, b, (cx, cy), "y", -TRAEGER_H / 2, z, [(D_EINSCHMELZ_M3, 12.0)], "Einschmelz_Grundbrett")
    farbe(b, *RAHMEN)

# --- Lager und Wellen (Kaufteile)
def lager(k, c, z0, name):
    b = zylinder(k, c, D_LAGER, z0, z0 + B_LAGER, name=name)
    bohrung(k, b, [c], D_WELLE, z0, z0 + B_LAGER, name + "_Bohrung")
    farbe(b, *KAUF)
    return b


k = teil("Kaufteile_Lager_608")
for n, c in ACHSEN.items():
    lager(k, c, -B_LAGER, "Lager_%s_links" % n)
    lager(k, c, W, "Lager_%s_rechts" % n)
k = teil("Kaufteile_Wellen_8mm")
for n, c in ACHSEN.items():
    farbe(zylinder(k, c, D_WELLE, -B_LAGER, -B_LAGER + L_WELLE, name="Welle_" + n), *KAUF)

# --- Motor NEMA 17, 60 mm (Kaufteil), aussen an der linken Wange
k = teil("Kaufteil_Motor_NEMA17_60")
n = (-U_MOTOR[1], U_MOTOR[0])
h = 21.15
ecken = [(M[0] + a * h * U_MOTOR[0] + b * h * n[0], M[1] + a * h * U_MOTOR[1] + b * h * n[1])
         for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
mb = polygon(k, ecken, -T_WANGE - 60, -T_WANGE, "Motor")
zylinder(k, M, 22.0, -T_WANGE, -T_WANGE + 2, body=mb)
zylinder(k, M, 5.0, -T_WANGE + 2, -T_WANGE + 24, body=mb)
farbe(mb, *MOTOR)

# --- Gekaufte Ritzel (Annahmen zu Bord und Nabe, nach Lieferung nachmessen)
k = teil("Kaufteil_Ritzel_GT2_Z20_B5")
b = zylinder(k, M, 16.0, 1.0, 7.0, name="Ritzel_GT2_Z20")          # Nabe mit Gewindestiften
zylinder(k, M, 16.0, 7.0, 8.0, body=b)
zylinder(k, M, PD20 - 0.5, 8.0, 19.0, body=b)
zylinder(k, M, 16.0, 19.0, 20.0, body=b)
bohrung(k, b, [M], 5.0, 1.0, 20.0)
farbe(b, *ALU)

k = teil("Kaufteil_Ritzel_3M_Z16_B8")
b = zylinder(k, A, 18.0, 29.0, 30.0, name="Ritzel_3M_Z16")
zylinder(k, A, PD16 - 0.76, Z_3M[0], Z_3M[1], body=b)
zylinder(k, A, 18.0, 46.5, 47.5, body=b)
zylinder(k, A, 14.0, 47.5, 53.5, body=b)                           # Nabe
bohrung(k, b, [A], D_WELLE, 29.0, 53.5)
farbe(b, *ALU)

k = teil("Kaufteil_Ritzel_5M_Z18_B8")
b = zylinder(k, B, 32.0, 2.0, 3.5, name="Ritzel_5M_Z18")
zylinder(k, B, PD18 - 1.14, Z_5M[0], Z_5M[1], body=b)
zylinder(k, B, 32.0, 20.0, 21.5, body=b)
zylinder(k, B, 20.0, 21.5, 29.5, body=b)                           # Nabe, greift in die Z64-Scheibe
bohrung(k, b, [B], D_WELLE, 2.0, 29.5)
farbe(b, *ALU)

# --- Gedruckte Scheibe Z72 (GT2) auf Welle A: Distanzbund, Zahnkranz, Nabe mit 2 Gewindestiften
k = teil("Scheibe_GT2_Z72")
b = zahnscheibe(k, A, 72, 2, "GT2", Z_GT2[0], Z_GT2[1], "Scheibe_GT2_Z72")
zylinder(k, A, 24.0, Z_GT2[1], 28.8, body=b)
bohrung(k, b, [A], D_BOHRUNG_WELLE, Z_GT2[0], 28.8)
for ri in ("x", "y"):
    radialbohrung(k, b, A, ri, 12.0, 24.3, [(D_EINSCHMELZ_M3, 5.5), (3.2, 12.0)], "Gewindestift_" + ri)
bohrung(k, b, BLOCKIER, 3.0, Z_GT2[0], Z_GT2[1], "Blockierbohrungen")   # saugend, mit 3-mm-Bohrer aufreiben
farbe(b, *DRUCK)

def distanzring(name, c, z0, z1, d=D_ANLAGE):
    kk = teil(name)
    bb = zylinder(kk, c, d, z0, z1, name=name)
    bohrung(kk, bb, [c], D_BOHRUNG_WELLE + 0.15, z0, z1)
    farbe(bb, *DRUCK)


distanzring("Distanzring_A_links", A, 0.2, Z_GT2[0] - 0.1)
distanzring("Distanzring_A_rechts", A, 53.6, W - 0.2)

# --- Gedruckte Scheibe Z64 (3M) auf Welle B: Huelse ueber der Ritzelnabe, Schrauben durch Huelse in die Nabe
k = teil("Scheibe_3M_Z64")
b = zahnscheibe(k, B, 64, 3, "3M", Z_3M[0], Z_3M[1], "Scheibe_3M_Z64")
zylinder(k, B, 34.0, 22.0, Z_3M[0], body=b)
bohrung(k, b, [B], D_BOHRUNG_WELLE, 22.0, Z_3M[1])
bohrung(k, b, [B], 20.3, 22.0, 29.6, "Aufnahme_Ritzelnabe")
for ri in ("x", "y"):
    radialbohrung(k, b, B, ri, 17.0, 25.75, [(D_MITNAHME_M4, 8.0)], "Mitnahmeschraube_" + ri)
farbe(b, *DRUCK)

distanzring("Distanzring_B_links", B, 0.2, 2.0)
distanzring("Distanzring_B_rechts", B, Z_3M[1] + 0.1, W - 0.2)

# --- Gedruckte Scheibe Z90 (5M) auf der Abtriebswelle, mit 6 Einschmelzgewinden fuer den Hebel
k = teil("Scheibe_5M_Z90")
b = zahnscheibe(k, O, 90, 5, "5M", Z_5M[0], Z_5M[1], "Scheibe_5M_Z90")
zylinder(k, O, D_ANLAGE, 0.2, Z_5M[0], body=b)
bohrung(k, b, [O], D_BOHRUNG_ABTRIEB, 0.2, Z_5M[1])
bohrung(k, b, LOCHKREIS + [(O[0], O[1] - r) for r in R_ZEIGER_SCHRAUBEN], D_EINSCHMELZ_M3, Z_5M[1] - T_EINSCHMELZ_TIEF, Z_5M[1], "Einschmelz_Hebel_Zeiger")
bohrung(k, b, [(O[0] + 48 * cos(radians(60 * i)), O[1] + 48 * sin(radians(60 * i))) for i in range(6)], 24.0, Z_5M[0], Z_5M[1], "Fenster")
farbe(b, *DRUCK)

# --- Lasthebel: Nabe auf der Z90-Scheibe verschraubt, Arm zeigt in der Grundstellung nach oben
k = teil("Lasthebel")
b = zylinder(k, O, 2 * R_HEBELNABE, Z_HEBEL[0], Z_HEBEL[1], name="Lasthebel")
sk = skizze(k, "Hebelarm")
for i in range(4):
    sk.sketchCurves.sketchLines.addByTwoPoints(p(O[0] + HEBEL_KONTUR[i][0], O[1] + HEBEL_KONTUR[i][1]),
                                               p(O[0] + HEBEL_KONTUR[(i + 1) % 4][0], O[1] + HEBEL_KONTUR[(i + 1) % 4][1]))
extrudiere(k, alle_profile(sk), Z_HEBEL[0], Z_HEBEL[1], JOIN, b)
zylinder(k, (O[0], O[1] + L_HEBEL), B_HEBEL_ENDE, Z_HEBEL[0], Z_HEBEL[1], body=b)
zylinder(k, O, 22.0, Z_HEBEL[1], 52.0, body=b)
zylinder(k, O, D_ANLAGE, 52.0, W - 0.2, body=b)
bohrung(k, b, [O], D_BOHRUNG_ABTRIEB, Z_HEBEL[0], W - 0.2)
bohrung(k, b, LOCHKREIS, D_M3_DURCH, Z_HEBEL[0], Z_HEBEL[1], "Schrauben_Hebel")
bohrung(k, b, LOCHKREIS, 6.5, Z_HEBEL[0] + 8.0, Z_HEBEL[1], "Senkung_Hebel")
bohrung(k, b, [(O[0], O[1] + L_HEBEL)], 8.2, Z_HEBEL[0], Z_HEBEL[1], "Lastbohrung")
radialbohrung(k, b, O, "x", 11.0, 46.0, [(D_EINSCHMELZ_M3, 5.5), (3.2, 11.0)], "Gewindestift_Welle")
farbe(b, *DRUCK)

# --- Messzeiger: unbelastet auf die Z90-Scheibe geschraubt, zeigt dem Hebel entgegen
k = teil("Messzeiger")
b = polygon(k, [(O[0] - B_ZEIGER / 2, O[1] - R_ZEIGER[1]), (O[0] + B_ZEIGER / 2, O[1] - R_ZEIGER[1]),
                (O[0] + B_ZEIGER / 2, O[1] - R_ZEIGER[0]), (O[0] - B_ZEIGER / 2, O[1] - R_ZEIGER[0])],
            Z_ZEIGER[0], Z_ZEIGER[1], "Messzeiger")
sk = skizze(k, "Tastklotz")
tk = [(O[0] - B_TASTKLOTZ / 2, O[1] - R_TASTKLOTZ[1]), (O[0] + B_TASTKLOTZ / 2, O[1] - R_TASTKLOTZ[1]),
      (O[0] + B_TASTKLOTZ / 2, O[1] - R_TASTKLOTZ[0]), (O[0] - B_TASTKLOTZ / 2, O[1] - R_TASTKLOTZ[0])]
for i in range(4):
    sk.sketchCurves.sketchLines.addByTwoPoints(p(*tk[i]), p(*tk[(i + 1) % 4]))
extrudiere(k, alle_profile(sk), Z_TASTKLOTZ[0], Z_TASTKLOTZ[1], JOIN, b)
zs = [(O[0], O[1] - r) for r in R_ZEIGER_SCHRAUBEN]
bohrung(k, b, zs, D_M3_DURCH, Z_ZEIGER[0], Z_TASTKLOTZ[1], "Schrauben_Zeiger")
bohrung(k, b, zs, 6.5, Z_ZEIGER[1], Z_TASTKLOTZ[1], "Zugang_Zeigerschrauben")
bohrung(k, b, zs, 6.5, Z_ZEIGER[0] + 8.0, Z_ZEIGER[1], "Senkung_Zeiger")
farbe(b, *DRUCK)

# --- Messuhrhalter: aussen an der rechten Wange, haelt die Messuhr senkrecht ueber dem Zeiger (abnehmbar)
k = teil("Messuhrhalter")
xm = MESSHALTER["links"]
zh = W + T_WANGE
b = polygon(k, [(xm - 15, 150), (xm + 15, 150), (xm + 15, 214), (xm - 15, 214)], zh, zh + 10, "Messuhrhalter")
sk = skizze(k, "Halterarm")
for a_, b_ in (((xm - 15, 200), (xm + 15, 200)), ((xm + 15, 200), (xm + 15, 214)),
               ((xm + 15, 214), (xm - 15, 214)), ((xm - 15, 214), (xm - 15, 200))):
    sk.sketchCurves.sketchLines.addByTwoPoints(p(*a_), p(*b_))
Z_ARM = 24.0
extrudiere(k, alle_profile(sk), Z_ARM, zh, JOIN, b)
bohrung(k, b, [(xm - 8, 160.0), (xm + 8, 160.0)], D_M3_DURCH, zh, zh + 10, "Schrauben_Halter")
radialbohrung(k, b, (xm, 207.0), "y", 7.0, Z_MESSUHR, [(D_MESSUHR_SCHAFT, 14.0)], "Messuhr_Schaft")
# Klemmschlitz von der Armstirn bis in die Schaftbohrung, M3 x 25 quer dazu
sk = skizze(k, "Klemmschlitz")
sl = [(xm - 0.75, 199.0), (xm + 0.75, 199.0), (xm + 0.75, 215.0), (xm - 0.75, 215.0)]
for i in range(4):
    sk.sketchCurves.sketchLines.addByTwoPoints(p(*sl[i]), p(*sl[(i + 1) % 4]))
extrudiere(k, alle_profile(sk), Z_ARM, Z_MESSUHR + 10.0, CUT, b)   # durch die Bohrung hindurch, damit die Backen federn
radialbohrung(k, b, (xm, 207.0), "x", 15.0, Z_ARM + 5.5, [(6.5, 5.0), (D_M3_DURCH, 15.5)], "Klemmschraube_Durchgang")
radialbohrung(k, b, (xm, 207.0), "x", -15.0, Z_ARM + 5.5, [(D_EINSCHMELZ_M3, 6.0), (3.2, 15.0)], "Klemmschraube_Einschmelz")
farbe(b, *RAHMEN)

# --- Spannrolle 5M: gedruckte Rolle ueber 2x 608 auf M8-Schraube, Huelsen klemmen zwischen den Wangen
k = teil("Spannrolle_5M")
b = zylinder(k, I3, 2 * R_ROLLE_5M, Z_5M[0], Z_5M[1], name="Spannrolle_5M")
bohrung(k, b, [I3], 19.0, Z_5M[0], Z_5M[1])
bohrung(k, b, [I3], D_LAGER + TOL_LAGERSITZ, Z_5M[0] + 0.6, Z_5M[1], "Lagersitz")
farbe(b, *DRUCK)
kl = teil("Kaufteile_Lager_608_Spannrollen")
lager(kl, I3, Z_5M[0] + 0.6, "Lager_Rolle5M_1")
lager(kl, I3, Z_5M[1] - B_LAGER, "Lager_Rolle5M_2")
lager(kl, I2, 31.5, "Lager_Rolle3M_1")
lager(kl, I2, 38.5, "Lager_Rolle3M_2")

k = teil("Distanzhuelsen_Spannrollen")
# (Name, Mitte, z0, z1, z ab dem die Huelse 16 mm dick ist oder None)
for name, c, z0, z1, z_dick in (("Huelse_5M_links", I3, 0.0, Z_5M[0] + 0.6, None),
                                ("Huelse_5M_mitte", I3, Z_5M[0] + 0.6 + B_LAGER, Z_5M[1] - B_LAGER, None),
                                ("Huelse_5M_rechts", I3, Z_5M[1], W, Z_5M[1] + 1.0),
                                ("Huelse_3M_links", I2, 0.0, 31.5, None),      # bleibt 12 mm: laeuft am GT2-Riemen vorbei
                                ("Huelse_3M_rechts", I2, 45.5, W, 46.5)):
    b = zylinder(k, c, D_ANLAGE, z0, z1, name=name)
    if z_dick is not None:
        zylinder(k, c, 16.0, z_dick, z1, body=b)
    bohrung(k, b, [c], 8.3, z0, z1)
    farbe(b, *DRUCK)

k = teil("Kaufteile_Schrauben_M8x90")
for name, c in (("Schraube_Rolle_5M", I3), ("Schraube_Rolle_3M", I2)):
    b = zylinder(k, c, 8.0, -T_WANGE - 1.6, W + T_WANGE + 16.4, name=name)
    zylinder(k, c, 14.4, -T_WANGE - 6.9, -T_WANGE - 1.6, body=b)
    zylinder(k, c, 16.0, -T_WANGE - 1.6, -T_WANGE, body=b)
    zylinder(k, c, 16.0, W + T_WANGE, W + T_WANGE + 1.6, body=b)
    zylinder(k, c, 14.4, W + T_WANGE + 1.6, W + T_WANGE + 9.6, body=b)
    farbe(b, *KAUF)

# --- Riemen (Darstellung)
k = teil("Kaufteile_Riemen")
farbe(riemen(k, [(M, PD20 / 2, 1), (A, PD72 / 2, 1)], "GT2", 8.5, 18.5, "Riemen_GT2_200"), *GUMMI)
farbe(riemen(k, [(A, PD16 / 2, 1), (B, PD64 / 2, 1), (I2, R_ROLLE_3M + PROFIL["3M"]["t_out"], -1)], "3M", 30.75, 45.75, "Riemen_3M_252"), *GUMMI)
farbe(riemen(k, [(B, PD18 / 2, 1), (O, PD90 / 2, 1), (I3, R_ROLLE_5M + PROFIL["5M"]["t_out"], -1)], "5M", 4.25, 19.25, "Riemen_5M_525"), *GUMMI)

ergebnis = {
    "A": [round(v, 2) for v in A], "B": [round(v, 2) for v in B], "M": [round(v, 2) for v in M], "O": list(O),
    "Rolle_5M": [round(v, 2) for v in I3], "Rolle_3M": [round(v, 2) for v in I2],
    "Umschlingung_5M_Grad(Z18,Z90,Rolle)": [round(math.degrees(w)) for w in WRAP3],
    "Umschlingung_3M_Grad(Z16,Z64,Rolle)": [round(math.degrees(w)) for w in WRAP2],
    "Freie_Trume_5M_mm": [round(v, 1) for v in TRUME3], "Freie_Trume_3M_mm": [round(v, 1) for v in TRUME2],
    "Spannreserve_mm(5M,3M)": [round(RESERVE3, 2), round(RESERVE2, 2)],
    "Anschlag_Grad(links,rechts)": [ANSCHLAG_LINKS, ANSCHLAG_RECHTS],
    "Blockierstift": [round(v, 2) for v in BLOCKIER[0]],
    "Teile": haupt.occurrences.count,
}
