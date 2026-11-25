"""Gestaltungsmodell des ganzen Arms (NUR Form und Optik, keine Mechanik).

Zweck: Proportionen und Aussehen nach der Bildvorlage des Nutzers prüfen
(docs/design-vorgabe.md), bevor die Baugruppen von unten nach oben konstruiert
werden. Weisse, facettierte Schalen (Achteck-Querschnitte mit grossen Fasen),
dunkler Sockel, dunkle Gelenkkappen. Hauptmasse aus docs/parameter.md;
die Querschnitte sind Startwerte, die bei der Konstruktion der Baugruppen
(Motoren, Lager, Riemenscheiben innen) bestätigt oder angepasst werden.

Ausführen im Fusion-Python (MCP-Add-in):
    exec(open(pfad, encoding="utf-8").read())
Masse in mm; Weltachsen: x nach vorn, y quer, z nach oben, z = 0 Tisch.
Pose wie die Vorlage: Oberarm nach hinten geneigt, Unterarm waagrecht nach vorn.
"""
import math

import adsk.core
import adsk.fusion

MM = 0.1  # Fusion rechnet intern in cm

# ---------------------------------------------------------------- Pose (Grad)
Q1, Q2, Q3, Q4, Q5, Q6 = 0.0, -30.0, 120.0, 0.0, 0.0, 0.0

# ---------------------------------------------------------------- Masse (docs/parameter.md)
H_SCHULTER, L_OBERARM, L_UNTERARM, L_HAND = 200.0, 200.0, 190.0, 60.0

# ---------------------------------------------------------------- Querschnitte (Startwerte)
SOCKEL = dict(h=60.0, unten=170.0, oben=162.0, fase=28.0)     # dunkler Sockel, Lochbild 120 mm innen
SAEULE = dict(z0=66.0, z1=150.0, unten=(132.0, 122.0), oben=(120.0, 104.0), fase=28.0)
SCHULTER = dict(r=80.0, b=104.0, fase=7.0, kappe_r=46.0, kappe_t=4.0)  # Platz für 5M-90er-Scheibe (Ø ~143)
OBERARM = dict(wurzel=(100.0, 104.0), ende=(84.0, 96.0), fase=24.0)
ELLBOGEN = dict(r=58.0, b=96.0, fase=5.0, kappe_r=34.0, kappe_t=4.0)   # Platz für 5M-60er-Scheibe (Ø ~95)
UNTERARM = dict(l1=120.0, a=(84.0, 96.0), b=(74.0, 84.0), fuge_r=40.0, fuge_t=6.0,
                c=(72.0, 82.0), d=(66.0, 78.0), fase=18.0)
HAND_GELENK = dict(r=40.0, b=86.0, kappe_r=24.0, kappe_t=3.0)
HAND = dict(a=(64.0, 64.0), b=(56.0, 56.0), fase=14.0, flansch_r=26.0, flansch_t=10.0)

app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
design.designType = adsk.fusion.DesignTypes.ParametricDesignType
root = design.rootComponent
tbm = adsk.fusion.TemporaryBRepManager.get()
P = lambda x, y, z: adsk.core.Point3D.create(x * MM, y * MM, z * MM)
V = adsk.core.Vector3D.create

# ---------------------------------------------------------------- Farben
_FARBEN = {"Weiss": (238, 239, 241), "Anthrazit": (58, 62, 68), "Grau": (128, 134, 142)}


def farbe(name):
    voll = "AG_" + name
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


# ---------------------------------------------------------------- Komponenten
def komponente(eltern, name, verschiebung=(0, 0, 0), achse=None, winkel=0.0):
    m = adsk.core.Matrix3D.create()
    if achse:
        m.setToRotation(math.radians(winkel), V(*achse), adsk.core.Point3D.create(0, 0, 0))
    m.translation = V(*(v * MM for v in verschiebung))
    occ = eltern.occurrences.addNewComponent(m)
    occ.component.name = name
    return occ.component


# ---------------------------------------------------------------- Achteck-Loft (lokale z-Achse)
def _achteck(sk, w, h, k):
    k = min(k, w / 2 - 1, h / 2 - 1)
    pts = [(w / 2 - k, h / 2), (-w / 2 + k, h / 2), (-w / 2, h / 2 - k), (-w / 2, -h / 2 + k),
           (-w / 2 + k, -h / 2), (w / 2 - k, -h / 2), (w / 2, -h / 2 + k), (w / 2, h / 2 - k)]
    lines = sk.sketchCurves.sketchLines
    p3 = [adsk.core.Point3D.create(x * MM, y * MM, 0) for x, y in pts]
    for i in range(8):
        lines.addByTwoPoints(p3[i], p3[(i + 1) % 8])
    return sk.profiles.item(0)


def achteck_loft(comp, name, schnitte, f="Weiss"):
    """schnitte: Liste (z, w, h, fase) in mm entlang der lokalen z-Achse; w quer x, h quer y."""
    li = comp.features.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    for z, w, h, k in schnitte:
        if abs(z) < 1e-9:
            ebene = comp.xYConstructionPlane
        else:
            ei = comp.constructionPlanes.createInput()
            ei.setByOffset(comp.xYConstructionPlane, adsk.core.ValueInput.createByReal(z * MM))
            ebene = comp.constructionPlanes.add(ei)
            ebene.isLightBulbOn = False
        sk = comp.sketches.add(ebene)
        sk.isVisible = False
        li.loftSections.add(_achteck(sk, w, h, k))
    li.isSolid = True
    lf = comp.features.loftFeatures.add(li)
    k = lf.bodies.item(0)
    k.name = name
    k.appearance = farbe(f)
    return k


# ---------------------------------------------------------------- Drehkörper über Temp-BRep
_wartend = {}


def _merken(comp, name, body, f):
    _wartend.setdefault(comp.entityToken, (comp, []))[1].append((name, body, f))


def nabe(comp, name, mitte, achse, r, b, fase=0.0, f="Weiss"):
    """Zylinder mit Fasen an beiden Stirnseiten. achse: Einheitsvektor (Tupel)."""
    ax = [a * b / 2 for a in achse]
    p0 = [mitte[i] - ax[i] for i in range(3)]
    p1 = [mitte[i] + ax[i] for i in range(3)]
    if fase <= 0:
        _merken(comp, name, tbm.createCylinderOrCone(P(*p0), r * MM, P(*p1), r * MM), f)
        return
    fa = [a * fase for a in achse]
    q0 = [p0[i] + fa[i] for i in range(3)]
    q1 = [p1[i] - fa[i] for i in range(3)]
    k = tbm.createCylinderOrCone(P(*q0), r * MM, P(*q1), r * MM)
    for a, bb in ((p0, q0), (p1, q1)):
        kegel = tbm.createCylinderOrCone(P(*a), (r - fase) * MM, P(*bb), r * MM)
        tbm.booleanOperation(k, kegel, adsk.fusion.BooleanTypes.UnionBooleanType)
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
    if root.occurrences.item(i).component.name == "Arm_Gestaltung":
        root.occurrences.item(i).deleteMe()

G = komponente(root, "Arm_Gestaltung")

# ================================================================ Sockel (fest)
s = SOCKEL
sockel = komponente(G, "Sockel")
achteck_loft(sockel, "Sockel", [(0, s["unten"], s["unten"], s["fase"]),
                                (s["h"], s["oben"], s["oben"], s["fase"] - 2)], "Anthrazit")
nabe(sockel, "J1_Fuge", (0, 0, s["h"] + 3), (0, 0, 1), 68.0, 6.0, 0, "Anthrazit")

# ================================================================ J1 Säule mit Schulter
j1 = komponente(G, "Saeule_J1", (0, 0, 0), (0, 0, 1), Q1)
sa = SAEULE
achteck_loft(j1, "Saeule", [(sa["z0"], sa["unten"][0], sa["unten"][1], sa["fase"]),
                            (sa["z1"], sa["oben"][0], sa["oben"][1], sa["fase"] - 3)])
sc = SCHULTER
nabe(j1, "Schultergehaeuse", (0, 0, H_SCHULTER), (0, 1, 0), sc["r"], sc["b"], sc["fase"])
for sgn in (1, -1):
    y = sgn * (sc["b"] / 2 + sc["kappe_t"] / 2)
    nabe(j1, f"Schulterkappe_{'L' if sgn > 0 else 'R'}", (0, y, H_SCHULTER), (0, 1, 0),
         sc["kappe_r"], sc["kappe_t"], 1.5, "Grau")

# ================================================================ Oberarm (J2)
oa = komponente(j1, "Oberarm_J2", (0, 0, H_SCHULTER), (0, 1, 0), Q2)
o = OBERARM
achteck_loft(oa, "Oberarm", [(0, o["wurzel"][0], o["wurzel"][1], o["fase"]),
                             (L_OBERARM, o["ende"][0], o["ende"][1], o["fase"] - 3)])
e = ELLBOGEN
nabe(oa, "Ellbogengehaeuse", (0, 0, L_OBERARM), (0, 1, 0), e["r"], e["b"], e["fase"])
for sgn in (1, -1):
    y = sgn * (e["b"] / 2 + e["kappe_t"] / 2)
    nabe(oa, f"Ellbogenkappe_{'L' if sgn > 0 else 'R'}", (0, y, L_OBERARM), (0, 1, 0),
         e["kappe_r"], e["kappe_t"], 1.2, "Grau")

# ================================================================ Unterarm (J3, J4)
ua = komponente(oa, "Unterarm_J3", (0, 0, L_OBERARM), (0, 1, 0), Q3)
u = UNTERARM
achteck_loft(ua, "Unterarm_hinten", [(0, u["a"][0], u["a"][1], u["fase"] + 4),
                                     (u["l1"], u["b"][0], u["b"][1], u["fase"])])
nabe(ua, "J4_Fuge", (0, 0, u["l1"] + u["fuge_t"] / 2), (0, 0, 1), u["fuge_r"], u["fuge_t"], 0, "Anthrazit")
j4 = komponente(ua, "Unterarm_J4", (0, 0, 0), (0, 0, 1), Q4)
achteck_loft(j4, "Unterarm_vorn", [(u["l1"] + u["fuge_t"], u["c"][0], u["c"][1], u["fase"]),
                                   (L_UNTERARM - 20.0, u["d"][0], u["d"][1], u["fase"] - 2)])
hg = HAND_GELENK
nabe(j4, "Handgelenk", (0, 0, L_UNTERARM), (0, 1, 0), hg["r"], hg["b"], 4.0)
for sgn in (1, -1):
    y = sgn * (hg["b"] / 2 + hg["kappe_t"] / 2)
    nabe(j4, f"Handkappe_{'L' if sgn > 0 else 'R'}", (0, y, L_UNTERARM), (0, 1, 0),
         hg["kappe_r"], hg["kappe_t"], 1.0, "Grau")

# ================================================================ Hand (J5, J6)
ha = komponente(j4, "Hand_J5", (0, 0, L_UNTERARM), (0, 1, 0), Q5)
h = HAND
achteck_loft(ha, "Hand", [(0, h["a"][0], h["a"][1], h["fase"]),
                          (L_HAND - h["flansch_t"], h["b"][0], h["b"][1], h["fase"] - 1)])
fl = komponente(ha, "Flansch_J6", (0, 0, 0), (0, 0, 1), Q6)
nabe(fl, "Flansch", (0, 0, L_HAND - h["flansch_t"] / 2), (0, 0, 1), h["flansch_r"], h["flansch_t"], 1.0, "Anthrazit")

einfuegen()
app.activeViewport.fit()
"Gestaltungsmodell erstellt"
