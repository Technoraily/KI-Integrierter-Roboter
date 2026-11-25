"""Gestaltungsmodell V4 (NUR Form und Optik, keine Mechanik).

V4: weisse Schalen als echte Low-Poly-Körper (konvexe Hülle aus Eckpunkten, ebene
Dreiecksflächen, schräge Grate) in der Formsprache des Arctos-Arms (nur Anregung,
keine Dateien oder Masse übernommen). Gerüst wie V3.1: beidseitige Gabeln an
Schulter, Ellbogen und Handgelenk, kein Querversatz. Die weissen Schalen sind
Netzkörper (nur für die Optik); tragende Teile folgen bei der Konstruktion.

Parameter, Pose und Hilfsfunktionen kommen aus arm_gestaltung_v3.py (bis zum
Abschnitt «Aufräumen»), damit beide Fassungen dieselben Masse nutzen.

Ausführen im Fusion-Python (MCP-Add-in):
    exec(open(pfad, encoding="utf-8").read())
"""
import math
import os
import random

_ORDNER = r"C:\Claude\KI-Integrierter Roboter\cad\skripte"
_quelle = open(os.path.join(_ORDNER, "arm_gestaltung_v3.py"), encoding="utf-8").read()
exec(_quelle[:_quelle.index("# ---------------------------------------------------------------- Aufräumen")])

_FARBEN_V4 = dict(_FARBEN)


def farbe(name):  # eigene Darstellungen für V4
    voll = "AG4_" + name
    a = design.appearances.itemByName(voll)
    if a:
        return a
    lib = app.materialLibraries.itemByName("Fusion Appearance Library")
    a = design.appearances.addByCopy(lib.appearances.itemByName("Plastic - Matte (White)"), voll)
    r, g, b = _FARBEN_V4[name]
    for i in range(a.appearanceProperties.count):
        p = a.appearanceProperties.item(i)
        if isinstance(p, adsk.core.ColorProperty) and p.value:
            p.value = adsk.core.Color.create(r, g, b, 255)
            break
    return a


# ---------------------------------------------------------------- Low-Poly: konvexe Hülle und Netzkörper
def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _kreuz(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def _skalar(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def huelle(punkte):
    """Konvexe Hülle (inkrementell) einer kleinen Punktmenge (mm).
    Rückgabe (Punkte, Dreiecke), Dreiecke von aussen gegen den Uhrzeigersinn."""
    rnd = random.Random(7)
    P = [(x + rnd.uniform(-1e-3, 1e-3), y + rnd.uniform(-1e-3, 1e-3), z + rnd.uniform(-1e-3, 1e-3))
         for x, y, z in punkte]
    n = len(P)
    i0 = 0
    i1 = max(range(n), key=lambda i: _skalar(_sub(P[i], P[i0]), _sub(P[i], P[i0])))

    def flaeche(i):
        c = _kreuz(_sub(P[i1], P[i0]), _sub(P[i], P[i0]))
        return _skalar(c, c)

    i2 = max(range(n), key=flaeche)
    nrm = _kreuz(_sub(P[i1], P[i0]), _sub(P[i2], P[i0]))
    i3 = max(range(n), key=lambda i: abs(_skalar(nrm, _sub(P[i], P[i0]))))
    tet = [i0, i1, i2, i3]
    mitte = tuple(sum(P[i][k] for i in tet) / 4.0 for k in range(3))

    def ausrichten(f):
        a, b, c = f
        nn = _kreuz(_sub(P[b], P[a]), _sub(P[c], P[a]))
        return (a, b, c) if _skalar(nn, _sub(P[a], mitte)) > 0 else (a, c, b)

    flaechen = [ausrichten(f) for f in ((i0, i1, i2), (i0, i1, i3), (i0, i2, i3), (i1, i2, i3))]
    for ip in range(n):
        if ip in tet:
            continue
        p = P[ip]
        sichtbar = set()
        for f in flaechen:
            a, b, c = f
            nn = _kreuz(_sub(P[b], P[a]), _sub(P[c], P[a]))
            if _skalar(nn, _sub(p, P[a])) > 1e-6:
                sichtbar.add(f)
        if not sichtbar:
            continue
        kanten = set()
        for a, b, c in sichtbar:
            kanten.update(((a, b), (b, c), (c, a)))
        horizont = [(u, v) for (u, v) in kanten if (v, u) not in kanten]
        flaechen = [f for f in flaechen if f not in sichtbar] + [(u, v, ip) for (u, v) in horizont]
    return P, flaechen


def netz(comp, name, punkte, f="Weiss"):
    """Konvexer Volumenkörper aus der Hülle der Punkte: ein grosser Quader wird an jeder
    Flächenebene der Hülle beschnitten (Schnitt der Halbräume). Ergebnis: echter
    BRep-Körper mit ebenen Facetten (Low-Poly), gleiche Ebenen werden zusammengefasst."""
    P, F = huelle(punkte)
    ebenen = []
    for a, b, c in F:
        nn = _kreuz(_sub(P[b], P[a]), _sub(P[c], P[a]))
        l = math.sqrt(_skalar(nn, nn))
        if l < 1e-9:
            continue
        nn = (nn[0] / l, nn[1] / l, nn[2] / l)
        dd = _skalar(nn, P[a])
        # fast gleiche Ebenen zusammenfassen (verhindert Splitterflächen und Boolean-Fehler)
        if any(_skalar(nn, e[0]) > 0.995 and abs(dd - e[1]) < 1.5 for e in ebenen):
            continue
        mitte_f = tuple((P[a][k] + P[b][k] + P[c][k]) / 3.0 for k in range(3))
        ebenen.append((nn, dd, mitte_f, l))
    ebenen.sort(key=lambda e: -e[3])
    xs = [p[0] for p in P]; ys = [p[1] for p in P]; zs = [p[2] for p in P]
    c0 = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, (min(zs) + max(zs)) / 2)
    gr = max(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)) + 20.0
    obb = adsk.core.OrientedBoundingBox3D.create(P(*c0) if False else adsk.core.Point3D.create(c0[0] * MM, c0[1] * MM, c0[2] * MM),
                                                 V(1, 0, 0), V(0, 1, 0), gr * MM, gr * MM, gr * MM)
    koerper = tbm.createBox(obb)
    S = gr * 3.0
    for nn, dd, mf, _ in ebenen:
        hilf = (1.0, 0.0, 0.0) if abs(nn[0]) < 0.9 else (0.0, 1.0, 0.0)
        u = _kreuz(nn, hilf)
        lu = math.sqrt(_skalar(u, u))
        u = (u[0] / lu, u[1] / lu, u[2] / lu)
        v = _kreuz(nn, u)
        # Punkt auf der Ebene: Flächenmitte; Quadermitte S/2 nach aussen. Bei einem
        # Boolean-Fehler (fast deckungsgleiche Kanten) die Ebene minimal nach aussen schieben.
        for zug in (0.0, 0.05, 0.2):
            cm = (mf[0] + nn[0] * (S / 2 + zug), mf[1] + nn[1] * (S / 2 + zug), mf[2] + nn[2] * (S / 2 + zug))
            ob = adsk.core.OrientedBoundingBox3D.create(adsk.core.Point3D.create(cm[0] * MM, cm[1] * MM, cm[2] * MM),
                                                        V(*u), V(*v), S * MM, S * MM, S * MM)
            try:
                versuch = tbm.copy(koerper)
                tbm.booleanOperation(versuch, tbm.createBox(ob), adsk.fusion.BooleanTypes.DifferenceBooleanType)
                koerper = versuch
                break
            except Exception:
                continue
    _wartend.setdefault(comp.entityToken, (comp, []))[1].append((name, koerper, f))
    return koerper


def einziehen2(pts, d):
    cx = sum(a for a, _ in pts) / len(pts)
    cb = sum(b for _, b in pts) / len(pts)
    out = []
    for a, b in pts:
        da, db = a - cx, b - cb
        l = math.hypot(da, db) or 1.0
        k = max(l - d, 0.15 * l) / l
        out.append((cx + da * k, cb + db * k))
    return out


def _grat_punkte(umriss, s=1.0):
    cx = sum(a for a, _ in umriss) / len(umriss)
    cb = sum(b for _, b in umriss) / len(umriss)
    A = max(abs(a - cx) for a, _ in umriss)
    B = max(abs(b - cb) for _, b in umriss)
    # langer, schräger Grat aus 2 Punkten: 20 % bis 80 % der Länge, ca. 12 Grad zur Gliedachse
    return [(cx - 0.13 * B * s, cb - 0.6 * B), (cx + 0.13 * B * s, cb + 0.6 * B)]


def edelstein_seite(comp, name, umriss, y0, t, richtung, grat=2.5, f="Weiss"):
    """Einseitige Schale in der x-z-Ebene des Rahmens (umriss: Liste (x, z)), Dicke in y.
    Grundfläche bei y0, Aussenseite bei y0 + richtung * t, schräger Grat obenauf."""
    pts = [(a, y0, b) for a, b in umriss]
    pts += [(a, y0 + richtung * 0.4 * t, b) for a, b in umriss]                 # senkrechte Seitenwand
    pts += [(a, y0 + richtung * t, b) for a, b in einziehen2(umriss, 0.5 * t)]  # Fase, flache Deckfläche
    pts += [(a, y0 + richtung * (t + grat), b) for a, b in _grat_punkte(umriss)]
    return netz(comp, name, pts, f)


def edelstein_beide(comp, name, umriss, hw, fase, grat=2.5, f="Weiss"):
    """Symmetrischer Körper zwischen y = -hw und +hw mit Fasen und Graten beidseitig."""
    pts = []
    for sgn in (1, -1):
        pts += [(a, sgn * (hw - fase), b) for a, b in umriss]
        pts += [(a, sgn * hw, b) for a, b in einziehen2(umriss, fase)]
        pts += [(a, sgn * (hw + grat), b) for a, b in _grat_punkte(umriss, sgn)]
    return netz(comp, name, pts, f)


def edelstein_achse(comp, name, schnitte, f="Weiss"):
    """Körper entlang der lokalen z-Achse aus Achteck-Schnitten (z, w, h, fase)."""
    pts = []
    for z, w, h, k in schnitte:
        pts += [(x, y, z) for x, y in achteck(w, h, k)]
    return netz(comp, name, pts, f)


def kreis2(cx, cb, r, n=10, phase=0.0):
    n = 6 if n >= 10 else (5 if n >= 8 else 4)   # wenige, grosse Facetten (Arctos-Charakter)
    return [(cx + r * math.cos(phase + 2 * math.pi * i / n), cb + r * math.sin(phase + 2 * math.pi * i / n))
            for i in range(n)]


# ---------------------------------------------------------------- Aufräumen
for i in range(root.occurrences.count - 1, -1, -1):
    if root.occurrences.item(i).component.name.startswith("Arm_Gestaltung"):
        root.occurrences.item(i).deleteMe()

G = komponente(root, "Arm_Gestaltung_V4")

# ================================================================ Sockel (8-Eck), Kasten mit weisser Kappe
s = SOCKEL
so = komponente(G, "Sockel")
ph = math.pi / 8
loft(so, "Sockel", [(0, vieleck(s["r"], 8, ph)), (s["h"] - s["fase"], vieleck(s["r"], 8, ph)),
                    (s["h"], vieleck(s["r"] - s["fase"], 8, ph))], "Anthrazit")
k = KASTEN
xa, xb = k["x"] - k["t"] / 2, k["x"] + k["t"] / 2
kp = [(xb, -k["b"] / 2), (xb, k["b"] / 2), (xa + 12, k["b"] / 2), (xa, k["b"] / 2 - 12),
      (xa, -k["b"] / 2 + 12), (xa + 12, -k["b"] / 2)]
loft(so, "Elektronikkasten", [(0, kp), (s["h"] - 14, kp)], "Anthrazit")
kappe = [(x, y, s["h"] - 14) for x, y in kp]
kappe += [(x, y, s["h"] - 2) for x, y in einziehen2(kp, 6)]
kappe += [(x, y, s["h"] + 6) for x, y in einziehen2(kp, 24)]
netz(so, "Kastenkappe", kappe)
scheibe(so, "Ring_J1", (0, 0, s["h"] + RING["t"] / 2), (0, 0, 1), RING["r"], RING["t"], "Akzent")

# ================================================================ J1: Drehteller, Haube, Gabel-Wangen
j1 = komponente(G, "Drehteil_J1", (0, 0, 0), (0, 0, 1), Q1)
z_d = s["h"] + RING["t"]
d = DREH
loft(j1, "Drehteller", [(z_d, vieleck(d["r"], 12, math.pi / 12)),
                        (z_d + d["h"] - d["fase"], vieleck(d["r"], 12, math.pi / 12)),
                        (z_d + d["h"], vieleck(d["r"] - d["fase"], 12, math.pi / 12))], "Anthrazit")
hb = HAUBE
z_h = z_d + d["h"]
trapez = [(-hb["l"] / 2, z_h), (hb["l"] / 2, z_h), (hb["l_oben"] / 2, z_h + hb["h"]),
          (-hb["l_oben"] / 2, z_h + hb["h"])]
edelstein_beide(j1, "Schulterhaube", trapez, hb["b"] + 4.0, 8.0, 2.0)
w = WANGE
yi = OA_B + SPALT
L_w = H_SCHULTER - w["z_unten"]
# Weisse Wangenschale nur als kompakte Kappe um das J2-Lager (kein grosser Tropfen mehr);
# darunter bleibt die dunkle Kernplatte sichtbar.
KAPPE_W = dict(r_oben=42.0, r_unten=30.0, abstand=38.0, t=9.0, grat=2.5)
um_w = (kreis2(0, H_SCHULTER - KAPPE_W["abstand"], KAPPE_W["r_unten"], 8)
        + kreis2(0, H_SCHULTER, KAPPE_W["r_oben"], 10, math.pi / 10))
wange = ebene_komp(j1, "Wangen_Form", 0.0)
platte(wange, "Wange_Kern_L", w["r_unten"] + 3, w["r_oben"] + 3, L_w, yi, yi + 4, 0.5, "plus", "Anthrazit",
       y0=w["z_unten"])
platte(wange, "Wange_Kern_R", w["r_unten"] + 3, w["r_oben"] + 3, L_w, -yi - 4, -yi, 0.5, "minus", "Anthrazit",
       y0=w["z_unten"])
edelstein_seite(j1, "Wange_L", um_w, yi + 4, KAPPE_W["t"], 1, KAPPE_W["grat"])
edelstein_seite(j1, "Wange_R", um_w, -yi - 4, KAPPE_W["t"], -1, KAPPE_W["grat"])

# ================================================================ Oberarm J2
oa = komponente(j1, "Oberarm_J2", (0, 0, H_SCHULTER), (0, 1, 0), Q2)
o = OBERARM
# FUSS: "A" = Mechanik unverändert (Scheibe 5M 90 Z., Ø ca. 143): Fuss als flache dunkle
#       Gelenkscheibe, der weisse Oberarm beginnt erst darüber schlank.
#       "B" = letzte Stufe 5M 18:72 (Ø ca. 115) statt 18:90, Fuss kleiner (r 62), weiss.
try:
    FUSS
except NameError:
    FUSS = "B"  # Entscheid 26.11.2026
if FUSS == "A":
    oe_f = ebene_komp(oa, "Fuss_Form")
    platte(oe_f, "Oberarm_Gelenkscheibe", o["r2"], o["r2"], 0.5, -OA_B + 3, OA_B - 3, 3.0, "beide", "Anthrazit")
    edelstein_beide(oa, "Oberarm_Fuss",
                    kreis2(0, 40.0, 40.0, 8) + kreis2(0, o["l_taille"], o["r_taille"], 8), OA_B, 8.0)
else:
    edelstein_beide(oa, "Oberarm_Fuss",
                    kreis2(0, 0, 62.0, 12, math.pi / 12) + kreis2(0, o["l_taille"], o["r_taille"], 8), OA_B, 8.0)
ub_g = UA_B + SPALT
y_g = ub_g + 4 + 12
jz0, jz1 = o["joch_z"]
edelstein_beide(oa, "Oberarm_Joch", kreis2(0, jz0, o["joch_r"][0], 8) + kreis2(0, jz1, o["joch_r"][1], 8),
                y_g, 7.0, 2.0, "Anthrazit")
gz0 = o["gabel_z0"]
um_g = ([(-o["gabel_r"][0], gz0), (o["gabel_r"][0], gz0)]          # unten gerade gekappt
        + kreis2(0, L_OBERARM, o["gabel_r"][1], 12, math.pi / 12))
oe = ebene_komp(oa, "Oberarm_Form")
platte(oe, "Gabel_Kern_L", o["gabel_r"][0] + 3, o["gabel_r"][1] + 3, L_OBERARM - gz0, ub_g, ub_g + 4, 0.5, "plus",
       "Anthrazit", y0=gz0)
platte(oe, "Gabel_Kern_R", o["gabel_r"][0] + 3, o["gabel_r"][1] + 3, L_OBERARM - gz0, -ub_g - 4, -ub_g, 0.5, "minus",
       "Anthrazit", y0=gz0)
edelstein_seite(oa, "Gabel_L", um_g, ub_g + 4, 12.0, 1)
edelstein_seite(oa, "Gabel_R", um_g, -ub_g - 4, 12.0, -1)

# ================================================================ Unterarm J3, J4
ua = komponente(oa, "Unterarm_J3", (0, 0, L_OBERARM), (0, 1, 0), Q3)
u = UNTERARM
um_u = (kreis2(0, -u["rucksack_l"], u["rucksack_r"], 8) + kreis2(0, 0, u["r3"], 12, math.pi / 12)
        + kreis2(0, u["l_hinten"], u["r_hinten"], 8))
edelstein_beide(ua, "Unterarm_hinten", um_u, UA_B, 9.0, 4.0)
z_r = u["l_hinten"] + u["r_hinten"] * 0.3
scheibe(ua, "Ring_J4", (0, 0, z_r + u["ring_t"] / 2), (0, 0, 1), u["ring_r"], u["ring_t"], "Anthrazit")
j4 = komponente(ua, "Unterarm_J4", (0, 0, 0), (0, 0, 1), Q4)
(w0, h0, k0), (w1, h1, k1) = u["vorn"]
z4 = z_r + u["ring_t"]
zm = (z4 + u["vorn_z1"]) / 2
edelstein_beide(j4, "Unterarm_vorn", kreis2(z4 * 0 + 0, z4, w0 / 2, 10, math.pi / 10) + kreis2(0, u["vorn_z1"], w1 / 2, 8),
                h0 / 2, 8.0, 2.5)
hg = HANDGABEL
yi_h = hg["b_innen"] + SPALT
um_h = kreis2(0, hg["z0"], hg["r0"], 8) + kreis2(0, L_UNTERARM, hg["r1"], 10, math.pi / 10)
he = ebene_komp(j4, "Handgabel_Form")
platte(he, "Handgabel_Kern_L", hg["r0"] - 2, hg["r1"] - 2, L_UNTERARM - hg["z0"], yi_h, yi_h + 3, 0.5, "plus",
       "Anthrazit", y0=hg["z0"])
platte(he, "Handgabel_Kern_R", hg["r0"] - 2, hg["r1"] - 2, L_UNTERARM - hg["z0"], -yi_h - 3, -yi_h, 0.5, "minus",
       "Anthrazit", y0=hg["z0"])
edelstein_seite(j4, "Handgabel_L", um_h, yi_h + 3, 10.0, 1, 4.0)
edelstein_seite(j4, "Handgabel_R", um_h, -yi_h - 3, 10.0, -1, 4.0)

# ================================================================ Hand J5, Flansch J6
ha = komponente(j4, "Hand_J5", (0, 0, L_UNTERARM), (0, 1, 0), Q5)
h = HAND
bi = 2 * hg["b_innen"]
edelstein_achse(ha, "Hand", [(h["z0"], h["w"] - 8, bi - 8, h["k"]), (h["z0"] + 10, h["w"], bi, h["k"]),
                             (h["z1"] - 6, h["w"] - 4, bi - 4, h["k"]), (h["z1"], h["w"] - 12, bi - 12, h["k"] - 2)])
scheibe(ha, "Ring_Flansch", (0, 0, h["z1"] + h["ring_t"] / 2), (0, 0, 1), h["ring_r"], h["ring_t"], "Akzent")
fl = komponente(ha, "Flansch_J6", (0, 0, 0), (0, 0, 1), Q6)
scheibe(fl, "Flansch", (0, 0, (h["z1"] + h["ring_t"] + L_HAND) / 2), (0, 0, 1), h["flansch_r"],
        L_HAND - h["z1"] - h["ring_t"], "Anthrazit")

einfuegen()
"Gestaltungsmodell V4 erstellt"
