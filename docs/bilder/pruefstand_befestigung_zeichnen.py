"""Zeichnet, wie der J2-Prüfstand auf dem Grundbrett und am Tisch befestigt wird.

Aufruf:  python docs/bilder/pruefstand_befestigung_zeichnen.py
Masse in mm, entsprechen cad/skripte/j2_pruefstand.py (x/y in der Wangenebene, z quer).
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

B, H = 3150, 2600
S = 3.0  # Pixel pro mm in beiden Ansichten

WEISS, TEXT, RAND = (255, 255, 255), (30, 30, 30), (70, 76, 86)
TISCH, BRETT, WANGE, TRAEGER = (226, 214, 196), (206, 170, 120), (222, 226, 232), (170, 178, 190)
DRUCK, MOTOR, ZWINGE, SCHRAUBE, MASS = (236, 150, 60), (90, 94, 102), (36, 110, 160), (200, 40, 40), (90, 90, 90)
MESSING, LAST = (214, 176, 70), (150, 158, 170)

# Prüfstand (aus dem CAD-Skript)
UMRISS = [(-95, 0), (100, 0), (100, 145), (45, 196), (-45, 196), (-95, 150), (-95, 97), (-80, 97), (-80, 83), (-95, 83)]
TRAEGER_UNTEN = (-85, 88)          # x der unteren Querträger, 14 breit, 24 hoch
TRAEGER_OBEN = ((-85, 124), (88, 124))
O = (0, 170)                       # Abtriebsachse
W, T_WANGE = 56, 8                 # lichte Weite, Wangendicke
Z_SCHRAUBEN = (14, 42)             # Einschmelzgewinde in den unteren Querträgern
X_STELL, Z_STELL = 10, (-4, 60)    # Stellschrauben der 3M-Spannrolle ragen unten aus den Wangen
L_HEBEL = 190

# Grundbrett und Tisch
D_BRETT = 12
BRETT_X = (-108.5, 111.5)          # 220 lang, Prüfstand mittig: das Brett lässt sich für die Gegenrichtung umdrehen
BRETT_Z = (-106, 94)               # 200 breit; auf der Motorseite breiter, damit die Zwinge neben dem Motor Platz hat
TISCHKANTE = BRETT_X[1]
D_TISCH = 30

img = Image.new("RGB", (B, H), WEISS)
d = ImageDraw.Draw(img)


def schrift(groesse, fett=False):
    return ImageFont.truetype("arialbd.ttf" if fett else "arial.ttf", groesse)


F, FK, FT, FU = schrift(30), schrift(26), schrift(44, True), schrift(34, True)

# ------------------------------------------------------------ Seitenansicht
NULL_A = (1000, 1010)               # Pixel von x = 0, y = 0 (Oberkante Brett)


def a(x, y):
    return (NULL_A[0] + x * S, NULL_A[1] - y * S)


def rechteck(f, x0, y0, x1, y1, fuellung, rand=RAND, breite=3):
    p0, p1 = f(x0, y0), f(x1, y1)
    d.rectangle([min(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[0], p1[0]), max(p0[1], p1[1])], fill=fuellung, outline=rand, width=breite)


def kreis(f, x, y, r, fuellung=None, rand=RAND, breite=3):
    c = f(x, y)
    d.ellipse([c[0] - r * S, c[1] - r * S, c[0] + r * S, c[1] + r * S], fill=fuellung, outline=rand, width=breite)


def hinweis(text, ziel, ort, anker="lm", farbe=TEXT):
    """Beschriftung bei <ort> (Pixel) mit Linie zum <ziel> (Pixel)."""
    d.line([ort, ziel], fill=farbe, width=2)
    d.ellipse([ziel[0] - 5, ziel[1] - 5, ziel[0] + 5, ziel[1] + 5], fill=farbe)
    versatz = 10 if anker[0] == "l" else -10
    d.text((ort[0] + versatz, ort[1]), text, font=FK, fill=farbe, anchor=anker)


def mass_h(f, x0, x1, y, text, oben=True):
    """Waagrechte Masslinie zwischen x0 und x1 auf Höhe y (mm)."""
    p0, p1 = f(x0, y), f(x1, y)
    d.line([p0, p1], fill=MASS, width=2)
    for q in (p0, p1):
        d.line([(q[0], q[1] - 12), (q[0], q[1] + 12)], fill=MASS, width=2)
    d.text(((p0[0] + p1[0]) / 2, p0[1] + (-8 if oben else 8)), text, font=FK, fill=MASS, anchor="mb" if oben else "mt")


def mass_v(f, x, y0, y1, text, links=True):
    p0, p1 = f(x, y0), f(x, y1)
    d.line([p0, p1], fill=MASS, width=2)
    for q in (p0, p1):
        d.line([(q[0] - 12, q[1]), (q[0] + 12, q[1])], fill=MASS, width=2)
    d.text((p0[0] + (-10 if links else 10), (p0[1] + p1[1]) / 2), text, font=FK, fill=MASS, anchor="rm" if links else "lm")


d.text((60, 40), "Prüfstand J2: Befestigung auf dem Grundbrett", font=FT, fill=TEXT)
d.text((60, 120), "Seitenansicht (Hebel waagrecht nach rechts, grösste Last)", font=FU, fill=TEXT)

# Tisch, Brett
rechteck(a, -250, -D_BRETT - D_TISCH, TISCHKANTE, -D_BRETT, TISCH)
rechteck(a, BRETT_X[0], -D_BRETT, BRETT_X[1], 0, BRETT)
# Wange, Scheibe, Querträger
d.polygon([a(*q) for q in UMRISS], fill=WANGE, outline=RAND)
d.line([a(*q) for q in UMRISS] + [a(*UMRISS[0])], fill=RAND, width=3)
kreis(a, O[0], O[1], 71.6, fuellung=(244, 200, 150))
for x in TRAEGER_UNTEN:
    rechteck(a, x - 7, 0, x + 7, 24, TRAEGER)
for x, y in TRAEGER_OBEN:
    rechteck(a, x - 7, y - 12, x + 7, y + 12, TRAEGER)
# Hebel waagrecht nach rechts
kreis(a, O[0], O[1], 35, fuellung=DRUCK)
d.polygon([a(15, O[1] + 30), a(L_HEBEL, O[1] + 15), a(L_HEBEL, O[1] - 15), a(15, O[1] - 30)], fill=DRUCK, outline=RAND)
kreis(a, L_HEBEL, O[1], 15, fuellung=DRUCK)
kreis(a, L_HEBEL, O[1], 4, fuellung=WEISS)
kreis(a, O[0], O[1], 4, fuellung=RAND)
# Gewicht an kurzer Schlaufe, Unterlage
d.line([a(L_HEBEL, O[1]), a(L_HEBEL, 118)], fill=RAND, width=4)
rechteck(a, L_HEBEL - 45, -62, L_HEBEL + 45, 118, LAST)
rechteck(a, L_HEBEL - 65, -130, L_HEBEL + 65, -92, (240, 220, 150))
mass_v(a, L_HEBEL + 78, -92, -62, "höchstens 30", links=False)
# Schrauben von unten
for x in TRAEGER_UNTEN:
    p0, p1 = a(x, -D_BRETT), a(x, 11)
    d.line([p0, p1], fill=SCHRAUBE, width=7)
    d.rectangle([p0[0] - 9, p0[1] - 9, p0[0] + 9, p0[1]], fill=SCHRAUBE)
# Schraubzwinge an der Tischkante
xz = TISCHKANTE + 22
d.line([a(xz, 34), a(xz, -100)], fill=ZWINGE, width=14)
d.line([a(xz, 30), a(74, 30)], fill=ZWINGE, width=12)
d.line([a(78, 30), a(78, 0)], fill=ZWINGE, width=12)
d.line([a(xz, -92), a(74, -92)], fill=ZWINGE, width=12)
d.line([a(78, -92), a(78, -D_BRETT - D_TISCH)], fill=ZWINGE, width=8)
d.rectangle([a(68, -D_BRETT - D_TISCH)[0], a(0, -D_BRETT - D_TISCH)[1], a(88, 0)[0], a(0, -D_BRETT - D_TISCH - 5)[1]], fill=ZWINGE)

hinweis("Lasthebel", a(110, O[1] + 20), (a(110, 0)[0], a(0, 262)[1]), "lm")
hinweis("90er-Scheibe", a(-45, 225), (a(-150, 0)[0], a(0, 262)[1]), "rm")
hinweis("Wange", a(-60, 60), (a(-215, 0)[0], a(0, 100)[1]), "rm")
hinweis("oberer Querträger = Endanschlag (10 mm Spalt)", a(-85, 130), (a(-125, 0)[0], a(0, 205)[1]), "rm")
hinweis("unterer Querträger", a(-88, 12), (a(-215, 0)[0], a(0, 45)[1]), "rm")
hinweis("Grundbrett 220 × 200 × 12", a(-100, -6), (a(-215, 0)[0], a(0, -75)[1]), "rm")
hinweis("Tisch", a(-230, -30), (a(-215, 0)[0], a(0, -110)[1]), "rm")
hinweis("4× M3 × 20 von unten", a(-85, -6), (a(-60, 0)[0], a(0, -90)[1]), "lm", SCHRAUBE)
d.line([(a(-60, 0)[0], a(0, -90)[1]), a(88, -10)], fill=SCHRAUBE, width=2)
hinweis("Schraubzwinge (2 Stück)", a(xz, -70), (a(250, 0)[0], a(0, 40)[1]), "lm", ZWINGE)
hinweis("Gewicht bis 6,3 kg", a(L_HEBEL + 40, 60), (a(250, 0)[0], a(0, 90)[1]), "lm")
hinweis("kurze Schlaufe", a(L_HEBEL, 135), (a(250, 0)[0], a(0, 140)[1]), "lm")
hinweis("Unterlage oder Fangschnur", a(L_HEBEL + 60, -112), (a(270, 0)[0], a(0, -125)[1]), "lm")
mass_h(a, 0, L_HEBEL, O[1] + 62, "190")
mass_h(a, TISCHKANTE, L_HEBEL, -150, "78,5", oben=False)
d.line([a(TISCHKANTE, -D_BRETT - D_TISCH), a(TISCHKANTE, -165)], fill=MASS, width=1)
d.line([a(L_HEBEL, -130), a(L_HEBEL, -165)], fill=MASS, width=1)
mass_v(a, -110, 0, O[1], "170")

# ------------------------------------------------------------ Draufsicht
NULL_B = (1000, 1790)               # Pixel von x = 0, z = BRETT_Z[0]


def b(x, z):
    return (NULL_B[0] + x * S, NULL_B[1] + (z - BRETT_Z[0]) * S)


d.text((60, 1640), "Draufsicht (Blick von oben, Motorseite oben)", font=FU, fill=TEXT)
rechteck(b, -250, BRETT_Z[0] - 15, TISCHKANTE, BRETT_Z[1] + 15, TISCH, rand=TISCH)
d.line([b(TISCHKANTE, BRETT_Z[0] - 15), b(TISCHKANTE, BRETT_Z[1] + 15)], fill=RAND, width=4)
rechteck(b, BRETT_X[0], BRETT_Z[0], BRETT_X[1], BRETT_Z[1], BRETT)
rechteck(b, 34, -68, 94, -T_WANGE, MOTOR)
rechteck(b, -95, -T_WANGE, 100, 0, WANGE)
rechteck(b, -95, W, 100, W + T_WANGE, WANGE)
for x in TRAEGER_UNTEN:
    rechteck(b, x - 7, 0, x + 7, W, TRAEGER)
rechteck(b, 0, 20, L_HEBEL + 15, 40, DRUCK)
c = b(L_HEBEL, 30)
d.ellipse([c[0] - 45 * S, c[1] - 45 * S, c[0] + 45 * S, c[1] + 45 * S], outline=RAND, width=2)
for z in (-88, 80):
    rechteck(b, 62, z - 9, TISCHKANTE + 28, z + 9, ZWINGE, rand=ZWINGE)
for x in TRAEGER_UNTEN:
    for z in Z_SCHRAUBEN:
        q = b(x, z)
        d.ellipse([q[0] - 9, q[1] - 9, q[0] + 9, q[1] + 9], fill=SCHRAUBE)

for z in Z_STELL:
    q = b(X_STELL, z)
    d.ellipse([q[0] - 15, q[1] - 15, q[0] + 15, q[1] + 15], fill=WEISS, outline=ZWINGE, width=4)
hinweis("2 Löcher Ø 10 (Stellschrauben)", b(X_STELL, Z_STELL[1]), (b(-25, 0)[0], b(0, 80)[1]), "rm", ZWINGE)
d.line([(b(-25, 0)[0], b(0, 80)[1]), b(X_STELL, Z_STELL[0])], fill=ZWINGE, width=2)
mass_h(b, X_STELL, BRETT_X[1], BRETT_Z[0] - 30, "101,5")
d.line([b(X_STELL, BRETT_Z[0] - 30), b(X_STELL, Z_STELL[0])], fill=MASS, width=1)
xr = BRETT_X[1] + 60
mass_v(b, xr, BRETT_Z[0], Z_STELL[0], "102", links=False)
mass_v(b, xr + 45, BRETT_Z[0], Z_STELL[1], "166", links=False)
hinweis("Motor", b(64, -40), (b(-20, 0)[0], b(0, -70)[1]), "rm")
hinweis("Wange links", b(-60, -4), (b(-40, 0)[0], b(0, -40)[1]), "rm")
hinweis("Wange rechts", b(-60, 60), (b(-215, 0)[0], b(0, 75)[1]), "rm")
hinweis("Tischkante", b(TISCHKANTE, 104), (b(250, 0)[0], b(0, 104)[1]), "lm")
hinweis("Schraubzwinge", b(TISCHKANTE + 20, 80), (b(250, 0)[0], b(0, 84)[1]), "lm", ZWINGE)
hinweis("Gewicht hängt neben dem Tisch", b(L_HEBEL + 40, 50), (b(290, 0)[0], b(0, 50)[1]), "lm")
# Bohrbild im Brett
zu = BRETT_Z[1] + 34
mass_h(b, TRAEGER_UNTEN[1], BRETT_X[1], zu, "23,5", oben=False)
mass_h(b, TRAEGER_UNTEN[0], TRAEGER_UNTEN[1], zu, "173", oben=False)
mass_h(b, BRETT_X[0], TRAEGER_UNTEN[0], zu, "23,5", oben=False)
for x in TRAEGER_UNTEN:
    d.line([b(x, Z_SCHRAUBEN[1]), b(x, zu)], fill=MASS, width=1)
xl = BRETT_X[0] - 20
mass_v(b, xl, BRETT_Z[0], Z_SCHRAUBEN[0], "120")
mass_v(b, xl - 45, BRETT_Z[0], Z_SCHRAUBEN[1], "148")
for z in Z_SCHRAUBEN:
    d.line([b(xl - 45, z), b(TRAEGER_UNTEN[0], z)], fill=MASS, width=1)

# ------------------------------------------------------------ Detail Verschraubung
SD = 16.0
NULL_C = (2520, 2000)              # Pixel der Schraubenachse auf Brettoberkante


def cdet(x, y):
    return (NULL_C[0] + x * SD, NULL_C[1] - y * SD)


def rechteck_c(x0, y0, x1, y1, fuellung, rand=RAND):
    p0, p1 = cdet(x0, y1), cdet(x1, y0)
    d.rectangle([p0[0], p0[1], p1[0], p1[1]], fill=fuellung, outline=rand, width=3)


d.text((2150, 1540), "Schnitt durch eine Verschraubung", font=FU, fill=TEXT)
rechteck_c(-17, -D_BRETT - 6, 17, -D_BRETT, TISCH)
rechteck_c(-17, -D_BRETT, 17, 0, BRETT)
rechteck_c(-7, 0, 7, 22, TRAEGER)
rechteck_c(-2, 0, 2, 12, WEISS)                    # Bohrung 12 tief
rechteck_c(-2.5, 0, 2.5, 5, MESSING)               # Einschmelzgewinde
rechteck_c(-1.75, -D_BRETT, 1.75, 0, WEISS)        # Durchgang im Brett
rechteck_c(-3.25, -D_BRETT, 3.25, -D_BRETT + 3, WEISS)   # Senkung
rechteck_c(-1.5, -D_BRETT + 3, 1.5, 11, SCHRAUBE, rand=SCHRAUBE)
rechteck_c(-2.75, -D_BRETT, 2.75, -D_BRETT + 3, SCHRAUBE, rand=SCHRAUBE)
hinweis("unterer Querträger", cdet(5, 18), (cdet(9, 0)[0], cdet(0, 20)[1]), "lm")
hinweis("Einschmelzgewinde M3", cdet(2.4, 2.5), (cdet(9, 0)[0], cdet(0, 5)[1]), "lm")
hinweis("Bohrung Ø 3,5", cdet(1.75, -5), (cdet(9, 0)[0], cdet(0, -4.5)[1]), "lm")
hinweis("Senkung Ø 6,5, 3,5 tief", cdet(3.2, -10.5), (cdet(9, 0)[0], cdet(0, -9.5)[1]), "lm")
hinweis("Tisch", cdet(12, -15), (cdet(9, 0)[0], cdet(0, -16)[1]), "lm")
hinweis("M3 × 20", cdet(-1.5, 6), (cdet(-9, 0)[0], cdet(0, 12)[1]), "rm", SCHRAUBE)
hinweis("Brett 12 mm", cdet(-12, -6), (cdet(-9, 0)[0], cdet(0, 2)[1]), "rm")

# ------------------------------------------------------------ Vorgehen
schritte = [
    "Vorgehen",
    "1. Brett 220 × 200 × 12 mm zuschneiden (Sperrholz oder MDF).",
    "2. Vier Löcher Ø 3,5 nach dem Bohrbild bohren, von unten Ø 6,5",
    "    und 3,5 mm tief ansenken: Die Schraubenköpfe dürfen nicht",
    "    vorstehen, sonst wackelt das Brett auf dem Tisch.",
    "3. Zwei Löcher Ø 10 für die Stellschrauben der 3M-Spannrolle",
    "    bohren. Sie ragen unten aus den Wangen und verschwinden",
    "    im Brett.",
    "4. Prüfstand aufsetzen, 4× M3 × 20 von unten in die",
    "    Einschmelzgewinde der unteren Querträger drehen.",
    "5. 3M-Riemen spannen, solange das Brett noch frei ist",
    "    (Stellschrauben von unten durch die Löcher Ø 10).",
    "6. Brett bündig an die Tischkante legen, mit zwei Zwingen",
    "    links und rechts vom Prüfstand festspannen.",
    "7. Für die Gegenrichtung (Hebel nach links) das Brett um",
    "    180° drehen und neu spannen. Der Prüfstand sitzt mittig,",
    "    die Last hängt in beiden Lagen neben dem Tisch.",
    "",
    "Ohne Zwingen kippt der Aufbau: 6,3 kg hängen 78,5 mm",
    "ausserhalb der Tischkante.",
]
y = 190
for i, zeile in enumerate(schritte):
    d.text((2150, y), zeile, font=FU if i == 0 else F, fill=TEXT)
    y += 56 if i == 0 else 44

ziel = Path(__file__).with_name("pruefstand_befestigung.png")
img.save(ziel)
print(ziel)
