"""Basis mit J1 - Bauraummodell V2 (Gutachten Runde 1 eingearbeitet, 26.11.2026).

Grundplatte mit festem Lagerzapfen (Hohlschaft Ø 30 frei) und 7 Rippen, zwei 6810 in
O-Anordnung (Vorspannung über O-Ring 49 × 2 im Spannring, Spannring auf Block gegen den
Zapfen), Nabe = Drehteller J1 mit angeformter 3M-80-Scheibe (echtes Zahnprofil),
Halbmond-Nocken für den Endschalter und fester Anschlag bei ca. ±173°.
Antrieb 20:1: GT2 20:80 (Riemen 240) und 3M 16:80 (Riemen 318, damit die Zwischenwelle
ausserhalb des Tellers liegt). Bock zweiteilig (oberer Arm flach gedruckt), 4 Langlöcher
mit Muttern in der Grundplatten-Lasche, Spannschraube M3 × 25.
Schalen: Sockelgehäuse und Farbring zweiteilig, Kappe auf dem Kasten, Magnete 6 × 3.
Schnittstelle zur Säule: Lochbild 120 mm, 4 × M5 (Muttern im Teller), Zentrierzapfen der
Säule Ø 65,0 in der Nabenbohrung Ø 65,2, höchstens 8 mm tief, innen ≥ Ø 58 frei.
V1 (vor dem Gutachten) liegt in basis_j1_v1.py.

Ausführen im Fusion-Python (MCP-Add-in):  exec(open(pfad, encoding="utf-8").read())
Masse in mm; x nach vorn, y quer, z nach oben, z = 0 Oberseite Holzplatte, J1-Achse = z.
"""
import math
import os

_ORDNER = r"C:\Claude\KI-Integrierter Roboter\cad\skripte"
_q = open(os.path.join(_ORDNER, "arm_gestaltung_v4.py"), encoding="utf-8").read()
exec(_q[:_q.index("\n# ---------------------------------------------------------------- Aufräumen")])

_FARBEN_V4.update({"Stahl": (175, 178, 182), "Motor": (38, 38, 40), "Riemen": (20, 20, 20),
                   "Alu": (200, 204, 210), "PETG": (215, 228, 236), "Rot": AKZENT,
                   "Schraube": (90, 90, 95), "Kabel": (40, 90, 200)})

# ---------------------------------------------------------------- Parameter (mm)
BODEN = 5.0
SO_R = 92.0
WAND = 3.0
DECK = (81.0, 85.0)
RING_Z = (85.0, 90.0)           # Farbring 5 mm (Teller ab 91,5)
RING_RI = 44.0
L6810 = dict(d=50.0, D=65.0, B=7.0, sitz=65.2, welle=49.9)   # Passprobe vorher!
LU, LO = 40.0, 80.0             # Unterkanten der 6810 (Mittenabstand 40)
ZAPFEN = dict(r_bund=26.5, bohr=30.0, oben=87.0, fenster=(5.5, 16.0, 24.0))
NABE = dict(z0=17.0, r_rohr=37.5, flansch=(91.5, 103.5), r_flansch=72.0, lochkreis=120.0)
SPANN = dict(r=28.0, ri=16.0, h=4.0, schr_r=19.5)   # aussen Ø 56, Freistich 0,5 über dem Innenring
ORING = dict(ri=25.0, ra=27.0, tiefe=0.6)          # O-Ring 50 × 1,5 NBR, Nut 2,0 × 0,6
EINSAETZE = []                                        # (Teil, x0,y0,z0, x1,y1,z1) für die Wandprüfung
MAG = (3.1, 3.2)                # Magnettasche 6 × 3: Radius, Tiefe
INS = 2.0                       # M3-Einschmelz: Bohrung Ø 4,0
d3_16, d3_80 = 16 * 3 / math.pi, 80 * 3 / math.pi
d2_20, d2_80 = 20 * 2 / math.pi, 80 * 2 / math.pi


def achsabstand(L, d1, d2):
    a, b = (d2 - d1) ** 2 / 4.0, L - math.pi * (d1 + d2) / 2.0
    C = b / 2.0
    for _ in range(40):
        C = (b - a / C) / 2.0
    return C


L3M, LGT2 = 318.0, 240.0
C2 = achsabstand(L3M, d3_16, d3_80)
C1 = achsabstand(LGT2, d2_20, d2_80)
XZ = -C2
XM = XZ - C1
Z3 = (19.5, 35.5)               # 3M-Zahnbreite
Z2 = (54.5, 65.5)               # GT2-Zahnbreite
MOTOR = dict(face=44.0, l=40.0, k=42.3, welle=24.0)
KASTEN_P = dict(xa=-190.0, xb=-60.0, b=118.0, h=71.0, fase=12.0, boden=3.0)
LASCHE = dict(x0=-118.0, x1=-62.0, y0=-46.0, y1=56.0)       # Verlängerung der Grundplatte für den Bock
BOCK = dict(hx=15.0, y0=-15.0, wy=(30.0, 40.0), arm_u=(BODEN, 16.0), arm_o=(69.0, 79.0), ruecken=69.0)
SCHALTER = dict(x0=50.0, x1=60.0, z0=38.5, h=6.4, rolle_r=2.4, rolle_frei=42.7)   # KW11 liegend, vor dem Kauf ausmessen


# ---------------------------------------------------------------- Temp-BRep-Grundkörper
def zyl(x, y, z0, z1, r, r1=None):
    return tbm.createCylinderOrCone(P(x, y, z0), r * MM, P(x, y, z1), (r if r1 is None else r1) * MM)


def zyl_x(x0, x1, y, z, r):
    return tbm.createCylinderOrCone(P(x0, y, z), r * MM, P(x1, y, z), r * MM)


def zyl_y(x, y0, y1, z, r):
    return tbm.createCylinderOrCone(P(x, y0, z), r * MM, P(x, y1, z), r * MM)


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
    return u[:-1] + o[:-1]


def prisma(pts, z0, z1):
    h = _huelle2(pts)
    xs = [p[0] for p in h]; ys = [p[1] for p in h]
    k = quader(min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1, z0, z1)
    S = 4 * max(max(xs) - min(xs), max(ys) - min(ys)) + 50
    for i in range(len(h)):
        (ax, ay), (bx, by) = h[i], h[(i + 1) % len(h)]
        l = math.hypot(bx - ax, by - ay)
        if l < 1e-6:
            continue
        nx, ny = (by - ay) / l, -(bx - ax) / l
        mx, my = (ax + bx) / 2 + nx * S / 2, (ay + by) / 2 + ny * S / 2
        ob = adsk.core.OrientedBoundingBox3D.create(P(mx, my, (z0 + z1) / 2), V(nx, ny, 0), V(-ny, nx, 0),
                                                    S * MM, S * MM, (z1 - z0 + 10) * MM)
        tbm.booleanOperation(k, tbm.createBox(ob), adsk.fusion.BooleanTypes.DifferenceBooleanType)
    return k


def huellkoerper(punkte):
    """Konvexer Körper aus 3D-Punkten (Keile, Stützkegel), ohne ihn abzulegen."""
    k = netz(root, "_tmp", punkte)
    _wartend[root.entityToken][1].pop()
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


def schnitt(k, w):
    tbm.booleanOperation(k, w, adsk.fusion.BooleanTypes.IntersectionBooleanType)
    return k


def ring(x, y, z0, z1, ra, ri):
    return minus(zyl(x, y, z0, z1, ra), zyl(x, y, z0 - 1, z1 + 1, ri))


def ablegen(comp, name, k, f):
    _wartend.setdefault(comp.entityToken, (comp, []))[1].append((name, k, f))


def riemen(x1, r1, x2, r2, z0, z1, t=1.6):
    aussen = prisma(kreis(x1, 0, r1 + t, 40) + kreis(x2, 0, r2 + t, 40), z0, z1)
    return minus(aussen, prisma(kreis(x1, 0, r1, 40) + kreis(x2, 0, r2, 40), z0 - 1, z1 + 1))


def zahnscheibe(x, y, z0, z1, z_zahl, teilung, pld, tiefe, rg):
    """Zahnscheibe mit Rillen (Kreisbögen): Aussendurchmesser = Teilkreis - 2 × PLD."""
    ra = z_zahl * teilung / math.pi / 2 - pld
    k = zyl(x, y, z0, z1, ra)
    rc = ra - tiefe + rg
    for i in range(z_zahl):
        a = 2 * math.pi * i / z_zahl
        minus(k, zyl(x + rc * math.cos(a), y + rc * math.sin(a), z0 - 1, z1 + 1, rg))
    return k


def okt(r):
    return vieleck(r, 8, math.pi / 8)


def haelften(k, fuge=0.2):
    a, b = tbm.copy(k), tbm.copy(k)
    schnitt(a, quader(-300, 300, fuge / 2, 300, -50, 300))
    schnitt(b, quader(-300, 300, -300, -fuge / 2, -50, 300))
    return a, b


def polar(r, w):
    return r * math.cos(math.radians(w)), r * math.sin(math.radians(w))


# ---------------------------------------------------------------- Aufräumen
for i in range(root.occurrences.count - 1, -1, -1):
    if root.occurrences.item(i).component.name.startswith("Basis_J1"):
        root.occurrences.item(i).deleteMe()
B = komponente(root, "Basis_J1")
fest = komponente(B, "Basis_fest")
kauf = komponente(B, "Basis_Kaufteile")
dreh = komponente(B, "J1_Drehteil", (0, 0, 0), (0, 0, 1), Q1)
schale = komponente(B, "Basis_Schalen")
hilfe = komponente(B, "Basis_Hilfskoerper")       # Schraubenköpfe, Kabel (nur Prüfung)

# ================================================================ Grundplatte (PLA grau)
zp = ZAPFEN
la = LASCHE
gp = prisma(okt(SO_R), 0, BODEN)
plus(gp, quader(la["x0"], la["x1"], la["y0"], la["y1"], 0, BODEN))
plus(gp, zyl(0, 0, BODEN, LU, zp["r_bund"]), zyl(0, 0, LU - 0.5, zp["oben"], L6810["welle"] / 2))
RIPPEN = {0: 46.0, 45: 62.0, 135: 50.0, 180: 62.0, 225: 62.0, 270: 62.0, 315: 62.0}
for w, r_end in RIPPEN.items():                                                    # 7 Rippen 5 × 10
    a = math.radians(w)
    pts = [(math.cos(a) * r - math.sin(a) * s, math.sin(a) * r + math.cos(a) * s) for r in (20.0, r_end) for s in (-2.5, 2.5)]
    plus(gp, prisma(pts, BODEN - 0.1, 15.0))
minus(gp, zyl(0, 0, -1, zp["oben"] + 1, zp["bohr"] / 2))
f0, f1, fb = zp["fenster"]
minus(gp, quader(-fb / 2, fb / 2, 0, zp["r_bund"] + 3, f0, f1))                    # Kabelfenster nach +y
HOLZ_SCHR = [polar(70, w) for w in (340.0, 112.5, 225.0, 315.0)] + [polar(40, 67.5 + 90 * k) for k in range(4)]
for x, y in HOLZ_SCHR:
    minus(gp, zyl(x, y, -1, BODEN + 1, 2.25))
SPANN_SCHR = [polar(SPANN["schr_r"], 90 + 120 * k) for k in range(3)]
for x, y in SPANN_SCHR:
    minus(gp, zyl(x, y, zp["oben"] - 8, zp["oben"] + 1, INS))
    EINSAETZE.append(("Grundplatte", x, y, zp["oben"] - 5, x, y, zp["oben"]))
# Lasche: 4 Muttertaschen M3 von unten für den Bock, Spannklotz
BOCK_SCHR = [(XZ + dx, y) for dx in (-8, 8) for y in (-36.0, 47.0)]
for x, y in BOCK_SCHR:
    minus(gp, zyl(x, y, -1, BODEN + 1, 1.7), prisma([(x + u, y + v) for u, v in vieleck(3.2, 6)], -1, 2.6))
KLOTZ = (XZ - 24.0, XZ - 16.0)                                                     # hinter dem Bockrücken
SP_Y, SP_Z = 35.0, 12.0
plus(gp, quader(KLOTZ[0], KLOTZ[1], 28, 40, BODEN - 0.1, 18.0))
minus(gp, zyl_x(KLOTZ[0] - 1, KLOTZ[1] + 1, SP_Y, SP_Z, 1.7))
# Endschalter-Säule mit Anschlagfinger (vorne, +x)
sw = SCHALTER
ANSCHLAG_W = 25.0                                                                  # Lage des Anschlagfingers (Grad)


def radial_quader(w, r0, r1, b, z0, z1):
    a = math.radians(w)
    return prisma([(math.cos(a) * r - math.sin(a) * t, math.sin(a) * r + math.cos(a) * t) for r in (r0, r1) for t in (-b / 2, b / 2)], z0, z1)


HALTER = dict(z0=sw["z0"] - 4.0, x1=sw["x1"] + 6.5)                               # Lasche 0,5 vor dem Absatz (1 Scheibe)
ABSATZ_X1 = sw["x1"] + 6.0
plus(gp, quader(sw["x0"], ABSATZ_X1, -12, 12, BODEN - 0.1, HALTER["z0"]),          # Absatz für den Halter
     radial_quader(ANSCHLAG_W, 52.0, 70.0, 16.0, BODEN - 0.1, 53.0),               # Pfosten massiv
     radial_quader(ANSCHLAG_W, 46.0, 52.1, 6.0, 47.0, 53.0))                       # Fingerstummel
_af = math.radians(ANSCHLAG_W)
plus(gp, huellkoerper([(math.cos(_af) * r - math.sin(_af) * t, math.sin(_af) * r + math.cos(_af) * t, z)
                       for t in (-3.0, 3.0) for (r, z) in ((52.1, 41.0), (52.1, 47.0), (46.0, 47.0))]))  # 45°-Schräge
SW_SCHR = [(55.0, -4.75), (55.0, 4.75)]
HALTER_SCHR = (ABSATZ_X1, 0.0, HALTER["z0"] - 7.0)                                 # M3 waagrecht von vorne
minus(gp, zyl_x(HALTER_SCHR[0] - 8, HALTER_SCHR[0] + 1, 0.0, HALTER_SCHR[2], INS))
for x, y in SW_SCHR:                                                                # Nuten für die Schraubenenden
    minus(gp, quader(sw["x0"] - 1, ABSATZ_X1 + 1, y - 2.2, y + 2.2, HALTER["z0"] - 3.0, HALTER["z0"] + 1))
EINSAETZE.append(("Grundplatte", HALTER_SCHR[0] - 5, 0.0, HALTER_SCHR[2], HALTER_SCHR[0], 0.0, HALTER_SCHR[2]))
for x in (-20.0, -45.0):                                                            # Kabelbinder-Ösen (Niederhalter)
    for y in (37.0, 53.0):
        minus(gp, quader(x - 2, x + 2, y - 1, y + 1, -1, BODEN + 1))
    minus(gp, quader(x - 2, x + 2, 36.0, 54.0, -1, 1.5))
for w in (22.5, 112.5, 247.5, 337.5):                                               # Magnete zum Gehäuse
    x, y = polar(82, w)
    minus(gp, zyl(x, y, BODEN - MAG[1], BODEN + 1, MAG[0]))
for w in (67.5, 292.5):                                                              # Zylinderstifte
    x, y = polar(82, w)
    minus(gp, zyl(x, y, BODEN - 4, BODEN + 1, 1.55))
ablegen(fest, "Grundplatte", gp, "Grau")

# ================================================================ Lager 6810, O-Ring, Spannring
ablegen(kauf, "Lager_6810_unten", ring(0, 0, LU, LU + L6810["B"], L6810["D"] / 2, L6810["d"] / 2), "Stahl")
ablegen(kauf, "Lager_6810_oben", ring(0, 0, LO, LO + L6810["B"], L6810["D"] / 2, L6810["d"] / 2), "Stahl")
zo = zp["oben"]
sp = ring(0, 0, zo, zo + SPANN["h"], SPANN["r"], SPANN["ri"])
minus(sp, ring(0, 0, zo - 1, zo + 0.5, SPANN["r"] + 1, 24.95),                        # Freistich 0,5 über dem Lager
      ring(0, 0, zo - 1, zo + 0.5 + ORING["tiefe"], ORING["ra"], ORING["ri"]))      # Nut O-Ring
for x, y in SPANN_SCHR:
    minus(sp, zyl(x, y, zo - 1, zo + 10, 1.7))
ablegen(fest, "Spannring", sp, "Grau")
ablegen(kauf, "O_Ring_50x1_5", ring(0, 0, zo, zo + 1.1, ORING["ra"] - 0.25, ORING["ri"] + 0.25), "Motor")

# ================================================================ Nabe = Drehteller (PLA grau)
n = NABE
fz0, fz1 = n["flansch"]
nabe = zahnscheibe(0, 0, Z3[0], Z3[1], 80, 3.0, 0.381, 1.17, 0.95)
plus(nabe, zyl(0, 0, n["z0"], Z3[0], 41.0, 37.4),                                  # Bord unten (Kegel)
     zyl(0, 0, Z3[1], Z3[1] + 3.0, 37.4, 41.0),                                    # Bord oben (Kegel)
     zyl(0, 0, Z3[1] + 3.0, Z3[1] + 4.0, 41.0),
     zyl(0, 0, Z3[1] + 4.0, Z3[1] + 7.5, 41.0, 37.4),                              # 45°-Kegel (Druck kopfüber)
     zyl(0, 0, Z3[1], fz0 + 0.1, n["r_rohr"]),
     prisma(vieleck(n["r_flansch"], 12, math.pi / 12), fz0, fz1))
# Halbmond (y < 0) und Mitnehmer für den Anschlag
RAMPE = 12.0                                                                       # Grad, Rampe an jedem Ende
rampen = []
for a0, a1, r0, r1 in ((176.0, 184.0, 42.0, 44.0), (360.0 - RAMPE, 360.0, 44.0, 42.0)):
    pts = []
    for i in range(7):
        a = math.radians(a0 + (a1 - a0) * i / 6)
        r = r0 + (r1 - r0) * i / 6
        pts.append((r * math.cos(a), r * math.sin(a)))
    pts += [polar(37.5, a0), polar(37.5, a1)]
    rampen.append(prisma(pts, 39.0, 46.0))
hm = ring(0, 0, 39.0, 46.0, 42.0, 37.0)
schnitt(hm, quader(-50, 50, -50, 0, 30, 50))
hm_aussen = ring(0, 0, 39.0, 46.0, 44.0, 41.9)
schnitt(hm_aussen, prisma([(0, 0)] + [polar(60, w) for w in range(184, 361 - int(RAMPE), 4)], 30, 50))
plus(hm, hm_aussen, *rampen)
kegel_hm = zyl(0, 0, 46.0, 52.5, 44.0, 37.4)                                       # 45°-Kegel über dem Halbmond
schnitt(kegel_hm, quader(-50, 50, -50, 0, 30, 60))
MITN_W = 180.0 + ANSCHLAG_W
mitn = radial_quader(MITN_W, 36.0, 50.0, 5.0, 47.0, 53.0)
_a = math.radians(MITN_W)
_rot = lambda r, t: (math.cos(_a) * r - math.sin(_a) * t, math.sin(_a) * r + math.cos(_a) * t)
keil = huellkoerper([_rot(r, t) + (z,) for t in (-2.5, 2.5) for (r, z) in ((50.0, 53.0), (36.0, 53.0), (37.0, 66.0))])
plus(nabe, hm, kegel_hm, mitn, keil)
minus(nabe, zyl(0, 0, n["z0"] - 1, LU, 33.0),                                     # K1: Lager von unten
      zyl(0, 0, LU - 0.01, LU + L6810["B"], L6810["sitz"] / 2),
      zyl(0, 0, LU, LO + 0.01, 31.0),                                             # Schulter Ø 62
      zyl(0, 0, LO, fz1 + 1, L6810["sitz"] / 2))
M5_POS = [polar(n["lochkreis"] / 2, 45 + 90 * k) for k in range(4)]
for x, y in M5_POS:
    minus(nabe, zyl(x, y, fz0 - 1, fz1 + 1, 2.75), prisma([(x + u, y + v) for u, v in vieleck(4.7, 6)], fz0 - 1, fz0 + 4.5))
ablegen(dreh, "Nabe_Drehteller", nabe, "Anthrazit")

# ================================================================ Zwischenwelle, Bock (zweiteilig)
b = BOCK
hx = b["hx"]
bu = quader(XZ - hx, XZ + hx, b["y0"], b["wy"][1], b["arm_u"][0], b["arm_u"][1])
plus(bu, zyl(XZ, 0, b["arm_u"][0], b["arm_u"][1], 15),
     quader(XZ - hx, XZ + hx, b["wy"][0], b["wy"][1], BODEN, b["ruecken"]),
     quader(XZ - 16, XZ + 16, -42.0, b["y0"] + 0.1, BODEN, BODEN + 5),             # Lasche -y
     quader(XZ - 16, XZ + 16, b["wy"][1] - 0.1, 54.0, BODEN, BODEN + 5))           # Lasche +y
minus(bu, zyl(XZ, 0, 8, b["arm_u"][1] + 1, 11.1), zyl(XZ, 0, 0, 30, 6.5))           # Freigang Innenring
for x, y in BOCK_SCHR:
    minus(bu, quader(x - 6.5, x + 6.5, y - 1.7, y + 1.7, 0, 20))
minus(bu, zyl_x(XZ - hx - 1, XZ - hx + 6, SP_Y, SP_Z, INS))                       # Spannschraube im Rücken
EINSAETZE.append(("Bock_unten", XZ - hx, SP_Y, SP_Z, XZ - hx + 5, SP_Y, SP_Z))
DECKEL_SCHR = [(XZ - 5, 35.0), (XZ + 5, 35.0)]
DECKEL_STIFT = [(XZ - 11, 35.0), (XZ + 11, 35.0)]
for x, y in DECKEL_SCHR:
    minus(bu, zyl(x, y, b["ruecken"] - 10, b["ruecken"] + 1, INS))
    EINSAETZE.append(("Bock_unten", x, y, b["ruecken"] - 5, x, y, b["ruecken"]))
for x, y in DECKEL_STIFT:
    minus(bu, zyl(x, y, b["ruecken"] - 6, b["ruecken"] + 1, 1.55))
ablegen(fest, "Bock_unten", bu, "Grau")
bo = quader(XZ - hx, XZ + hx, b["y0"], b["wy"][1], b["arm_o"][0], b["arm_o"][1])
plus(bo, zyl(XZ, 0, b["arm_o"][0], b["arm_o"][1], 15))
minus(bo, zyl(XZ, 0, b["arm_o"][0] - 1, b["arm_o"][0] + 7.7, 11.1), zyl(XZ, 0, 60, 90, 6.5))
for x, y in DECKEL_SCHR:
    minus(bo, zyl(x, y, 60, 90, 1.7), zyl(x, y, b["arm_o"][1] - 1.7, b["arm_o"][1] + 0.01, 1.7, 3.3))  # Senkung
for x, y in DECKEL_STIFT:
    minus(bo, zyl(x, y, 60, b["arm_o"][1] - 2, 1.55))
ablegen(fest, "Bock_Deckel", bo, "Grau")
ablegen(kauf, "Welle_8x72", zyl(XZ, 0, 6.5, 78.5, 4), "Stahl")
ablegen(kauf, "Lager_608_unten", ring(XZ, 0, 8, 15, 11, 4), "Stahl")
ablegen(kauf, "Lager_608_oben", ring(XZ, 0, 69.5, 76.5, 11, 4), "Stahl")
ablegen(fest, "Distanzring_unten", ring(XZ, 0, 15, 16.5, 6, 4.1), "Grau")
r16 = zyl(XZ, 0, 16.5, 18.5, 8)
plus(r16, zyl(XZ, 0, 18.5, Z3[0], 10.5), zyl(XZ, 0, Z3[0], Z3[1], d3_16 / 2 - 0.38), zyl(XZ, 0, Z3[1], Z3[1] + 1, 10.5))
ablegen(kauf, "Ritzel_3M_16Z", r16, "Alu")
s80 = zahnscheibe(XZ, 0, Z2[0], Z2[1], 80, 2.0, 0.254, 0.75, 0.6)
plus(s80, zyl(XZ, 0, 45.0, 52.0, 10), zyl(XZ, 0, 52.0, Z2[0], 28, 25.4), zyl(XZ, 0, Z2[1], Z2[1] + 1.5, 28))
minus(s80, zyl(XZ, 0, 40, 70, 4.05), zyl_x(XZ - 11, XZ - 3, 0, 48.5, INS), zyl_y(XZ, 3, 11, 48.5, INS))
EINSAETZE.append(("Scheibe_GT2_80Z", XZ - 9, 0, 48.5, XZ - 4, 0, 48.5))
EINSAETZE.append(("Scheibe_GT2_80Z", XZ, 4, 48.5, XZ, 9, 48.5))
ablegen(fest, "Scheibe_GT2_80Z", s80, "Grau")
ablegen(fest, "Distanzring_oben", ring(XZ, 0, Z2[1] + 1.5, 69.5, 6, 4.1), "Grau")

# ================================================================ Motor J1 im Kasten
m = MOTOR
mk = m["k"] / 2
mot = quader(XM - mk, XM + mk, -mk, mk, m["face"] - m["l"], m["face"])
plus(mot, zyl(XM, 0, m["face"], m["face"] + 2, 11), zyl(XM, 0, m["face"], m["face"] + m["welle"], 2.5))
ablegen(kauf, "Motor_J1_17CS04A", mot, "Motor")
r20 = zyl(XM, 0, m["face"] + 5.5, Z2[0], 8)
plus(r20, zyl(XM, 0, Z2[0], Z2[1], d2_20 / 2 - 0.25), zyl(XM, 0, Z2[1], Z2[1] + 0.8, 8))
ablegen(kauf, "Ritzel_GT2_20Z", r20, "Alu")
ka = KASTEN_P
kp = [(ka["xb"], -ka["b"] / 2), (ka["xb"], ka["b"] / 2), (ka["xa"] + ka["fase"], ka["b"] / 2),
      (ka["xa"], ka["b"] / 2 - ka["fase"]), (ka["xa"], -ka["b"] / 2 + ka["fase"]), (ka["xa"] + ka["fase"], -ka["b"] / 2)]
MAG_KASTEN = [(x, sy * 53) for x in (-150.0, -100.0) for sy in (-1, 1)]
MP_X = (XM - 31.0, XM + 30.0)                                                      # Motorplatte, Spannweg nach hinten
SPANNWEG_M = 7.0
mp = schnitt(prisma(einziehen2(kp, WAND + 0.5), m["face"], m["face"] + 5), quader(MP_X[0], MP_X[1], -80, 80, 0, 60))
schnitt(mp, prisma([(x + SPANNWEG_M, y) for x, y in einziehen2(kp, WAND + 0.5)], m["face"] - 1, m["face"] + 6))
minus(mp, zyl(XM, 0, 0, 60, 11.5))
for x, y in MAG_KASTEN:
    sy_ = 1 if y > 0 else -1
    minus(mp, quader(x - 13, x + 13, y - 7 * sy_, y + 10 * sy_, 40, 55))
for sx in (-15.5, 15.5):
    for sy in (-15.5, 15.5):
        minus(mp, quader(XM + sx - 6, XM + sx + 6, sy - 1.7, sy + 1.7, 40, 55))
AUFLAGE = [(x, sy * 52) for x in (MP_X[0] + 8, MP_X[1] - 10) for sy in (-1, 1)]
for x, y in AUFLAGE:
    minus(mp, quader(x - 1.7, x + SPANNWEG_M + 3.4, y - 1.7, y + 1.7, 40, 55))     # Langloch: Platte wandert nach hinten
ablegen(fest, "Motorplatte", mp, "PETG")

ablegen(kauf, "Riemen_3M_318_15", riemen(0, d3_80 / 2, XZ, d3_16 / 2, Z3[0] + 0.5, Z3[1] - 0.5), "Riemen")
ablegen(kauf, "Riemen_GT2_240_10", riemen(XZ, d2_80 / 2, XM, d2_20 / 2, Z2[0] + 0.5, Z2[1] - 0.5, 1.4), "Riemen")
es = quader(sw["x0"], sw["x1"], -10, 10, sw["z0"], sw["z0"] + sw["h"])              # KW11 liegend
plus(es, quader(sw["rolle_frei"] + sw["rolle_r"], sw["x0"], -1.0, 1.0, sw["z0"] + 1.5, sw["z0"] + 4.9))
ablegen(kauf, "Endschalter_J1_KW11", es, "Motor")
ablegen(kauf, "Endschalter_Rolle", zyl(sw["rolle_frei"] + sw["rolle_r"], 0, sw["z0"] + 1.0, sw["z0"] + 5.4, sw["rolle_r"]), "Stahl")
ha = quader(sw["x0"], HALTER["x1"], -11, 11, HALTER["z0"], sw["z0"])                # Platte unter dem Schalter
plus(ha, quader(HALTER["x1"], HALTER["x1"] + 4, -6, 6, HALTER_SCHR[2] - 5, sw["z0"]))  # Lasche vorne
for x, y in SW_SCHR:
    minus(ha, zyl(x, y, HALTER["z0"] - 1, sw["z0"] + 1, 1.1),
          prisma([(x + u, y + v) for u, v in vieleck(2.45, 6)], HALTER["z0"] - 1, HALTER["z0"] + 1.8))
minus(ha, zyl_x(HALTER["x1"] - 1, HALTER["x1"] + 5, 0.0, HALTER_SCHR[2], 1.7))
ablegen(fest, "Schalterhalter", ha, "Grau")

# ================================================================ Motorkasten (PLA grau)
kas = prisma(kp, 0, ka["h"])
minus(kas, prisma(einziehen2(kp, WAND), ka["boden"], ka["h"] + 1),
      quader(ka["xb"] - 10, ka["xb"] + 1, -50, 50, ka["boden"], ka["h"] + 1),
      zyl_x(ka["xa"] - 2, ka["xa"] + 6, 30, 20, 8),                                # Kabelaustritt (Verschraubung M16)
      prisma(okt(SO_R), -1, ka["h"] + 1),
      quader(la["x0"] - 0.3, la["x1"], la["y0"] - 0.3, la["y1"] + 0.3, -1, BODEN + 0.3))
for sy in (-1, 1):                                                                 # Auflagen mit 45°-Stütze
    y_in, y_aus = sy * (ka["b"] / 2 - WAND - 8), sy * (ka["b"] / 2 - WAND)
    xa_, xb_ = ka["xa"] + ka["fase"] + 2, MP_X[1] + 2
    plus(kas, quader(xa_, xb_, y_in, y_aus, m["face"] - 4, m["face"]))
    plus(kas, huellkoerper([(x, y, z) for x in (xa_, xb_) for (y, z) in ((y_in, m["face"] - 4), (y_aus, m["face"] - 4),
                                                                          (y_aus, m["face"] - 12))]))
for x, y in MAG_KASTEN:
    plus(kas, zyl(x, y, ka["h"] - 10, ka["h"], 6), zyl(x, y, ka["h"] - 16, ka["h"] - 10, 0.5, 6))
    minus(kas, zyl(x, y, ka["h"] - MAG[1], ka["h"] + 1, MAG[0]))
for x, y in AUFLAGE:
    minus(kas, zyl(x, y, m["face"] - 6, m["face"] + 1, INS))
    EINSAETZE.append(("Motorkasten", x, y, m["face"] - 5, x, y, m["face"]))
KASTEN_SCHR = [(-180.0, 35.0), (-180.0, -35.0), (-125.0, -45.0)]
for x, y in KASTEN_SCHR:
    minus(kas, zyl(x, y, -1, ka["boden"] + 1, 2.25))
ablegen(fest, "Motorkasten", kas, "Anthrazit")
ablegen(fest, "Steckerfeld_Platzhalter", quader(-174, -122, 51, 54, ka["boden"], 30), "Grau")

# ================================================================ Schalen
geh = prisma(okt(SO_R), BODEN, DECK[1])
minus(geh, prisma(okt(SO_R - WAND / math.cos(math.pi / 8)), BODEN - 1, DECK[0]),
      zyl(0, 0, DECK[0] - 1, DECK[1] + 1, RING_RI),
      quader(-100, -55, -56, 56, BODEN - 1, 80.5))
for w in (22.5, 67.5, 112.5, 247.5, 292.5, 337.5):
    x, y = polar(82, w)
    plus(geh, zyl(x, y, BODEN, BODEN + 10, 7), zyl(x, y, BODEN + 10, BODEN + 17, 7, 0.5))   # Kegel: druckbar
    if w in (67.5, 292.5):
        minus(geh, zyl(x, y, BODEN - 1, BODEN + 8, 1.55))
    else:
        minus(geh, zyl(x, y, BODEN - 1, BODEN + MAG[1], MAG[0]))
WINKEL_RING = (45, 135, 225, 315)
for w in WINKEL_RING:
    x, y = polar(60, w)
    minus(geh, zyl(x, y, DECK[1] - MAG[1], DECK[1] + 1, MAG[0]))
for zf in (30.0, 60.0):                                                            # Fuge vorne: 2 Magnete quer
    plus(geh, quader(74, 83, -8, 8, zf - 7, zf + 7),
         huellkoerper([(x, y, z) for y in (-8, 8) for (x, z) in ((74, zf + 7), (83, zf + 7), (83, zf + 16))]))
    minus(geh, zyl_y(78.5, -MAG[1] - 0.1, MAG[1] + 0.1, zf, MAG[0]))
g_l, g_r = haelften(geh)
ablegen(schale, "Sockelgehaeuse_links", g_l, "Anthrazit")
ablegen(schale, "Sockelgehaeuse_rechts", g_r, "Anthrazit")
fr = ring(0, 0, RING_Z[0], RING_Z[1], 76.0, RING_RI)
for w in WINKEL_RING:
    x, y = polar(60, w)
    minus(fr, zyl(x, y, RING_Z[0] - 1, RING_Z[0] + MAG[1], MAG[0]))
f_l, f_r = haelften(fr)
ablegen(schale, "Farbring_J1_links", f_l, "Rot")
ablegen(schale, "Farbring_J1_rechts", f_r, "Rot")
kappe = [(x, y, ka["h"]) for x, y in kp]
kappe += [(x, y, ka["h"] + 12) for x, y in einziehen2(kp, 6)]
kappe += [(x, y, ka["h"] + 20) for x, y in einziehen2(kp, 24)]
kk = netz(schale, "Kastenkappe", kappe, "Weiss")
kk_voll = tbm.copy(kk)
for x, y in MAG_KASTEN:                                                             # massiv, mit 15 % Füllung drucken
    minus(kk, zyl(x, y, ka["h"] - 1, ka["h"] + MAG[1], MAG[0]))
minus(kk, prisma(okt(SO_R), ka["h"] - 1, ka["h"] + 30), zyl(XZ, 0, ka["h"] - 1, 82, 23.0),
      quader(XZ - hx - 3, XZ + hx + 3, b["y0"] - 3, b["wy"][1] + 3, ka["h"] - 1, b["arm_o"][1] + 3))

# ================================================================ Hilfskörper: Schraubenköpfe, Kabel (nur Prüfung)
def kopf(name, x, y, z, r=2.8, h=3.0):
    ablegen(hilfe, name, zyl(x, y, z, z + h, r), "Schraube")


for i, (x, y) in enumerate(BOCK_SCHR):
    kopf(f"Kopf_Bock_{i}", x, y, BODEN + 5)
for i, (x, y) in enumerate(AUFLAGE):
    kopf(f"Kopf_Auflage_{i}", x, y, m["face"] + 5)
for i, (x, y) in enumerate(SPANN_SCHR):
    kopf(f"Kopf_Spannring_{i}", x, y, zo + SPANN["h"])
for i, (x, y) in enumerate(HOLZ_SCHR):
    kopf(f"Kopf_Holz_{i}", x, y, BODEN, 4.0, 2.5)
ablegen(hilfe, "Kopf_Spannschraube", zyl_x(KLOTZ[0] - 3, KLOTZ[0], SP_Y, SP_Z, 2.8), "Schraube")
ablegen(hilfe, "Kopf_Halterschraube", zyl_x(HALTER["x1"] + 4, HALTER["x1"] + 7, 0.0, HALTER_SCHR[2], 2.8), "Schraube")
kab = quader(-6, 6, 24.0, 48.0, BODEN + 0.5, 15.5)                                 # Bündel 10 + USB, Weg zum Kasten
plus(kab, quader(-58, 6, 40.0, 50.0, BODEN + 0.5, 15.5), quader(-62, -54, 40.0, 50.0, BODEN + 0.5, 26.0),
     quader(-130, -56, 41.0, 51.0, 15.0, 26.0))
ablegen(hilfe, "Kabelweg_Platzhalter", kab, "Kabel")

# ================================================================ Passproben
test = komponente(B, "Basis_Testteile", (240, 0, 0))
pp = ring(0, 0, 0, L6810["B"] + 2, L6810["sitz"] / 2 + 3, L6810["sitz"] / 2)
plus(pp, ring(0, 0, 0, 2, L6810["sitz"] / 2 + 3, 31.0))
for w in (0, 120, 240):                                                            # Magnettaschen-Probe
    x, y = polar(L6810["sitz"] / 2 + 1.5 + 3, w)
    plus(pp, zyl(x, y, 0, 5, 5.5))
    minus(pp, zyl(x, y, 5 - MAG[1], 6, MAG[0]))
ablegen(test, "Passprobe_6810_Sitz_Magnet", pp, "Grau")
pz = zyl(0, 90, 0, 3, 30)
plus(pz, zyl(0, 90, 3, 3 + L6810["B"] + 2, L6810["welle"] / 2))
minus(pz, zyl(0, 90, -1, 20, ZAPFEN["bohr"] / 2))
for x, y in [polar(SPANN["schr_r"], 90 + 120 * k) for k in range(3)]:
    minus(pz, zyl(x, y + 90, 6, 13, INS))
ablegen(test, "Passprobe_6810_Zapfen", pz, "Grau")
spt = tbm.copy(sp)                                                                   # Spannring für die Probe
mt = adsk.core.Matrix3D.create()
mt.translation = adsk.core.Vector3D.create(0, -90 * MM, -zo * MM)
tbm.transform(spt, mt)
ablegen(test, "Spannring_fuer_Probe", spt, "Grau")

einfuegen()
print(f"C2 (3M-{L3M:.0f}) = {C2:.2f} mm, C1 (GT2-{LGT2:.0f}) = {C1:.2f} mm, Zwischenwelle x = {XZ:.1f}, Motor x = {XM:.1f}")
