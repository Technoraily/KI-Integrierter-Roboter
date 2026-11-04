"""Werkzeugflansch am Handgelenk: Greiferwechsler (kinematische Kupplung + Magnete + Pogo-Pins) und Kamerahalter.

Vorbereitung nach docs/konzept.md 3.5 («nur vorsehen»); Reserve am Flansch insgesamt 150 g für Wechsler und Kamera.

  WF_Master        Roboterseite, Ø 70 x 8 mm. Rückseite auf dem Flansch ISO 9409-1-31,5-4-M5 (4 x Ø 5,5 auf Lochkreis 31,5 mm,
                   Senkung für niedrigen M5-Zylinderkopf mit Scheibe von der Kupplungsseite), 3 Stahlkugeln Ø 6 mm in Taschen, 3 Magnete
                   Ø 10 x 3 mm in Taschen, 6 Bohrungen für Pogo-Pins, Aufnahme für einen Codierstift Ø 3 x 6 mm bei 60°/r = 11 mm, Mittelbohrung Ø 10 mm für das Kabel, zwei
                   Einschmelzgewinde M3 auf der Rückseite (r = 31 mm) für den Kamerahalter.
  WF_Werkzeug      Werkzeugseite, Ø 70 x 8 mm: 3 V-Nuten (90 Grad) für die Kugeln, 3 Magnettaschen (andere Polung),
                   6 Löcher Ø 2,2 für Schrauben M2 als Kontaktflächen, Mittelbohrung, 4 Einschmelzgewinde M3 auf Ø 28 mm
                   als Startwert für den Greifer (an den gekauften Greifer anpassen).
  WF_Magnetprobe   zwei Blöcke 34 x 30 x 12 mit je einer Magnettasche und einem Kernloch Ø 3,3 mm von hinten für eine Ringschraube M4 (axialer Zug in der Magnetachse): Haltekraft eines Magnetpaares
                   messen, bevor der Wechsler gedruckt wird.
  WF_Kamerahalter  Z-förmiger Halter: Fuss auf der Rückseite des Masters (2 x M3), Arm ausserhalb des Rands nach vorn,
                   Kameraplatte für ein Platinenmodul 25 x 24 mm (Lochbild 21 x 12,5 mm, M2; Startwerte, ungeprüft).

Alle Masse zu Kaufteilen (ISO-Flansch, Kugeln, Magnete, Pogo-Pins, Kameramodul) sind Startwerte und wurden nicht an
einem gelieferten Teil geprüft. Ausführen im Fusion-Python (MCP-Add-in):
    exec(open(pfad, encoding="utf-8").read())
Masse in mm. Die Kupplungsseite liegt in den Platten oben (z = T_PLATTE), gedruckt wird mit der Rückseite auf dem Bett.
Export: AUSGABE = "<Ordner>" vorher setzen.
"""
import math

import adsk.core
import adsk.fusion

MM = 0.1

# ---------------------------------------------------------------- Masse
D_PLATTE, T_PLATTE = 70.0, 8.0
R_KIN = 27.0                              # Kreis für Kugeln und Magnete (ausserhalb der M5-Senkungen auf r = 15,75 + 4,75)
PCD_ISO, D_M5_DURCH, D_M5_SENK, T_M5_SENK = 31.5, 5.5, 9.5, 5.5       # PCD aus docs/parameter.md; Senkung für M5 Zylinderkopf (Ø 8,5)
ISO_WINKEL = (0.0, 90.0, 180.0, 270.0)
K_M5, T_SCHEIBE_M5, KOPF_RESERVE = 3.5, 1.0, 0.5                       # niedriger Zylinderkopf M5 (DIN 7984, k = 3,5) + Scheibe Ø 9 x 1; Kopf bleibt 0,5 mm unter der Fläche
KUGEL_D, KUGEL_SPIEL = 6.0, 0.15          # Stahlkugel (Lagerkugel) in Tasche, Kugelmitte liegt in der Fläche (halb eingesenkt)
KUGEL_WINKEL = (90.0, 210.0, 330.0)
MAGNET_D, MAGNET_T, MAGNET_SPIEL = 10.0, 3.0, 0.2                      # Scheibenmagnet Ø 10 x 3 (Startwert); Tasche zum Einkleben
MAGNET_WINKEL = (30.0, 150.0, 270.0)
SPALT = 0.4                               # Abstand der Platten im gekuppelten Zustand (Kugelmitte steht SPALT über der Nutfläche)
POGO_R, POGO_N, D_POGO = 9.0, 6, 1.7                                    # Pogo-Pins (Startwert Ø 1,7)
D_KONTAKT, D_KONTAKT_KOPF, T_KONTAKT_KOPF = 2.4, 4.2, 1.3              # Werkzeugseite: M2 x 6 Schlitz-Zylinderkopf (DIN 84, Ø 3,8 x 1,3) bündig in der Senkung
L_KONTAKT_SCHRAUBE = 6.0
MUTTER_M2_SW, MUTTER_M2_T = 4.3, 1.8                                   # Sechskanttasche hinten für Mutter M2 (SW 4 + 0,3)
CODE_R, CODE_WINKEL = 11.0, 60.0                                       # Codierstift Ø 3 x 6 mm im Master; Loch im Werkzeug am gespiegelten Winkel
D_CODE_MASTER, T_CODE_MASTER, D_CODE_WERKZEUG, T_CODE_WERKZEUG = 3.1, 4.5, 3.5, 3.0
D_MITTE = 10.0
KAM_WINKEL = (170.0, 190.0)               # Einschmelzgewinde für den Kamerahalter, Rückseite, r = 29,5 mm
KAM_R = 31.0
D_EINSCHMELZ_M3, T_EINSCHMELZ = 4.0, 6.0
GREIFER_R, GREIFER_WINKEL = 16.0, (0.0, 90.0, 180.0, 270.0)           # Startwert Greiferbefestigung (4 x M3, Ø 32 mm)

# Kamerahalter (Montagelage: x tangential, y radial nach aussen ab r = 24,5 mm, z von der Rückseite des Masters nach vorn)
KH_B = 28.0
KH_FUSS_R0 = 24.5                         # Abstand der Fussinnenkante von der Achse
KH_FUSS_Y, KH_FUSS_T = 16.0, 4.0
KH_ARM_Y0, KH_ARM_T, KH_ARM_H = 12.0, 4.0, 56.0     # Arm bei r = 36,5 .. 40,5 mm: 1,5 mm ausserhalb des Plattenrands (r = 35)
KH_PLATTE_T, KH_PLATTE_Y1 = 4.0, 46.0
KH_Y_KAMERA = 30.0                        # Mitte des Kameramoduls in y (Platine reicht von y = 18 bis 42, Arm endet bei y = 16)
KH_LOCH_X, KH_LOCH_Y, D_KH_M2 = 21.0, 12.5, 2.2     # Startwerte: Raspberry-Pi-Kameramodul (Lochbild 21 x 12,5)
KH_LINSE = 11.0                           # Fenster für die Linse (quadratisch)
KH_FFC_B, KH_FFC_T = 19.0, 2.2            # Schlitz für das Flachbandkabel

# ---------------------------------------------------------------- Prüfungen
polar_ = lambda r, grad: (r * math.cos(math.radians(grad)), r * math.sin(math.radians(grad)))
R_AUSSEN = D_PLATTE / 2
assert R_KIN + MAGNET_D / 2 + MAGNET_SPIEL / 2 + 2.5 <= R_AUSSEN, "Magnettasche zu nah am Rand"
for a_iso in ISO_WINKEL:                  # Abstand Senkung M5 zu Kugel- und Magnettaschen (Mitte zu Mitte, minus Radien)
    px, py = PCD_ISO / 2 * math.cos(math.radians(a_iso)), PCD_ISO / 2 * math.sin(math.radians(a_iso))
    for a_k, r_t in [(w, KUGEL_D / 2 + KUGEL_SPIEL / 2) for w in KUGEL_WINKEL] + \
                    [(w, MAGNET_D / 2 + MAGNET_SPIEL / 2) for w in MAGNET_WINKEL]:
        kx, ky = R_KIN * math.cos(math.radians(a_k)), R_KIN * math.sin(math.radians(a_k))
        assert math.hypot(px - kx, py - ky) - D_M5_SENK / 2 - r_t >= 1.2, "Senkung M5 zu nah an einer Tasche (Winkel %s / %s)" % (a_iso, a_k)
assert K_M5 + T_SCHEIBE_M5 + KOPF_RESERVE <= T_M5_SENK, "M5-Kopf mit Scheibe steht über der Kupplungsfläche"
_sitz = T_PLATTE - T_KONTAKT_KOPF                                      # Kopfauflage der Kontaktschraube (z)
_spitze = _sitz - L_KONTAKT_SCHRAUBE
assert _spitze >= 0.0, "Kontaktschraube ragt hinten aus der Platte"
assert MUTTER_M2_T - _spitze >= 1.0, "Kontaktschraube fasst weniger als 1 mm in der Mutter"
cx_, cy_ = polar_(CODE_R, CODE_WINKEL)
for w in GREIFER_WINKEL:                                               # Codierloch (gespiegelt) gegen Greifer-Einschmelzgewinde
    gx, gy = polar_(GREIFER_R, w)
    hx, hy = polar_(CODE_R, -CODE_WINKEL)
    assert math.hypot(gx - hx, gy - hy) - D_EINSCHMELZ_M3 / 2 - D_CODE_WERKZEUG / 2 >= 1.5, "Codierloch zu nah am Greifer-Einschmelzgewinde"
    for i in range(POGO_N):
        qx, qy = polar_(POGO_R, 360.0 / POGO_N * i + 30.0)
        assert math.hypot(gx - qx, gy - qy) - D_EINSCHMELZ_M3 / 2 - MUTTER_M2_SW / 2 >= 1.5, "Greifer-Einschmelzgewinde zu nah an einer Mutterntasche"
for i in range(POGO_N):
    px_, py_ = polar_(POGO_R, 360.0 / POGO_N * i + 30.0)
    assert math.hypot(px_ - cx_, py_ - cy_) - D_POGO / 2 - D_CODE_WERKZEUG / 2 >= 1.5, "Codierstift zu nah an einem Pogo-Pin"
for a_iso in ISO_WINKEL:
    px, py = polar_(PCD_ISO / 2, a_iso)
    assert math.hypot(px - cx_, py - cy_) - D_M5_SENK / 2 - D_CODE_WERKZEUG / 2 >= 1.5, "Codierstift zu nah an einer Senkung M5"
# Nutgeometrie: 90-Grad-V, Kugelmitte SPALT über der Nutfläche
NUT_TIEFE = KUGEL_D / 2 / math.sin(math.radians(45.0)) - SPALT
assert NUT_TIEFE < T_PLATTE - 2.0, "V-Nut zu tief"
for a_m, a_k in [(m, k) for m in MAGNET_WINKEL for k in KAM_WINKEL]:
    kx, ky = KAM_R * math.cos(math.radians(a_k)), KAM_R * math.sin(math.radians(a_k))
    mx, my = R_KIN * math.cos(math.radians(a_m)), R_KIN * math.sin(math.radians(a_m))
    assert math.hypot(kx - mx, ky - my) - D_EINSCHMELZ_M3 / 2 - (MAGNET_D + MAGNET_SPIEL) / 2 >= 2.0, "Einschmelzgewinde zu nah an einer Magnettasche"

app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
root = design.rootComponent
tbm = adsk.fusion.TemporaryBRepManager.get()
P = lambda x, y, z: adsk.core.Point3D.create(x * MM, y * MM, z * MM)
V = adsk.core.Vector3D.create


def farbe(name="WF_Druckteil"):
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


def matrix(zeilen):
    m = adsk.core.Matrix3D.create()
    for r in range(3):
        for c in range(3):
            m.setCell(r, c, zeilen[r][c])
        m.setCell(r, 3, zeilen[r][3] * MM)
    return m


def polar(r, grad):
    return r * math.cos(math.radians(grad)), r * math.sin(math.radians(grad))


def nut_v(winkel, r0, r1, z_flaeche, tiefe):
    """V-Nut (90 Grad) radial bei 'winkel' von r0 bis r1; Spitze 'tiefe' unter z_flaeche. Rauten-Prisma, Mitte auf der Fläche."""
    a = math.radians(winkel)
    u = V(math.cos(a), math.sin(a), 0)
    w = V((-math.sin(a) + 0) / math.sqrt(2), math.cos(a) / math.sqrt(2), 1 / math.sqrt(2))
    seite = tiefe * math.sqrt(2)
    rm = (r0 + r1) / 2
    obb = adsk.core.OrientedBoundingBox3D.create(P(rm * math.cos(a), rm * math.sin(a), z_flaeche), u, w, (r1 - r0) * MM, seite * MM, seite * MM)
    return tbm.createBox(obb)


def sechskant_z(x, y, z0, z1, sw):
    teile = []
    for w in (0.0, 60.0, 120.0):
        a = math.radians(w)
        obb = adsk.core.OrientedBoundingBox3D.create(P(x, y, (z0 + z1) / 2), V(math.cos(a), math.sin(a), 0),
                                                     V(-math.sin(a), math.cos(a), 0), 30 * MM, sw * MM, abs(z1 - z0) * MM)
        teile.append(tbm.createBox(obb))
    tbm.booleanOperation(teile[0], teile[1], adsk.fusion.BooleanTypes.IntersectionBooleanType)
    tbm.booleanOperation(teile[0], teile[2], adsk.fusion.BooleanTypes.IntersectionBooleanType)
    return teile[0]


def platte():
    return zylinder((0, 0, 0), (0, 0, T_PLATTE), D_PLATTE / 2)


def pogo(body, d, z0, z1):
    for i in range(POGO_N):
        x, y = polar(POGO_R, 360.0 / POGO_N * i + 30.0)
        minus(body, zylinder((x, y, z0), (x, y, z1), d / 2))


def gespiegelt(winkel):
    """Beim Kuppeln wird die Werkzeugplatte umgedreht (um die x-Achse): Winkel w liegt dann bei -w."""
    return tuple((-w) % 360.0 for w in winkel)


def magnete(body, winkel):
    for w in winkel:
        x, y = polar(R_KIN, w)
        minus(body, zylinder((x, y, T_PLATTE - MAGNET_T), (x, y, T_PLATTE + 1), (MAGNET_D + MAGNET_SPIEL) / 2))


for i in range(root.occurrences.count - 1, -1, -1):
    root.occurrences.item(i).deleteMe()

# ================================================================ Master (Roboterseite)
m = platte()
for w in KUGEL_WINKEL:                                                    # Kugeltaschen: halb eingesenkt
    x, y = polar(R_KIN, w)
    minus(m, zylinder((x, y, T_PLATTE - KUGEL_D / 2), (x, y, T_PLATTE + 1), (KUGEL_D + KUGEL_SPIEL) / 2))
magnete(m, MAGNET_WINKEL)
for w in ISO_WINKEL:                                                      # ISO-Flansch: Durchgang + Senkung von der Kupplungsseite
    x, y = polar(PCD_ISO / 2, w)
    minus(m, zylinder((x, y, -1), (x, y, T_PLATTE + 1), D_M5_DURCH / 2))
    minus(m, zylinder((x, y, T_PLATTE - T_M5_SENK), (x, y, T_PLATTE + 1), D_M5_SENK / 2))
pogo(m, D_POGO, -1, T_PLATTE + 1)
xc_, yc_ = polar(CODE_R, CODE_WINKEL)                                      # Aufnahme für den Codierstift Ø 3 x 6 mm (steht 1,5 mm vor)
minus(m, zylinder((xc_, yc_, T_PLATTE - T_CODE_MASTER), (xc_, yc_, T_PLATTE + 1), D_CODE_MASTER / 2))
minus(m, zylinder((0, 0, -1), (0, 0, T_PLATTE + 1), D_MITTE / 2))
for w in KAM_WINKEL:                                                      # Einschmelzgewinde M3 von der Rückseite (senkrecht, ohne Stützen)
    x, y = polar(KAM_R, w)
    minus(m, zylinder((x, y, -1), (x, y, T_EINSCHMELZ), D_EINSCHMELZ_M3 / 2))
c = komponente("Druck_WF_Master", (0, 0, 0))
k1 = einsetzen(c, "WF_Master", m)
exportieren(k1, "WF_Master")

# ================================================================ Werkzeugseite
t = platte()
for w in gespiegelt(KUGEL_WINKEL):                                        # V-Nuten unter den Kugeln (Platte ist beim Kuppeln gespiegelt)
    minus(t, nut_v(w, R_KIN - 5.0, R_KIN + 5.0, T_PLATTE, NUT_TIEFE))
magnete(t, gespiegelt(MAGNET_WINKEL))
for i in range(POGO_N):                                                   # Kontakt: M2 x 8 von vorn, Kopf bündig, Mutter hinten
    x, y = polar(POGO_R, 360.0 / POGO_N * i + 30.0)
    minus(t, zylinder((x, y, -1), (x, y, T_PLATTE + 1), D_KONTAKT / 2))
    minus(t, zylinder((x, y, T_PLATTE - T_KONTAKT_KOPF), (x, y, T_PLATTE + 1), D_KONTAKT_KOPF / 2))
    minus(t, sechskant_z(x, y, -1, MUTTER_M2_T, MUTTER_M2_SW))
xc_, yc_ = polar(CODE_R, -CODE_WINKEL)                                     # Codierloch (gespiegelt zum Stift im Master)
minus(t, zylinder((xc_, yc_, T_PLATTE - T_CODE_WERKZEUG), (xc_, yc_, T_PLATTE + 1), D_CODE_WERKZEUG / 2))
minus(t, zylinder((0, 0, -1), (0, 0, T_PLATTE + 1), D_MITTE / 2))
for w in GREIFER_WINKEL:
    x, y = polar(GREIFER_R, w)
    minus(t, zylinder((x, y, -1), (x, y, T_EINSCHMELZ), D_EINSCHMELZ_M3 / 2))
c = komponente("Druck_WF_Werkzeug", (80, 0, 0))
k2 = einsetzen(c, "WF_Werkzeug", t)
exportieren(k2, "WF_Werkzeug")

# ================================================================ Magnetprobe (zwei gleiche Blöcke, 0,4 mm Papier oder Karton als Spalt dazwischen)
PROBE_T = 12.0
for i, x0 in enumerate((0.0, 50.0)):                                       # Zug mittig: Gewinde M4 von hinten (Ringschraube), Magnet in der Kontaktfläche
    b = quader(0, 34, 0, 30, 0, PROBE_T)
    minus(b, zylinder((17, 15, PROBE_T - MAGNET_T), (17, 15, PROBE_T + 1), (MAGNET_D + MAGNET_SPIEL) / 2))
    minus(b, zylinder((17, 15, -1), (17, 15, PROBE_T - MAGNET_T - 1.0), 3.3 / 2))   # Kernloch für M4 (selbstschneidend), 1 mm Wand unter der Magnettasche
    c = komponente("Druck_WF_Magnetprobe_" + "AB"[i], (x0, 60, 0))
    k = einsetzen(c, "WF_Magnetprobe_" + "AB"[i], b)
    exportieren(k, "WF_Magnetprobe_" + "AB"[i])

# ================================================================ Kamerahalter (Montagelage, dann Druckorientierung: x senkrecht)
h = quader(-KH_B / 2, KH_B / 2, 0, KH_FUSS_Y, 0, KH_FUSS_T)
plus(h, quader(-KH_B / 2, KH_B / 2, KH_ARM_Y0, KH_ARM_Y0 + KH_ARM_T, 0, KH_ARM_H))
plus(h, quader(-KH_B / 2, KH_B / 2, KH_ARM_Y0, KH_PLATTE_Y1, KH_ARM_H - KH_PLATTE_T, KH_ARM_H))
for w in KAM_WINKEL:                                # Fuss liegt bei 180 Grad; y = Abstand von der Achse minus 24,5 mm, x tangential
    px, py = polar(KAM_R, w)
    xl, y_loch = py, -px - KH_FUSS_R0
    assert 2.0 <= y_loch <= KH_FUSS_Y - 2.0, "Schraubenloch des Kamerahalters liegt nicht im Fuss"
    minus(h, zylinder((xl, y_loch, -1), (xl, y_loch, KH_FUSS_T + 1), 3.4 / 2))
    minus(h, zylinder((xl, y_loch, -1), (xl, y_loch, 2.2), 6.4 / 2))     # Senkung für den Schraubenkopf auf der Wrist-Seite
for sx in (-1, 1):
    for sy in (-1, 1):
        minus(h, zylinder((sx * KH_LOCH_X / 2, KH_Y_KAMERA + sy * KH_LOCH_Y / 2, KH_ARM_H - KH_PLATTE_T - 1),
                          (sx * KH_LOCH_X / 2, KH_Y_KAMERA + sy * KH_LOCH_Y / 2, KH_ARM_H + 1), D_KH_M2 / 2))
minus(h, quader(-KH_LINSE / 2, KH_LINSE / 2, KH_Y_KAMERA - KH_LINSE / 2, KH_Y_KAMERA + KH_LINSE / 2, KH_ARM_H - KH_PLATTE_T - 1, KH_ARM_H + 1))
minus(h, quader(-KH_FFC_B / 2, KH_FFC_B / 2, KH_Y_KAMERA + KH_LINSE / 2 + 1.5, KH_Y_KAMERA + KH_LINSE / 2 + 1.5 + KH_FFC_T,
                KH_ARM_H - KH_PLATTE_T - 1, KH_ARM_H + 1))
hd = tbm.copy(h)                                                           # Druckorientierung: (x, y, z) -> (y, z, x + 14), x wird zur Bauhöhe
tbm.transform(hd, matrix([[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, KH_B / 2]]))
c = komponente("Druck_WF_Kamerahalter", (0, 100, 0))
k4 = einsetzen(c, "WF_Kamerahalter", hd)
exportieren(k4, "WF_Kamerahalter")

vp = app.activeViewport
if vp:
    cam = vp.camera
    cam.isSmoothTransition = False
    cam.target = P(40, 40, 8)
    cam.eye = P(150, -90, 120)
    cam.upVector = V(0, 0, 1)
    vp.camera = cam
    vp.fit()
"fertig"
