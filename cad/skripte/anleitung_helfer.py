import adsk.core, adsk.fusion, os
J = design.rootComponent.occurrences.itemByName('J2_Pruefstand:1')
OCC = {o.name.split(':')[0]: o for o in J.component.occurrences}
# Karte Teilname -> (occurrence, body-Index oder None)
BODY = {}
for n, o in OCC.items():
    for i in range(o.bRepBodies.count):
        BODY[o.bRepBodies.item(i).name] = o.bRepBodies.item(i)
ORIG = {}
def sichern():
    if ORIG: return
    for n, b in BODY.items():
        ORIG[n] = (b.appearance, b.opacity, b.isLightBulbOn)
    for n, o in OCC.items():
        ORIG['occ:'+n] = o.isLightBulbOn
def wiederherstellen():
    for n, b in BODY.items():
        a, op, v = ORIG[n]
        b.appearance = a; b.opacity = op; b.isLightBulbOn = v
    for n, o in OCC.items():
        o.isLightBulbOn = ORIG['occ:'+n]
_FARBEN = {}
def farbe(name, rgb):
    if name in _FARBEN: return _FARBEN[name]
    base = list(BODY.values())[0].appearance
    ap = design.appearances.itemByName(name)
    if not ap:
        ap = design.appearances.addByCopy(base, name)
    for pid in ('opaque_albedo', 'surface_albedo'):
        p = ap.appearanceProperties.itemById(pid)
        if p:
            try:
                p.value = adsk.core.Color.create(rgb[0], rgb[1], rgb[2], 255)
            except: pass
    _FARBEN[name] = ap
    return ap
def zeige(teile_grau, teile_neu, versatz=None):
    """teile_*: Liste von Koerpernamen. Alles andere wird ausgeblendet."""
    sichern()
    for o in OCC.values(): o.isLightBulbOn = True
    grau = farbe('Anl_Grau', (190, 196, 205)); neu = farbe('Anl_Neu', (255, 120, 0))
    for n, b in BODY.items():
        sichtbar = n in teile_grau or n in teile_neu
        b.isLightBulbOn = sichtbar
        b.opacity = 1.0
        if n in teile_grau: b.appearance = grau
        if n in teile_neu: b.appearance = neu
def kamera(ex=(0,0,0), eye=(0,0,0), ziel=(0,0,0), breite=34.0):
    vp = app.activeViewport
    c = vp.camera
    c.isSmoothTransition = False
    c.cameraType = adsk.core.CameraTypes.OrthographicCameraType
    c.target = adsk.core.Point3D.create(*ziel)
    c.eye = adsk.core.Point3D.create(*eye)
    c.upVector = adsk.core.Vector3D.create(0, 1, 0)
    c.setExtents(breite, breite*0.75)
    vp.camera = c
def bild(datei, w=1600, h=1200):
    app.activeViewport.refresh()
    return app.activeViewport.saveAsImageFile(datei, w, h)
