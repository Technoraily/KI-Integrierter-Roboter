"""Zeichnet das Verdrahtungsbild für den Motorprüfstand (Schema, nicht massstäblich).

Aufruf:  python docs/bauanleitung/quellen/motorpruefstand/verdrahtung_zeichnen.py
Ergebnis: bilder/08_verdrahtung.png neben diesem Skript.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

B, H = 1800, 980
GRAU, WEISS, RAND = (222, 226, 232), (255, 255, 255), (70, 76, 86)
MOTOR, NETZ = (240, 160, 70), (255, 243, 214)
ROT, BLAU, GRUEN, SCHWARZ = (200, 60, 50), (50, 100, 200), (46, 139, 87), (30, 30, 30)
TEXT, HELL = (30, 30, 30), (80, 80, 80)

bild = Image.new("RGB", (B, H), "white")
z = ImageDraw.Draw(bild)


def schrift(groesse, fett=False):
    return ImageFont.truetype("arialbd.ttf" if fett else "arial.ttf", groesse)


def kasten(x0, y0, x1, y1, farbe, text=None, groesse=24, fett=True):
    z.rounded_rectangle((x0, y0, x1, y1), radius=14, fill=farbe, outline=RAND, width=3)
    if text:
        z.multiline_text(((x0 + x1) / 2, (y0 + y1) / 2), text, font=schrift(groesse, fett), fill=TEXT,
                         anchor="mm", align="center", spacing=6)


def leitung(punkte, farbe, breite=6):
    z.line(punkte, fill=farbe, width=breite, joint="curve")


z.text((B / 2, 40), "Motorprüfstand: Verdrahtung (Schema)", font=schrift(40, True), fill=TEXT, anchor="mm")

# Bausteine
kasten(40, 120, 330, 290, GRAU, "PC\nG-Code-Sender\n(UGS oder Candle)", 24)
kasten(480, 110, 1080, 640, GRAU)
z.multiline_text((780, 145), "Arduino Uno mit GRBL\n+ CNC-Shield obendrauf", font=schrift(26, True), fill=TEXT,
                 anchor="ma", align="center")
kasten(540, 300, 760, 500, WEISS, "A4988\nSteckplatz X", 24)
z.multiline_text((650, 290), "Poti: Vref für 1,0 A", font=schrift(20), fill=HELL, anchor="md")
z.multiline_text((650, 515), "darunter alle 3 Jumper\nstecken (1/16-Schritt)", font=schrift(20), fill=HELL,
                 anchor="ma", align="center")
kasten(850, 320, 1010, 460, WEISS, "Motor-\nstecker X\n(4 Pins)", 20, False)
kasten(830, 540, 1060, 620, WEISS, "Schraubklemme\n+  /  −", 20, False)
kasten(1250, 700, 1700, 830, NETZ, "Netzteil 12 V / 4 A", 30)
kasten(1340, 250, 1720, 480, MOTOR, "NEMA 17\n17CS04A-170E\nim Prüfstand", 28)

# USB
leitung([(330, 205), (480, 205)], SCHWARZ)
z.text((405, 190), "USB", font=schrift(22, True), fill=TEXT, anchor="md")

# Motorkabel, vier Adern
for i, f in enumerate((ROT, BLAU, GRUEN, SCHWARZ)):
    y = 345 + i * 30
    leitung([(1010, y), (1180, y), (1340, 300 + i * 40)], f, 5)
z.multiline_text((1225, 520), "Motorkabel, 4 Adern\n(je 2 Adern = eine Wicklung)", font=schrift(21), fill=TEXT,
                 anchor="mm", align="center")

# Versorgung
leitung([(1060, 565), (1180, 565), (1180, 740), (1250, 740)], ROT)
leitung([(1060, 600), (1140, 600), (1140, 790), (1250, 790)], SCHWARZ)
z.text((1200, 655), "+", font=schrift(40, True), fill=ROT, anchor="mm")
z.text((1112, 650), "−", font=schrift(40, True), fill=SCHWARZ, anchor="mm")

# Hinweise
hinweise = [
    "1  Alles nur OHNE Strom stecken. Den Motorstecker nie unter Spannung ziehen: das zerstört den A4988.",
    "2  Plus und Minus am Netzteil vor dem ersten Einschalten prüfen.",
    "3  A4988 richtig herum einsetzen: nach Aufdruck auf Shield und Treiber (Pin EN zu EN).",
    "4  Vref zwischen Poti und GND messen. Für 1,0 A: R100 → 0,80 V, R050 → 0,40 V, R200 → 1,60 V.",
]
for i, t in enumerate(hinweise):
    z.text((40, 710 + i * 58), t, font=schrift(21), fill=TEXT)

ziel = Path(__file__).parent / "bilder" / "08_verdrahtung.png"
bild.save(ziel)
print(ziel)
