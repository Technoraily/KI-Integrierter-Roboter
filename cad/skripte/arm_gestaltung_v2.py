"""Gestaltungsmodell V2 (NUR Form und Optik, keine Mechanik).

Nach Rückmeldung des Nutzers (V1 «keine Ähnlichkeit, J2 viel zu gross») und
zwei Vorlagen: eigene Bildvorlage und Arctos-Roboterarm (nur als Anregung).
Formsprache: flache, breite Glieder mit abgerundeten Enden («Stadion»), in
denen die grossen Riemenscheiben verschwinden; dunkle Kernplatten mit
weissen, kantigen Schalen (Low-Poly); Glieder seitlich versetzt; dunkler
Sockel mit angesetztem Elektronikkasten; Farbringe an J1 und am Flansch.

Kinematik bleibt wie in software/roboterarm (keine Versätze): Der Oberarm
liegt um +D_OBERARM quer versetzt, der Unterarm wieder in der Mitte. Weil
J2 und J3 parallel sind, heben sich die Querversätze auf.

Ausführen im Fusion-Python (MCP-Add-in):
    exec(open(pfad, encoding="utf-8").read())
Masse in mm; Weltachsen: x nach vorn, y quer, z nach oben, z = 0 Tisch.
"""
import math

import adsk.core
import adsk.fusion

MM = 0.1

# ---------------------------------------------------------------- Pose (Grad)
Q1, Q2, Q3, Q4, Q5, Q6 = 0.0, -25.0, 115.0, 0.0, 0.0, 0.0

# ---------------------------------------------------------------- Hauptmasse (docs/parameter.md)
H_SCHULTER, L_OBERARM, L_UNTERARM, L_HAND = 200.0, 200.0, 190.0, 60.0

# ---------------------------------------------------------------- Formparameter (Startwerte)
SOCKEL_R, SOCKEL_H, SOCKEL_N = 92.0, 72.0, 12          # Vieleck, dunkel
KASTEN = dict(x=-125.0, b=118.0, t=95.0, h=78.0)       # Elektronikkasten hinten (Mitte x)
RING_R, RING_T = 90.0, 7.0                              # Farbring J1
DREH_R, DREH_H = 84.0, 34.0                             # Drehteller J1 (weiss)
BOCK = dict(r_unten=58.0, r_oben=74.0, b=78.0, z_unten=128.0)   # Schulterbock (Mitte)
D_OBERARM = 90.0                                        # Querversatz Oberarm (Bock 53 + Luft 6 + halbe Oberarmdicke 31)
OBERARM = dict(r2=80.0, r3=60.0, kern=20.0, schale=21.0, fase=9.0)
UNTERARM = dict(r3=54.0, r_hinten=44.0, l_hinten=108.0, b=78.0, fase=10.0,
                r_vorn=36.0, ring_r=37.0, ring_t=7.0)
HAND = dict(r=34.0, b=74.0, flansch_r=27.0, ring_t=7.0)
AKZENT = (196, 64, 60)                                  # Farbring (wie Arctos rot); änderbar

app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
design.designType = adsk.fusion.DesignTypes.ParametricDesignType
root = design.rootComponent
tbm = adsk.fusion.TemporaryBRepManager.get()
P = lambda x, y, z: adsk.core.Point3D.create(x * MM, y * MM, z * MM)
V = adsk.core.Vector3D.create

_FARBEN = {"Weiss": (236, 234, 228), "Anthrazit": (72, 74, 78), "Grau": (120, 124, 130), "Akzent": AKZENT}


def farbe(name):
    voll = "AG2_" + name
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


def ebene_komp(eltern, name):
    """Hilfskomponente: lokale xy-Ebene = Armebene (x vorn, y entlang Glied = Welt z),
    lokale z-Achse = Welt -y (Dicke)."""
    return komponente(eltern, name, (0, 0, 0), (1, 0, 0), 90.0)


# ---------------------------------------------------------------- Vieleck-Umrisse
def stadion(r0, r1, L, n=6):
    """Konvexer Umriss zweier Kreise (Mitte (0,0) Radius r0 und (0,L) Radius r1),
    je Halbkreis n Segmente."""
    pts = []
    for i in range(n + 1):
        a = math.pi + math.pi * i / n          # unten: 180..360 Grad
        pts.append((r0 * math.cos(a), r0 * math.sin(a)))
    for i in range(n + 1):
        a = math.pi * i / n                    # oben: 0..180 Grad
        pts.append((r1 * math.cos(a), L + r1 * math.sin(a)))
    return pts


def vieleck(r, n, phase=0.0):
    return [(r * math.cos(phase + 2 * math.pi * i / n), r * math.sin(phase + 2 * math.pi * i / n)) for i in range(n)]


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
    """schnitte: Liste (z, Punktliste) entlang der lokalen z-Achse; gleiche Punktzahl."""
    li = comp.features.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    for z, pts in schnitte:
        li.loftSections.add(_profil(comp, z, pts))
    li.isSolid = True
    k = comp.features.loftFeatures.add(li).bodies.item(0)
    k.name = name
    k.appearance = farbe(f)
    return k


def schale(comp, name, r0, r1, L, z0, t, fase, n=6, f="Weiss", richtung=1):
    """Stadion-Körper mit kantiger Fase auf der Aussenseite (Low-Poly-Schale).
    richtung=+1: Fase bei z0+t, -1: Fase bei z0."""
    a = stadion(r0, r1, L, n)
    b = stadion(r0 - fase, r1 - fase, L, n)
    m = stadion(r0 - fase * 0.35, r1 - fase * 0.35, L, n)
    if richtung > 0:
        return loft(comp, name, [(z0, a), (z0 + t * 0.55, m), (z0 + t, b)], f)
    return loft(comp, name, [(z0, b), (z0 + t * 0.45, m), (z0 + t, a)], f)


# ---------------------------------------------------------------- Drehkörper (Temp-BRep)
_wartend = {}


def _merken(comp, name, body, f):
    _wartend.setdefault(comp.entityToken, (comp, []))[1].append((name, body, f))


def scheibe(comp, name, mitte, achse, r, b, f="Grau", fase=0.0):
    ax = [a * b / 2 for a in achse]
    p0 = [mitte[i] - ax[i] for i in range(3)]
    p1 = [mitte[i] + ax[i] for i in range(3)]
    k = tbm.createCylinderOrCone(P(*p0), r * MM, P(*p1), (r - fase) * MM)
    _merken(comp, name, k, f)


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
    if root.occurrences.item(i).component.name in ("Arm_Gestaltung", "Arm_Gestaltung_V2"):
        root.occurrences.item(i).deleteMe()

G = komponente(root, "Arm_Gestaltung_V2")

# ================================================================ Sockel mit Elektronikkasten
so = komponente(G, "Sockel")
loft(so, "Sockel", [(0, vieleck(SOCKEL_R, SOCKEL_N, math.pi / SOCKEL_N)),
                    (SOCKEL_H * 0.8, vieleck(SOCKEL_R, SOCKEL_N, math.pi / SOCKEL_N)),
                    (SOCKEL_H, vieleck(SOCKEL_R - 6, SOCKEL_N, math.pi / SOCKEL_N))], "Anthrazit")
k = KASTEN
kasten_pts = [(k["x"] + k["t"] / 2, -k["b"] / 2), (k["x"] + k["t"] / 2, k["b"] / 2),
              (k["x"] - k["t"] / 2 + 10, k["b"] / 2), (k["x"] - k["t"] / 2, k["b"] / 2 - 10),
              (k["x"] - k["t"] / 2, -k["b"] / 2 + 10), (k["x"] - k["t"] / 2 + 10, -k["b"] / 2)]
kasten_top = [(x * 0.97 + k["x"] * 0.03 + 4, y * 0.94) for x, y in kasten_pts]
loft(so, "Elektronikkasten", [(0, kasten_pts), (k["h"] * 0.82, kasten_pts), (k["h"], kasten_top)], "Anthrazit")
scheibe(so, "Ring_J1", (0, 0, SOCKEL_H + RING_T / 2), (0, 0, 1), RING_R, RING_T, "Akzent")

# ================================================================ J1: Drehteller und Schulterbock
j1 = komponente(G, "Drehteil_J1", (0, 0, 0), (0, 0, 1), Q1)
z_d = SOCKEL_H + RING_T
loft(j1, "Drehteller", [(z_d, vieleck(DREH_R, 12, math.pi / 12)),
                        (z_d + DREH_H * 0.7, vieleck(DREH_R - 2, 12, math.pi / 12)),
                        (z_d + DREH_H, vieleck(DREH_R - 14, 12, math.pi / 12))])
bk = komponente(j1, "Schulterbock")
bk_e = ebene_komp(bk, "Schulterbock_Form")
L_b = H_SCHULTER - BOCK["z_unten"]
# lokale Form: y entlang (Welt z), Start bei z_unten; Dicke lokal z = -Welt y
bk_l = komponente(bk_e, "Schulterbock_Lage", (0, BOCK["z_unten"], 0))
schale(bk_l, "Schulterbock_aussen", BOCK["r_unten"], BOCK["r_oben"], L_b, -BOCK["b"] / 2 - 14, 14, 8, 6, "Weiss", -1)
schale(bk_l, "Schulterbock_kern", BOCK["r_unten"] - 3, BOCK["r_oben"] - 3, L_b, -BOCK["b"] / 2, BOCK["b"], 0.01, 6, "Anthrazit")
schale(bk_l, "Schulterbock_innen", BOCK["r_unten"], BOCK["r_oben"], L_b, BOCK["b"] / 2, 14, 8, 6, "Weiss", 1)
scheibe(bk, "Schulterkappe", (0, -(BOCK["b"] / 2 + 14 + 2), H_SCHULTER), (0, 1, 0), 30, 4, "Grau")

# ================================================================ Oberarm J2 (quer versetzt)
oa = komponente(j1, "Oberarm_J2", (0, 0, H_SCHULTER), (0, 1, 0), Q2)
oa_e = ebene_komp(oa, "Oberarm_Form")
o = OBERARM
yc = D_OBERARM                      # Mitte in Welt-y; lokal z = -y
schale(oa_e, "Oberarm_kern", o["r2"] - 4, o["r3"] - 4, L_OBERARM, -yc - o["kern"] / 2, o["kern"], 0.01, 6, "Anthrazit")
schale(oa_e, "Oberarm_schale_aussen", o["r2"], o["r3"], L_OBERARM, -yc - o["kern"] / 2 - o["schale"], o["schale"], o["fase"], 6, "Weiss", -1)
schale(oa_e, "Oberarm_schale_innen", o["r2"], o["r3"], L_OBERARM, -yc + o["kern"] / 2, o["schale"], o["fase"], 6, "Weiss", 1)
y_aussen = yc + o["kern"] / 2 + o["schale"]
scheibe(oa, "Oberarmkappe_J2", (0, y_aussen + 2, 0), (0, 1, 0), 34, 4, "Grau")
scheibe(oa, "Oberarmkappe_J3", (0, y_aussen + 2, L_OBERARM), (0, 1, 0), 26, 4, "Grau")

# ================================================================ Unterarm J3 (Mitte), J4
ua = komponente(oa, "Unterarm_J3", (0, 0, L_OBERARM), (0, 1, 0), Q3)
u = UNTERARM
ua_e = ebene_komp(ua, "Unterarm_Form")
schale(ua_e, "Unterarm_hinten_a", u["r3"], u["r_hinten"], u["l_hinten"], -u["b"] / 2, u["b"] * 0.5, u["fase"], 6, "Weiss", -1)
schale(ua_e, "Unterarm_hinten_b", u["r3"], u["r_hinten"], u["l_hinten"], 0, u["b"] * 0.5, u["fase"], 6, "Weiss", 1)
scheibe(ua, "Ring_J4", (0, 0, u["l_hinten"] + u["r_hinten"] * 0.2 + u["ring_t"] / 2), (0, 0, 1), u["ring_r"], u["ring_t"], "Anthrazit")
scheibe(ua, "Ellbogenkappe", (0, -(u["b"] / 2 + 2), 0), (0, 1, 0), 28, 4, "Grau")
j4 = komponente(ua, "Unterarm_J4", (0, 0, 0), (0, 0, 1), Q4)
z4 = u["l_hinten"] + u["r_hinten"] * 0.2 + u["ring_t"]
loft(j4, "Unterarm_vorn", [(z4, vieleck(u["r_vorn"] + 2, 10, math.pi / 10)),
                           (L_UNTERARM - HAND["r"] * 0.6, vieleck(u["r_vorn"], 10, math.pi / 10))])
# Handgelenk J5 als kantiger Block (Stadion quer)
hg_e = ebene_komp(j4, "Handgelenk_Form")
hg_l = komponente(hg_e, "Handgelenk_Lage", (0, L_UNTERARM - 30.0, 0))
schale(hg_l, "Handgelenk_a", HAND["r"], HAND["r"], 30.0, -HAND["b"] / 2, HAND["b"] / 2, 7, 5, "Weiss", -1)
schale(hg_l, "Handgelenk_b", HAND["r"], HAND["r"], 30.0, 0, HAND["b"] / 2, 7, 5, "Weiss", 1)

# ================================================================ Hand J5, Flansch J6
ha = komponente(j4, "Hand_J5", (0, 0, L_UNTERARM), (0, 1, 0), Q5)
loft(ha, "Hand", [(10.0, vieleck(HAND["r"] - 4, 10, math.pi / 10)),
                  (L_HAND - HAND["ring_t"] - 4, vieleck(HAND["r"] - 8, 10, math.pi / 10))])
scheibe(ha, "Ring_Flansch", (0, 0, L_HAND - HAND["ring_t"] / 2 - 4), (0, 0, 1), HAND["r"] - 6, HAND["ring_t"], "Akzent")
scheibe(ha, "Flansch", (0, 0, L_HAND - 2), (0, 0, 1), HAND["flansch_r"], 4, "Anthrazit")

einfuegen()
"Gestaltungsmodell V2 erstellt"
