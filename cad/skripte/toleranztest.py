"""Toleranz-Testteil: legt die Drucktoleranzen für den A1 fest (docs/parameter.md, «Drucktoleranzen»).

Teile (alle gedruckt, zusammen auf ein Druckbett):
  Toleranz_Platte    liegend gedruckt, Löcher senkrecht, vier Reihen von links (kleinstes Mass) nach rechts:
                       A  Lagersitz 608 (Aussen 22 mm): 22,00 / 22,05 / 22,10 / 22,15 / 22,20 / 22,25
                       B  Wellenbohrung 5 mm: 5,0 / 5,1 / 5,2 / 5,3  |  Achse 8 mm: 8,0 / 8,1 / 8,2 / 8,3
                       C  Einschmelzgewinde M3: 3,8 / 4,0 / 4,2 / 4,4  |  M4: 5,2 / 5,4 / 5,6 / 5,8 (Sackloch 6 mm)
                       D  Passzapfen 10 mm: Loch 10,1 / 10,2 / 10,3 / 10,4  |  M3 Durchgang 3,2 / 3,4 / 3,6 / 3,8
                     Jede Reihe beginnt links mit einer Kerbe am vorderen Rand (Reihe A, B, C, D von vorn nach hinten).
  Toleranz_Stehend   hochkant gedruckt, Löcher waagrecht (hängende Decke!): Lager 22,10 / 22,20 / 22,30, Welle 5,2 / 8,2.
  Passzapfen         Ø 10 mm, 14 mm lang, mit Bund, zum Prüfen der Reihe D (und Welle 5/8 mm der Reihe B als Messstift).

Auswertung: pro Reihe das Mass nehmen, bei dem das Teil gerade noch ohne Hammer, aber ohne Spiel sitzt
(Lager: saugend von Hand eindrücken, kein Wackeln). Das ergibt tol_lagersitz, tol_passung, d_einschmelz_M3/M4.

Ausführen im Fusion-Python (MCP-Add-in):
    exec(open(pfad, encoding="utf-8").read())
Masse in mm. Teile liegen in Druckorientierung; z = Druckrichtung.
Export: setze vorher AUSGABE = "<Ordner>" (sonst wird nicht exportiert).
"""
import adsk.core
import adsk.fusion

MM = 0.1

# ---------------------------------------------------------------- Masse
T_PLATTE = 8.0                       # Dicke: 608-Lager 7 mm + 1 mm Auflage
B_PLATTE, L_PLATTE = 90.0, 186.0     # y (tief) x x (lang)
LAGER = [22.00, 22.05, 22.10, 22.15, 22.20, 22.25]
WELLE5 = [5.0, 5.1, 5.2, 5.3]
ACHSE8 = [8.0, 8.1, 8.2, 8.3]
M3EIN = [3.8, 4.0, 4.2, 4.4]
M4EIN = [5.2, 5.4, 5.6, 5.8]
ZAPFEN = [10.1, 10.2, 10.3, 10.4]
M3DURCH = [3.2, 3.4, 3.6, 3.8]
T_LAGER, D_LAGERAUSLASS = 7.0, 16.0  # Sitztiefe, Durchgang darunter zum Ausdrücken
T_EINSCHMELZ = 6.0
D_ZAPFEN, L_ZAPFEN, D_BUND, T_BUND = 10.0, 14.0, 16.0, 3.0

# Reihenabstand y und erster Lochmittelpunkt x, Teilung x
ROWS = {"A": (16.0, 17.0, 30.0), "B": (40.0, 14.0, 16.0), "C": (58.0, 14.0, 16.0), "D": (76.0, 14.0, 16.0)}

# Stehend: Breite x, Höhe z, Dicke y
X_ST, Z_ST, Y_ST = 100.0, 42.0, 8.0

app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
root = design.rootComponent
tbm = adsk.fusion.TemporaryBRepManager.get()
P = lambda x, y, z: adsk.core.Point3D.create(x * MM, y * MM, z * MM)
V = adsk.core.Vector3D.create


def farbe():
    a = design.appearances.itemByName("TT_Druckteil")
    if a:
        return a
    lib = app.materialLibraries.itemByName("Fusion Appearance Library")
    a = design.appearances.addByCopy(lib.appearances.itemByName("Plastic - Matte (White)"), "TT_Druckteil")
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

# ================================================================ Platte (liegend)
p = quader(0, L_PLATTE, 0, B_PLATTE, 0, T_PLATTE)


def reihe(name, masse, tiefe=None, versatz=0):
    y, x0, dx = ROWS[name]
    for i, d in enumerate(masse):
        x = x0 + versatz + i * dx
        if tiefe is None:                                  # Durchgang
            minus(p, zylinder((x, y, -1), (x, y, T_PLATTE + 1), d / 2))
        else:                                              # Sackloch von oben
            minus(p, zylinder((x, y, T_PLATTE - tiefe), (x, y, T_PLATTE + 1), d / 2))


reihe("A", LAGER, T_LAGER)
for i in range(len(LAGER)):                                # Auslass unter dem Lagersitz
    x = ROWS["A"][1] + i * ROWS["A"][2]
    minus(p, zylinder((x, ROWS["A"][0], -1), (x, ROWS["A"][0], T_PLATTE), D_LAGERAUSLASS / 2))
reihe("B", WELLE5)
reihe("B", ACHSE8, versatz=len(WELLE5) * ROWS["B"][2] + 8.0)
reihe("C", M3EIN, T_EINSCHMELZ)
reihe("C", M4EIN, T_EINSCHMELZ, versatz=len(M3EIN) * ROWS["C"][2] + 8.0)
reihe("D", ZAPFEN)
reihe("D", M3DURCH, versatz=len(ZAPFEN) * ROWS["D"][2] + 8.0)
for y, _, _ in ROWS.values():                              # Kerbe: Reihenbeginn am linken Rand
    minus(p, quader(-1, 4.0, y - 1.5, y + 1.5, T_PLATTE - 2.0, T_PLATTE + 1))
c = komponente("Toleranz_Platte", (0, 0, 0))
k_platte = einsetzen(c, "Toleranz_Platte", p)
exportieren(k_platte, "Toleranz_Platte")

# ================================================================ Stehend (Löcher waagrecht)
s = quader(0, X_ST, 0, Y_ST, 0, Z_ST)
loecher = [(18.0, 22.10), (50.0, 22.20), (82.0, 22.30)]   # Lager, Mittelpunkt z unten
zl = 13.0
for x, d in loecher:
    minus(s, zylinder((x, -1, zl), (x, T_LAGER, zl), d / 2))
    minus(s, zylinder((x, T_LAGER - 0.01, zl), (x, Y_ST + 1, zl), D_LAGERAUSLASS / 2))
for x, d in [(18.0, 5.2), (50.0, 8.2)]:
    minus(s, zylinder((x, -1, 34.0), (x, Y_ST + 1, 34.0), d / 2))
c = komponente("Toleranz_Stehend", (0, 110, 0))
k_st = einsetzen(c, "Toleranz_Stehend", s)
exportieren(k_st, "Toleranz_Stehend")

# ================================================================ Passzapfen
z = zylinder((0, 0, 0), (0, 0, T_BUND), D_BUND / 2)
plus(z, zylinder((0, 0, T_BUND - 0.01), (0, 0, T_BUND + L_ZAPFEN), D_ZAPFEN / 2))
c = komponente("Passzapfen", (130, 110, 0))
k_z = einsetzen(c, "Passzapfen", z)
exportieren(k_z, "Passzapfen")

vp = app.activeViewport
cam = vp.camera
cam.isSmoothTransition = False
cam.target = P(L_PLATTE / 2, 60, 0)
cam.eye = P(L_PLATTE / 2 + 80, -140, 260)
cam.upVector = V(0, 0, 1)
vp.camera = cam
vp.fit()
"fertig"
