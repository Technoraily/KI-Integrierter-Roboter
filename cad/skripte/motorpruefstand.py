"""Motorprüfstand für einen vorhandenen NEMA 17 – ohne Kaufteile.

Teile (alle gedruckt):
  Motorhalter   Grundplatte mit Wiege; der Motor liegt darin, die Welle ragt
                durch die Stirnwand über die Tischkante hinaus.
  Niederhalter  Bügel mit zwei Zapfen, hält den Motor in der Wiege.
  Waagebalken   ausgeglichener Hebel, Schnurlöcher bei ±100 mm (Test A, Haltemoment).
  Seiltrommel   gestuft: Wickelradius 20 mm und 10 mm mit 1-mm-Schnur
                (Test B, Moment bei Drehzahl; Test C, Schrittverlust).
Beide Naben werden mit je einer M3-Schraube (12–16 mm) und Mutter auf die Welle geklemmt.

Ausführen im Fusion-Python (MCP-Add-in):
    exec(open(pfad, encoding="utf-8").read())
Masse in mm. Welt: Welle entlang +y, x quer, z nach oben, z = 0 Tischfläche,
y = 40 Vorderkante der Grundplatte; sie ragt 20 mm über die Tischkante (Tischkante bei y = 20).
Waagebalken und Seiltrommel sind lokal in Druckorientierung modelliert (z = Druckrichtung).
"""
import math

import adsk.core
import adsk.fusion

MM = 0.1

# ---------------------------------------------------------------- Masse
NEMA = 42.3              # Kantenlänge Motor
SPIEL = 0.3              # Spiel Motor in der Wiege (je Seite 0,15)
L_MOTOR = 40.0           # nur für das Dummy-Modell; die Wiege passt für 34–60 mm
D_BUND, H_BUND = 22.0, 2.0
D_WELLE, L_WELLE = 5.0, 24.0
LOCHABSTAND = 31.0       # Motorschrauben M3, optional

T_BODEN = 5.0
Y_HINTEN, Y_STIRN = -6.0, 36.0      # Wiege von hinten bis Innenseite Stirnwand
Y_PLATTE_HINTEN = -70.0             # Grundplatte reicht weiter nach hinten: Zwingenlöcher liegen auf dem Tisch
Y_ZWINGE = -55.0
T_STIRN = 4.0
X_PLATTE = 100.0                    # Grundplatte x = ±100: Lasten bei ±100 hängen innerhalb
T_WAND = 10.0
H_WAND = 40.0                       # Oberkante Seitenwände (z)
B_INNEN = NEMA + SPIEL
Z_ACHSE = T_BODEN + NEMA / 2
D_ZAPFEN, D_ZAPFENLOCH, T_ZAPFENLOCH = 5.0, 5.4, 9.0

D_BOHRUNG = 5.1                     # Nabe auf 5-mm-Welle
SCHLITZ = 1.5
D_M3, M3_KOPF, M3_MUTTER_SW, M3_MUTTER_H = 3.4, 6.4, 5.9, 2.6

L_HEBEL, B_HEBEL, T_HEBEL = 100.0, 12.0, 6.0
R_NABE, H_NABE = 14.0, 10.0
R_KERN_20, R_KERN_10 = 19.5, 9.5   # Kern + Schnur 0,5 = Wickelradius 20 bzw. 10 mm
R_FLANSCH, R_BORD = 25.0, 22.0      # Aussenflansch / Bord zwischen den Stufen

app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
root = design.rootComponent
tbm = adsk.fusion.TemporaryBRepManager.get()
P = lambda x, y, z: adsk.core.Point3D.create(x * MM, y * MM, z * MM)
V = adsk.core.Vector3D.create

_FARBEN = {"Druckteil": (215, 220, 228), "Druckteil_dunkel": (120, 135, 160),
           "Motor": (240, 160, 70), "Stahl": (90, 95, 105), "Kamera": (35, 35, 40)}


def farbe(name):
    voll = "MP_" + name
    a = design.appearances.itemByName(voll)
    if a:
        return a
    lib = app.materialLibraries.itemByName("Fusion Appearance Library")
    a = design.appearances.addByCopy(lib.appearances.itemByName("Plastic - Matte (White)"), voll)
    for i in range(a.appearanceProperties.count):
        p = a.appearanceProperties.item(i)
        if isinstance(p, adsk.core.ColorProperty) and p.value:
            p.value = adsk.core.Color.create(*_FARBEN[name], 255)
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


def einsetzen(comp, name, body, f="Druckteil"):
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    k = comp.bRepBodies.add(body, bf)
    bf.finishEdit()
    k = comp.bRepBodies.item(comp.bRepBodies.count - 1)
    k.name = name
    k.appearance = farbe(f)
    return k


def komponente(name, ursprung=(0, 0, 0), x=(1, 0, 0), y=(0, 1, 0), z=(0, 0, 1)):
    m = adsk.core.Matrix3D.create()
    m.setWithCoordinateSystem(P(*ursprung), V(*x), V(*y), V(*z))
    occ = root.occurrences.addNewComponent(m)
    occ.component.name = name
    return occ.component


def klemmnabe(body, z0, z1, z_schlitz=None):
    """Bohrung, Schlitz nach +y und M3-Klemmschraube entlang x in einer Nabe (Achse z, Radius R_NABE)."""
    zm = (z0 + z1) / 2
    ys = 9.0                                      # Abstand Schraubenachse von der Wellenachse
    minus(body, quader(-SCHLITZ / 2, SCHLITZ / 2, 0, R_NABE + 1, (z0 if z_schlitz is None else z_schlitz) - 0.01, z1 + 0.01))
    minus(body, zylinder((-R_NABE - 1, ys, zm), (R_NABE + 1, ys, zm), D_M3 / 2))
    # Kopfsenkung (links) und Mutternfalle (rechts) als flache Taschen ab |x| = 6: Klemmlänge 12 mm -> M3 x 16
    minus(body, quader(-R_NABE - 1, -6.0, ys - M3_KOPF / 2, ys + M3_KOPF / 2, zm - M3_KOPF / 2, zm + M3_KOPF / 2))
    minus(body, quader(6.0, R_NABE + 1, ys - M3_MUTTER_SW / 2, ys + M3_MUTTER_SW / 2, zm - 3.3, zm + 3.3))


for i in range(root.occurrences.count - 1, -1, -1):
    root.occurrences.item(i).deleteMe()

# ================================================================ Motorhalter
xi, xa = B_INNEN / 2, B_INNEN / 2 + T_WAND
h = quader(-X_PLATTE, X_PLATTE, Y_PLATTE_HINTEN, Y_STIRN + T_STIRN, 0, T_BODEN)
for s in (-1, 1):
    plus(h, quader(s * xi, s * xa, Y_HINTEN, Y_STIRN, T_BODEN - 0.01, H_WAND))
z_stirn_oben = T_BODEN + NEMA
plus(h, quader(-xa, xa, Y_STIRN, Y_STIRN + T_STIRN, T_BODEN - 0.01, z_stirn_oben))
# Schlitz für Bund und Welle, oben offen
r_schlitz = D_BUND / 2 + 0.5
minus(h, zylinder((0, Y_STIRN - 1, Z_ACHSE), (0, Y_STIRN + T_STIRN + 1, Z_ACHSE), r_schlitz))
minus(h, quader(-r_schlitz, r_schlitz, Y_STIRN - 1, Y_STIRN + T_STIRN + 1, Z_ACHSE, z_stirn_oben + 1))
# optionale Motorschrauben M3 (Lochbild 31 mm)
for dx in (-LOCHABSTAND / 2, LOCHABSTAND / 2):
    for dz in (-LOCHABSTAND / 2, LOCHABSTAND / 2):
        minus(h, zylinder((dx, Y_STIRN - 1, Z_ACHSE + dz), (dx, Y_STIRN + T_STIRN + 1, Z_ACHSE + dz), D_M3 / 2))
# Zapfenlöcher für den Niederhalter
Y_ZAPFEN = 15.0
X_ZAPFEN = (xi + xa) / 2
for s in (-1, 1):
    minus(h, zylinder((s * X_ZAPFEN, Y_ZAPFEN, H_WAND - T_ZAPFENLOCH), (s * X_ZAPFEN, Y_ZAPFEN, H_WAND + 1), D_ZAPFENLOCH / 2))
# Löcher für Schraubzwinge oder Schrauben, hinten auf dem Tisch
for s in (-1, 1):
    minus(h, zylinder((s * 88, Y_ZWINGE, -1), (s * 88, Y_ZWINGE, T_BODEN + 1), 3.0))
mh = komponente("Motorhalter")
einsetzen(mh, "Motorhalter", h)

# ================================================================ Niederhalter
z_motor_oben = T_BODEN + NEMA
n = quader(-xa, xa, Y_ZAPFEN - 8, Y_ZAPFEN + 8, z_motor_oben + 0.2, z_motor_oben + 5.2)
for s in (-1, 1):
    plus(n, zylinder((s * X_ZAPFEN, Y_ZAPFEN, H_WAND - T_ZAPFENLOCH + 0.5), (s * X_ZAPFEN, Y_ZAPFEN, z_motor_oben + 0.3), D_ZAPFEN / 2))
nh = komponente("Niederhalter")
einsetzen(nh, "Niederhalter", n)

# ================================================================ Motor (Dummy, wird nicht gedruckt)
m = quader(-NEMA / 2, NEMA / 2, Y_STIRN - L_MOTOR, Y_STIRN, T_BODEN, T_BODEN + NEMA)
md = komponente("Dummy_NEMA17")
einsetzen(md, "Motor_NEMA17", m, "Motor")
einsetzen(md, "Bund", zylinder((0, Y_STIRN, Z_ACHSE), (0, Y_STIRN + H_BUND, Z_ACHSE), D_BUND / 2), "Stahl")
einsetzen(md, "Welle", zylinder((0, Y_STIRN, Z_ACHSE), (0, Y_STIRN + L_WELLE, Z_ACHSE), D_WELLE / 2), "Stahl")

# ================================================================ Waagebalken (lokal: Achse z, flach gedruckt)
w = zylinder((0, 0, 0), (0, 0, H_NABE), R_NABE)
plus(w, quader(-L_HEBEL, L_HEBEL, -B_HEBEL / 2, B_HEBEL / 2, 0, T_HEBEL))
for s in (-1, 1):
    plus(w, zylinder((s * L_HEBEL, 0, 0), (s * L_HEBEL, 0, T_HEBEL), B_HEBEL / 2))
    minus(w, zylinder((s * L_HEBEL, 0, -1), (s * L_HEBEL, 0, T_HEBEL + 1), 1.5))          # Schnurloch
minus(w, zylinder((0, 0, -1), (0, 0, H_NABE + 1), D_BOHRUNG / 2))
klemmnabe(w, 0, H_NABE)
# Montage: lokal z -> Welle (+y), lokal y -> -z (Schlitz nach unten); Nabenboden an der Stirnwand
wb = komponente("Waagebalken", (0, Y_STIRN + T_STIRN + 1, Z_ACHSE), (1, 0, 0), (0, 0, -1), (0, 1, 0))
einsetzen(wb, "Waagebalken", w, "Druckteil_dunkel")

# ================================================================ Seiltrommel (lokal: Achse z, Aussenflansch unten)
# Von unten nach oben werden die Radien nie grösser ohne 45°-Kegel: druckbar ohne Stützen.
Z_K20 = (1.5, 7.0)          # Kern r = 20 mm
Z_BORD = (7.0, 9.5)         # Kegel 19,5 -> 22 (Bord, hält die Schnur auf ihrer Stufe)
Z_K10 = (9.5, 18.0)         # Kern r = 10 mm, breit genug für 300 mm Schnur in einer Lage
Z_KEGEL = (18.0, 22.5)      # Kegel 9,5 -> 14 in die Nabe
Z_NABE = (22.5, 32.5)
t = zylinder((0, 0, 0), (0, 0, Z_K20[0]), R_FLANSCH)
plus(t, zylinder((0, 0, Z_K20[0] - 0.01), (0, 0, Z_K20[1]), R_KERN_20))
plus(t, zylinder((0, 0, Z_BORD[0] - 0.01), (0, 0, Z_BORD[1]), R_KERN_20, R_BORD))
plus(t, zylinder((0, 0, Z_K10[0] - 0.01), (0, 0, Z_K10[1]), R_KERN_10))
plus(t, zylinder((0, 0, Z_KEGEL[0] - 0.01), (0, 0, Z_KEGEL[1]), R_KERN_10, R_NABE))
plus(t, zylinder((0, 0, Z_NABE[0] - 0.01), (0, 0, Z_NABE[1]), R_NABE))
minus(t, zylinder((0, 0, -1), (0, 0, Z_NABE[1] + 1), D_BOHRUNG / 2))
klemmnabe(t, Z_NABE[0], Z_NABE[1], z_schlitz=Z_NABE[0] - 2.0)
# Schnurbefestigung: radial in den Kern, axial nach unten zum Knoten unter dem Aussenflansch
zm = sum(Z_K20) / 2
minus(t, zylinder((14.0, 0, zm), (R_KERN_20 + 1, 0, zm), 1.25))
minus(t, zylinder((15.5, 0, -1), (15.5, 0, zm + 1.25), 1.25))
zm = sum(Z_K10) / 2
minus(t, zylinder((-5.0, 0, zm), (-R_KERN_10 - 1, 0, zm), 1.25))
minus(t, zylinder((-7.0, 0, -1), (-7.0, 0, zm + 1.25), 1.25))
# Montage (nur zur Ansicht neben dem Halter liegend, Druckorientierung)
st = komponente("Seiltrommel", (60, 100, 0))
einsetzen(st, "Seiltrommel", t, "Druckteil_dunkel")

vp = app.activeViewport
cam = vp.camera
cam.isSmoothTransition = False
cam.target = P(0, 20, 20)
cam.eye = P(250, 350, 220)
cam.upVector = V(0, 0, 1)
vp.camera = cam
vp.fit()
"fertig"
