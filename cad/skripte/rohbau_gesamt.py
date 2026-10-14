"""Vereinfachter Rohbau des ganzen Roboters (NUR Anschauung, kein Konzept).

Klötze und Zylinder in den Hauptmassen aus docs/parameter.md: Schiene J0,
Schlitten, Basis J1, Schulter J2, Oberarm, Ellbogen J3, Unterarm J4,
Hand J5, Flansch J6, Greiferwechsler mit Werkzeugablage.
Nichts davon ist konstruiert: Wandstärken, Lager, Riemen und Verkleidung
fehlen oder sind nur angedeutet.

Ausführen im Fusion-Python (MCP-Add-in):
    exec(open(pfad, encoding="utf-8").read())
Die Gelenkwinkel Q1..Q6 und die Schlittenposition X_SCHLITTEN unten ändern
und das Skript neu laufen lassen, um eine andere Pose zu sehen.
Masse in mm; Weltachsen: x entlang der Schiene, y quer, z nach oben, z = 0 Tisch.
"""
import math

import adsk.core
import adsk.fusion

MM = 0.1  # Fusion rechnet intern in cm

# ---------------------------------------------------------------- Pose
X_SCHLITTEN = -150.0           # Lage des Schlittens auf der Schiene (Mitte = 0)
Q1, Q2, Q3, Q4, Q5, Q6 = 0.0, 35.0, 65.0, 0.0, 80.0, 0.0   # Grad; Q2..Q5 = 0: Arm senkrecht

# ---------------------------------------------------------------- Masse (aus docs/parameter.md)
H_SCHULTER, L_OBERARM, L_UNTERARM, L_HAND = 170.0, 200.0, 190.0, 60.0
L_SCHIENE, SPUR = 1250.0, 160.0
Z_SCHLITTEN = 71.0             # Oberkante Schlittenplatte = Aufstellfläche des Arms

app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
root = design.rootComponent
tbm = adsk.fusion.TemporaryBRepManager.get()
P = lambda x, y, z: adsk.core.Point3D.create(x * MM, y * MM, z * MM)
V = adsk.core.Vector3D.create

# ---------------------------------------------------------------- Farben
_FARBEN = {
    "Druckteil": (215, 220, 228), "Druckteil_dunkel": (150, 160, 175),
    "Motor": (240, 160, 70), "Riemen": (40, 110, 160), "Alu": (190, 195, 200),
    "Stahl": (75, 80, 90), "Werkzeug": (70, 130, 210), "Gummi": (40, 40, 45),
    "Kamera": (30, 30, 30),
}


def farbe(name):
    voll = "RB_" + name
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


# ---------------------------------------------------------------- Körper
_wartend = {}  # Komponente -> [(Name, Temp-Körper, Farbe)]


def _neu(comp, name, body, f):
    _wartend.setdefault(comp.entityToken, (comp, []))[1].append((name, body, f))
    return body


def box(comp, name, c, s, f="Druckteil"):
    """Quader mit Mittelpunkt c und Kantenlängen s (mm)."""
    obb = adsk.core.OrientedBoundingBox3D.create(P(*c), V(1, 0, 0), V(0, 1, 0), s[0] * MM, s[1] * MM, s[2] * MM)
    return _neu(comp, name, tbm.createBox(obb), f)


def zyl(comp, name, p1, p2, r1, f="Druckteil", r2=None):
    """Zylinder (oder Kegelstumpf) von p1 nach p2."""
    b = tbm.createCylinderOrCone(P(*p1), r1 * MM, P(*p2), (r2 if r2 is not None else r1) * MM)
    return _neu(comp, name, b, f)


def abziehen(ziel, werkzeug):
    tbm.booleanOperation(ziel, werkzeug, adsk.fusion.BooleanTypes.DifferenceBooleanType)


def einfuegen():
    for comp, liste in _wartend.values():
        bf = comp.features.baseFeatures.add()
        bf.startEdit()
        for name, body, f in liste:
            if body is None:
                continue
            k = comp.bRepBodies.add(body, bf)
            k.name = name
            k.appearance = farbe(f)
        bf.finishEdit()
    _wartend.clear()


def komponente(eltern, name, verschiebung=(0, 0, 0), achse=None, winkel=0.0):
    m = adsk.core.Matrix3D.create()
    if achse:
        m.setToRotation(math.radians(winkel), V(*achse), adsk.core.Point3D.create(0, 0, 0))
    m.translation = V(*(v * MM for v in verschiebung))
    occ = eltern.occurrences.addNewComponent(m)
    occ.component.name = name
    return occ.component


# ---------------------------------------------------------------- Aufräumen
for i in range(root.occurrences.count - 1, -1, -1):
    o = root.occurrences.item(i)
    if o.component.name in ("Schiene_J0", "Schlitten", "Werkzeugablage"):
        o.deleteMe()

# ================================================================ Schiene J0
s = komponente(root, "Schiene_J0")
hl = L_SCHIENE / 2
for seite, y in (("links", -SPUR / 2), ("rechts", SPUR / 2)):
    box(s, f"Profil_40x40_{seite}", (0, y, 20), (L_SCHIENE, 40, 40), "Alu")
    box(s, f"MGN12_{seite}", (0, y, 44), (L_SCHIENE - 50, 12, 8), "Stahl")
box(s, "Endplatte_Motor", (-hl - 10, 0, 32), (20, 240, 64))
box(s, "Endplatte_Umlenkung", (hl + 10, 0, 32), (20, 240, 64))
box(s, "Motor_M0", (-hl - 45, 0, 36), (50, 42, 42), "Motor")
zyl(s, "Ritzel_J0", (-hl + 15, -6, 40), (-hl + 15, 6, 40), 7, "Stahl")
zyl(s, "Umlenkrolle_J0", (hl - 15, -6, 40), (hl - 15, 6, 40), 7, "Stahl")
box(s, "Riemen_J0_oben", (0, 0, 47.5), (L_SCHIENE - 30, 10, 1.5), "Riemen")
box(s, "Riemen_J0_unten", (0, 0, 32.5), (L_SCHIENE - 30, 10, 1.5), "Riemen")
# Schleppkette: unteres Trum auf dem Tisch, Bogen, oberes Trum zum Schlitten
yk = SPUR / 2 + 60
box(s, "Schleppkette_unten", ((-hl + X_SCHLITTEN - 60) / 2, yk, 10), (X_SCHLITTEN - 60 + hl, 20, 20), "Gummi")
zyl(s, "Schleppkette_Bogen", (X_SCHLITTEN - 60, yk - 10, 35), (X_SCHLITTEN - 60, yk + 10, 35), 35, "Gummi")
abziehen(_wartend[s.entityToken][1][-1][1],
         tbm.createCylinderOrCone(P(X_SCHLITTEN - 60, yk - 11, 35), 15 * MM, P(X_SCHLITTEN - 60, yk + 11, 35), 15 * MM))
abziehen(_wartend[s.entityToken][1][-1][1],
         tbm.createBox(adsk.core.OrientedBoundingBox3D.create(P(X_SCHLITTEN - 60 + 40, yk, 35), V(1, 0, 0), V(0, 1, 0), 8, 3, 8)))
box(s, "Schleppkette_oben", (X_SCHLITTEN - 30, yk, 60), (60, 20, 20), "Gummi")

# ================================================================ Schlitten
sl = komponente(root, "Schlitten", (X_SCHLITTEN, 0, 0))
for dx in (-60, 60):
    for dy in (-SPUR / 2, SPUR / 2):
        box(sl, f"Wagen_MGN12H_{'v' if dx > 0 else 'h'}{'r' if dy > 0 else 'l'}", (dx, dy, 54.5), (45, 27, 13), "Stahl")
box(sl, "Schlittenplatte", (0, 0, Z_SCHLITTEN - 5), (240, 240, 10), "Alu")
box(sl, "Riemenklemme", (0, 0, 52), (40, 16, 8), "Druckteil_dunkel")

# ================================================================ Basis (fest auf dem Schlitten)
ba = komponente(sl, "Basis", (0, 0, Z_SCHLITTEN))
zyl(ba, "Basis_Fuss", (0, 0, 0), (0, 0, 90), 90, "Druckteil", r2=75)
box(ba, "Motor_M1", (-85, 0, 40), (48, 42, 42), "Motor")
zyl(ba, "Lager_J1", (0, 0, 90), (0, 0, 96), 72, "Stahl")

# ---------------------------------------------------------------- J1 Drehteil mit Schulterbock
j1 = komponente(ba, "J1_Drehteil", achse=(0, 0, 1), winkel=Q1)
zyl(j1, "Drehteller", (0, 0, 96), (0, 0, 116), 75)
for seite, y0, y1 in (("links", -52, -38), ("rechts", 38, 52)):
    box(j1, f"Schulterwange_{seite}", (0, (y0 + y1) / 2, 143), (110, 14, 54))
    zyl(j1, f"Schulterauge_{seite}", (0, y0, H_SCHULTER), (0, y1, H_SCHULTER), 55)
box(j1, "Riemengehaeuse_J2", (-25, -85, 165), (150, 66, 110), "Druckteil_dunkel")
box(j1, "Motor_M2_60mm", (-75, -148, 150), (42, 60, 42), "Motor")

# ---------------------------------------------------------------- Oberarm (J2)
oa = komponente(j1, "Oberarm_J2", (0, 0, H_SCHULTER), (0, 1, 0), Q2)
zyl(oa, "Schulternabe", (0, -38, 0), (0, 38, 0), 40)
box(oa, "Oberarm_Schaft", (0, 0, 60), (60, 76, 120))
for seite, y0, y1 in (("links", -42, -30), ("rechts", 30, 42)):
    box(oa, f"Ellbogengabel_{seite}", (0, (y0 + y1) / 2, 155), (60, 12, 90))
    zyl(oa, f"Ellbogenauge_{seite}", (0, y0, L_OBERARM), (0, y1, L_OBERARM), 32)
box(oa, "Riemengehaeuse_J3", (0, 55, 132), (50, 22, 145), "Druckteil_dunkel")
box(oa, "Motor_M3", (-51, 0, 60), (42, 48, 42), "Motor")

# ---------------------------------------------------------------- Unterarm (J3), hinterer Teil mit M4/M5
ua = komponente(oa, "Unterarm_J3", (0, 0, L_OBERARM), (0, 1, 0), Q3)
zyl(ua, "Ellbogennabe", (0, -29, 0), (0, 29, 0), 30)
box(ua, "Unterarm_Gehaeuse", (0, 0, 45), (58, 56, 130))
box(ua, "Motor_M4", (0, 50, 55), (42, 44, 42), "Motor")
box(ua, "Motor_M5_34mm", (0, -45, 60), (42, 34, 42), "Motor")
zyl(ua, "Lager_J4", (0, 0, 110), (0, 0, 116), 27, "Stahl")

# ---------------------------------------------------------------- Unterarm-Rolle (J4)
j4 = komponente(ua, "Unterarm_Rolle_J4", achse=(0, 0, 1), winkel=Q4)
zyl(j4, "Unterarm_Rohr", (0, 0, 116), (0, 0, 155), 25)
for seite, y0, y1 in (("links", -32, -22), ("rechts", 22, 32)):
    box(j4, f"Handgabel_{seite}", (0, (y0 + y1) / 2, 170), (44, 10, 40))
    zyl(j4, f"Handauge_{seite}", (0, y0, L_UNTERARM), (0, y1, L_UNTERARM), 22)

# ---------------------------------------------------------------- Hand (J5)
ha = komponente(j4, "Hand_J5", (0, 0, L_UNTERARM), (0, 1, 0), Q5)
zyl(ha, "Handnabe", (0, -21, 0), (0, 21, 0), 20)
box(ha, "Handkoerper", (0, 0, 24), (40, 40, 48))
box(ha, "Motor_M6_NEMA14", (-38, 0, 24), (36, 35, 35), "Motor")
box(ha, "Kamera_spaeter", (30, 0, 30), (16, 30, 22), "Kamera")
zyl(ha, "Lager_J6", (0, 0, 48), (0, 0, 52), 20, "Stahl")

# ---------------------------------------------------------------- Flansch (J6) und Wechsler
fl = komponente(ha, "Flansch_J6", (0, 0, 52), (0, 0, 1), Q6)
zyl(fl, "Flansch_ISO9409_31_5", (0, 0, 0), (0, 0, L_HAND - 52), 25, "Stahl")
zyl(fl, "Wechsler_Roboterseite", (0, 0, 8), (0, 0, 18), 30, "Druckteil_dunkel")
box(fl, "Pogo_Kontakte", (22, 0, 13), (10, 14, 10), "Kamera")


def werkzeugplatte(comp, name):
    zyl(comp, f"{name}_Wechselplatte", (0, 0, 0), (0, 0, 8), 30, "Werkzeug")
    zyl(comp, f"{name}_Hals", (0, 0, 8), (0, 0, 30), 18, "Werkzeug")


def parallelgreifer(comp):
    werkzeugplatte(comp, "Parallelgreifer")
    box(comp, "Parallelgreifer_Servogehaeuse", (0, 0, 50), (70, 34, 40), "Werkzeug")
    for x in (-20, 20):
        box(comp, f"Finger_{'rechts' if x > 0 else 'links'}", (x, 0, 95), (8, 22, 50), "Gummi")


def sauggreifer(comp):
    werkzeugplatte(comp, "Sauggreifer")
    zyl(comp, "Sauggreifer_Rohr", (0, 0, 30), (0, 0, 100), 6, "Stahl")
    zyl(comp, "Saugnapf", (0, 0, 100), (0, 0, 115), 8, "Gummi", r2=20)


def magnetgreifer(comp):
    werkzeugplatte(comp, "Magnetgreifer")
    zyl(comp, "Elektromagnet", (0, 0, 30), (0, 0, 60), 25, "Kamera")


# Am Arm: Parallelgreifer. Werkzeug-Achse zeigt in +z vom Flansch weg.
gr = komponente(fl, "Werkzeug_Parallelgreifer", (0, 0, 18))
parallelgreifer(gr)

# ================================================================ Werkzeugablage am Schienenende
wa = komponente(root, "Werkzeugablage", (hl - 150, SPUR / 2 + 170, 0))
Z_ABLAGE = 262.0
box(wa, "Ablage_Fuss", (0, 20, 4), (230, 130, 8))
box(wa, "Ablage_Saeule", (0, 60, (8 + Z_ABLAGE) / 2), (30, 30, Z_ABLAGE - 8))
platte = box(wa, "Ablage_Platte", (0, 0, Z_ABLAGE - 6), (230, 120, 12))
for x in (-75, 0, 75):  # drei Gabeln, offen zur Schiene (-y); Mitte frei für das Werkzeug am Arm
    abziehen(platte, tbm.createBox(adsk.core.OrientedBoundingBox3D.create(
        P(x, -40, Z_ABLAGE - 6), V(1, 0, 0), V(0, 1, 0), 4.0, 8.0, 2.0)))
    zyl(wa, f"Fang_{x:+.0f}", (x, -20, Z_ABLAGE), (x, -20, Z_ABLAGE + 4), 32, "Druckteil_dunkel")
    abziehen(_wartend[wa.entityToken][1][-1][1], tbm.createCylinderOrCone(
        P(x, -20, Z_ABLAGE - 1), 30.5 * MM, P(x, -20, Z_ABLAGE + 5), 30.5 * MM))
    abziehen(_wartend[wa.entityToken][1][-1][1], tbm.createBox(adsk.core.OrientedBoundingBox3D.create(
        P(x, -50, Z_ABLAGE + 2), V(1, 0, 0), V(0, 1, 0), 4.4, 6.0, 1.0)))

# Werkzeuge hängen kopfüber in der Ablage: Wechselplatte liegt oben auf, Werkzeug zeigt nach unten
for x, name, bauer in ((-75, "Werkzeug_Sauggreifer", sauggreifer), (75, "Werkzeug_Magnetgreifer", magnetgreifer)):
    w = komponente(wa, name, (x, -20, Z_ABLAGE + 8), (1, 0, 0), 180)
    bauer(w)

einfuegen()

# Kamera: schräg von vorne
vp = app.activeViewport
cam = vp.camera
cam.isSmoothTransition = False
cam.target = P(0, 0, 200)
cam.eye = P(900, -1600, 900)
cam.upVector = V(0, 0, 1)
vp.camera = cam
vp.fit()
"fertig"
