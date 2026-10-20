"""Zeichnet den Aufbau der drei Wellen des J2-Prüfstands (z-Lage der Teile, Schema).

Aufruf:  python docs/bauanleitung/quellen/j2_pruefstand/wellen_zeichnen.py
Ergebnis: bilder/wellen.png neben diesem Skript.
Masse = z-Lagen aus cad/skripte/j2_pruefstand.py (z = 0 innere Fläche der linken Wange, 56 = innere Fläche der rechten).
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HIER = Path(__file__).parent
(HIER / "bilder").mkdir(exist_ok=True)

B, H = 2000, 1000
X0, S = 150, 25.0          # Pixel links, Pixel pro mm
Z_MIN = -8.0
WEISS, RAND, TEXT = (255, 255, 255), (60, 66, 76), (30, 30, 30)
WANGE, LAGER, WELLE = (200, 204, 210), (120, 128, 140), (150, 156, 166)
DRUCK, KAUF, RING = (240, 160, 70), (170, 185, 205), (250, 215, 150)

bild = Image.new("RGB", (B, H), WEISS)
z = ImageDraw.Draw(bild)


def schrift(g, fett=False):
    return ImageFont.truetype("arialbd.ttf" if fett else "arial.ttf", g)


def px(zmm):
    return X0 + (zmm - Z_MIN) * S


def balken(y, z0, z1, farbe, h=70, text=None, klein=False):
    z.rectangle((px(z0), y - h / 2, px(z1), y + h / 2), fill=farbe, outline=RAND, width=2)
    if text:
        z.text(((px(z0) + px(z1)) / 2, y), text, font=schrift(17 if klein else 20), fill=TEXT, anchor="mm")


z.text((B / 2, 38), "J2-Prüfstand: Aufbau der drei Wellen (Schnitt längs der Welle, Schema)",
       font=schrift(36, True), fill=TEXT, anchor="mm")

# Wangen als senkrechte Bänder
for z0, z1, name in ((-8, 0, "linke Wange\n(Motorseite)"), (56, 64, "rechte Wange")):
    z.rectangle((px(z0), 90, px(z1), 930), fill=WANGE, outline=RAND, width=2)
    z.multiline_text(((px(z0) + px(z1)) / 2, 80), name, font=schrift(18, True), fill=TEXT, anchor="md", align="center")
z.text((px(0), 945), "z = 0", font=schrift(18), fill=TEXT, anchor="mt")
z.text((px(56), 945), "z = 56", font=schrift(18), fill=TEXT, anchor="mt")

reihen = [
    ("Welle A  (Stufe 1 → 2)", 230, -7, 63, [
        (-7, 0, KAUF, "Lager 608"), (0.2, 7.4, RING, "Dist. A links"), (7.5, 19.5, DRUCK, "Z72 Zahnkranz"),
        (19.5, 28.8, DRUCK, "Nabe"), (29, 53.5, KAUF, "Ritzel 3M 16 Z"), (53.6, 55.8, RING, "Dist."),
        (56, 63, KAUF, "Lager 608")]),
    ("Welle B  (Stufe 2 → 3)", 520, -7, 63, [
        (-7, 0, KAUF, "Lager 608"), (0.2, 2, RING, ""), (2, 29.5, KAUF, "Ritzel 5M 18 Z mit Nabe"),
        (30, 46.5, DRUCK, "Z64 Zahnkranz"), (46.6, 55.8, RING, "Dist. B rechts"), (56, 63, KAUF, "Lager 608")]),
    ("Abtriebswelle O  (Stufe 3)", 810, -7, 63, [
        (-7, 0, KAUF, "Lager 608"), (0.2, 3.5, RING, ""), (3.5, 20, DRUCK, "Z90 Zahnkranz"),
        (20, 40, DRUCK, "Lasthebel"), (40, 55.8, DRUCK, "Nabenbund"), (56, 63, KAUF, "Lager 608")]),
]
for titel, y, w0, w1, teile in reihen:
    z.text((px(1), y - 68), titel, font=schrift(26, True), fill=TEXT, anchor="ls")
    z.rectangle((px(w0), y - 9, px(w1), y + 9), fill=WELLE, outline=RAND, width=2)
    for z0, z1, farbe, text in teile:
        balken(y, z0, z1, farbe, 70 if farbe != RING else 50, text, klein=(z1 - z0) < 12)

# Spannrollen-Hinweise und Legende
legende = [(KAUF, "Kaufteil"), (DRUCK, "Druckteil (PETG/PLA)"), (RING, "Distanzring (gedruckt)"), (WELLE, "Stahlwelle 8 mm, 70 mm")]
for i, (f, t) in enumerate(legende):
    x = 150 + i * 460
    z.rectangle((x, 975, x + 34, 995), fill=f, outline=RAND, width=2)
    z.text((x + 44, 985), t, font=schrift(20), fill=TEXT, anchor="lm")
z.text((px(28), 890), "Alle Masse in mm. Die Welle schliesst links bündig mit der Aussenfläche des Lagers ab (z = −7).\n"
       "Scheiben und Ritzel nehmen die Welle über Gewindestifte auf angefeilten Flächen mit.",
       font=schrift(21), fill=TEXT, anchor="ma", spacing=6, align="center")

bild.save(HIER / "bilder" / "wellen.png")
print(HIER / "bilder" / "wellen.png")
