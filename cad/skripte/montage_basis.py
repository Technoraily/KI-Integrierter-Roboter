# Montageprüfung Basis J1 (nach basis_j1.py ausführen): Endzustand, Drehung ±170°,
# Einschiebewege je Montageschritt und Werkzeugzugang zu den Schrauben.
# Meldet Überschneidungen > GRENZE mm³ (gewollte Paare sind ausgenommen).
import math
import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
root = design.rootComponent
tbm = adsk.fusion.TemporaryBRepManager.get()
GRENZE = 1.0
MM = 0.1

basis = [root.occurrences.item(i) for i in range(root.occurrences.count)
         if root.occurrences.item(i).component.name == "Basis_J1"][0]
K = {}
for i in range(basis.childOccurrences.count):
    occ = basis.childOccurrences.item(i)
    if occ.component.name == "Basis_Testteile":
        continue
    for j in range(occ.bRepBodies.count):
        bd = occ.bRepBodies.item(j)
        k = tbm.copy(bd)
        tbm.transform(k, occ.transform2)
        K[bd.name] = k
DREH = {"Nabe_Drehteller"}
GEWOLLT = {frozenset(p) for p in [("Welle_8x72", "Ritzel_3M_16Z"), ("Welle_8x72", "Scheibe_GT2_80Z"),
                                  ("Motor_J1_17CS04A", "Ritzel_GT2_20Z"), ("Welle_8x72", "Distanzring_unten"),
                                  ("Welle_8x72", "Distanzring_oben"), ("Kabelweg_Platzhalter", "Grundplatte"),
                                  ("Welle_8x72", "Lager_608_oben"), ("Welle_8x72", "Lager_608_unten"),
                                  ("Nabe_Drehteller", "Endschalter_Rolle"), ("Endschalter_J1_KW11", "Endschalter_Rolle")]}


def verschoben(k, dx=0, dy=0, dz=0, rot_z=None):
    c = tbm.copy(k)
    m = adsk.core.Matrix3D.create()
    if rot_z is not None:
        m.setToRotation(math.radians(rot_z), adsk.core.Vector3D.create(0, 0, 1), adsk.core.Point3D.create(0, 0, 0))
    m.translation = adsk.core.Vector3D.create(dx * MM, dy * MM, dz * MM)
    tbm.transform(c, m)
    return c


def vol(a, b):
    if not a.boundingBox.intersects(b.boundingBox):
        return 0.0
    s = tbm.copy(a)
    try:
        tbm.booleanOperation(s, tbm.copy(b), adsk.fusion.BooleanTypes.IntersectionBooleanType)
        return s.volume * 1000.0
    except Exception:
        return -1.0


bericht = []


def pruefe(titel, bewegt, feste, schritte):
    """bewegt: Liste Namen; schritte: Liste (dx,dy,dz,rot) relativ zum Endzustand."""
    fehler = {}
    for (dx, dy, dz, rot) in schritte:
        for nb in bewegt:
            kb = verschoben(K[nb], dx, dy, dz, rot)
            for nf in feste:
                if nf in bewegt or frozenset((nb, nf)) in GEWOLLT:
                    continue
                v = vol(kb, K[nf])
                if v > GRENZE or v < 0:
                    key = f"{nb} x {nf}"
                    fehler[key] = max(fehler.get(key, 0), v)
    bericht.append(f"{titel}: " + ("ok" if not fehler else "; ".join(f"{k} {v:.0f} mm3" for k, v in fehler.items())))


alle = list(K.keys())
schalen = ["Sockelgehaeuse_links", "Sockelgehaeuse_rechts", "Farbring_J1_links", "Farbring_J1_rechts", "Kastenkappe"]
# 1 Endzustand
pruefe("1 Endzustand", [n for n in alle], alle, [(0, 0, 0, None)]) if False else None
fehler = []
for i in range(len(alle)):
    for j in range(i + 1, len(alle)):
        if frozenset((alle[i], alle[j])) in GEWOLLT:
            continue
        v = vol(K[alle[i]], K[alle[j]])
        if v > GRENZE or v < 0:
            fehler.append(f"{alle[i]} x {alle[j]} {v:.0f} mm3")
bericht.append("1 Endzustand: " + ("ok" if not fehler else "; ".join(fehler)))
# 2 Drehung ±170° (Nabe gegen alles Feste inkl. Kabel)
fest_alle = [n for n in alle if n not in DREH and n != "Endschalter_Rolle"]
pruefe("2 Drehung J1 -170..+170", list(DREH), fest_alle, [(0, 0, 0, w) for w in range(-170, 171, 10)])
# 2b Anschlag: bei ±176° muss der Mitnehmer den Finger treffen
anschlag = []
for w in (176, -176):
    anschlag.append(vol(verschoben(K["Nabe_Drehteller"], rot_z=w), K["Grundplatte"]))
bericht.append(f"2b Anschlag bei ±176° greift: {['ja' if v > 1 else 'NEIN' for v in anschlag]}")
# 3 Montagewege
hub_set = ["Grundplatte", "Motorkasten", "Bock_unten", "Lager_608_unten", "Kopf_Holz_0", "Kopf_Holz_1", "Kopf_Holz_2",
           "Kopf_Holz_3", "Kopf_Holz_4", "Kopf_Holz_5", "Kopf_Holz_6", "Kopf_Holz_7"]
pruefe("3a 6810 unten von unten in die Nabe", ["Lager_6810_unten"], ["Nabe_Drehteller"], [(0, 0, -d, None) for d in range(2, 40, 2)])
pruefe("3b Nabe + 6810 unten von oben auf den Zapfen", ["Nabe_Drehteller", "Lager_6810_unten"], hub_set,
       [(0, 0, d, None) for d in range(2, 90, 3)])
pruefe("3c 6810 oben von oben", ["Lager_6810_oben"], ["Nabe_Drehteller", "Grundplatte"], [(0, 0, d, None) for d in range(1, 30, 2)])
nach_nabe = hub_set + ["Nabe_Drehteller", "Lager_6810_unten", "Lager_6810_oben", "Spannring"]
weg_deckel = [(-d, 0, 10.5, None) for d in range(60, -1, -4)] + [(0, 0, d, None) for d in (10.5, 8, 6, 4, 2)]
pruefe("3d Bock-Deckel: 10,5 mm hoch von hinten einschieben, dann absenken", ["Bock_Deckel", "Lager_608_oben"], nach_nabe, weg_deckel)
pruefe("3e Welle von oben (durch den Deckel)", ["Welle_8x72"], nach_nabe + ["Bock_Deckel", "Lager_608_oben"],
       [(0, 0, d, None) for d in range(2, 90, 3)])
mit_bock = nach_nabe + ["Welle_8x72", "Bock_Deckel", "Lager_608_oben", "Scheibe_GT2_80Z", "Ritzel_3M_16Z", "Distanzring_oben"]
pruefe("3f Motor + Platte von oben", ["Motorplatte", "Motor_J1_17CS04A", "Ritzel_GT2_20Z"], mit_bock, [(0, 0, d, None) for d in range(2, 60, 3)])
pruefe("3g Endschalter auf Halter von vorne (+x) einschieben", ["Endschalter_J1_KW11", "Schalterhalter"], mit_bock,
       [(d, 0, 0, None) for d in range(2, 40, 2)])
innen = mit_bock + ["Motorplatte", "Motor_J1_17CS04A", "Ritzel_GT2_20Z", "Endschalter_J1_KW11", "Schalterhalter", "Steckerfeld_Platzhalter",
                    "Riemen_3M_318_15", "Riemen_GT2_240_10", "Kabelweg_Platzhalter"]
for seite, sy in (("links", 1), ("rechts", -1)):
    weg = [(0, 0, d, None) for d in range(1, 5)] + [(3, sy * d, 4, None) for d in range(2, 110, 4)]
    pruefe(f"3h Gehäuse {seite}: 4 mm heben, 3 mm vor, seitlich weg", [f"Sockelgehaeuse_{seite}"], innen, weg)
# 4 Werkzeugzugang (Inbus Ø 6 senkrecht bis z 250) im Zustand vor dem Schalenaufsetzen
zugang_fest = [n for n in innen if not n.startswith("Kopf_") and n != "Kabelweg_Platzhalter"]
fehl = []
for name in [n for n in alle if n.startswith("Kopf_") and n not in ("Kopf_Spannschraube", "Kopf_Halterschraube")]:
    kb = K[name].boundingBox
    cx = (kb.minPoint.x + kb.maxPoint.x) / 2 / MM
    cy = (kb.minPoint.y + kb.maxPoint.y) / 2 / MM
    z0 = kb.maxPoint.z / MM + 0.2
    if name.startswith("Kopf_Holz"):
        menge = ["Grundplatte", "Motorkasten"]          # vor der Nabe montiert
    else:
        menge = zugang_fest
    stab = tbm.createCylinderOrCone(adsk.core.Point3D.create(cx * MM, cy * MM, z0 * MM), 3.0 * MM,
                                    adsk.core.Point3D.create(cx * MM, cy * MM, 250 * MM), 3.0 * MM)
    for nf in menge:
        v = vol(stab, K[nf])
        if v > GRENZE:
            fehl.append(f"{name} -> {nf} {v:.0f} mm3")
kb = K["Kopf_Spannschraube"].boundingBox
x0 = kb.minPoint.x / MM - 0.2
yc, zc = (kb.minPoint.y + kb.maxPoint.y) / 2, (kb.minPoint.z + kb.maxPoint.z) / 2
stab = tbm.createCylinderOrCone(adsk.core.Point3D.create(x0 * MM, yc, zc), 3.0 * MM,
                                adsk.core.Point3D.create((x0 - 14) * MM, yc, zc), 3.0 * MM)
for nf in zugang_fest:
    v = vol(stab, K[nf])
    if v > GRENZE:
        fehl.append(f"Spannschraube (Winkelschlüssel 14 mm) -> {nf} {v:.0f} mm3")
kb = K["Kopf_Halterschraube"].boundingBox
x0 = kb.maxPoint.x / MM + 0.2
yc, zc = (kb.minPoint.y + kb.maxPoint.y) / 2, (kb.minPoint.z + kb.maxPoint.z) / 2
stab = tbm.createCylinderOrCone(adsk.core.Point3D.create(x0 * MM, yc, zc), 3.0 * MM,
                                adsk.core.Point3D.create((x0 + 12) * MM, yc, zc), 3.0 * MM)
for nf in zugang_fest:
    v = vol(stab, K[nf])
    if v > GRENZE:
        fehl.append(f"Halterschraube (waagrecht 12 mm) -> {nf} {v:.0f} mm3")
bericht.append("4 Werkzeugzugang: " + ("ok" if not fehl else "; ".join(fehl)))
# 5 Wand um jedes Einschmelzgewinde: Ring r 2,0 … 3,2 um die Bohrung muss voll Material sein
try:
    EINSAETZE
except NameError:
    EINSAETZE = []
wand = []
for teil, x0, y0, z0, x1, y1, z1 in EINSAETZE:
    p0 = adsk.core.Point3D.create(x0 * MM, y0 * MM, z0 * MM)
    p1 = adsk.core.Point3D.create(x1 * MM, y1 * MM, z1 * MM)
    huelle_ = tbm.createCylinderOrCone(p0, 3.2 * MM, p1, 3.2 * MM)
    tbm.booleanOperation(huelle_, tbm.createCylinderOrCone(p0, 2.05 * MM, p1, 2.05 * MM), adsk.fusion.BooleanTypes.DifferenceBooleanType)
    tbm.booleanOperation(huelle_, tbm.copy(K[teil]), adsk.fusion.BooleanTypes.DifferenceBooleanType)
    v = huelle_.volume * 1000.0
    if v > 0.5:
        wand.append(f"{teil} ({x0:.1f}/{y0:.1f}/{z0:.1f}): {v:.1f} mm3 fehlende Wand")
bericht.append(f"5 Wand um {len(EINSAETZE)} Einsätze: " + ("ok" if not wand else "; ".join(wand)))
print("\n".join(bericht))
