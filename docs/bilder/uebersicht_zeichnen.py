"""Zeichnet die Übersichtsskizze des Roboters (Seitenansicht) nach uebersicht.png.

Aufruf:  python docs/bilder/uebersicht_zeichnen.py
Masse in mm, entsprechen docs/parameter.md.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

B, H = 2400, 1250
MASSSTAB = 2.0  # Pixel pro mm
NULL = (860, 1010)  # Pixel der Schlittenoberkante unter der J1-Achse

GRAU, DUNKEL, RAND = (222, 226, 232), (150, 158, 170), (70, 76, 86)
MOTOR, RIEMEN, SCHIENE = (240, 160, 70), (36, 110, 160), (120, 170, 120)
TEXT = (30, 30, 30)


def px(x, z):
    return (NULL[0] + x * MASSSTAB, NULL[1] - z * MASSSTAB)


def schrift(groesse, fett=False):
    return ImageFont.truetype("arialbd.ttf" if fett else "arial.ttf", groesse)


def punkt(start, winkel_grad, laenge):
    """Punkt in <laenge> mm Abstand; Winkel ab der Senkrechten, im Uhrzeigersinn."""
    w = math.radians(winkel_grad)
    return (start[0] + laenge * math.sin(w), start[1] + laenge * math.cos(w))


bild = Image.new("RGB", (B, H), "white")
z = ImageDraw.Draw(bild)


def balken(a, b, breite, farbe=GRAU):
    z.line([px(*a), px(*b)], fill=RAND, width=int(breite * MASSSTAB) + 6)
    z.line([px(*a), px(*b)], fill=farbe, width=int(breite * MASSSTAB))
    for p in (a, b):
        kreis(p, breite / 2, farbe)


def kreis(mitte, radius, farbe, rand=RAND, dicke=3):
    x, y = px(*mitte)
    r = radius * MASSSTAB
    z.ellipse([x - r, y - r, x + r, y + r], fill=farbe, outline=rand, width=dicke)


def kasten(mitte, breite, hoehe, farbe, text=None):
    x, y = px(*mitte)
    b, h = breite * MASSSTAB / 2, hoehe * MASSSTAB / 2
    z.rounded_rectangle([x - b, y - h, x + b, y + h], radius=8, fill=farbe, outline=RAND, width=3)
    if text:
        z.text((x, y), text, font=schrift(22, True), fill=TEXT, anchor="mm")


def bogen(mitte, radius, von, bis, farbe, dicke=7):
    """Bogen; Winkel wie bei punkt() ab der Senkrechten im Uhrzeigersinn."""
    x, y = px(*mitte)
    r = radius * MASSSTAB
    z.arc([x - r, y - r, x + r, y + r], start=von - 90, end=bis - 90, fill=farbe, width=dicke)


# --- Geometrie der gezeichneten Stellung ---
S = (0, 170)  # Schulterachse J2
E = punkt(S, 25, 200)  # Ellbogen J3
W = punkt(E, 100, 190)  # Handgelenkmitte J5
F = punkt(W, 150, 60)  # Flansch
G = punkt(F, 150, 75)  # Greiferspitze

# --- Tisch und Schiene (J0) ---
z.line([px(-400, -62), px(440, -62)], fill=RAND, width=4)
z.rectangle([*px(-300, -22), *px(400, -60)], fill=(205, 210, 216), outline=RAND, width=3)  # Aluprofil
z.rectangle([*px(-280, -12), *px(380, -22)], fill=SCHIENE, outline=RAND, width=2)  # Linearführung
kasten((-330, -30), 46, 46, MOTOR, "M0")
kreis((-296, -6), 7, RIEMEN)
kreis((392, -6), 7, RIEMEN)
z.line([px(-296, 1), px(392, 1)], fill=RIEMEN, width=5)
z.line([px(-296, -13), px(392, -13)], fill=RIEMEN, width=5)
z.rectangle([*px(-80, -3), *px(-48, -22)], fill=DUNKEL, outline=RAND, width=2)  # Führungswagen
z.rectangle([*px(48, -3), *px(80, -22)], fill=DUNKEL, outline=RAND, width=2)
z.rectangle([*px(-105, 8), *px(105, -3)], fill=GRAU, outline=RAND, width=3)  # Schlittenplatte

# --- Basis (J1) ---
z.polygon([px(-78, 8), px(78, 8), px(62, 100), px(-62, 100)], fill=GRAU, outline=RAND, width=3)
kasten((-30, 48), 42, 42, MOTOR, "M1")
kreis((28, 60), 20, "white", RIEMEN, 5)  # grosses Riemenrad J1
z.line([px(-22, 70), px(28, 80)], fill=RIEMEN, width=5)
z.line([px(-22, 30), px(28, 40)], fill=RIEMEN, width=5)

# --- Drehturm mit Schulter (J2) ---
z.polygon([px(-58, 104), px(58, 104), px(48, 150), px(-48, 150)], fill=GRAU, outline=RAND, width=3)
kasten((-74, 150), 42, 60, MOTOR, "M2")

# --- Arm ---
balken(S, E, 46)
balken(E, W, 40)
balken(W, F, 30)
z.line([px(*punkt(S, 25, 62)), px(*punkt(S, 25, 176))], fill=RIEMEN, width=5)
kasten(punkt(S, 25, 62), 36, 36, MOTOR, "M3")
kasten(punkt(E, 100, 44), 34, 34, MOTOR, "M4")
kasten(punkt(E, 100, 92), 30, 30, MOTOR, "M5")
z.line([px(*punkt(E, 100, 108)), px(*punkt(E, 100, 186))], fill=RIEMEN, width=5)
kasten(punkt(W, 150, 26), 24, 24, MOTOR, "M6")

# Gelenke und Seiltriebe
kreis(S, 40, "white")
bogen(S, 40, -75, 125, RIEMEN)
kreis(punkt(S, 205, 47), 7, MOTOR)  # Ritzel der Endstufe J2
kreis(S, 6, RAND)
kreis(E, 28, "white")
bogen(E, 28, -40, 190, RIEMEN)
kreis(punkt(E, 250, 34), 6, MOTOR)  # Ritzel der Endstufe J3
kreis(E, 5, RAND)
kreis(W, 15, "white")
kreis(W, 4, RAND)

# Flansch und Greifer
quer = (math.cos(math.radians(150)), -math.sin(math.radians(150)))
for seite in (-1, 1):
    a = (F[0] + seite * 20 * quer[0], F[1] + seite * 20 * quer[1])
    b = (G[0] + seite * 14 * quer[0], G[1] + seite * 14 * quer[1])
    z.line([px(*a), px(*b)], fill=RAND, width=14)
    z.line([px(*a), px(*b)], fill=DUNKEL, width=8)
z.line([px(F[0] - 24 * quer[0], F[1] - 24 * quer[1]), px(F[0] + 24 * quer[0], F[1] + 24 * quer[1])],
       fill=RAND, width=12)

# --- Beschriftung rechts mit Hinweislinien ---
z.text((B / 2, 44), "Roboterarm: Aufbau und Antriebe (Seitenansicht, Schema)",
       font=schrift(40, True), fill=TEXT, anchor="mm")

zeilen = [
    (E, "J3  Ellbogen", "M3: NEMA 17 nahe der Schulter · GT2 + HTD-3M + HTD-5M, 60:1"),
    (punkt(E, 100, 60), "J4  Unterarm drehen", "M4: NEMA 17 · GT2 + HTD-3M, 20:1"),
    (W, "J5  Hand nicken", "M5: NEMA 17 (34 mm) im Unterarm · GT2 + HTD-3M, 18,75:1"),
    (punkt(W, 150, 40), "J6  Flansch drehen", "M6: NEMA 14 · GT2 zweistufig, 8:1"),
    (G, "Greifer am Normflansch", "ISO 9409, später Wechselsystem und Kamera"),
    (S, "J2  Schulter", "M2: NEMA 17 (60 mm) · GT2 + HTD-3M + HTD-5M, 72:1"),
    ((40, 60), "J1  Basis drehen", "M1: NEMA 17 · GT2 + HTD-3M, 20:1"),
    ((250, -6), "J0  Schiene", "M0: NEMA 17 · GT2 offen, zwei Linearführungen"),
]
x_text = 1700
for i, (ziel, titel, detail) in enumerate(zeilen):
    y = 140 + i * 128
    zx, zy = px(*ziel)
    z.line([(zx, zy), (x_text - 60, y + 14), (x_text - 14, y + 14)], fill=(110, 110, 110), width=2)
    z.ellipse([zx - 6, zy - 6, zx + 6, zy + 6], fill=(110, 110, 110))
    z.text((x_text, y), titel, font=schrift(28, True), fill=TEXT)
    z.text((x_text, y + 36), detail, font=schrift(21), fill=(70, 70, 70))

# --- Legende und Masse links ---
legende = [(GRAU, "Druckteile (PLA / PETG)"), (MOTOR, "Motor / Ritzel"),
           (RIEMEN, "Zahnriemen (GT2 / HTD)"), (SCHIENE, "Linearführung")]
for i, (farbe, name) in enumerate(legende):
    y = 130 + i * 42
    z.rounded_rectangle([50, y, 96, y + 26], radius=5, fill=farbe, outline=RAND, width=2)
    z.text((112, y - 1), name, font=schrift(23), fill=TEXT)
masse = ["Schulterhöhe 170 mm", "Oberarm 200 mm", "Unterarm 190 mm", "Hand 60 mm",
         "Reichweite 450 mm", "Nutzlast 1 kg"]
for i, text in enumerate(masse):
    z.text((50, 380 + i * 34), text, font=schrift(23), fill=(70, 70, 70))

ziel = Path(__file__).with_name("uebersicht.png")
bild.save(ziel)
print(ziel)
