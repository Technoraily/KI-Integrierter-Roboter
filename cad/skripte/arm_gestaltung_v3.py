"""Gestaltungsmodell V3.1 (NUR Form und Optik, keine Mechanik).

V3.1: Gutachten Runde 2 eingearbeitet (dunkler Fuss an J2, Oberarm in einem Zug,
Längsgrate, Schulterhaube statt Teller, Unterarm gegliedert, Hand in Pose).

Änderungen gegenüber V2 (Rückmeldung Nutzer + Gutachten 26.11.2026):
- Oberarm beidseitig gelagert: Der Schulterbock ist eine Gabel aus zwei schmalen
  Wangen; der Oberarm-Fuss mit der grossen J2-Scheibe (ca. 143 mm) liegt dazwischen.
  Nur EIN grosser Kreis an J2 (Oberarm-Fuss), die Wangen bleiben klein.
- Oberarm schlank mit Taille; am Ellbogen eine Gabel aus zwei Wangen, die den
  Unterarm-Fuss mit der J3-Scheibe (ca. 95 mm) beidseitig fasst. Kein Querversatz.
- Ellbogen-«Rucksack» hinter J3, Unterarm vorn kantig, Handgelenk als Gabel,
  Hand geneigt; flacher Drehteller; ruhiger 8-eckiger Sockel mit Kasten.

Ausführen im Fusion-Python (MCP-Add-in):
    exec(open(pfad, encoding="utf-8").read())
Masse in mm; Weltachsen: x nach vorn, y quer, z nach oben, z = 0 Tisch.
"""
import math

import adsk.core
import adsk.fusion

MM = 0.1

# ---------------------------------------------------------------- Pose (Grad)
Q1, Q2, Q3, Q4, Q5, Q6 = 0.0, -25.0, 115.0, 0.0, -35.0, 0.0

# ---------------------------------------------------------------- Hauptmasse (docs/parameter.md)
H_SCHULTER, L_OBERARM, L_UNTERARM, L_HAND = 200.0, 200.0, 190.0, 60.0

# ---------------------------------------------------------------- Formparameter (Startwerte)
N = 5                                                   # Segmente je Halbkreis (Low-Poly)
SPALT = 2.0                                             # Luft zwischen bewegten Teilen
SOCKEL = dict(r=92.0, h=85.0, fase=5.0)                 # 8-Eck, dunkel
KASTEN = dict(x=-128.0, b=118.0, t=92.0)                # Elektronikkasten, gleiche Höhe wie Sockel
RING = dict(r=76.0, t=6.0)                              # Farbring J1
DREH = dict(r=72.0, h=12.0, fase=3.0)                   # Drehteller J1, gerade Wände
HAUBE = dict(l=120.0, l_oben=70.0, h=14.0, b=46.0, fase=4.0)   # Schulterhaube unter den Wangen
OA_B = 30.0                                             # halbe Breite Oberarm-Fuss (zwischen den Wangen)
WANGE = dict(t=14.0, r_unten=42.0, r_oben=50.0, z_unten=112.0, fase=6.0)  # Schulterbock-Wangen
GRAT = dict(h=4.0, versatz=8.0, s=0.5)                  # Längsgrat auf Aussenflächen
OBERARM = dict(r2=76.0, r_taille=44.0, l_taille=100.0, fase=12.0,
               weiss_ab=35.0, weiss_r=52.0,              # Fuss dunkel um J2, weiss erst ab hier
               joch_z=(88.0, 108.0), joch_r=(30.0, 36.0),
               gabel_r=(40.0, 54.0), gabel_z0=95.0, gabel_t=12.0, gabel_fase=5.0)
UA_B = 30.0                                             # halbe Breite Unterarm-Fuss (in der Ellbogengabel)
UNTERARM = dict(r3=50.0, r_hinten=36.0, l_hinten=85.0, fase=8.0,
                rucksack_l=55.0, rucksack_r=40.0,
                ring_r=33.0, ring_t=6.0,
                vorn=((70.0, 64.0, 14.0), (60.0, 56.0, 12.0)), vorn_z1=160.0)
HANDGABEL = dict(b_innen=22.0, t=12.0, r0=30.0, r1=30.0, z0=160.0, fase=4.0, kappe_r=20.0)
HAND = dict(w=44.0, k=10.0, z0=-12.0, z1=40.0, ring_r=28.0, ring_t=8.0, flansch_r=22.0)
AKZENT = (196, 64, 60)

app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
design.designType = adsk.fusion.DesignTypes.ParametricDesignType
root = design.rootComponent
tbm = adsk.fusion.TemporaryBRepManager.get()
P = lambda x, y, z: adsk.core.Point3D.create(x * MM, y * MM, z * MM)
V = adsk.core.Vector3D.create

_FARBEN = {"Weiss": (236, 234, 228), "Anthrazit": (72, 74, 78), "Grau": (120, 124, 130), "Akzent": AKZENT}


def farbe(name):
    voll = "AG3_" + name
    a = design.appearances.itemByName(voll)
    if a:
        return a
    lib = app.materialLibraries.itemByName("Fusion Appearance Library")
    a = design.appearances.addByCopy(lib.appearances.itemByName("Plastic - Matte (White)"), voll)
    r, g, b = _FARBEN[name]
    for i in range(a.appearanceProperties.count):
        p = a.appearanceProperties.item(i)
        if isinstance(p, adsk.core.ColorProperty) and p.value:
            p.value = adsk.core.Color.create(r, g, b, 255)
            break
    return a


def komponente(eltern, name, verschiebung=(0, 0, 0), achse=None, winkel=0.0):
    m = adsk.core.Matrix3D.create()
    if achse:
        m.setToRotation(math.radians(winkel), V(*achse), adsk.core.Point3D.create(0, 0, 0))
    m.translation = V(*(v * MM for v in verschiebung))
    occ = eltern.occurrences.addNewComponent(m)
    occ.component.name = name
    return occ.component


def ebene_komp(eltern, name, laengs=0.0):
    """Hilfskomponente in der Armebene: lokal x = vorn, lokal y = entlang Glied
    (= z der Eltern), lokal z = -y der Eltern (Dicke). laengs verschiebt entlang Glied."""
    m = adsk.core.Matrix3D.create()
    m.setToRotation(math.radians(90.0), V(1, 0, 0), adsk.core.Point3D.create(0, 0, 0))
    m.translation = V(0, 0, laengs * MM)
    occ = eltern.occurrences.addNewComponent(m)
    occ.component.name = name
    return occ.component


# ---------------------------------------------------------------- Umrisse
def stadion(r0, r1, L, n=N, y0=0.0):
    pts = []
    for i in range(n + 1):
        a = math.pi + math.pi * i / n
        pts.append((r0 * math.cos(a), y0 + r0 * math.sin(a)))
    for i in range(n + 1):
        a = math.pi * i / n
        pts.append((r1 * math.cos(a), y0 + L + r1 * math.sin(a)))
    return pts


def vieleck(r, n, phase=0.0):
    return [(r * math.cos(phase + 2 * math.pi * i / n), r * math.sin(phase + 2 * math.pi * i / n)) for i in range(n)]


def achteck(w, h, k):
    k = min(k, w / 2 - 1, h / 2 - 1)
    return [(w / 2 - k, h / 2), (-w / 2 + k, h / 2), (-w / 2, h / 2 - k), (-w / 2, -h / 2 + k),
            (-w / 2 + k, -h / 2), (w / 2 - k, -h / 2), (w / 2, -h / 2 + k), (w / 2, h / 2 - k)]


def _profil(comp, z, pts):
    if abs(z) < 1e-9:
        ebene = comp.xYConstructionPlane
    else:
        ei = comp.constructionPlanes.createInput()
        ei.setByOffset(comp.xYConstructionPlane, adsk.core.ValueInput.createByReal(z * MM))
        ebene = comp.constructionPlanes.add(ei)
        ebene.isLightBulbOn = False
    sk = comp.sketches.add(ebene)
    sk.isVisible = False
    lines = sk.sketchCurves.sketchLines
    p3 = [adsk.core.Point3D.create(x * MM, y * MM, 0) for x, y in pts]
    for i in range(len(p3)):
        lines.addByTwoPoints(p3[i], p3[(i + 1) % len(p3)])
    return sk.profiles.item(0)


def loft(comp, name, schnitte, f="Weiss"):
    """Kantiger Loft: je zwei benachbarte Schnitte ein eigener (gerader) Loft,
    danach verbunden. So bleiben alle Facetten eben (Low-Poly), statt dass ein
    Loft über mehrere Schnitte die Flächen wölbt."""
    profile = [_profil(comp, z, pts) for z, pts in schnitte]
    koerper = []
    for a, b in zip(profile[:-1], profile[1:]):
        li = comp.features.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        li.loftSections.add(a)
        li.loftSections.add(b)
        li.isSolid = True
        koerper.append(comp.features.loftFeatures.add(li).bodies.item(0))
    k = koerper[0]
    if len(koerper) > 1:
        werkzeuge = adsk.core.ObjectCollection.create()
        for kk in koerper[1:]:
            werkzeuge.add(kk)
        ci = comp.features.combineFeatures.createInput(k, werkzeuge)
        ci.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
        k = comp.features.combineFeatures.add(ci).bodies.item(0)
    k.name = name
    k.appearance = farbe(f)
    return k


def platte(comp, name, r0, r1, L, ya, yb, fase, seite="beide", f="Weiss", n=N, y0=0.0):
    """Stadion-Platte in einer ebene_komp zwischen Welt-y ya < yb (lokal z = -y).
    seite: 'plus' Fase auf der +y-Fläche, 'minus' auf der -y-Fläche, 'beide'."""
    voll = stadion(r0, r1, L, n, y0)
    mitte = stadion(r0 - fase * 0.35, r1 - fase * 0.35, L, n, y0)
    klein = stadion(r0 - fase, r1 - fase, L, n, y0)
    z_plus, z_minus = -yb, -ya            # lokale z der +y- bzw. -y-Fläche
    t = yb - ya
    if seite == "plus":
        return loft(comp, name, [(z_plus, klein), (z_plus + t * 0.4, mitte), (z_minus, voll)], f)
    if seite == "minus":
        return loft(comp, name, [(z_plus, voll), (z_minus - t * 0.4, mitte), (z_minus, klein)], f)
    return loft(comp, name, [(z_plus, klein), (z_plus + t * 0.2, mitte), (z_plus + t * 0.5, voll),
                             (z_minus - t * 0.2, mitte), (z_minus, klein)], f)


def grat(comp, name, r0, r1, L, y_flaeche, richtung, y0=0.0, f="Weiss"):
    """Längsgrat auf einer Aussenfläche (Welt-y = y_flaeche, richtung +1 = nach +y):
    flache Kuppe, aus der Gliedmitte versetzt (Arctos-Facetten)."""
    g = GRAT
    v = g["versatz"]
    unten = [(x + v, y) for x, y in stadion(r0 * g["s"], r1 * g["s"], L, N, y0)]
    oben = [(x + v, y) for x, y in stadion(r0 * g["s"] * 0.55, r1 * g["s"] * 0.55, L, N, y0)]
    return loft(comp, name, [(-y_flaeche, unten), (-(y_flaeche + richtung * g["h"]), oben)], f)


def einziehen(pts, d):
    cx = sum(x for x, _ in pts) / len(pts)
    cy = sum(y for _, y in pts) / len(pts)
    out = []
    for x, y in pts:
        dx, dy = x - cx, y - cy
        l = math.hypot(dx, dy) or 1.0
        out.append((x - dx / l * d, y - dy / l * d))
    return out


# ---------------------------------------------------------------- Scheiben (Temp-BRep)
_wartend = {}


def scheibe(comp, name, mitte, achse, r, b, f="Grau", fase=0.0):
    ax = [a * b / 2 for a in achse]
    p0 = [mitte[i] - ax[i] for i in range(3)]
    p1 = [mitte[i] + ax[i] for i in range(3)]
    k = tbm.createCylinderOrCone(P(*p0), r * MM, P(*p1), (r - fase) * MM)
    _wartend.setdefault(comp.entityToken, (comp, []))[1].append((name, k, f))


def einfuegen():
    for comp, liste in _wartend.values():
        bf = comp.features.baseFeatures.add()
        bf.startEdit()
        for name, body, f in liste:
            kk = comp.bRepBodies.add(body, bf)
            kk.name = name
            kk.appearance = farbe(f)
        bf.finishEdit()
    _wartend.clear()


# ---------------------------------------------------------------- Aufräumen
for i in range(root.occurrences.count - 1, -1, -1):
    if root.occurrences.item(i).component.name.startswith("Arm_Gestaltung"):
        root.occurrences.item(i).deleteMe()

G = komponente(root, "Arm_Gestaltung_V3")

# ================================================================ Sockel (8-Eck) mit Kasten
s = SOCKEL
so = komponente(G, "Sockel")
ph = math.pi / 8
loft(so, "Sockel", [(0, vieleck(s["r"], 8, ph)), (s["h"] - s["fase"], vieleck(s["r"], 8, ph)),
                    (s["h"], vieleck(s["r"] - s["fase"], 8, ph))], "Anthrazit")
k = KASTEN
xa, xb = k["x"] - k["t"] / 2, k["x"] + k["t"] / 2
kp = [(xb, -k["b"] / 2), (xb, k["b"] / 2), (xa + 12, k["b"] / 2), (xa, k["b"] / 2 - 12),
      (xa, -k["b"] / 2 + 12), (xa + 12, -k["b"] / 2)]
kp_top = [(x if x > k["x"] else x + 10, y * 0.9) for x, y in kp]
loft(so, "Elektronikkasten", [(0, kp), (s["h"] - 10, kp), (s["h"], kp_top)], "Anthrazit")
scheibe(so, "Ring_J1", (0, 0, s["h"] + RING["t"] / 2), (0, 0, 1), RING["r"], RING["t"], "Akzent")

# ================================================================ J1: Drehteller, Haube, Gabel-Wangen
j1 = komponente(G, "Drehteil_J1", (0, 0, 0), (0, 0, 1), Q1)
z_d = s["h"] + RING["t"]
d = DREH
loft(j1, "Drehteller", [(z_d, vieleck(d["r"], 12, math.pi / 12)),
                        (z_d + d["h"] - d["fase"], vieleck(d["r"], 12, math.pi / 12)),
                        (z_d + d["h"], vieleck(d["r"] - d["fase"], 12, math.pi / 12))])
wange = ebene_komp(j1, "Wangen_Form", 0.0)
hb = HAUBE
z_h = z_d + d["h"]
trapez = [(-hb["l"] / 2, z_h), (hb["l"] / 2, z_h), (hb["l_oben"] / 2, z_h + hb["h"]), (-hb["l_oben"] / 2, z_h + hb["h"])]
loft(wange, "Schulterhaube", [(-hb["b"], einziehen(trapez, hb["fase"])), (-hb["b"] + hb["fase"], trapez),
                              (hb["b"] - hb["fase"], trapez), (hb["b"], einziehen(trapez, hb["fase"]))])
w = WANGE
L_w = H_SCHULTER - w["z_unten"]
yi = OA_B + SPALT
platte(wange, "Wange_L", w["r_unten"], w["r_oben"], L_w, yi, yi + w["t"], w["fase"], "plus", y0=w["z_unten"])
platte(wange, "Wange_R", w["r_unten"], w["r_oben"], L_w, -yi - w["t"], -yi, w["fase"], "minus", y0=w["z_unten"])
grat(wange, "Grat_Wange_L", w["r_unten"], w["r_oben"], L_w, yi + w["t"], 1, y0=w["z_unten"])
grat(wange, "Grat_Wange_R", w["r_unten"], w["r_oben"], L_w, -yi - w["t"], -1, y0=w["z_unten"])
for sgn, nm in ((1, "L"), (-1, "R")):
    scheibe(j1, f"Kappe_J2_{nm}", (0, sgn * (yi + w["t"] + GRAT["h"] + 1.5), H_SCHULTER), (0, 1, 0), 26, 3, "Grau")

# ================================================================ Oberarm J2 (in einem Zug: Fuss, Taille, Gabel)
oa = komponente(j1, "Oberarm_J2", (0, 0, H_SCHULTER), (0, 1, 0), Q2)
o = OBERARM
oe = ebene_komp(oa, "Oberarm_Form")
platte(oe, "Oberarm_Fuss_dunkel", o["r2"], o["r2"] - 6, 1.0, -OA_B + 2, OA_B - 2, 4.0, "beide", "Anthrazit")
platte(oe, "Oberarm_Fuss", o["weiss_r"], o["r_taille"], o["l_taille"] - o["weiss_ab"], -OA_B, OA_B, o["fase"],
       "beide", y0=o["weiss_ab"])
ub_g = UA_B + SPALT
y_g = ub_g + o["gabel_t"]
jz0, jz1 = o["joch_z"]
platte(oe, "Oberarm_Joch", o["joch_r"][0], o["joch_r"][1], jz1 - jz0, -y_g, y_g, o["fase"], "beide", y0=jz0)
gz0 = o["gabel_z0"]
gl = L_OBERARM - gz0
platte(oe, "Gabel_L", o["gabel_r"][0], o["gabel_r"][1], gl, ub_g, y_g, o["gabel_fase"], "plus", y0=gz0)
platte(oe, "Gabel_R", o["gabel_r"][0], o["gabel_r"][1], gl, -y_g, -ub_g, o["gabel_fase"], "minus", y0=gz0)
grat(oe, "Grat_Gabel_L", o["gabel_r"][0], o["gabel_r"][1], gl, y_g, 1, y0=gz0)
grat(oe, "Grat_Gabel_R", o["gabel_r"][0], o["gabel_r"][1], gl, -y_g, -1, y0=gz0)
for sgn, nm in ((1, "L"), (-1, "R")):
    scheibe(oa, f"Kappe_J3_{nm}", (0, sgn * (y_g + GRAT["h"] + 1.5), L_OBERARM), (0, 1, 0), 24, 3, "Grau")

# ================================================================ Unterarm J3, J4
ua = komponente(oa, "Unterarm_J3", (0, 0, L_OBERARM), (0, 1, 0), Q3)
u = UNTERARM
ue = ebene_komp(ua, "Unterarm_Form")
platte(ue, "Unterarm_Rucksack", u["rucksack_r"], u["r3"], u["rucksack_l"], -UA_B, UA_B, u["fase"], "beide",
       y0=-u["rucksack_l"])
platte(ue, "Unterarm_hinten", u["r3"], u["r_hinten"], u["l_hinten"], -UA_B, UA_B, u["fase"], "beide")
z_r = u["l_hinten"] + u["r_hinten"] * 0.3
scheibe(ua, "Ring_J4", (0, 0, z_r + u["ring_t"] / 2), (0, 0, 1), u["ring_r"], u["ring_t"], "Anthrazit")
j4 = komponente(ua, "Unterarm_J4", (0, 0, 0), (0, 0, 1), Q4)
(w0, h0, k0), (w1, h1, k1) = u["vorn"]
z4 = z_r + u["ring_t"]
loft(j4, "Unterarm_vorn", [(z4, achteck(w0, h0, k0)), (u["vorn_z1"], achteck(w1, h1, k1))])
hg = HANDGABEL
he = ebene_komp(j4, "Handgabel_Form")
yi_h = hg["b_innen"] + SPALT
platte(he, "Handgabel_L", hg["r0"], hg["r1"], L_UNTERARM - hg["z0"], yi_h, yi_h + hg["t"], hg["fase"], "plus",
       y0=hg["z0"])
platte(he, "Handgabel_R", hg["r0"], hg["r1"], L_UNTERARM - hg["z0"], -yi_h - hg["t"], -yi_h, hg["fase"], "minus",
       y0=hg["z0"])
grat(he, "Grat_Handgabel_L", hg["r0"], hg["r1"], L_UNTERARM - hg["z0"], yi_h + hg["t"], 1, y0=hg["z0"])
grat(he, "Grat_Handgabel_R", hg["r0"], hg["r1"], L_UNTERARM - hg["z0"], -yi_h - hg["t"], -1, y0=hg["z0"])
for sgn, nm in ((1, "L"), (-1, "R")):
    scheibe(j4, f"Kappe_J5_{nm}", (0, sgn * (yi_h + hg["t"] + GRAT["h"] + 1.5), L_UNTERARM), (0, 1, 0), hg["kappe_r"], 3, "Grau")

# ================================================================ Hand J5, Flansch J6
ha = komponente(j4, "Hand_J5", (0, 0, L_UNTERARM), (0, 1, 0), Q5)
h = HAND
loft(ha, "Hand", [(h["z0"], achteck(h["w"], 2 * hg["b_innen"], h["k"])),
                  (h["z1"], achteck(h["w"] - 6, 2 * hg["b_innen"] - 6, h["k"] - 2))])
scheibe(ha, "Ring_Flansch", (0, 0, h["z1"] + h["ring_t"] / 2), (0, 0, 1), h["ring_r"], h["ring_t"], "Akzent")
fl = komponente(ha, "Flansch_J6", (0, 0, 0), (0, 0, 1), Q6)
scheibe(fl, "Flansch", (0, 0, (h["z1"] + h["ring_t"] + L_HAND) / 2), (0, 0, 1), h["flansch_r"],
        L_HAND - h["z1"] - h["ring_t"], "Anthrazit")

einfuegen()
"Gestaltungsmodell V3 erstellt"
