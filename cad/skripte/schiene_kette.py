"""Schleppkette der Schiene J0 (Stufe C): Klemme für das Endglied der Kette, gleiches Teil für beide Enden.

  Kettenklemme_Sockel  Fuss 76 x 49,4 x 5 mm mit zwei Langlöchern für M4 (Abstand 54 mm, in einer Reihe auf der Mittellinie: für die
                       20-mm-Seite des Profils 2040 mit der einen Nut in der Mitte und T-Nutenstein M4, Fuss ragt dort je 14,7 mm
                       über; bzw. auf eine Schlittenplatte mit Gewinde M4; Schraubenkopf mit Scheibe liegt auf dem
                       Fuss) und ein Block mit U-Tasche für das letzte Kettenglied; zwei Einschmelzgewinde M3 für den Deckel.
  Kettenklemme_Deckel  Platte 4 mm, zwei Schrauben M3 x 8 (Kopf 2 mm versenkt, Bohrung im Block 8 mm tief), zwei Rippen an der
                       Unterseite pressen das Glied um PRESS mm (Reibklemme, KEIN Formschluss).

Die Klemme ist ein Notbehelf: Eine Kette mit mitgelieferten Anschlussstücken (Endglieder mit Flansch) braucht sie nicht und
ist vorzuziehen. Haltekraft nach dem ersten Druck mit der Federwaage prüfen (Soll mindestens 20 N, Zug der Kette wenige N).

Die Kette 10 x 15 mm (Innenmass Höhe x Breite) hat je nach Hersteller andere Aussenmasse (gefunden: 13 x 25, 15 x 23,
Biegeradius 18 bis 28 mm). KETTE_B und KETTE_H sind Startwerte: am gelieferten Endglied mit der Schieblehre nachmessen.
Die Kette liegt in der Tasche mit der Breite KETTE_B quer (y) und der Höhe KETTE_H nach oben (z).

Ausführen im Fusion-Python (MCP-Add-in):
    exec(open(pfad, encoding="utf-8").read())
Masse in mm. Export: AUSGABE = "<Ordner>" vorher setzen.
"""
import adsk.core
import adsk.fusion

MM = 0.1

KETTE_B, KETTE_H = 25.0, 15.0              # Startwerte: Aussenbreite und Aussenhöhe des Endglieds
# Beim Nachmessen auch PRESS setzen (Pressung der Rippen): bei dünnerem Glied (z. B. 13 mm statt 15 mm) bleibt sonst keine Pressung.
SPIEL = 0.4                                # Spiel in der Breite (y): Tasche = KETTE_B + SPIEL
H_SPIEL, PRESS = 0.2, 0.8                  # Höhe der Tasche = KETTE_H + H_SPIEL; die Rippen des Deckels pressen das Glied um PRESS
L_KLEMME = 20.0                            # Länge der Klemme entlang der Kette (x)
WAND = 10.0                                # Seitenwand neben der Tasche (3 mm Material je Seite um das Einschmelzgewinde Ø 4)
T_FUSS = 5.0
RIPPE_B, RIPPE_X = 1.5, 5.0                 # Rippen am Deckel: Breite, Abstand von der Mitte
FUSS_L, FUSS_LOCH, FUSS_TEILUNG, FUSS_LANG = 76.0, 4.5, 54.0, 8.0     # Langloch 8 mm lang: Feineinstellung der Lage
D_SCHEIBE_M4 = 9.0                         # Scheibe DIN 125 (Aussen-Ø 9) liegt auf dem Fuss, keine Senkung
D_EINSCHMELZ_M3, T_EINSCHMELZ = 4.0, 8.0
D_M3, D_KOPF_M3, T_KOPF_M3 = 3.4, 6.4, 2.0
T_DECKEL = 4.0

P_B, P_H = KETTE_B + SPIEL, KETTE_H + H_SPIEL
B_BLOCK = P_B + 2 * WAND
FUSS_B = B_BLOCK + 4.0
SCHRAUBE_Y = P_B / 2 + WAND / 2            # Schraubenmitte in der Seitenwand
assert (WAND - D_EINSCHMELZ_M3) / 2 >= 3.0, "Wand um das Einschmelzgewinde unter 3 mm je Seite"
assert FUSS_TEILUNG / 2 + FUSS_LANG / 2 + D_SCHEIBE_M4 / 2 + 2.0 <= FUSS_L / 2, "Scheibe ragt über den Fussrand"
assert FUSS_TEILUNG / 2 - FUSS_LANG / 2 - D_SCHEIBE_M4 / 2 >= L_KLEMME / 2, "Scheibe liegt auf dem Block"

app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
root = design.rootComponent
tbm = adsk.fusion.TemporaryBRepManager.get()
P = lambda x, y, z: adsk.core.Point3D.create(x * MM, y * MM, z * MM)
V = adsk.core.Vector3D.create


def farbe(name="SK_Druckteil"):
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


for i in range(root.occurrences.count - 1, -1, -1):
    root.occurrences.item(i).deleteMe()

# ================================================================ Sockel (Fuss unten, Tasche oben offen)
h_block = T_FUSS + P_H
s = quader(-FUSS_L / 2, FUSS_L / 2, -FUSS_B / 2, FUSS_B / 2, 0, T_FUSS)
plus(s, quader(-L_KLEMME / 2, L_KLEMME / 2, -B_BLOCK / 2, B_BLOCK / 2, T_FUSS - 0.01, h_block))
minus(s, quader(-L_KLEMME / 2 - 1, L_KLEMME / 2 + 1, -P_B / 2, P_B / 2, T_FUSS, h_block + 1))      # Tasche, an beiden Enden offen
for sy in (-1, 1):
    x_, y_ = 0.0, sy * SCHRAUBE_Y
    minus(s, zylinder((x_, y_, h_block - T_EINSCHMELZ), (x_, y_, h_block + 1), D_EINSCHMELZ_M3 / 2))
for sx in (-1, 1):                                                     # Langlöcher für M4 mit Senkung von oben
    xc = sx * FUSS_TEILUNG / 2
    for dx in (-(FUSS_LANG) / 2, FUSS_LANG / 2):
        minus(s, zylinder((xc + dx, 0, -1), (xc + dx, 0, T_FUSS + 1), FUSS_LOCH / 2))
    minus(s, quader(xc - FUSS_LANG / 2, xc + FUSS_LANG / 2, -FUSS_LOCH / 2, FUSS_LOCH / 2, -1, T_FUSS + 1))
c = komponente("Druck_Kettenklemme_Sockel", (0, 0, 0))
k1 = einsetzen(c, "Kettenklemme_Sockel", s)
exportieren(k1, "Kettenklemme_Sockel")

# ================================================================ Deckel
# Druckorientierung: Kopfseite (Senkung) unten auf dem Bett, die Rippen zeigen nach oben (im Einbau nach unten in die Tasche)
d = quader(-L_KLEMME / 2, L_KLEMME / 2, -B_BLOCK / 2, B_BLOCK / 2, 0, T_DECKEL)
for sx in (-1, 1):
    plus(d, quader(sx * RIPPE_X - RIPPE_B / 2, sx * RIPPE_X + RIPPE_B / 2, -P_B / 2 + 0.3, P_B / 2 - 0.3, T_DECKEL - 0.01, T_DECKEL + H_SPIEL + PRESS))
for sy in (-1, 1):
    minus(d, zylinder((0, sy * SCHRAUBE_Y, -1), (0, sy * SCHRAUBE_Y, T_DECKEL + 1), D_M3 / 2))
    minus(d, zylinder((0, sy * SCHRAUBE_Y, -1), (0, sy * SCHRAUBE_Y, T_KOPF_M3), D_KOPF_M3 / 2))
c = komponente("Druck_Kettenklemme_Deckel", (0, 70, 0))
k2 = einsetzen(c, "Kettenklemme_Deckel", d)
exportieren(k2, "Kettenklemme_Deckel")

vp = app.activeViewport
if vp:
    cam = vp.camera
    cam.isSmoothTransition = False
    cam.target = P(0, 30, 10)
    cam.eye = P(110, -70, 90)
    cam.upVector = V(0, 0, 1)
    vp.camera = cam
    vp.fit()
"fertig"
