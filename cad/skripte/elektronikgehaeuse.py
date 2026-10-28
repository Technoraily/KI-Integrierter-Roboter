"""Elektronikgehäuse J2-Prüfstand: Netzteil LRS-350, Arduino Uno mit CNC-Shield, Netzeingang C14, Sicherung F1.

  EG_Wanne            Boden 5 mm, Wände 3 mm, Höhe 60 mm. Vier Pads mit Senkungen für das Netzteil (M4 von unten),
                      vier Dome für den Arduino (Einschmelzgewinde M3), zehn Dome für den Deckel, vier Dome für die
                      Netzblende (waagrechte Bohrung in Tropfenform), zwei Sechskanttaschen im Boden (von oben, Mutter wird eingelegt) für die
                      Klemmenabdeckung, vier Befestigungslöcher für ein Grundbrett, Kabelbinderschlitze,
                      Lüftungsschlitze, Öffnungen für USB und Motorkabel. Die Frontwand hat einen nach oben offenen
                      Ausschnitt (keine 110-mm-Brücke) mit einem Wandsteg und Dom für den Deckel, den die Netzblende schliesst.
  EG_Deckel           Platte 4 mm mit Lüftungsschlitzen über dem Netzteil, Zugangsschlitz zu Poti V ADJ und LED,
                      zehn Schrauben M3, Lippe 2 x 6 mm unter dem Rand links, rechts und hinten (druckt mit der
                      Oberseite nach unten).
  EG_Netzblende       Platte 5 mm in der Frontwand bis unter den Deckel: Ausschnitt C14 (zwei Schraubenlöcher mit
                      Mutterntaschen) und Bohrung für den Bajonett-Sicherungshalter. Getrennt gedruckt, damit nur sie
                      nachgedruckt werden muss, falls die Masse der gekauften Teile abweichen.
  EG_Passprobe_C14    Testplatte 56 x 100 x 5 mm mit drei Stufen des C14-Ausschnitts und des Lochabstands (je 1 bis 3 Grübchen).
  EG_Passprobe_F1     Testplatte 114 x 26 x 5 mm mit fünf Bohrungen für den Sicherungshalter (je 1 bis 5 Grübchen).
                      Beide Passproben sind eigenständig (ohne Wanne) und drucken in unter einer Stunde.
  EG_Klemmenabdeckung Haube über der Klemmleiste des Netzteils (Berührschutz): Die Ringschuh-Kabel laufen in einem
                      10 mm breiten Gang links vom Netzteil (unter der Haube) nach vorne bzw. hinten und treten
                      durch unten offene Schlitze in den Stirnwänden aus; so lässt sich die Haube nach dem
                      Verdrahten von oben aufsetzen. Zwei Laschen vorne, Schrauben M3 x 10 in Muttern in Taschen im Boden.

Alle Masse mit dem Vermerk 'Startwert' sind vor dem Druck an den gekauften Teilen nachzumessen
(docs/stuecklisten/elektronikgehaeuse.md, Abschnitt «Zu messen»).

Koordinaten (Zusammenbau): x nach rechts, y nach hinten, z nach oben; Ursprung unten vorne links aussen.
Innenkoordinaten (ix, iy, iz) beginnen an der Innenseite der Wände und auf dem Boden.

Ausführen im Fusion-Python (MCP-Add-in):
    exec(open(pfad, encoding="utf-8").read())
Masse in mm. Die Druckteile liegen in Druckorientierung in den Komponenten «Druck_*», der Zusammenbau in «Bau_*».
Export: setze vorher AUSGABE = "<Ordner>" (sonst wird nicht exportiert).
"""
import math

import adsk.core
import adsk.fusion

MM = 0.1

# ---------------------------------------------------------------- Gehäuse
L_IN, W_IN = 234.0, 232.0               # lichte Länge (x) und Breite (y); Aussen 240 x 238 (Bauraum A1: 240)
T_W, T_B, H_AUSSEN, T_DECKEL = 3.0, 5.0, 60.0, 4.0
L_AUSSEN, W_AUSSEN = L_IN + 2 * T_W, W_IN + 2 * T_W
D_DOM, D_EINSCHMELZ_M3, T_EINSCHMELZ_TIEFE = 8.0, 4.0, 10.0   # Messung 20.10.: Bohrung 4,0 mm; Tiefe 10 mm für Schraube M3 x 10 im Deckel
D_M3, D_KOPF_M3, T_KOPF = 3.4, 6.4, 2.0
D_DOM_BLENDE = 9.0                       # waagrechte Dome hinter der Netzblende: 1,7 mm Material über der Tropfenspitze
STEG_X, STEG_B = 100.0, 8.0                # Wandsteg im Frontausschnitt (trägt einen Deckeldom), Aussenkoordinaten
DOM_A = 3.5                              # Mittelpunkt der Wanddome 3,5 mm von der Innenwand: überlappt die Wand um 0,5 mm
DECKEL_DOME = [(DOM_A, DOM_A), (L_IN - DOM_A, DOM_A), (DOM_A, W_IN - DOM_A), (L_IN - DOM_A, W_IN - DOM_A), (195.0, DOM_A), (195.0, W_IN - DOM_A),
               (DOM_A, 150.0), (L_IN - DOM_A, 190.0), (115.0, W_IN - DOM_A), (STEG_X - T_W, DOM_A)]   # 10 Dome; seitlich dort, wo weder Netzteil noch Haube stehen

# ---------------------------------------------------------------- Netzteil Mean Well LRS-350 (Datenblatt Case 207A)
PSU_L, PSU_B, PSU_H = 215.0, 115.0, 30.0
PSU_X0, PSU_Y0 = 15.0, 46.0              # innen (46 mm von der Frontwand bis zum Netzteil, 27 mm hinter dem C14-Körper); Klemmleiste am linken Ende, Klemme 1 (Netz L) vorne
PSU_LOCH = [(32.5, 32.5), (182.5, 32.5), (32.5, 82.5), (182.5, 82.5)]   # 4 x M4, Gewindetiefe nur 3 mm (!)
PAD_H, D_PAD = 2.5, 14.0
D_M4, D_KOPF_M4, T_KOPF_M4 = 4.5, 8.2, 4.0   # Senkung von unten für Zylinder- oder Linsenkopf M4; Schraube M4 x 6

# ---------------------------------------------------------------- Arduino Uno R3 mit CNC-Shield V3
UNO_L, UNO_B = 68.6, 53.3
UNO_LOCH = [(13.97, 2.54), (15.24, 50.8), (66.04, 7.62), (66.04, 35.56)]
AX0, AY0 = 12.0, PSU_Y0 + PSU_B + 8.0    # innen; USB links, Unterkante der Platine zum Netzteil hin
H_AB, D_AB = 6.0, 8.0                    # Abstandsdome (Schraube M3 x 6)
USB_Y, USB_B, USB_H = 32.0, 30.0, 15.0   # Startwert: Öffnung links, Mitte ab Unterkante der Platine, Breite (gross, Lage ungeprüft), Höhe
MOTOR_X = [(22.0, 42.0), (47.0, 67.0), (72.0, 92.0)]   # drei Kabelöffnungen hintere Wand, je 20 mm (Brücke ≤ 20 mm)
MOTOR_Z0, MOTOR_Z1 = 12.0, 24.0                        # Startwert

# ---------------------------------------------------------------- Netzblende (Frontwand)
FENSTER_X0, FENSTER_X1, FENSTER_Z0 = 40.0, 150.0, 10.0   # Ausschnitt Frontwand, nach oben offen (Aussenkoordinaten)
BLENDE_X0, BLENDE_X1, BLENDE_Z0, BLENDE_Z1, T_BLENDE = 28.0, 162.0, 3.0, H_AUSSEN, 5.0   # reicht bis unter den Deckel
BLENDE_SCHRAUBEN = [(34.0, 7.0), (156.0, 7.0), (34.0, 53.0), (156.0, 53.0)]
C14_X, C14_Z, C14_B, C14_H, C14_LOCH = 62.0, 30.0, 28.0, 20.0, 40.0    # Startwert; Lochabstand 36 mm innen/innen gemessen
F1_X, F1_Z, D_F1 = 120.0, 30.0, 12.8                                    # Gewinde etwas über 12 mm, Startwert
MUTTER_SW, MUTTER_T = 5.8, 2.6                                         # Sechskant M3 (5,5 + 0,3), Tiefe
# Passproben: eigenständige Testplatten mit abgestuften Massen (Stufen links nach rechts bzw. oben nach unten aufsteigend)
PASS_C14 = [(-0.6, -0.4), (0.0, 0.0), (0.6, 0.4)]                       # je Stufe: Zugabe Ausschnitt (b und h), Zugabe Lochabstand
PASS_F1 = [-0.4, -0.2, 0.0, 0.2, 0.4]                                    # Zugabe zum Bohrungsdurchmesser D_F1

# ---------------------------------------------------------------- Klemmenabdeckung
KL_X0, KL_X1 = 5.0, 35.0                 # innen, lichte Weite (lokal -10 .. +20 zum Netzteil; Klemmleiste laut Zeichnung bis 16,7)
KL_Y0, KL_Y1 = PSU_Y0 - 2.0, PSU_Y0 + 91.5   # innen; Rückwand 1,2 mm: Aussenfläche bei 92,7 mm, Poti V ADJ ab 93,2 mm
T_KL_HINTEN = 1.2
KL_Z_INNEN = 44.0
T_KL = 2.4
KL_AUS_B, KL_AUS_H = 10.0, 14.0           # Kabelaustritt in den Stirnwänden (über dem Kabelgang links vom Netzteil), offen nach unten
LASCHE_T, LASCHE_B = 5.0, 9.0             # zwei Laschen vorne auf dem Boden (z 0..5); Schraube M3 x 10, Spitze bündig mit der Unterseite
KL_LASCHEN = [(20.0, KL_Y0 - T_KL - 5.0), (31.0, KL_Y0 - T_KL - 5.0)]   # Lochmitten innen (x, y); Mutter M3 in Tasche im Boden (von oben eingelegt)

# ---------------------------------------------------------------- Sonstiges
BODENLOCH = [(120.0, 205.0), (215.0, 205.0), (170.0, 18.0), (215.0, 18.0)]   # innen: Befestigung auf Grundbrett (M4)
D_BODENLOCH, D_SENKUNG = 4.5, 9.0
BINDER_SLITZE = [(150.0, 195.0), (190.0, 195.0), (25.0, 22.0), (40.0, 22.0), (100.0, 22.0)]   # innen; zwei Schlitze je Stelle; vorne für die Netzkabel zum Kabelgang
LUEFT_DECKEL_X = [150.0 + 10.0 * k for k in range(8)]   # über dem Lüfter (Mitte 47,45 mm vom rechten, 78,3 mm vom vorderen Rand)
LUEFT_Y, LUEFT_LANG = 78.3, 50.0
LIPPE_T, LIPPE_H, LIPPE_SPIEL = 2.0, 6.0, 0.3   # Rippe unter dem Deckelrand links, rechts, hinten: steift den Rand zwischen den Schrauben
# Zugang zum Poti V ADJ und zur LED durch den Deckel (Lage aus dem Datenblatt ausgemessen: Poti 5,5 / 96,6, LED y 105,8 mm vom
# linken und vorderen Rand des Netzteils; am Gerät nachmessen). Der Deckel bleibt für die Einstellung der 24 V geschlossen.
POTI_X, POTI_Y0, POTI_Y1, POTI_B = 5.5, 92.0, 110.0, 9.0

app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
root = design.rootComponent
tbm = adsk.fusion.TemporaryBRepManager.get()
P = lambda x, y, z: adsk.core.Point3D.create(x * MM, y * MM, z * MM)
V = adsk.core.Vector3D.create


def farbe(name="EG_Druckteil", rgb=(215, 220, 228)):
    a = design.appearances.itemByName(name)
    if a:
        return a
    lib = app.materialLibraries.itemByName("Fusion Appearance Library")
    a = design.appearances.addByCopy(lib.appearances.itemByName("Plastic - Matte (White)"), name)
    for i in range(a.appearanceProperties.count):
        p = a.appearanceProperties.item(i)
        if isinstance(p, adsk.core.ColorProperty) and p.value:
            p.value = adsk.core.Color.create(rgb[0], rgb[1], rgb[2], 255)
            break
    return a


def quader(x0, x1, y0, y1, z0, z1):
    obb = adsk.core.OrientedBoundingBox3D.create(P((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), V(1, 0, 0), V(0, 1, 0),
                                                 abs(x1 - x0) * MM, abs(y1 - y0) * MM, abs(z1 - z0) * MM)
    return tbm.createBox(obb)


def qi(x0, x1, y0, y1, z0, z1):
    """Quader in Innenkoordinaten."""
    return quader(x0 + T_W, x1 + T_W, y0 + T_W, y1 + T_W, z0 + T_B, z1 + T_B)


def zylinder(p1, p2, r1, r2=None):
    return tbm.createCylinderOrCone(P(*p1), r1 * MM, P(*p2), (r1 if r2 is None else r2) * MM)


def plus(a, b):
    tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.UnionBooleanType)


def minus(a, b):
    tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.DifferenceBooleanType)


def schnitt(a, b):
    tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.IntersectionBooleanType)


def tropfen_y(x, z, y0, y1, d):
    """Waagrechte Bohrung (Achse y) in Tropfenform: Spitze nach oben, damit sie ohne Stützen druckt."""
    zyl = zylinder((x, y0, z), (x, y1, z), d / 2)
    a = math.radians(45.0)
    obb = adsk.core.OrientedBoundingBox3D.create(P(x, (y0 + y1) / 2, z), V(math.cos(a), 0, math.sin(a)), V(0, 1, 0),
                                                 d * MM, abs(y1 - y0) * MM, d * MM)
    spitze = tbm.createBox(obb)
    schnitt(spitze, tbm.createBox(adsk.core.OrientedBoundingBox3D.create(
        P(x, (y0 + y1) / 2, z + d / 2 * math.sin(math.radians(45.0)) + d / 2), V(1, 0, 0), V(0, 1, 0), 2 * d * MM,
        abs(y1 - y0) * MM, d * MM)))   # Raute erst ab den Tangentenpunkten des Kreises behalten (z + r * sin 45)
    plus(zyl, spitze)
    return zyl


def sechskant_z(x, y, z0, z1, sw):
    """Sechskantprisma, Achse z, Schlüsselweite sw."""
    teile = []
    for w in (0.0, 60.0, 120.0):
        a = math.radians(w)
        obb = adsk.core.OrientedBoundingBox3D.create(P(x, y, (z0 + z1) / 2), V(math.cos(a), math.sin(a), 0),
                                                     V(-math.sin(a), math.cos(a), 0), 30 * MM, sw * MM, abs(z1 - z0) * MM)
        teile.append(tbm.createBox(obb))
    schnitt(teile[0], teile[1])
    schnitt(teile[0], teile[2])
    return teile[0]


def sechskant_y(x, z, y0, y1, sw):
    """Sechskantprisma, Achse y, Schlüsselweite sw, von y0 bis y1."""
    teile = []
    for w in (0.0, 60.0, 120.0):
        a = math.radians(w)
        u = V(math.cos(a), 0, math.sin(a))
        obb = adsk.core.OrientedBoundingBox3D.create(P(x, (y0 + y1) / 2, z), u, V(0, 1, 0), 30 * MM, abs(y1 - y0) * MM, sw * MM)
        teile.append(tbm.createBox(obb))
    schnitt(teile[0], teile[1])
    schnitt(teile[0], teile[2])
    return teile[0]


def komponente(name, ursprung=(0, 0, 0)):
    m = adsk.core.Matrix3D.create()
    m.translation = V(ursprung[0] * MM, ursprung[1] * MM, ursprung[2] * MM)
    occ = root.occurrences.addNewComponent(m)
    occ.component.name = name
    return occ.component


def einsetzen(comp, name, body, ref=False):
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    comp.bRepBodies.add(body, bf)
    bf.finishEdit()
    k = comp.bRepBodies.item(comp.bRepBodies.count - 1)
    k.name = name
    k.appearance = farbe("EG_Referenz", (120, 130, 145)) if ref else farbe()
    return k


def matrix(zeilen):
    """3 x 4: [[a, b, c, tx], ...] in mm."""
    m = adsk.core.Matrix3D.create()
    for r in range(3):
        for c in range(3):
            m.setCell(r, c, zeilen[r][c])
        m.setCell(r, 3, zeilen[r][3] * MM)
    return m


def drucklage(body, zeilen):
    kopie = tbm.copy(body)
    tbm.transform(kopie, matrix(zeilen))
    return kopie


def exportieren(k, datei):
    if "AUSGABE" not in globals():
        return
    o = design.exportManager.createSTLExportOptions(k, AUSGABE + "/" + datei + ".stl")
    o.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
    design.exportManager.execute(o)


for i in range(root.occurrences.count - 1, -1, -1):
    root.occurrences.item(i).deleteMe()

# ================================================================ Wanne
g = quader(0, L_AUSSEN, 0, W_AUSSEN, 0, H_AUSSEN)
minus(g, qi(0, L_IN, 0, W_IN, 0, H_AUSSEN))

for (ix, iy) in DECKEL_DOME:                                      # Deckeldome
    plus(g, zylinder((ix + T_W, iy + T_W, T_B - 0.01), (ix + T_W, iy + T_W, H_AUSSEN), D_DOM / 2))
    minus(g, zylinder((ix + T_W, iy + T_W, H_AUSSEN - T_EINSCHMELZ_TIEFE), (ix + T_W, iy + T_W, H_AUSSEN + 1), D_EINSCHMELZ_M3 / 2))

for (lx, ly) in PSU_LOCH:                                         # Netzteil: Pads, Löcher, Senkungen von unten
    x, y = PSU_X0 + lx + T_W, PSU_Y0 + ly + T_W
    plus(g, zylinder((x, y, T_B - 0.01), (x, y, T_B + PAD_H), D_PAD / 2))
    minus(g, zylinder((x, y, -1), (x, y, T_B + PAD_H + 1), D_M4 / 2))
    minus(g, zylinder((x, y, -1), (x, y, T_KOPF_M4), D_KOPF_M4 / 2))

for (hx, hy) in UNO_LOCH:                                         # Arduino: Abstandsdome mit Einschmelzgewinde
    x, y = AX0 + hx + T_W, AY0 + hy + T_W
    plus(g, zylinder((x, y, T_B - 0.01), (x, y, T_B + H_AB), D_AB / 2))
    minus(g, zylinder((x, y, T_B + H_AB - 6.0), (x, y, T_B + H_AB + 1), D_EINSCHMELZ_M3 / 2))

for (bx, bz) in BLENDE_SCHRAUBEN:                                 # Dome hinter der Netzblende (Achse y)
    plus(g, zylinder((bx, T_W - 0.01, bz), (bx, T_W + 7.0, bz), D_DOM_BLENDE / 2))
    minus(g, tropfen_y(bx, bz, T_W + 1.0, T_W + 8.0, D_EINSCHMELZ_M3))
    minus(g, zylinder((bx, -1, bz), (bx, T_W + 1.5, bz), D_M3 / 2))
minus(g, quader(FENSTER_X0, STEG_X - STEG_B / 2, -1, T_W + 1, FENSTER_Z0, H_AUSSEN + 1))   # Ausschnitte Frontwand, oben offen (keine Brücke)
minus(g, quader(STEG_X + STEG_B / 2, FENSTER_X1, -1, T_W + 1, FENSTER_Z0, H_AUSSEN + 1))

for (ix, iy) in KL_LASCHEN:                                       # Klemmenabdeckung: Schraube M3, Mutter in Tasche im Boden (von oben)
    x, y = ix + T_W, iy + T_W
    minus(g, zylinder((x, y, -1), (x, y, T_B + 1), D_M3 / 2))
    minus(g, sechskant_z(x, y, T_B - MUTTER_T, T_B + 0.5, MUTTER_SW))   # Tasche von oben: Mutter wird eingelegt, Haubenlasche hält sie

for (ix, iy) in BODENLOCH:                                        # Befestigung auf Grundbrett
    x, y = ix + T_W, iy + T_W
    minus(g, zylinder((x, y, -1), (x, y, T_B + 1), D_BODENLOCH / 2))
    minus(g, tbm.createCylinderOrCone(P(x, y, T_B - 2.2), (D_BODENLOCH / 2) * MM, P(x, y, T_B + 0.01), (D_SENKUNG / 2) * MM))

for (ix, iy) in BINDER_SLITZE:                                    # Kabelbinder: je zwei Schlitze 3,8 x 2,2 im Abstand 8
    for dy in (-4.0, 4.0):
        minus(g, quader(ix + T_W - 1.9, ix + T_W + 1.9, iy + T_W + dy - 1.1, iy + T_W + dy + 1.1, -1, T_B + 1))

# USB links, Motorkabel hinten, Lüftung rechts
uy = AY0 + USB_Y + T_W
minus(g, quader(-1, T_W + 1, uy - USB_B / 2, uy + USB_B / 2, T_B + H_AB + 1.6 - 1.9, T_B + H_AB + 1.6 - 1.9 + USB_H))
for (mx0, mx1) in MOTOR_X:
    minus(g, quader(mx0 + T_W, mx1 + T_W, W_AUSSEN - T_W - 1, W_AUSSEN + 1, T_B + MOTOR_Z0, T_B + MOTOR_Z1))
for k in range(6):
    minus(g, quader(L_AUSSEN - T_W - 1, L_AUSSEN + 1, PSU_Y0 + T_W + 8 + k * 18 - 1.5, PSU_Y0 + T_W + 8 + k * 18 + 1.5, 14.0, 38.0))

c_wanne = komponente("Bau_Wanne")
k_wanne = einsetzen(c_wanne, "EG_Wanne", g)
c = komponente("Druck_Wanne", (0, -(W_AUSSEN + 20), 0))
k1 = einsetzen(c, "EG_Wanne", drucklage(g, [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]))
exportieren(k1, "EG_Wanne")

# ================================================================ Deckel
d = quader(0, L_AUSSEN, 0, W_AUSSEN, 0, T_DECKEL)
for (ix, iy) in DECKEL_DOME:
    minus(d, zylinder((ix + T_W, iy + T_W, -1), (ix + T_W, iy + T_W, T_DECKEL + 1), D_M3 / 2))
    minus(d, zylinder((ix + T_W, iy + T_W, T_DECKEL - T_KOPF), (ix + T_W, iy + T_W, T_DECKEL + 1), D_KOPF_M3 / 2))
for ix in LUEFT_DECKEL_X:
    yc = PSU_Y0 + LUEFT_Y + T_W
    minus(d, quader(ix + T_W - 1.5, ix + T_W + 1.5, yc - LUEFT_LANG / 2, yc + LUEFT_LANG / 2, -1, T_DECKEL + 1))
minus(d, quader(PSU_X0 + POTI_X + T_W - POTI_B / 2, PSU_X0 + POTI_X + T_W + POTI_B / 2, PSU_Y0 + POTI_Y0 + T_W, PSU_Y0 + POTI_Y1 + T_W, -1, T_DECKEL + 1))
a0 = T_W + LIPPE_SPIEL                                              # Lippe liegt 0,3 mm innerhalb der Wandinnenfläche
for (x0, x1, y0, y1) in ((a0, a0 + LIPPE_T, a0, W_AUSSEN - a0),                                   # links
                         (L_AUSSEN - a0 - LIPPE_T, L_AUSSEN - a0, a0, W_AUSSEN - a0),             # rechts
                         (a0, L_AUSSEN - a0, W_AUSSEN - a0 - LIPPE_T, W_AUSSEN - a0)):            # hinten
    lippe = quader(x0, x1, y0, y1, -LIPPE_H, 0.01)
    for (ix, iy) in DECKEL_DOME:                                          # um die Dome herum aussparen
        minus(lippe, zylinder((ix + T_W, iy + T_W, -LIPPE_H - 1), (ix + T_W, iy + T_W, 1), D_DOM / 2 + 0.6))
    plus(d, lippe)
c_deckel = komponente("Bau_Deckel")
einsetzen(c_deckel, "EG_Deckel", drucklage(d, [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, H_AUSSEN]]))
# Druckorientierung: Oberseite unten auf dem Bett, Lippe nach oben (180 Grad um x): y' = -y + W_AUSSEN, z' = -z + T_DECKEL
dd = drucklage(d, [[1, 0, 0, 0], [0, -1, 0, W_AUSSEN], [0, 0, -1, T_DECKEL]])
c = komponente("Druck_Deckel", (0, W_AUSSEN + 20, 0))
k2 = einsetzen(c, "EG_Deckel", dd)
exportieren(k2, "EG_Deckel")

# ================================================================ Netzblende (Zusammenbaulage: y von -T_BLENDE bis 0)
b = quader(BLENDE_X0, BLENDE_X1, -T_BLENDE, 0, BLENDE_Z0, BLENDE_Z1)
for (bx, bz) in BLENDE_SCHRAUBEN:
    minus(b, zylinder((bx, -T_BLENDE - 1, bz), (bx, 1, bz), D_M3 / 2))
minus(b, quader(C14_X - C14_B / 2, C14_X + C14_B / 2, -T_BLENDE - 1, 1, C14_Z - C14_H / 2, C14_Z + C14_H / 2))
for dx in (-C14_LOCH / 2, C14_LOCH / 2):
    minus(b, zylinder((C14_X + dx, -T_BLENDE - 1, C14_Z), (C14_X + dx, 1, C14_Z), D_M3 / 2))
    minus(b, sechskant_y(C14_X + dx, C14_Z, -MUTTER_T, 1, MUTTER_SW))
minus(b, zylinder((F1_X, -T_BLENDE - 1, F1_Z), (F1_X, 1, F1_Z), D_F1 / 2))
c_blende = komponente("Bau_Netzblende")
einsetzen(c_blende, "EG_Netzblende", b)
# Druckorientierung: Aussenfläche (y = -5) unten, x' = x, y' = -z + 57, z' = y + 5
dl = drucklage(b, [[1, 0, 0, 0], [0, 0, -1, BLENDE_Z1], [0, 1, 0, T_BLENDE]])
c = komponente("Druck_Netzblende", (0, 2 * (W_AUSSEN + 20), 0))
k3 = einsetzen(c, "EG_Netzblende", dl)
exportieren(k3, "EG_Netzblende")

# ================================================================ Klemmenabdeckung (Zusammenbaulage)
kx0, kx1 = KL_X0 - T_KL, KL_X1 + T_KL
ky0, ky1 = KL_Y0 - T_KL, KL_Y1 + T_KL_HINTEN
kz1 = KL_Z_INNEN + T_KL
h = qi(kx0, kx1, ky0, ky1, 0, kz1)
minus(h, qi(KL_X0, KL_X1, KL_Y0, KL_Y1, -1, KL_Z_INNEN))
for (y0, y1) in ((ky0 - 1, KL_Y0 + 0.01), (KL_Y1 - 0.01, ky1 + 1)):   # Kabelaustritt vorne und hinten, offen nach unten
    minus(h, qi(KL_X0, KL_X0 + KL_AUS_B, y0, y1, -1, KL_AUS_H))
for (ix, iy) in KL_LASCHEN:                                       # Laschen vorne mit Loch (liegen auf dem Boden)
    plus(h, qi(ix - LASCHE_B / 2, ix + LASCHE_B / 2, iy - LASCHE_B / 2, ky0 + 0.5, 0, LASCHE_T))
    minus(h, zylinder((ix + T_W, iy + T_W, T_B - 1), (ix + T_W, iy + T_W, T_B + LASCHE_T + 1), D_M3 / 2))
minus(h, qi(PSU_X0, PSU_X0 + PSU_L, PSU_Y0, PSU_Y0 + PSU_B, -1, PAD_H + PSU_H))   # Netzteil freischneiden, bis zum Boden
c_haube = komponente("Bau_Klemmenabdeckung")
einsetzen(c_haube, "EG_Klemmenabdeckung", h)
# Druckorientierung: Dach unten (180 Grad um x): y' = -y + W_AUSSEN, z' = -z + (T_B + kz1). Nur die zwei Laschen brauchen Stützen.
dh = drucklage(h, [[1, 0, 0, 0], [0, -1, 0, W_AUSSEN], [0, 0, -1, T_B + kz1]])
c = komponente("Druck_Klemmenabdeckung", (0, 3 * (W_AUSSEN + 20), 0))
k4 = einsetzen(c, "EG_Klemmenabdeckung", dh)
exportieren(k4, "EG_Klemmenabdeckung")

# ================================================================ Passprobe C14 (liegt in Druckorientierung: Aussenseite unten)
PC_RAND, PC_RASTER = 8.0, 32.0
pc_b = C14_LOCH + 0.4 + 2 * PC_RAND
pc_h = PC_RASTER * len(PASS_C14) + 4.0
pc = quader(0, pc_b, 0, pc_h, 0, T_BLENDE)
for i, (dm, dl) in enumerate(PASS_C14):
    yc = 2.0 + PC_RASTER * (i + 0.5)
    minus(pc, quader(pc_b / 2 - (C14_B + dm) / 2, pc_b / 2 + (C14_B + dm) / 2, yc - (C14_H + dm) / 2, yc + (C14_H + dm) / 2, -1, T_BLENDE + 1))
    for sx in (-1, 1):
        x = pc_b / 2 + sx * (C14_LOCH + dl) / 2
        minus(pc, zylinder((x, yc, -1), (x, yc, T_BLENDE + 1), D_M3 / 2))
        minus(pc, sechskant_z(x, yc, T_BLENDE - MUTTER_T, T_BLENDE + 1, MUTTER_SW))
    for k in range(i + 1):                                         # Stufe i + 1 = i + 1 Grübchen an der rechten Kante
        minus(pc, zylinder((pc_b - 3.0, yc + (k - i / 2.0) * 3.0, T_BLENDE - 0.6), (pc_b - 3.0, yc + (k - i / 2.0) * 3.0, T_BLENDE + 1), 0.8))
c = komponente("Druck_Passprobe_C14", (L_AUSSEN + 40, 0, 0))
k5 = einsetzen(c, "EG_Passprobe_C14", pc)
exportieren(k5, "EG_Passprobe_C14")

# ================================================================ Passprobe Sicherungshalter F1
PF_RASTER, PF_B = 22.0, 26.0
pf_l = PF_RASTER * len(PASS_F1) + 4.0
pf = quader(0, pf_l, 0, PF_B, 0, T_BLENDE)
for i, dd in enumerate(PASS_F1):
    xc = 2.0 + PF_RASTER * (i + 0.5)
    minus(pf, zylinder((xc, 12.0, -1), (xc, 12.0, T_BLENDE + 1), (D_F1 + dd) / 2))
    for k in range(i + 1):                                         # Stufe i + 1 = i + 1 Grübchen oberhalb der Bohrung
        minus(pf, zylinder((xc + (k - i / 2.0) * 3.0, PF_B - 2.5, T_BLENDE - 0.6), (xc + (k - i / 2.0) * 3.0, PF_B - 2.5, T_BLENDE + 1), 0.8))
c = komponente("Druck_Passprobe_F1", (L_AUSSEN + 40, 130, 0))
k6 = einsetzen(c, "EG_Passprobe_F1", pf)
exportieren(k6, "EG_Passprobe_F1")

# ================================================================ Referenzkörper (nicht gedruckt)
ref = komponente("Ref_Netzteil")
einsetzen(ref, "LRS-350", qi(PSU_X0, PSU_X0 + PSU_L, PSU_Y0, PSU_Y0 + PSU_B, PAD_H, PAD_H + PSU_H), ref=True)
ref = komponente("Ref_Arduino")
einsetzen(ref, "Uno_Shield", qi(AX0, AX0 + UNO_L, AY0, AY0 + UNO_B, H_AB, 45.0), ref=True)
einsetzen(ref, "USB_Buchse", qi(AX0 - 6.0, AX0 + 0.5, AY0 + USB_Y - 6, AY0 + USB_Y + 6, H_AB + 1.6, H_AB + 1.6 + 11.0), ref=True)
ref = komponente("Ref_Netzeingang")
einsetzen(ref, "C14", quader(C14_X - 13.5, C14_X + 13.5, -T_BLENDE - 3, 22, C14_Z - 9.5, C14_Z + 9.5), ref=True)
ref = komponente("Ref_Sicherungshalter")
einsetzen(ref, "F1", zylinder((F1_X, -T_BLENDE - 8, F1_Z), (F1_X, 25, F1_Z), 6.25), ref=True)

vp = app.activeViewport
cam = vp.camera
cam.isSmoothTransition = False
cam.target = P(L_AUSSEN / 2, W_AUSSEN / 2, 25)
cam.eye = P(L_AUSSEN / 2 + 330, -330, 330)
cam.upVector = V(0, 0, 1)
vp.camera = cam
vp.fit()
"fertig"
