"""Zeichnet, wo die Einschmelzgewinde M3 im J2-Prüfstand sitzen (Schema, Masse aus cad/skripte/j2_pruefstand.py).

Aufruf:  python docs/bilder/einschmelz_zeichnen.py
Ergebnis: docs/bilder/einschmelz_positionen.png
Einsatz: Messing M3, Aussen-Ø 5 mm, Länge 4 mm (gelb), Bohrung Ø 4,0 mm (weiss), Schraube rot.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

B, H = 2000, 1780
WEISS, RAND, TEXT, HELL = (255, 255, 255), (60, 66, 76), (30, 30, 30), (110, 116, 126)
TEIL, TEIL2, LOCH, WELLE = (226, 231, 238), (240, 160, 70), (255, 255, 255), (150, 156, 166)
EINSATZ, EIRAND, SCHRAUBE, SRAND, ROT = (230, 190, 40), (150, 110, 10), (200, 70, 60), (120, 30, 30), (200, 60, 50)

bild = Image.new("RGB", (B, H), WEISS)
z = ImageDraw.Draw(bild)


def f(g, fett=False):
    return ImageFont.truetype("arialbd.ttf" if fett else "arial.ttf", g)


def panel(x0, y0, x1, y1, kopf, unter):
    z.rounded_rectangle((x0, y0, x1, y1), radius=14, outline=(190, 196, 206), width=2)
    z.text((x0 + 22, y0 + 14), kopf, font=f(32, True), fill=TEXT, anchor="la")
    z.text((x0 + 22, y0 + 56), unter, font=f(21), fill=HELL, anchor="la")


def rect(x0, y0, x1, y1, fill, outline=RAND, w=3):
    z.rectangle((x0, y0, x1, y1), fill=fill, outline=outline, width=w)


def loch(x0, y0, x1, y1):
    rect(x0, y0, x1, y1, LOCH, outline=HELL, w=2)


def einsatz(x0, y0, x1, y1):
    rect(x0, y0, x1, y1, EINSATZ, outline=EIRAND, w=2)


def schraube(x0, y0, x1, y1):
    rect(x0, y0, x1, y1, SCHRAUBE, outline=SRAND, w=2)


def label(text, punkt, pos, anchor="la"):
    z.line((punkt[0], punkt[1], pos[0], pos[1]), fill=ROT, width=3)
    z.ellipse((punkt[0] - 6, punkt[1] - 6, punkt[0] + 6, punkt[1] + 6), fill=ROT)
    z.multiline_text(pos, text, font=f(22), fill=TEXT, anchor=anchor, spacing=4)


def notiz(xy, text, anchor="la"):
    z.multiline_text(xy, text, font=f(20), fill=HELL, anchor=anchor, spacing=4)


z.text((B / 2, 36), "Einschmelzgewinde M3: wo sie sitzen und wie die Löcher aussehen", font=f(42, True), fill=TEXT, anchor="mm")
z.text((B / 2, 84), "gelb = Einsatz (Messing, Ø 5 × 4 mm) · weiss = Bohrung Ø 4,0 mm im Kunststoff · rot = Schraube · Schema, Tiefen nach CAD",
       font=f(23), fill=HELL, anchor="mm")

# ================================================================ A  Querträger
panel(30, 120, 990, 690, "A  Querträger (4 Stück, 16 + 4 Einsätze)", "Klotz 14 × 24 × 56 mm, hier von der Seite gesehen; 2 Einsätze an jedem Ende")
S = 7.5
x0, L, Hh = 90, 56 * S, 24 * S
y0 = 230
rect(x0, y0, x0 + L, y0 + Hh, TEIL)
for yy in (-6, 6):
    yc = y0 + Hh / 2 + yy * S
    loch(x0, yc - 2 * S, x0 + 9 * S, yc + 2 * S)
    loch(x0 + L - 9 * S, yc - 2 * S, x0 + L, yc + 2 * S)
    einsatz(x0, yc - 2.5 * S, x0 + 4 * S, yc + 2.5 * S)
    einsatz(x0 + L - 4 * S, yc - 2.5 * S, x0 + L, yc + 2.5 * S)
label("Loch 9 mm tief, Einsatz\nbündig mit der Stirnfläche", (x0 + 2 * S, y0 + Hh / 2 - 6 * S), (x0 + L + 40, y0 + 10))
notiz((x0 + L + 40, y0 + 110), "an beiden Enden gleich:\n2 Löcher, 12 mm auseinander")
y1 = 470
rect(x0, y1, x0 + L, y1 + Hh, TEIL)
for zz in (14, 42):
    xc = x0 + zz * S
    loch(xc - 2 * S, y1 + Hh - 12 * S, xc + 2 * S, y1 + Hh)
    einsatz(xc - 2.5 * S, y1 + Hh - 4 * S, xc + 2.5 * S, y1 + Hh)
label("nur die 2 unteren Träger: zusätzlich\n2 Löcher von unten, 12 mm tief\n(fürs Grundbrett, M3 × 20)", (x0 + 14 * S, y1 + Hh - 2 * S),
      (x0 + L + 40, y1 + 30))

# ================================================================ B  Z72-Nabe
panel(1010, 120, 1970, 690, "B  Scheibe Z72, Nabe (2 Einsätze)", "Schnitt entlang der Welle A: links Zahnkranz, rechts die dicke Nabe")
S = 7.0
cx, cy = 1070, 430


def zx(zm):
    return cx + (zm - 7.5) * S * 1.6


rect(zx(7.5), cy - 23 * S, zx(19.5), cy + 23 * S, TEIL2)
rect(zx(19.5), cy - 12 * S, zx(28.8), cy + 12 * S, TEIL2)
rect(zx(7.5), cy - 4 * S, zx(28.8), cy + 4 * S, WELLE, outline=RAND, w=2)
zc = zx(24.3)
loch(zc - 2 * S, cy - 12 * S, zc + 2 * S, cy - 6.5 * S)
loch(zc - 1.6 * S, cy - 6.5 * S, zc + 1.6 * S, cy - 4 * S)
einsatz(zc - 2.5 * S, cy - 12 * S, zc + 2.5 * S, cy - 8 * S)
schraube(zc - 1.5 * S, cy - 17 * S, zc + 1.5 * S, cy - 4 * S)
z.ellipse((zc - 2.5 * S, cy + 6.5 * S, zc + 2.5 * S, cy + 11.5 * S), fill=EINSATZ, outline=EIRAND, width=2)
z.ellipse((zc - 1.4 * S, cy + 7.6 * S, zc + 1.4 * S, cy + 10.4 * S), fill=LOCH, outline=EIRAND, width=2)
label("Gewindestift M3 × 10:\ndrückt auf die angefeilte\nFläche der Welle", (zc, cy - 14 * S), (zx(30) + 40, cy - 22 * S))
label("zweites Loch, 90° versetzt\n(hier von vorn gesehen)", (zc, cy + 9 * S), (zx(30) + 40, cy + 6 * S))
notiz((zx(13.5), cy + 25 * S), "Zahnkranz", "ma")
notiz((zx(24), cy + 13.5 * S), "Nabe", "ma")
notiz((zx(30) + 40, cy + 18 * S), "Loch nur 5,5 mm tief (dann Ø 3,2\nbis zur Welle): hier passen\nnur 4-mm-Einsätze", "la")

# ================================================================ C  Hebelnabe
panel(30, 710, 990, 1280, "C  Lasthebel, Nabe (1 Einsatz)", "Schnitt entlang der Abtriebswelle: links Hebelplatte, rechts Bund")
S = 7.5
cx, cy = 90, 1000


def zy(zm):
    return cx + (zm - 20) * S * 1.5


rect(zy(20), cy - 24 * S, zy(40), cy + 24 * S, TEIL2)
rect(zy(40), cy - 11 * S, zy(52), cy + 11 * S, TEIL2)
rect(zy(52), cy - 6 * S, zy(55.8), cy + 6 * S, TEIL2)
rect(zy(20), cy - 4 * S, zy(55.8), cy + 4 * S, WELLE, outline=RAND, w=2)
for yy in (-24, 24):
    z.line((zy(20), cy + yy * S, zy(40), cy + yy * S), fill=TEIL2, width=1)
zc = zy(46)
loch(zc - 2 * S, cy - 11 * S, zc + 2 * S, cy - 5.5 * S)
loch(zc - 1.6 * S, cy - 5.5 * S, zc + 1.6 * S, cy - 4 * S)
einsatz(zc - 2.5 * S, cy - 11 * S, zc + 2.5 * S, cy - 7 * S)
schraube(zc - 1.5 * S, cy - 15 * S, zc + 1.5 * S, cy - 4 * S)
label("Gewindestift M3 × 8\nauf die Abtriebswelle", (zc, cy - 13 * S), (zy(58) + 20, cy - 22 * S))
notiz((zy(58) + 20, cy + 14 * S), "Hebelplatte links (Ø 70, nur der\nmittlere Teil gezeichnet): die 6 Schrauben\nzur Z90 gehen hier ohne Einsatz durch")
notiz((zy(58) + 20, cy + 6 * S), "Loch 5,5 mm tief:\n4-mm-Einsatz")

# ================================================================ D  Wangen-Stellschrauben
panel(1010, 710, 1970, 1280, "D  Wangen: Stellschrauben der Spannrollen (4 Einsätze)", "Ansicht auf die Wange (Ausschnitt); je Rolle eine Stellschraube je Wange")
S = 9.0
px, py = 1060, 800
rect(px, py, px + 420, py + 170, TEIL)
rect(px, py + 40, px + 15 * S, py + 130, WEISS, outline=RAND)
yl = py + 85
loch(px + 15 * S, yl - 2 * S, px + 21 * S, yl + 2 * S)
einsatz(px + 15 * S, yl - 2.5 * S, px + 19 * S, yl + 2.5 * S)
loch(px + 21 * S, yl - 1.6 * S, px + 330, yl + 1.6 * S)
schraube(px + 15 * S - 40, yl - 1.5 * S, px + 19 * S, yl + 1.5 * S)
z.ellipse((px + 330, yl - 40, px + 410, yl + 40), fill=WEISS, outline=RAND, width=3)
label("5M-Rolle: Einsatz in der Nische\nan der linken Wangenkante", (px + 17 * S, yl - 8), (px + 450, py + 10))
qx, qy = 1060, 1000
rect(qx, qy, qx + 420, qy + 190, TEIL)
xc = qx + 90
loch(xc - 2 * S, qy + 190 - 6 * S, xc + 2 * S, qy + 190)
einsatz(xc - 2.5 * S, qy + 190 - 4 * S, xc + 2.5 * S, qy + 190)
loch(xc - 1.6 * S, qy + 52, xc + 1.6 * S, qy + 190 - 6 * S)
schraube(xc - 1.5 * S, qy + 190 - 4 * S, xc + 1.5 * S, qy + 190 + 45)
z.ellipse((xc - 40, qy + 12, xc + 40, qy + 92), fill=WEISS, outline=RAND, width=3)
label("3M-Rolle: Einsatz von unten\nin der unteren Wangenkante", (xc + 10, qy + 190 - 2 * S), (qx + 450, qy + 60))
notiz((px, qy + 232), "Die Wand ist nur 8 mm dick: der Einsatz (Ø 5) sitzt in der Mitte, auf jeder Seite bleiben rund 1,5 mm.\n"
      "Loch 6 mm tief: 4-mm-Einsatz, bündig mit dem Grund der Nische bzw. der Kante.")

# ================================================================ E  Wangen: übrige
panel(30, 1300, 1970, 1760, "E  Wangen: Blockierstift und Messuhrhalter (5 Einsätze)", "Löcher 7 mm tief in der 8 mm dicken Wange (Blick auf die Wange von der Seite), 1 mm Wand bleibt")
S = 14.0
wx, wy = 120, 1430
rect(wx, wy, wx + 8 * S, wy + 260, TEIL)
loch(wx, wy + 40, wx + 7 * S, wy + 40 + 4 * S)
einsatz(wx, wy + 40 + 0.75 * S, wx + 3 * S, wy + 40 + 3.25 * S)
label("Linke Wange, Innenseite:\n1 Einsatz für den Blockierstift\n(Schraube M3 × 25, nur angelegt)", (wx + S, wy + 40 + 2 * S), (wx + 8 * S + 50, wy + 30))
rect(wx + 900, wy, wx + 900 + 8 * S, wy + 260, TEIL)
for dy in (40, 150):
    loch(wx + 900 + S, wy + dy, wx + 900 + 8 * S, wy + dy + 4 * S)
    einsatz(wx + 900 + 5 * S, wy + dy + 0.75 * S, wx + 900 + 8 * S, wy + dy + 3.25 * S)
label("Rechte Wange, Aussenseite:\n4 Einsätze für den Messuhrhalter\n(je 2 hier, 2 weitere auf der anderen\nSeite der Mitte, bei x = ±56 / ±72 mm)",
      (wx + 900 + 6.5 * S, wy + 40 + 2 * S), (wx + 900 + 8 * S + 50, wy + 30))
notiz((wx, wy + 275), "Der Messuhrhalter hat zusätzlich 1 Einsatz für seine Klemmschraube (M3 × 25).")

bild.save(Path(__file__).parent / "einschmelz_positionen.png")
print(Path(__file__).parent / "einschmelz_positionen.png")
