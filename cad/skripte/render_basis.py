# Renders der Basis J1. Vorher RENDER = [(dateiname, auge(x,y,z mm), ziel, schalen_sichtbar, arm_sichtbar)] setzen.
import adsk.core, adsk.fusion
app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
root = design.rootComponent
ORD = r"C:\Claude\KI-Integrierter Roboter\cad\renders"


def occ_suchen(name, eltern=None):
    eltern = eltern or root
    for i in range(eltern.occurrences.count):
        o = eltern.occurrences.item(i)
        if o.component.name == name:
            return o
    return None


basis = occ_suchen("Basis_J1")
arm = occ_suchen("Arm_Gestaltung_V4")
for datei, auge, ziel, schalen, arm_an in RENDER:
    if arm:
        arm.isLightBulbOn = arm_an
    for i in range(basis.childOccurrences.count):
        o = basis.childOccurrences.item(i)
        if o.component.name == "Basis_Schalen":
            o.isLightBulbOn = schalen
        if o.component.name == "Basis_fest":
            for j in range(o.component.bRepBodies.count):
                b = o.component.bRepBodies.item(j)
                if b.name == "Motorkasten":
                    b.isLightBulbOn = schalen
    vp = app.activeViewport
    cam = vp.camera
    cam.eye = adsk.core.Point3D.create(*(v * 0.1 for v in auge))
    cam.target = adsk.core.Point3D.create(*(v * 0.1 for v in ziel))
    cam.upVector = adsk.core.Vector3D.create(0, 0, 1)
    cam.isFitView = True
    vp.camera = cam
    vp.fit()
    vp.saveAsImageFile(ORD + "\\" + datei, 1600, 1100)
print("ok")
