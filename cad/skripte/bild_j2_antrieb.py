# Erklärbild J2-Antrieb Variante B (5M 18:72, 3M 16:80, GT2 20:72 = 72:1). Pillow, Masse in mm.
import math
from PIL import Image, ImageDraw, ImageFont

S = 2.6                     # px pro mm
W, H = 2100, 960
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/arial.ttf", s)
FB = lambda s: ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", s)
OX, OY = 420, 40            # Bildpunkt von x=0, z=290


def p(x, z):
    return OX + x * S, OY + (290 - z) * S


def kreis(x, z, r, fill=None, outline="black", w=3):
    a, b = p(x - r, z + r), p(x + r, z - r)
    d.ellipse([a, b], fill=fill, outline=outline, width=w)


def riemen(a, b, farbe, w):
    (x1, z1, r1), (x2, z2, r2) = a, b
    dx, dz = x2 - x1, z2 - z1
    L = math.hypot(dx, dz)
    ux, uz = dx / L, dz / L
    for s in (1, -1):
        g = math.asin((r1 - r2) / L) * s
        # äussere Tangente
        nx = -uz * math.cos(g) * s - ux * math.sin(g)
        nz = ux * math.cos(g) * s - uz * math.sin(g)
        nx, nz = (-uz * s, ux * s)
        k = (r1 - r2) / L
        tx = nx * math.sqrt(1 - k * k) + ux * k
        tz = nz * math.sqrt(1 - k * k) + uz * k
        d.line([p(x1 + tx * r1, z1 + tz * r1), p(x2 + tx * r2, z2 + tz * r2)], fill=farbe, width=w)
    kreis(x1, z1, r1, outline=farbe, w=w)
    kreis(x2, z2, r2, outline=farbe, w=w)


def text(x, z, t, f=None, farbe="black", anker="la"):
    d.text(p(x, z), t, font=f or F(30), fill=farbe, anchor=anker)


# Wellen (mm): J2, Zwischenwelle, Vorgelegewelle, Motor
J2 = (0, 200); ZW = (0, 110); VW = (-62, 118); MO = (-62, 68)
r5g, r5k = 72 * 5 / math.pi / 2, 18 * 5 / math.pi / 2
r3g, r3k = 80 * 3 / math.pi / 2, 16 * 3 / math.pi / 2
r2g, r2k = 72 * 2 / math.pi / 2, 20 * 2 / math.pi / 2

# Arm (Silhouette, hellgrau) am J2
kreis(*J2, 62, fill=(235, 235, 235), outline=(170, 170, 170), w=2)
d.polygon([p(-44, 200 + 90), p(44, 200 + 90), p(52, 200 + 30), p(-52, 200 + 30)], fill=(235, 235, 235))
text(0, 262, "Oberarm", F(30), (120, 120, 120), "mm")

# Motor + Bremse
mx, mz = MO
d.rectangle([p(mx - 21, mz + 21), p(mx + 21, mz - 21)], fill=(60, 60, 60))
text(mx, mz - 26, "Motor", FB(26), "black", "mt")

riemen((MO[0], MO[1], r2k), (VW[0], VW[1], r2g), (40, 110, 200), 4)          # Stufe 1 GT2
riemen((VW[0], VW[1], r3k), (ZW[0], ZW[1], r3g), (30, 150, 70), 6)           # Stufe 2 3M
riemen((ZW[0], ZW[1], r5k), (J2[0], J2[1], r5g), (196, 64, 60), 10)          # Stufe 3 5M 25 mm
for x, z in (J2, ZW, VW, MO):
    kreis(x, z, 3.5, fill="black")

text(J2[0] + 5, J2[1] + 5, "J2", FB(30))
text(ZW[0] + 5, ZW[1] - 3, "Z", FB(26)); text(VW[0] - 5, VW[1] + 5, "V", FB(26), anker="rs")
LX, LY = 760, 60
zeilen = [("Ablauf von unten nach oben:", FB(30), "black"),
          ("1. Motor (unten, Bremse dahinter)", F(27), "black"),
          ("2. Stufe 1: GT2-Riemen 20 : 72  (3,6-fach) auf Welle V", F(27), (40, 110, 200)),
          ("3. Stufe 2: 3M-Riemen 16 : 80  (5-fach) auf Welle Z", F(27), (30, 150, 70)),
          ("4. Stufe 3: 5M-Riemen 25 mm, 18 : 72  (4-fach) auf J2", F(27), (196, 64, 60)),
          ("    Scheibe 72 Zähne, Ø 115, fest am Oberarm", F(27), (196, 64, 60)),
          ("", F(10), "black"),
          ("3,6 × 5 × 4 = 72 : 1  (wie bisher)", FB(30), "black"),
          ("Motor, Wellen V und Z liegen in der Schulter", F(25), (90, 90, 90)),
          ("(dreht mit J1). Im Oberarm steckt nur die rote Scheibe.", F(25), (90, 90, 90))]
for i, (t, f, c) in enumerate(zeilen):
    d.text((LX, LY + i * 42), t, font=f, fill=c)

# Unten rechts: Grössenvergleich (Massstab gleich wie links)
d.text((760, 520), "Grösse der letzten Scheibe (gleicher Massstab):", font=FB(28), fill="black")
for i, (dm, t1, t2, col) in enumerate([
        (143, "18 : 90 Prüfstand", "15 mm, gemessen", (150, 150, 150)),
        (115, "18 : 72 GEWÄHLT", "25 mm, Steifigk. ≈ gleich", (196, 64, 60)),
        (95, "15 : 60 noch kleiner", "Riemen am Limit, ~25 % weicher", (90, 90, 90))]):
    r = dm / 2 * S * 0.75
    cx, cy = 900 + i * 430, 700
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=5)
    d.text((cx, cy - 18), f"Ø {dm}", font=FB(30), fill=col, anchor="mm")
    d.text((cx, 700 + 143 / 2 * S * 0.75 + 30), t1, font=F(25), fill=col, anchor="mm")
    d.text((cx, 700 + 143 / 2 * S * 0.75 + 65), t2, font=F(21), fill=col, anchor="mm")

img.save("C:/Claude/KI-Integrierter Roboter/cad/renders/j2_antrieb_variante_b.png")
print("ok")
