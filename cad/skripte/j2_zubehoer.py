"""Zubehör für den J2-Prüfstand: Referenzschalter im Querträger, Schalterprobe, Motorkabelklemme.

  J2_Quertraeger_oben_Schalter  Ersatz für einen oberen Querträger (Masse wie im J2-Skript, 14 x 24 x 56 mm, gleiche
                                Einschmelzbohrungen), mit Tasche für einen Mikroschalter KW12-3 mit Rollenhebel. Die Rolle
                                steht ROLLE_FREI mm über der Oberkante des Querträgers; der Lasthebel drückt sie kurz vor dem
                                mechanischen Anschlag nieder. Symmetrisch: dasselbe Teil passt links und rechts.
  J2_Schalterprobe              Kurzer Block mit derselben Tasche (Querschnitt 14 x 16 mm): Probe am gekauften Schalter, BEVOR die
                                Querträger gedruckt werden.
  J2_Motorkabelklemme           Sattel auf dem Motorgehäuse (NEMA 17, 42,3 mm), mit Kabelbinder um den Motor befestigt;
                                Rille für das Motorkabel, zwei Kabelbinder-Schlitze darüber (Zugentlastung).

Alle Masse mit dem Vermerk 'Startwert' sind Annahmen zu Kaufteilen (Schalter KW12-3): vor dem Druck am
gelieferten Teil nachmessen. Die Masse des J2-Prüfstands stehen in j2_pruefstand.py und werden hier nur gespiegelt.

Ausführen im Fusion-Python (MCP-Add-in):
    exec(open(pfad, encoding="utf-8").read())
Masse in mm. Teile liegen in Druckorientierung (z = Druckrichtung). Export: AUSGABE = "<Ordner>" vorher setzen.
"""
import math
from math import cos, sin, radians

import adsk.core
import adsk.fusion

MM = 0.1

# ---------------------------------------------------------------- Masse des Prüfstands (gespiegelt aus j2_pruefstand.py)
W = 56.0                                   # lichte Weite zwischen den Wangen = Länge der Querträger
TR_B, TR_H, TR_LOCH = 14.0, 24.0, 6.0      # Querträger 14 x 24, Schrauben bei +-6 mm in y
D_EINSCHMELZ_M3, T_EINSCHMELZ_TIEF = 4.0, 9.0
O_Y = 170.0                                # Abtriebsachse bei x = 0, y = 170
HEBEL = [(-30.0, 15.0), (30.0, 15.0), (15.0, 190.0), (-15.0, 190.0)]   # Hebelarm in der Grundstellung (nach oben)
Z_HEBEL = (20.0, 40.0)                     # axiale Lage des Lasthebels zwischen den Wangen
TRAEGER = {"rechts": (88.0, 124.0), "links": (-85.0, 124.0)}           # Mitte x, y der oberen Querträger
ANSCHLAG = {"rechts": 96.7, "links": 96.7}  # aus dem J2-Skript (Hebel berührt den Querträger), Grad aus der Senkrechten

# ---------------------------------------------------------------- Mikroschalter KW12-3 (Startwerte, ungeprüft!)
SW_L, SW_B, SW_T = 20.0, 10.5, 6.5         # Körper: Länge (z), Höhe (y), Dicke (x) - Angabe eines Händlers: 20 x 10,5 x 6,5
SW_LOCH = 9.5                              # Lochabstand (wie standardteile.py), Löcher mittig in der Länge
D_SW_SCHRAUBE = 2.4                        # M2 x 16 (x 14 knapp) mit Mutter in Sechskanttasche der Gegenwand
MUTTER_M2_SW, MUTTER_M2_T = 4.3, 1.8
SW_HEBEL_L = 6.0                           # Körperende bis Rollenmitte (Rollenhebel zeigt nach +z)
SW_ROLLE_D = 5.0                           # Rollendurchmesser (Startwert; Rolle misst in z ihren Durchmesser)
SW_ROLLE_HB = SW_ROLLE_D / 2
ROLLE_UEBER_KOERPER = 5.5                  # freie Rolle: Oberkante über der Körper-Oberkante
ROLLE_FREI = 2.2                           # freie Rolle steht so weit über der Querträger-Oberkante (Beilagen unter dem Schalter heben sie; mit den Startwerten höchstens +0,4 mm, sonst fehlt die Reserve)
BEILAGE = 1.0                              # Tasche ist so viel tiefer: Pappe oder Folie unter dem Schalter stellt die Rollenhöhe ein
RESERVE_MIN = 0.5                          # verlangte Reserve: Vorweg + Restweg >= ROLLE_FREI + RESERVE_MIN
VORWEG, UEBERWEG = 1.5, 1.6                # Vorlaufweg bis zum Schalten / Restweg danach (Startwerte, typisch KW12)
SW_Z0 = 11.0                               # Körper beginnt bei z = 11 (Einschmelzbohrung endet bei 9)
SPIEL_T = 0.4                              # Spiel Tasche zum Körper (Dicke), je Seite 0,2
SPIEL_L = 0.3

# ---------------------------------------------------------------- Motorkabelklemme
NEMA = 42.3
KL_L, KL_T = 20.0, 7.0
KL_RILLE_D = 6.4                           # Rille für Motorkabel (4 Adern in Mantel, Startwert)
BINDER_B, BINDER_D = 3.8, 2.2              # Schlitz für Kabelbinder 3,6 x 1,4 (wie Kabelhalter)
KL_FLUEGEL = 3.0                           # Mitte der Schlitze neben dem Motor

app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
root = design.rootComponent
tbm = adsk.fusion.TemporaryBRepManager.get()
P = lambda x, y, z: adsk.core.Point3D.create(x * MM, y * MM, z * MM)
V = adsk.core.Vector3D.create


def farbe(name="ZB_Druckteil"):
    a = design.appearances.itemByName(name)
    if a:
        return a
    lib = app.materialLibraries.itemByName("Fusion Appearance Library")
    a = design.appearances.addByCopy(lib.appearances.itemByName("Plastic - Matte (White)"), name)
    for i in range(a.appearanceProperties.count):
        p = a.appearanceProperties.item(i)
        if isinstance(p, adsk.core.ColorProperty) and p.value:
            p.value = adsk.core.Color.create(215, 220, 228, 255)
            break
    return a


def quader(x0, x1, y0, y1, z0, z1):
    obb = adsk.core.OrientedBoundingBox3D.create(P((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), V(1, 0, 0), V(0, 1, 0),
                                                 abs(x1 - x0) * MM, abs(y1 - y0) * MM, abs(z1 - z0) * MM)
    return tbm.createBox(obb)


def zylinder(p1, p2, r1, r2=None):
    return tbm.createCylinderOrCone(P(*p1), r1 * MM, P(*p2), (r1 if r2 is None else r2) * MM)


def plus(a, b):
    tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.UnionBooleanType)


def minus(a, b):
    tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.DifferenceBooleanType)


def komponente(name, ursprung=(0, 0, 0)):
    m = adsk.core.Matrix3D.create()
    m.translation = V(ursprung[0] * MM, ursprung[1] * MM, ursprung[2] * MM)
    occ = root.occurrences.addNewComponent(m)
    occ.component.name = name
    return occ.component


def einsetzen(comp, name, body):
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    comp.bRepBodies.add(body, bf)
    bf.finishEdit()
    k = comp.bRepBodies.item(comp.bRepBodies.count - 1)
    k.name = name
    k.appearance = farbe()
    return k


def exportieren(k, datei):
    if "AUSGABE" not in globals():
        return
    o = design.exportManager.createSTLExportOptions(k, AUSGABE + "/" + datei + ".stl")
    o.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
    design.exportManager.execute(o)


def sechskant_x(y, z, x0, x1, sw):
    """Sechskantprisma, Achse x, Schlüsselweite sw, von x0 bis x1 (Mutter M2 in der Gegenwand)."""
    teile = []
    for w in (0.0, 60.0, 120.0):
        a = math.radians(w)
        obb = adsk.core.OrientedBoundingBox3D.create(P((x0 + x1) / 2, y, z), V(0, math.cos(a), math.sin(a)), V(1, 0, 0),
                                                     30 * MM, abs(x1 - x0) * MM, sw * MM)
        teile.append(tbm.createBox(obb))
    tbm.booleanOperation(teile[0], teile[1], adsk.fusion.BooleanTypes.IntersectionBooleanType)
    tbm.booleanOperation(teile[0], teile[2], adsk.fusion.BooleanTypes.IntersectionBooleanType)
    return teile[0]


# ---------------------------------------------------------------- Rechnung: wann löst der Schalter aus?
def y_unten(winkel, richtung, xq):
    """Tiefster Punkt des Hebelarms bei x = xq. winkel: Grad aus der Senkrechten, richtung +1 links, -1 rechts."""
    w = radians(winkel) * richtung
    pts = [(O_Y * 0 + x * cos(w) - y * sin(w), O_Y + x * sin(w) + y * cos(w)) for x, y in HEBEL]
    tief = None
    for i in range(4):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % 4]
        if (x0 - xq) * (x1 - xq) <= 0 and x0 != x1:
            y = y0 + (y1 - y0) * (xq - x0) / (x1 - x0)
            tief = y if tief is None else min(tief, y)
    return tief


def winkel_fuer(y_soll, richtung, xq):
    """Kleinster Winkel (Grad aus der Senkrechten, ab 80), bei dem der Hebelarm bei x = xq bis y_soll herunterreicht."""
    for i in range(800, 1100):
        a = i / 10
        y = y_unten(a, richtung, xq)
        if y is not None and y <= y_soll:
            return a
    return None


y_traeger_oben = TRAEGER["rechts"][1] + TR_H / 2
ROLLE_Y_FREI = y_traeger_oben + ROLLE_FREI
AUSLOESUNG = {}
for seite, richtung in (("rechts", -1), ("links", 1)):
    xq = TRAEGER[seite][0]
    a_schalt = winkel_fuer(ROLLE_Y_FREI - VORWEG, richtung, xq)
    a_ende = winkel_fuer(ROLLE_Y_FREI - VORWEG - UEBERWEG, richtung, xq)
    a_auf = winkel_fuer(y_traeger_oben, richtung, xq)
    AUSLOESUNG[seite] = {"schaltet_bei": a_schalt, "Restweg_aufgebraucht_bei": a_ende, "Hebel_liegt_auf_bei": a_auf,
                         "Anschlag_Skript": ANSCHLAG[seite]}

# ---------------------------------------------------------------- Prüfungen der Annahmen
z_rolle = SW_Z0 + SW_L + SW_HEBEL_L
assert Z_HEBEL[0] + 1.0 <= z_rolle - SW_ROLLE_HB and z_rolle + SW_ROLLE_HB <= Z_HEBEL[1] - 0.5, \
    "Rolle liegt nicht sicher innerhalb der Hebeldicke (z %.1f..%.1f)" % (z_rolle - SW_ROLLE_HB, z_rolle + SW_ROLLE_HB)
assert SW_Z0 - SPIEL_L - (T_EINSCHMELZ_TIEF) >= 1.5, "Tasche zu nah an der Einschmelzbohrung (Wand < 1,5 mm)"
assert VORWEG + UEBERWEG >= ROLLE_FREI + RESERVE_MIN, "Rolle ragt weiter, als der Schalter nachgibt (Reserve unter %.1f mm): Hebel würde die Rolle zerdrücken" % RESERVE_MIN

for i in range(root.occurrences.count - 1, -1, -1):
    root.occurrences.item(i).deleteMe()


# ---------------------------------------------------------------- Tasche (gemeinsam für Querträger und Probe)
def tasche(body, px0, pz_oben_traeger):
    """Tasche in die Oberseite (pz = pz_oben_traeger) eines Blocks. Körper- und Hebelraum, M2-Löcher quer."""
    pz_koerper_oben = pz_oben_traeger + ROLLE_FREI - ROLLE_UEBER_KOERPER
    pz_koerper_unten = pz_koerper_oben - SW_B
    xm = px0 + TR_B / 2
    t = SW_T + SPIEL_T
    py0, py1 = SW_Z0 - SPIEL_L, SW_Z0 + SW_L + SPIEL_L
    minus(body, quader(xm - t / 2, xm + t / 2, py0, py1, pz_koerper_unten - BEILAGE - 0.2, pz_oben_traeger + 1))
    minus(body, quader(xm - t / 2, xm + t / 2, py1 - 0.01, SW_Z0 + SW_L + SW_HEBEL_L + SW_ROLLE_HB + 1.5,
                       pz_koerper_oben - 1.0, pz_oben_traeger + 1))
    zc = SW_Z0 + SW_L / 2
    for dz in (-SW_LOCH / 2, SW_LOCH / 2):
        minus(body, zylinder((px0 - 1, zc + dz, pz_koerper_unten + SW_B / 2), (px0 + TR_B + 1, zc + dz, pz_koerper_unten + SW_B / 2),
                             D_SW_SCHRAUBE / 2))
        minus(body, sechskant_x(zc + dz, pz_koerper_unten + SW_B / 2, px0 + TR_B - MUTTER_M2_T, px0 + TR_B + 1, MUTTER_M2_SW))
    return pz_koerper_unten


# ================================================================ Querträger mit Schalter (Druckorientierung: auf der 14 x 56 Fläche liegend, Tasche oben)
q = quader(0, TR_B, 0, W, 0, TR_H)
for pz in (TR_H / 2 - TR_LOCH, TR_H / 2 + TR_LOCH):                 # Einschmelzbohrungen wie im J2-Skript, von beiden Enden
    minus(q, zylinder((TR_B / 2, -1, pz), (TR_B / 2, T_EINSCHMELZ_TIEF, pz), D_EINSCHMELZ_M3 / 2))
    minus(q, zylinder((TR_B / 2, W - T_EINSCHMELZ_TIEF, pz), (TR_B / 2, W + 1, pz), D_EINSCHMELZ_M3 / 2))
pz_unten = tasche(q, 0.0, TR_H)
c = komponente("Druck_Quertraeger_Schalter", (0, 0, 0))
k1 = einsetzen(c, "J2_Quertraeger_oben_Schalter", q)
exportieren(k1, "J2_Quertraeger_oben_Schalter")

# ================================================================ Schalterprobe (Querschnitt 14 x 16, py 0..46 = gleiche z-Bezugskante wie der Querträger)
pr_h = TR_H - 8.0
pb = quader(0, TR_B, 0.0, 46.0, 0, pr_h)
tasche(pb, 0.0, pr_h)
c = komponente("Druck_Schalterprobe", (30, 0, 0))
k2 = einsetzen(c, "J2_Schalterprobe", pb)
exportieren(k2, "J2_Schalterprobe")

# ================================================================ Motorkabelklemme (flach: Unterseite auf dem Bett = Seite zum Motor)
kb = NEMA + 2 * (KL_FLUEGEL + BINDER_D / 2 + 1.7)
kl = quader(-kb / 2, kb / 2, -KL_L / 2, KL_L / 2, 0, KL_T)
minus(kl, zylinder((0, -KL_L / 2 - 1, KL_T), (0, KL_L / 2 + 1, KL_T), KL_RILLE_D / 2))
xs = NEMA / 2 + KL_FLUEGEL
for sx in (-1, 1):
    for sy in (-1, 1):                                              # Spanngurt um den Motor, zwei Stellen
        minus(kl, quader(sx * xs - BINDER_D / 2, sx * xs + BINDER_D / 2, sy * 6.0 - BINDER_B / 2, sy * 6.0 + BINDER_B / 2, -1, KL_T + 1))
    minus(kl, quader(sx * 9.0 - BINDER_D / 2, sx * 9.0 + BINDER_D / 2, -BINDER_B / 2, BINDER_B / 2, -1, KL_T + 1))   # Kabel halten
minus(kl, quader(-9.0 - BINDER_D / 2, 9.0 + BINDER_D / 2, -BINDER_B / 2, BINDER_B / 2, -1, 1.8))   # Kanal unten für den Kabelbinder
c = komponente("Druck_Motorkabelklemme", (0, 40, 0))
k3 = einsetzen(c, "J2_Motorkabelklemme", kl)
exportieren(k3, "J2_Motorkabelklemme")

vp = app.activeViewport
if vp:
    cam = vp.camera
    cam.isSmoothTransition = False
    cam.target = P(30, 40, 8)
    cam.eye = P(140, -90, 110)
    cam.upVector = V(0, 0, 1)
    vp.camera = cam
    vp.fit()
{"Ausloesung": AUSLOESUNG, "Rolle_z_Mitte": z_rolle, "Rolle_y_frei": ROLLE_Y_FREI, "Koerper_unten_pz": pz_unten}
