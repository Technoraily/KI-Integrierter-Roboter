"""Not-Aus-Gehäuse für einen Pilztaster Ø 22 mm (Typ LAY37 / XB2, 1 Öffner + 1 Schliesser, beide gedruckt).

  NotAus_Gehaeuse  offene Box 66 x 66 mm, Innentiefe 58 mm, vier Eckdome für Einschmelzgewinde M3,
                   zwei Kabelöffnungen Ø 9 mm in der linken Wand, zwei Befestigungsohren mit M4-Langlöchern.
  NotAus_Deckel    Platte 66 x 66 x 4 mm mit Montagebohrung Ø 22,3 mm (Taster), vier Senklöcher M3.

Der Öffnerkontakt (NC) trennt die Motorspannung bzw. gibt der Firmware das Signal (docs/konzept.md 3.4,
docs/verdrahtung.md). Der Taster hat hinten ein Kontaktblock-Paket von ca. 45 mm Tiefe: vor dem Druck die
Tiefe am gekauften Taster nachmessen und H_INNEN anpassen.

Ausführen im Fusion-Python (MCP-Add-in):
    exec(open(pfad, encoding="utf-8").read())
Masse in mm. Teile liegen in Druckorientierung (Boden bzw. Deckel unten, z = Druckrichtung).
Export: setze vorher AUSGABE = "<Ordner>" (sonst wird nicht exportiert).
"""
import adsk.core
import adsk.fusion

MM = 0.1

# ---------------------------------------------------------------- Masse
B_INNEN = 60.0                        # Innenmass x = y
T_WAND, T_BODEN, T_DECKEL = 3.0, 3.0, 4.0
H_INNEN = 58.0                        # Startwert, Taster mit Kontaktblöcken nachmessen
B_AUSSEN = B_INNEN + 2 * T_WAND
D_TASTER = 22.3                       # Montagebohrung (22 mm + 0,3 Spiel; Wert nach Toleranztest)
D_DOM, D_EINSCHMELZ_M3, T_EINSCHMELZ_TIEFE = 8.0, 4.0, 9.0
D_M3, D_KOPF_M3, T_KOPF = 3.4, 6.4, 2.0
D_KABEL = 9.0
Z_KABEL, Y_KABEL = 22.0, 12.0
OHR_L, OHR_B, OHR_LANG, D_OHR = 16.0, 22.0, 10.0, 4.5

app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
root = design.rootComponent
tbm = adsk.fusion.TemporaryBRepManager.get()
P = lambda x, y, z: adsk.core.Point3D.create(x * MM, y * MM, z * MM)
V = adsk.core.Vector3D.create


def farbe():
    a = design.appearances.itemByName("NA_Druckteil")
    if a:
        return a
    lib = app.materialLibraries.itemByName("Fusion Appearance Library")
    a = design.appearances.addByCopy(lib.appearances.itemByName("Plastic - Matte (White)"), "NA_Druckteil")
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

for i in range(root.occurrences.count - 1, -1, -1):
    root.occurrences.item(i).deleteMe()

# ================================================================ Gehäuse
h_aussen = T_BODEN + H_INNEN
a = B_AUSSEN / 2
i_ = B_INNEN / 2
g = quader(-a, a, -a, a, 0, h_aussen)
minus(g, quader(-i_, i_, -i_, i_, T_BODEN, h_aussen + 1))
dom = i_ - D_DOM / 2 + 0.5                              # Mittelpunkt der Dome
for sx in (-1, 1):
    for sy in (-1, 1):
        plus(g, zylinder((sx * dom, sy * dom, T_BODEN - 0.01), (sx * dom, sy * dom, h_aussen), D_DOM / 2))
        minus(g, zylinder((sx * dom, sy * dom, h_aussen - T_EINSCHMELZ_TIEFE), (sx * dom, sy * dom, h_aussen + 1), D_EINSCHMELZ_M3 / 2))
for sy in (-1, 1):                                       # Kabel durch die linke Wand
    minus(g, zylinder((-a - 1, sy * Y_KABEL, Z_KABEL), (-i_ + 1, sy * Y_KABEL, Z_KABEL), D_KABEL / 2))
for sx in (-1, 1):                                       # Befestigungsohren links/rechts am Boden
    plus(g, quader(sx * a, sx * (a + OHR_L), -OHR_B / 2, OHR_B / 2, 0, T_BODEN))
    xl = sx * (a + OHR_L / 2)
    for dy in (-OHR_LANG / 2, OHR_LANG / 2):
        minus(g, zylinder((xl, dy, -1), (xl, dy, T_BODEN + 1), D_OHR / 2))
    minus(g, quader(xl - D_OHR / 2, xl + D_OHR / 2, -OHR_LANG / 2, OHR_LANG / 2, -1, T_BODEN + 1))
c = komponente("NotAus_Gehaeuse", (0, 0, 0))
k1 = einsetzen(c, "NotAus_Gehaeuse", g)
exportieren(k1, "NotAus_Gehaeuse")

# ================================================================ Deckel
d = quader(-a, a, -a, a, 0, T_DECKEL)
minus(d, zylinder((0, 0, -1), (0, 0, T_DECKEL + 1), D_TASTER / 2))
for sx in (-1, 1):
    for sy in (-1, 1):
        minus(d, zylinder((sx * dom, sy * dom, -1), (sx * dom, sy * dom, T_DECKEL + 1), D_M3 / 2))
        minus(d, zylinder((sx * dom, sy * dom, T_DECKEL - T_KOPF), (sx * dom, sy * dom, T_DECKEL + 1), D_KOPF_M3 / 2))
c = komponente("NotAus_Deckel", (110, 0, 0))
k2 = einsetzen(c, "NotAus_Deckel", d)
exportieren(k2, "NotAus_Deckel")

vp = app.activeViewport
cam = vp.camera
cam.isSmoothTransition = False
cam.target = P(55, 0, 25)
cam.eye = P(190, -190, 150)
cam.upVector = V(0, 0, 1)
vp.camera = cam
vp.fit()
"fertig"
