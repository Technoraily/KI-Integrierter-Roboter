"""Schrittbilder der Bauanleitung Motorprüfstand aus Fusion erzeugen.

Voraussetzung: motorpruefstand.py ist im aktiven Dokument gelaufen.
Ausführen im Fusion-Python:  exec(open(pfad, encoding="utf-8").read())
Legt vorübergehend Tisch, Flasche und Schnur als Dummy-Komponenten an,
verschiebt Teile für Explosionsansichten, speichert die Bilder nach
docs/bauanleitung/bilder/ und stellt danach alles wieder her.
"""
import os

import adsk.core
import adsk.fusion

MM = 0.1
ZIEL = r"C:\Claude\KI-Integrierter Roboter\docs\bauanleitung\bilder"
Z_ACHSE = 5.0 + 42.3 / 2

app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
root = design.rootComponent
tbm = adsk.fusion.TemporaryBRepManager.get()
P = lambda x, y, z: adsk.core.Point3D.create(x * MM, y * MM, z * MM)
V = adsk.core.Vector3D.create
occ = {o.component.name: o for o in root.occurrences}
original = {n: o.transform2.copy() for n, o in occ.items()}


def farbe(name, rgb):
    a = design.appearances.itemByName("MP_" + name)
    if a:
        return a
    lib = app.materialLibraries.itemByName("Fusion Appearance Library")
    a = design.appearances.addByCopy(lib.appearances.itemByName("Plastic - Matte (White)"), "MP_" + name)
    for i in range(a.appearanceProperties.count):
        p = a.appearanceProperties.item(i)
        if isinstance(p, adsk.core.ColorProperty) and p.value:
            p.value = adsk.core.Color.create(*rgb, 255)
            break
    return a


def dummy(name, koerper, rgb):
    o = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    o.component.name = name
    bf = o.component.features.baseFeatures.add()
    bf.startEdit()
    for b in koerper:
        o.component.bRepBodies.add(b, bf)
    bf.finishEdit()
    for i in range(o.component.bRepBodies.count):
        o.component.bRepBodies.item(i).appearance = farbe(name, rgb)
    return o


def quader(x0, x1, y0, y1, z0, z1):
    return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(
        P((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), V(1, 0, 0), V(0, 1, 0),
        (x1 - x0) * MM, (y1 - y0) * MM, (z1 - z0) * MM))


def zyl(p1, p2, r1, r2=None):
    return tbm.createCylinderOrCone(P(*p1), r1 * MM, P(*p2), (r1 if r2 is None else r2) * MM)


def flasche(x, y, z_schnur_oben):
    return [zyl((x, y, -470), (x, y, -190), 45), zyl((x, y, -190), (x, y, -150), 45, 14),
            zyl((x, y, -150), (x, y, -125), 14), zyl((x, y, -125), (x, y, z_schnur_oben), 0.7)]


def setze(name, dx=0, dy=0, dz=0, matrix=None):
    m = (matrix or original[name]).copy()
    t = m.translation
    t.add(V(dx * MM, dy * MM, dz * MM))
    m.translation = t
    occ[name].transform2 = m


def sichtbar(*namen):
    for n, o in occ.items():
        o.isLightBulbOn = n in namen


def zuruecksetzen():
    for n, o in occ.items():
        o.transform2 = original[n]


def bild(datei, eye, target, breite=1400, hoehe=900):
    vp = app.activeViewport
    cam = vp.camera
    cam.isSmoothTransition = False
    cam.target = P(*target)
    cam.eye = P(*eye)
    cam.upVector = V(0, 0, 1)
    vp.camera = cam
    vp.fit()
    vp.saveAsImageFile(os.path.join(ZIEL, datei), breite, hoehe)


os.makedirs(ZIEL, exist_ok=True)
VORNE = ((300, 420, 260), (0, 20, 20))

# Montierte Trommel: Nabe an der Stirnwand (lokal z = 32,5 -> y = 41), lokal y nach oben
TROMMEL_MONTIERT = adsk.core.Matrix3D.create()
TROMMEL_MONTIERT.setWithCoordinateSystem(P(0, 41 + 32.5, Z_ACHSE), V(1, 0, 0), V(0, 0, 1), V(0, -1, 0))

try:
    # 1 Teile
    sichtbar("Motorhalter", "Niederhalter", "Waagebalken", "Seiltrommel")
    setze("Niederhalter", dz=60)
    setze("Waagebalken", dy=90)
    setze("Seiltrommel", dx=90, dy=60)
    bild("01_teile.png", (350, 520, 380), (0, 40, 20))
    zuruecksetzen()

    # 2 Klemmnabe: Mutterfalle und Schraubenloch
    sichtbar("Waagebalken")
    bild("02_klemmnabe.png", (150, 160, -40), (0, 46, 20), 1200, 900)

    # 3 Motor einlegen
    sichtbar("Motorhalter", "Dummy_NEMA17")
    setze("Dummy_NEMA17", dz=70)
    bild("03_motor_einlegen.png", *VORNE)
    zuruecksetzen()

    # 4 Niederhalter
    sichtbar("Motorhalter", "Dummy_NEMA17", "Niederhalter")
    setze("Niederhalter", dz=40)
    bild("04_niederhalter.png", *VORNE)
    zuruecksetzen()

    # 5 Waagebalken
    sichtbar("Motorhalter", "Dummy_NEMA17", "Niederhalter", "Waagebalken")
    setze("Waagebalken", dy=50)
    bild("05_waagebalken.png", *VORNE)
    zuruecksetzen()

    # 6 Aufstellung Test A: Tisch, Flasche am Loch bei +100 mm
    tisch = dummy("Dummy_Tisch", [quader(-350, 350, -350, 20, -30, 0)], (170, 130, 90))
    fl_a = dummy("Dummy_Flasche_A", flasche(100, 44, Z_ACHSE), (120, 190, 230))
    occ["Dummy_Tisch"], occ["Dummy_Flasche_A"] = tisch, fl_a
    sichtbar("Motorhalter", "Dummy_NEMA17", "Niederhalter", "Waagebalken", "Dummy_Tisch", "Dummy_Flasche_A")
    bild("06_test_a.png", (700, 900, 250), (0, 0, -150))

    # 7 Test B: Trommel montiert, Schnur läuft bei x = +20 ab (Stufe r = 20, y ca. 69)
    fl_b = dummy("Dummy_Flasche_B", flasche(20, 69, Z_ACHSE), (120, 190, 230))
    occ["Dummy_Flasche_B"] = fl_b
    original["Dummy_Tisch"] = tisch.transform2.copy()
    original["Dummy_Flasche_A"] = fl_a.transform2.copy()
    original["Dummy_Flasche_B"] = fl_b.transform2.copy()
    setze("Seiltrommel", matrix=TROMMEL_MONTIERT)
    sichtbar("Motorhalter", "Dummy_NEMA17", "Niederhalter", "Seiltrommel", "Dummy_Tisch", "Dummy_Flasche_B")
    bild("07_test_b.png", (700, 900, 250), (0, 0, -150))
finally:
    for n in ("Dummy_Tisch", "Dummy_Flasche_A", "Dummy_Flasche_B"):
        if n in occ:
            occ.pop(n).deleteMe()
            original.pop(n, None)
    zuruecksetzen()
    for o in root.occurrences:
        o.isLightBulbOn = True
"fertig"
