"""Standardteile für alle Gelenke und die Schiene: Endschalter-Halter und Kabelhalter (beide gedruckt).

  Endschalter_Halter  Fuss mit zwei M3-Langlöchern (28 mm Teilung, Spiel zum Einstellen) und Wand mit zwei
                      Langlöchern für Schalterschrauben M2 (Lochabstand SW_LOCH, senkrecht verstellbar).
                      Passt zu einem Mikroschalter vom Typ KW11/KW12 (Startwert, vor dem Druck am gekauften
                      Schalter nachmessen!). Schaltweg: Schaltkante des Hebels bis Wandfläche 'SW_ABSTAND'.
  Kabelhalter         Platte mit M3-Befestigung (Kopf versenkt) und zwei Schlitzen für Kabelbinder 2,5-3,6 mm
                      Breite; Zugentlastung für Kabelbündel bis ca. 10 mm Durchmesser.

Ausführen im Fusion-Python (MCP-Add-in):
    exec(open(pfad, encoding="utf-8").read())
Masse in mm. Teile liegen in Druckorientierung (Fuss/Platte unten, z = Druckrichtung).
Export: setze vorher AUSGABE = "<Ordner>" (sonst wird nicht exportiert).
"""
import adsk.core
import adsk.fusion

MM = 0.1

# ---------------------------------------------------------------- Masse
T_FUSS, B_FUSS, Y_FUSS = 4.0, 40.0, 24.0
FUSS_LOCH, FUSS_TEILUNG, FUSS_LANG = 3.4, 28.0, 8.0    # M3, Langloch 8 mm lang in y
T_WAND, B_WAND, H_WAND = 5.0, 32.0, 26.0
SW_LOCH, SW_D, SW_Z, SW_LANG = 9.5, 2.4, 13.0, 8.0     # Startwert KW12; M2 selbstschneidend in 2,4 mm
X_RIPPE0, X_RIPPE1 = 11.0, 16.0                         # Rippen |x| 11..16, Schalterkörper bleibt frei
KH_L, KH_B, KH_T = 32.0, 16.0, 4.0
KH_M3, KH_KOPF, KH_KOPFTIEFE = 3.4, 6.6, 2.4
KH_SLITZ_X, KH_SLITZ_B = 2.2, 3.8                        # Kabelbinder 3,6 x 1,4: Schlitz 2,2 (Dicke) x 3,8 (Breite)
KH_ABSTAND = 10.0                                       # Schlitzmitte zur Plattenmitte

app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
root = design.rootComponent
tbm = adsk.fusion.TemporaryBRepManager.get()
P = lambda x, y, z: adsk.core.Point3D.create(x * MM, y * MM, z * MM)
V = adsk.core.Vector3D.create


def farbe():
    a = design.appearances.itemByName("ST_Druckteil")
    if a:
        return a
    lib = app.materialLibraries.itemByName("Fusion Appearance Library")
    a = design.appearances.addByCopy(lib.appearances.itemByName("Plastic - Matte (White)"), "ST_Druckteil")
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


def langloch(body, x, y, z0, z1, d, lang, achse):
    """Langloch (Stadion) mit Durchmesser d, Länge lang, durch z0..z1 bzw. y; achse 'y' oder 'z'."""
    r = d / 2
    if achse == "y":    # Wand: Bohrrichtung y, Streckung in z
        for dz in (-(lang - d) / 2, (lang - d) / 2):
            minus(body, zylinder((x, z0, SW_Z + dz), (x, z1, SW_Z + dz), r))
        minus(body, quader(x - r, x + r, z0, z1, SW_Z - (lang - d) / 2, SW_Z + (lang - d) / 2))
    else:               # Fuss: Bohrrichtung z, Streckung in y
        for dy in (-(lang - d) / 2, (lang - d) / 2):
            minus(body, zylinder((x, y + dy, z0), (x, y + dy, z1), r))
        minus(body, quader(x - r, x + r, y - (lang - d) / 2, y + (lang - d) / 2, z0, z1))


for i in range(root.occurrences.count - 1, -1, -1):
    root.occurrences.item(i).deleteMe()

# ================================================================ Endschalter-Halter
h = quader(-B_FUSS / 2, B_FUSS / 2, 0, Y_FUSS, 0, T_FUSS)
yw0 = Y_FUSS - T_WAND
plus(h, quader(-B_WAND / 2, B_WAND / 2, yw0, Y_FUSS, T_FUSS - 0.01, H_WAND))
for s in (-1, 1):                                       # zwei Rippen neben dem Schalter (Schalter 20 mm breit)
    plus(h, quader(s * X_RIPPE0, s * X_RIPPE1, yw0 - 8.0, yw0 + 0.01, T_FUSS - 0.01, T_FUSS + 14.0))
for s in (-1, 1):
    langloch(h, s * FUSS_TEILUNG / 2, 9.0, -1, T_FUSS + 1, FUSS_LOCH, FUSS_LANG + FUSS_LOCH, "z")
    langloch(h, s * SW_LOCH / 2, 0, yw0 - 1, Y_FUSS + 1, SW_D, SW_LANG + SW_D, "y")
c = komponente("Endschalter_Halter", (0, 0, 0))
k1 = einsetzen(c, "Endschalter_Halter", h)
exportieren(k1, "Endschalter_Halter")

# ================================================================ Kabelhalter
k = quader(-KH_L / 2, KH_L / 2, -KH_B / 2, KH_B / 2, 0, KH_T)
minus(k, zylinder((0, 0, -1), (0, 0, KH_T + 1), KH_M3 / 2))
minus(k, zylinder((0, 0, KH_T - KH_KOPFTIEFE), (0, 0, KH_T + 1), KH_KOPF / 2))
for s in (-1, 1):
    minus(k, quader(s * KH_ABSTAND - KH_SLITZ_X / 2, s * KH_ABSTAND + KH_SLITZ_X / 2, -KH_SLITZ_B / 2, KH_SLITZ_B / 2, -1, KH_T + 1))
c = komponente("Kabelhalter", (70, 0, 0))
k2 = einsetzen(c, "Kabelhalter", k)
exportieren(k2, "Kabelhalter")

vp = app.activeViewport
cam = vp.camera
cam.isSmoothTransition = False
cam.target = P(35, 10, 8)
cam.eye = P(110, -90, 90)
cam.upVector = V(0, 0, 1)
vp.camera = cam
vp.fit()
"fertig"
