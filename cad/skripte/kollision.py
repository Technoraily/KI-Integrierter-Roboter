# Kollisionsprüfung: alle Körperpaare unter einer Komponente (OBEN = Name) schneiden,
# Volumen der Überschneidung > GRENZE mm³ melden. Körper werden in Weltlage verglichen.
import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
root = design.rootComponent
tbm = adsk.fusion.TemporaryBRepManager.get()
try:
    GRENZE
except NameError:
    GRENZE = 1.0


def sammeln(occ, liste):
    for j in range(occ.bRepBodies.count):
        b = occ.bRepBodies.item(j)
        k = tbm.copy(b)
        tbm.transform(k, occ.transform2)
        liste.append((occ.component.name + "/" + b.name, k))
    for i in range(occ.childOccurrences.count):
        sammeln(occ.childOccurrences.item(i), liste)


oben = [root.occurrences.item(i) for i in range(root.occurrences.count)
        if root.occurrences.item(i).component.name == OBEN][0]
koerper = []
sammeln(oben, koerper)
treffer = []
for i in range(len(koerper)):
    for j in range(i + 1, len(koerper)):
        a, b = koerper[i][1], koerper[j][1]
        if not a.boundingBox.intersects(b.boundingBox):
            continue
        s = tbm.copy(a)
        try:
            tbm.booleanOperation(s, tbm.copy(b), adsk.fusion.BooleanTypes.IntersectionBooleanType)
            vol = s.volume * 1000.0
        except Exception:
            vol = -1
        if vol > GRENZE or vol < 0:
            treffer.append(f"{koerper[i][0]} x {koerper[j][0]}: {vol:.1f} mm3")
print(f"{len(koerper)} Körper, {len(treffer)} Überschneidungen")
print("\n".join(treffer))
