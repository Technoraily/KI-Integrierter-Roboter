"""Basis mit J1 - Bauraummodell V1 (Konstruktion, nicht nur Optik).

Inhalt: Grundplatte mit festem Lagerzapfen (Hohlschaft), zwei Dünnringlager 6810
(Abstand 40 mm, vorgespannt über Spannring), Nabe = Drehteller J1 mit 3M-80er-Scheibe,
Zwischenwelle (8 mm, 2× 608) im verschiebbaren Bock, J1-Motor 17CS04A-170E im Kasten,
Stufe 1 GT2 20:80 (Riemen 240 mm), Stufe 2 3M 16:80 (Riemen 300 mm) = 20:1.
Schalen (Sockelgehäuse, Kasten, Kappe, Farbring) wie Gestaltung V4, mit Magneten.
Schnittstelle zur Säule: Lochbild 120 mm, 4× M5 (Muttern in der Nabe), Zentrierung Ø 90.

Ausführen im Fusion-Python (MCP-Add-in):  exec(open(pfad, encoding="utf-8").read())
Masse in mm; x nach vorn, y quer, z nach oben, z = 0 Oberseite Holzplatte, J1-Achse = z.
"""
import math
import os

_ORDNER = r"C:\Claude\KI-Integrierter Roboter\cad\skripte"
_q = open(os.path.join(_ORDNER, "arm_gestaltung_v4.py"), encoding="utf-8").read()
exec(_q[:_q.index("\n# ---------------------------------------------------------------- Aufräumen")])

_FARBEN_V4.update({"Stahl": (175, 178, 182), "Motor": (38, 38, 40), "Riemen": (20, 20, 20),
                   "Alu": (200, 204, 210), "PETG": (215, 228, 236), "Rot": AKZENT})

# ---------------------------------------------------------------- Parameter (mm)
BODEN = 5.0                     # Grundplatte
SO_R = 92.0                     # Sockel-8-Eck (Umkreis), wie Gestaltung V4
WAND = 3.0
DECK = (81.0, 85.0)             # Deckel des Sockelgehäuses
RING_Z = (85.0, 91.0)           # roter Farbring (fest)
RING_RI = 44.0
L6810 = dict(d=50.0, D=65.0, B=7.0, sitz=65.2, welle=49.9)   # Sitz/Zapfen: Testteil vorher!
LAGER_Z = (40.0, 80.0)          # Unterkanten der beiden 6810 (Mittenabstand 40)
ZAPFEN = dict(r_bund=28.0, bohr=34.0, oben=86.5, fenster=(5.5, 19.0, 24.0))
NABE = dict(z0=18.0, r_rohr=37.5, flansch=(91.5, 103.5), r_flansch=72.0, lochkreis=120.0,
            zentrier=65.2)            # Säule zentriert mit Zapfen Ø 65,0 in der Nabenbohrung
SPANN = dict(r=27.0, ri=18.0, h=4.0, schr_r=21.0)
# Riemen (Teilkreis-Durchmesser)
d3_16, d3_80 = 16 * 3 / math.pi, 80 * 3 / math.pi
d2_20, d2_80 = 20 * 2 / math.pi, 80 * 2 / math.pi


def achsabstand(L, d1, d2):
    a, b = (d2 - d1) ** 2 / 4.0, L - math.pi * (d1 + d2) / 2.0
    C = b / 2.0
    for _ in range(40):
        C = (b - a / C) / 2.0
    return C


C2 = achsabstand(300.0, d3_16, d3_80)       # 3M-300 (100 Z.)
C1 = achsabstand(240.0, d2_20, d2_80)       # GT2-240 (120 Z.)
XZ = -C2                                    # Zwischenwelle
XM = XZ - C1                                # Motor
Z3 = (19.5, 35.5)                           # 3M-Zahnbreite (Riemen 15)
Z2 = (53.5, 64.5)                           # GT2-Zahnbreite (Riemen 10)
MOTOR = dict(face=43.0, l=40.0, k=42.3, welle=24.0)
MAG = (3.1, 3.2)                # Magnettasche 6×3: Radius, Tiefe
INS = 2.0                       # M3-Einschmelz: Bohrung Ø 4,0
WINKEL_MAG = [22.5 + 45 * k for k in range(8) if k not in (3, 4)]   # Ecken ohne Kastenöffnung
WINKEL_STIFT = (67.5, 292.5)
KASTEN_P = dict(xa=-174.0, xb=-60.0, b=118.0, h=71.0, fase=12.0, boden=3.0)


# ---------------------------------------------------------------- Temp-BRep-Grundkörper
def zyl(x, y, z0, z1, r):
    return tbm.createCylinderOrCone(P(x, y, z0), r * MM, P(x, y, z1), r * MM)


def zyl_y(x, y0, y1, z, r):
    return tbm.createCylinderOrCone(P(x, y0, z), r * MM, P(x, y1, z), r * MM)


def haelften(k, fuge=0.2):
    """Teilt einen Körper an y = 0 in zwei Hälften (+y, -y) mit Fuge."""
    a, b = tbm.copy(k), tbm.copy(k)
    tbm.booleanOperation(a, quader(-300, 300, fuge / 2, 300, -50, 300), adsk.fusion.BooleanTypes.IntersectionBooleanType)
    tbm.booleanOperation(b, quader(-300, 300, -300, -fuge / 2, -50, 300), adsk.fusion.BooleanTypes.IntersectionBooleanType)
    return a, b


def zyl_x(x0, x1, y, z, r):
    return tbm.createCylinderOrCone(P(x0, y, z), r * MM, P(x1, y, z), r * MM)


def quader(x0, x1, y0, y1, z0, z1):
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)
    z0, z1 = min(z0, z1), max(z0, z1)
    ob = adsk.core.OrientedBoundingBox3D.create(P((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
                                                V(1, 0, 0), V(0, 1, 0),
                                                (x1 - x0) * MM, (y1 - y0) * MM, (z1 - z0) * MM)
    return tbm.createBox(ob)


def _huelle2(pts):
    pts = sorted(set((round(x, 6), round(y, 6)) for x, y in pts))
    def kr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    u, o = [], []
    for p in pts:
        while len(u) >= 2 and kr(u[-2], u[-1], p) <= 0:
            u.pop()
        u.append(p)
    for p in reversed(pts):
        while len(o) >= 2 and kr(o[-2], o[-1], p) <= 0:
            o.pop()
        o.append(p)
    return u[:-1] + o[:-1]                  # gegen den Uhrzeigersinn


def prisma(pts, z0, z1):
    """Konvexes Prisma (Umriss beliebig, wird zur Hülle) zwischen z0 und z1."""
    h = _huelle2(pts)
    xs = [p[0] for p in h]; ys = [p[1] for p in h]
    k = quader(min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1, z0, z1)
    S = 4 * max(max(xs) - min(xs), max(ys) - min(ys)) + 50
    for i in range(len(h)):
        (ax, ay), (bx, by) = h[i], h[(i + 1) % len(h)]
        l = math.hypot(bx - ax, by - ay)
        if l < 1e-6:
            continue
        nx, ny = (by - ay) / l, -(bx - ax) / l          # nach aussen (CCW)
        mx, my = (ax + bx) / 2 + nx * S / 2, (ay + by) / 2 + ny * S / 2
        ob = adsk.core.OrientedBoundingBox3D.create(P(mx, my, (z0 + z1) / 2), V(nx, ny, 0), V(-ny, nx, 0),
                                                    S * MM, S * MM, (z1 - z0 + 10) * MM)
        tbm.booleanOperation(k, tbm.createBox(ob), adsk.fusion.BooleanTypes.DifferenceBooleanType)
    return k


def kreis(x, y, r, n=48):
    return [(x + r * math.cos(2 * math.pi * i / n), y + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def minus(k, *werkzeuge):
    for w in werkzeuge:
        tbm.booleanOperation(k, w, adsk.fusion.BooleanTypes.DifferenceBooleanType)
    return k


def plus(k, *teile):
    for t in teile:
        tbm.booleanOperation(k, t, adsk.fusion.BooleanTypes.UnionBooleanType)
    return k


def ring(x, y, z0, z1, ra, ri):
    return minus(zyl(x, y, z0, z1, ra), zyl(x, y, z0 - 1, z1 + 1, ri))


def ablegen(comp, name, k, f):
    _wartend.setdefault(comp.entityToken, (comp, []))[1].append((name, k, f))


def riemen(x1, r1, x2, r2, z0, z1, t=1.6):
    aussen = prisma(kreis(x1, 0, r1 + t, 40) + kreis(x2, 0, r2 + t, 40), z0, z1)
    return minus(aussen, prisma(kreis(x1, 0, r1, 40) + kreis(x2, 0, r2, 40), z0 - 1, z1 + 1))


def okt(r):
    return vieleck(r, 8, math.pi / 8)


# ---------------------------------------------------------------- Aufräumen
for i in range(root.occurrences.count - 1, -1, -1):
    if root.occurrences.item(i).component.name.startswith("Basis_J1"):
        root.occurrences.item(i).deleteMe()
B = komponente(root, "Basis_J1")
fest = komponente(B, "Basis_fest")
kauf = komponente(B, "Basis_Kaufteile")
dreh = komponente(B, "J1_Drehteil", (0, 0, 0), (0, 0, 1), Q1)
schale = komponente(B, "Basis_Schalen")

# ================================================================ Grundplatte mit Lagerzapfen (PLA grau)
zp = ZAPFEN
gp = prisma(okt(SO_R), 0, BODEN)
plus(gp, zyl(0, 0, BODEN, LAGER_Z[0], zp["r_bund"]), zyl(0, 0, LAGER_Z[0] - 0.5, zp["oben"], L6810["welle"] / 2))
minus(gp, zyl(0, 0, -1, zp["oben"] + 1, zp["bohr"] / 2))
f0, f1, fb = zp["fenster"]
minus(gp, quader(-fb / 2, fb / 2, 0, zp["r_bund"] + 2, f0, f1))          # Kabelfenster nach +y
for k in range(4):                                                     # Holzschrauben Ø 4,5
    a = math.radians(22.5 + 90 * k)
    minus(gp, zyl(70 * math.cos(a), 70 * math.sin(a), -1, BODEN + 1, 2.25))
for k in range(3):                                                     # M3-Einschmelz Spannring
    a = math.radians(90 + 120 * k)
    minus(gp, zyl(SPANN["schr_r"] * math.cos(a), SPANN["schr_r"] * math.sin(a), zp["oben"] - 6, zp["oben"] + 1, 2.0))
for dx in (6, 17):                                                                 # Einschmelz für den Bock
    minus(gp, zyl(XZ + dx, 34, -1, BODEN + 1, INS))
plus(gp, quader(44, 68, -7, 7, BODEN, 9))                                          # Sockel Endschalter
for x in (51.25, 60.75):                                                           # M2, Mutter von unten
    minus(gp, zyl(x, 0, -1, 10, 1.1), prisma([(x + u, v) for u, v in vieleck(2.3, 6)], -1, 1.6))
for w in WINKEL_MAG:                                                               # Magnete/Stifte zum Gehäuse
    x, y = 82 * math.cos(math.radians(w)), 82 * math.sin(math.radians(w))
    if w in WINKEL_STIFT:
        minus(gp, zyl(x, y, BODEN - 4, BODEN + 1, 1.55))
    else:
        minus(gp, zyl(x, y, BODEN - MAG[1], BODEN + 1, MAG[0]))
ablegen(fest, "Grundplatte", gp, "Grau")

# ================================================================ Lager 6810 (Kauf)
for i, z in enumerate(LAGER_Z):
    ablegen(kauf, f"Lager_6810_{i + 1}", ring(0, 0, z, z + L6810["B"], L6810["D"] / 2, L6810["d"] / 2), "Stahl")

# ================================================================ Nabe = Drehteller J1 + 3M-80-Scheibe (PLA grau)
n = NABE
fz0, fz1 = n["flansch"]
nabe = zyl(0, 0, n["z0"], n["z0"] + 1.5, 41.0)                                     # Bord unten
plus(nabe, zyl(0, 0, Z3[0], Z3[1], d3_80 / 2 - 0.38),                             # Zähne (vereinfacht)
     zyl(0, 0, Z3[1], Z3[1] + 1.5, 41.0),                                         # Bord oben
     zyl(0, 0, Z3[1], fz0 + 0.1, n["r_rohr"]),
     prisma(vieleck(n["r_flansch"], 12, math.pi / 12), fz0, fz1))
lu, lo = LAGER_Z
minus(nabe, zyl(0, 0, n["z0"] - 1, lu, 30.0),                                     # Luft um den Bund
      zyl(0, 0, lu - 0.01, lu + L6810["B"], L6810["sitz"] / 2),                   # Sitz unten
      zyl(0, 0, lu, lo + 0.01, 29.0),                                             # Schulter dazwischen
      zyl(0, 0, lo, fz1 + 1, L6810["sitz"] / 2))                                  # Sitz oben + Zugang + Zentrierung
for k in range(4):                                                                 # 4× M5, Mutter von unten
    a = math.radians(45 + 90 * k)
    x, y = n["lochkreis"] / 2 * math.cos(a), n["lochkreis"] / 2 * math.sin(a)
    minus(nabe, zyl(x, y, fz0 - 1, fz1 + 1, 2.75), prisma([(x + u, y + v) for u, v in vieleck(4.7, 6, a)], fz0 - 1, fz0 + 4.5))
ablegen(dreh, "Nabe_Drehteller", nabe, "Anthrazit")

sp = ring(0, 0, lo + L6810["B"], lo + L6810["B"] + SPANN["h"], SPANN["r"], SPANN["ri"])
for k in range(3):
    a = math.radians(90 + 120 * k)
    minus(sp, zyl(SPANN["schr_r"] * math.cos(a), SPANN["schr_r"] * math.sin(a), lo, lo + 20, 1.7))
ablegen(fest, "Spannring", sp, "Grau")

# Nocken für den Endschalter (an der Nabe, Grundstellung hinten)
ablegen(dreh, "Endschalter_Nocken", quader(-44.0, -38.0, -3, 3, 12.0, n["z0"] + 0.1), "Anthrazit")

# ================================================================ Zwischenwelle im Bock (verschiebbar in x)
bock = quader(XZ - 12, XZ + 12, 30, 36, BODEN, 78)
plus(bock, quader(XZ - 12, XZ + 12, -14, 36, BODEN, 16), quader(XZ - 12, XZ + 12, -14, 36, 68, 78),
     zyl(XZ, 0, BODEN, 16, 15), zyl(XZ, 0, 68, 78, 15), quader(XZ - 4, XZ + 22, 26, 40, BODEN, BODEN + 4))
minus(bock, zyl(XZ, 0, 8, 17, 11.1), zyl(XZ, 0, 67, 77, 11.1), zyl(XZ, 0, 0, 90, 4.5))
for dx in (6, 17):                                                                 # Langlöcher M3
    minus(bock, quader(XZ + dx - 5, XZ + dx + 5, 32.3, 35.7, BODEN - 1, BODEN + 5))
ablegen(fest, "Zwischenwellen_Bock", bock, "Grau")
ablegen(kauf, "Welle_8x73", zyl(XZ, 0, 6, 79, 4), "Stahl")
ablegen(kauf, "Lager_608_unten", ring(XZ, 0, 8, 15, 11, 4), "Stahl")
ablegen(kauf, "Lager_608_oben", ring(XZ, 0, 70, 77, 11, 4), "Stahl")
r16 = zyl(XZ, 0, 16.5, 18.5, 8)
plus(r16, zyl(XZ, 0, 18.5, Z3[0], 10.5), zyl(XZ, 0, Z3[0], Z3[1], d3_16 / 2 - 0.38),
     zyl(XZ, 0, Z3[1], Z3[1] + 1, 10.5))
ablegen(kauf, "Ritzel_3M_16Z", r16, "Alu")
s80 = zyl(XZ, 0, 47, 52, 10)
plus(s80, zyl(XZ, 0, 52, Z2[0], 28), zyl(XZ, 0, Z2[0], Z2[1], d2_80 / 2 - 0.25), zyl(XZ, 0, Z2[1], Z2[1] + 1.5, 28))
minus(s80, zyl(XZ, 0, 40, 70, 4.05), zyl_x(XZ - 11, XZ - 3, 0, 49.5, INS))          # Madenschraube M3 radial
ablegen(fest, "Distanzhuelse_8", ring(XZ, 0, Z2[1] + 1.5, 70, 6, 4.1), "Grau")
ablegen(fest, "Scheibe_GT2_80Z", s80, "Grau")

# ================================================================ Motor J1 im Kasten
m = MOTOR
mk = m["k"] / 2
mot = quader(XM - mk, XM + mk, -mk, mk, m["face"] - m["l"], m["face"])
plus(mot, zyl(XM, 0, m["face"], m["face"] + 2, 11), zyl(XM, 0, m["face"], m["face"] + m["welle"], 2.5))
ablegen(kauf, "Motor_J1_17CS04A", mot, "Motor")
r20 = zyl(XM, 0, 49, Z2[0], 8)
plus(r20, zyl(XM, 0, Z2[0], Z2[1], d2_20 / 2 - 0.25), zyl(XM, 0, Z2[1], Z2[1] + 0.8, 8))
ablegen(kauf, "Ritzel_GT2_20Z", r20, "Alu")
ka = KASTEN_P
kp = [(ka["xb"], -ka["b"] / 2), (ka["xb"], ka["b"] / 2), (ka["xa"] + ka["fase"], ka["b"] / 2),
      (ka["xa"], ka["b"] / 2 - ka["fase"]), (ka["xa"], -ka["b"] / 2 + ka["fase"]), (ka["xa"] + ka["fase"], -ka["b"] / 2)]
mp = minus(prisma(einziehen2(kp, WAND + 0.5), m["face"], m["face"] + 5), quader(XM + 30, 0, -80, 80, 0, 60))
minus(mp, zyl(XM, 0, 0, 60, 11.5))
for x, y in [(x, sy * 52) for x in (-150, -118) for sy in (-1, 1)]:
    minus(mp, quader(x - 4, x + 4, y - 1.7, y + 1.7, 40, 50))                     # Langlöcher M3
for sx in (-15.5, 15.5):
    for sy in (-15.5, 15.5):
        minus(mp, quader(XM + sx - 4, XM + sx + 4, sy - 1.7, sy + 1.7, 40, 50))    # Langlöcher zum Spannen
ablegen(fest, "Motorplatte", mp, "PETG")

# Riemen
ablegen(kauf, "Riemen_3M_300_15", riemen(0, d3_80 / 2, XZ, d3_16 / 2, Z3[0] + 0.5, Z3[1] - 0.5), "Riemen")
ablegen(kauf, "Riemen_GT2_240_10", riemen(XZ, d2_80 / 2, XM, d2_20 / 2, Z2[0] + 0.5, Z2[1] - 0.5, 1.4), "Riemen")

# Endschalter (KW11, Platzhalter) vorne, löst erst bei ±180° aus
es = quader(46, 66, -5, 5, 9, 15)
plus(es, quader(40.5, 52, -2, 2, 13.0, 15.0))
ablegen(kauf, "Endschalter_J1", es, "Motor")

# ================================================================ Schalen (Optik wie V4, Magnete 6×3)
geh = prisma(okt(SO_R), BODEN, DECK[1])
minus(geh, prisma(okt(SO_R - WAND / math.cos(math.pi / 8)), BODEN - 1, DECK[0]),
      zyl(0, 0, DECK[0] - 1, DECK[1] + 1, RING_RI),
      quader(-100, -55, -56, 56, BODEN - 1, 78))                                   # offen zum Kasten
for w in WINKEL_MAG:
    x, y = 82 * math.cos(math.radians(w)), 82 * math.sin(math.radians(w))
    plus(geh, zyl(x, y, BODEN, BODEN + 10, 7))
    if w in WINKEL_STIFT:
        minus(geh, zyl(x, y, BODEN - 1, BODEN + 8, 1.55))                          # Zylinderstift 3 × 12
    else:
        minus(geh, zyl(x, y, BODEN - 1, BODEN + MAG[1], MAG[0]))
WINKEL_RING = (45, 135, 225, 315)
for w in WINKEL_RING:
    x, y = 60 * math.cos(math.radians(w)), 60 * math.sin(math.radians(w))
    minus(geh, zyl(x, y, DECK[1] - MAG[1], DECK[1] + 1, MAG[0]))
# Fuge vorne (x+): Buckel mit zwei Magneten quer zur Fuge, die die Hälften zusammenhalten
FUGE_Z = (30.0, 60.0)
for zf in FUGE_Z:
    plus(geh, quader(74, 83, -8, 8, zf - 7, zf + 7))
    minus(geh, zyl_y(78.5, -MAG[1] - 0.1, MAG[1] + 0.1, zf, MAG[0]))
g_l, g_r = haelften(geh)
ablegen(schale, "Sockelgehaeuse_links", g_l, "Anthrazit")
ablegen(schale, "Sockelgehaeuse_rechts", g_r, "Anthrazit")
fr = ring(0, 0, RING_Z[0], RING_Z[1], 76.0, RING_RI)
for w in WINKEL_RING:
    minus(fr, zyl(60 * math.cos(math.radians(w)), 60 * math.sin(math.radians(w)), RING_Z[0] - 1, RING_Z[0] + MAG[1], MAG[0]))
f_l, f_r = haelften(fr)
ablegen(schale, "Farbring_J1_links", f_l, "Rot")
ablegen(schale, "Farbring_J1_rechts", f_r, "Rot")

kas = prisma(kp, 0, ka["h"])
minus(kas, prisma(einziehen2(kp, WAND), ka["boden"], ka["h"] + 1),
      quader(ka["xb"] - 10, ka["xb"] + 1, -50, 50, ka["boden"], ka["h"] + 1),     # offen zum Sockel
      zyl_x(ka["xa"] - 2, ka["xa"] + 6, 40, 20, 8),                                # Kabelaustritt
      prisma(okt(SO_R), -1, ka["h"] + 1))                                          # an den Sockel angepasst
for sy in (-1, 1):                                                                 # Auflage Motorplatte
    plus(kas, quader(ka["xa"] + ka["fase"] + 2, XM + 30, sy * (ka["b"] / 2 - WAND - 8), sy * (ka["b"] / 2 - WAND), m["face"] - 4,
                     m["face"]))
MAG_KASTEN = [(x, sy * 53) for x in (-150, -95) for sy in (-1, 1)]
AUFLAGE = [(x, sy * 52) for x in (-150, -118) for sy in (-1, 1)]
for x, y in MAG_KASTEN:
    plus(kas, zyl(x, y, ka["h"] - 10, ka["h"], 6))
    minus(kas, zyl(x, y, ka["h"] - MAG[1], ka["h"] + 1, MAG[0]))
for x, y in AUFLAGE:
    minus(kas, zyl(x, y, m["face"] - 6, m["face"] + 1, INS))
for x, y in ((-110, 40), (-110, -40), (-167, 0)):
    minus(kas, zyl(x, y, -1, ka["boden"] + 1, 2.25))
ablegen(fest, "Motorkasten", kas, "Anthrazit")
ablegen(fest, "Steckerfeld_Platzhalter", quader(-165, -95, 44, 47, ka["boden"], 36), "Grau")

kappe = [(x, y, ka["h"]) for x, y in kp]
kappe += [(x, y, ka["h"] + 12) for x, y in einziehen2(kp, 6)]
kappe += [(x, y, ka["h"] + 20) for x, y in einziehen2(kp, 24)]
kk = netz(schale, "Kastenkappe", kappe, "Weiss")
for x, y in MAG_KASTEN:
    minus(kk, zyl(x, y, ka["h"] - 1, ka["h"] + MAG[1], MAG[0]))
minus(kk, prisma(okt(SO_R), ka["h"] - 1, ka["h"] + 30), zyl(XZ, 0, ka["h"] - 1, 80, 16.5))     # Luft um den Bock

test = komponente(B, "Basis_Testteile", (220, 0, 0))
pp = ring(0, 0, 0, L6810["B"] + 2, L6810["sitz"] / 2 + 3, L6810["sitz"] / 2)
plus(pp, ring(0, 0, 0, 2, L6810["sitz"] / 2 + 3, 29.0))
ablegen(test, "Passprobe_6810_Sitz", pp, "Grau")
pz = zyl(0, 90, 0, 3, 30)
plus(pz, zyl(0, 90, 3, 3 + L6810["B"] + 2, L6810["welle"] / 2))
minus(pz, zyl(0, 90, -1, 20, ZAPFEN["bohr"] / 2))
ablegen(test, "Passprobe_6810_Zapfen", pz, "Grau")
einfuegen()
print(f"C2 (3M) = {C2:.2f} mm, C1 (GT2) = {C1:.2f} mm, Zwischenwelle x = {XZ:.1f}, Motor x = {XM:.1f}")
