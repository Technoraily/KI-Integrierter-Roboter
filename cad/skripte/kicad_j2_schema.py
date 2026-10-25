"""Erzeugt das KiCad-Schema des J2-Prüfstands (docs/schema/verdrahtung-j2.md).

Aufruf: python cad/skripte/kicad_j2_schema.py
Ausgabe: cad/kicad/j2-pruefstand/j2-pruefstand.kicad_sch (+ .kicad_pro)
Masse in mm, Raster 2,54 mm. Alle Pins sind «passive», es sind einfache Kästchen-Symbole.
"""
import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "cad" / "kicad" / "j2-pruefstand"
PROJ = "j2-pruefstand"
ROOT_UUID = str(uuid.uuid5(uuid.NAMESPACE_URL, "j2/root"))
PITCH = 5.08
PIN_LEN = 5.08


def uid(key):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "j2/" + key))


def fmt(v):
    return f"{v:.3f}".rstrip("0").rstrip(".")


# name: (halbe Breite, Pins links, Pins rechts, Namen verbergen)
SYMBOLS = {
    "X1": (10.16, [], ["L", "N", "PE"], False),
    "FUSE": (5.08, ["1"], ["2"], True),
    "T1": (10.16, ["L", "N", "FG"], ["+V", "-V"], False),
    "A2": (10.16, ["VIN", "GND"], ["1B", "1A", "2A", "2B"], False),
    "M1": (10.16, ["Sp.1 a", "Sp.1 b", "Sp.2 a", "Sp.2 b"], [], False),
    "A1": (10.16, ["USB"], [], False),
    "PC": (10.16, [], ["USB"], False),
}

# Kz., Symbol, Mitte x, Mitte y, Wert
PARTS = [
    ("X1", "X1", 48.26, 68.58, "Einbaukaltstecker C14"),
    ("F1", "FUSE", 88.9, 63.5, "T 3,15 A 250 V"),
    ("T1", "T1", 127.0, 68.58, "Mean Well LRS-350-24"),
    ("F2", "FUSE", 167.64, 63.5, "Kfz 3 A"),
    ("A2", "A2", 205.74, 71.12, "CNC-Shield V3 + TMC2209 (X)"),
    ("M1", "M1", 256.54, 71.12, "NEMA 17, 60 mm"),
    ("A1", "A1", 205.74, 119.38, "Arduino Uno"),
    ("PC1", "PC", 154.94, 119.38, "PC"),
]

RED = (200, 0, 0)
BROWN = (130, 70, 0)
BLUE = (0, 70, 200)
GREEN = (0, 140, 0)
BLACK = None


def pin_rows(sym):
    half, left, right, _ = SYMBOLS[sym]
    n = max(len(left), len(right), 1)
    pins = {}
    for i, name in enumerate(left):
        pins[name] = (-(half + PIN_LEN), (n - 1 - 2 * i) * PITCH / 2, 0)
    for i, name in enumerate(right):
        pins[name] = (half + PIN_LEN, (n - 1 - 2 * i) * PITCH / 2, 180)
    return n, pins


def lib_symbol(sym):
    half, left, right, hide_names = SYMBOLS[sym]
    n, pins = pin_rows(sym)
    h = n * PITCH
    eff = "(effects (font (size 1.27 1.27)))"
    eff_h = "(effects (font (size 1.27 1.27)) (hide yes))"
    s = [f'(symbol "J2:{sym}" (pin_numbers (hide yes)) (pin_names (offset 1.016){" (hide yes)" if hide_names else ""})',
         ' (exclude_from_sim no) (in_bom yes) (on_board yes)',
         f' (property "Reference" "X" (at 0 {fmt(h / 2 + 1.8)} 0) {eff})',
         f' (property "Value" "{sym}" (at 0 {fmt(-h / 2 - 1.8)} 0) {eff})',
         f' (property "Footprint" "" (at 0 0 0) {eff_h})',
         f' (property "Datasheet" "" (at 0 0 0) {eff_h})',
         f' (symbol "{sym}_0_1" (rectangle (start {fmt(-half)} {fmt(h / 2)}) (end {fmt(half)} {fmt(-h / 2)})'
         ' (stroke (width 0.254) (type default)) (fill (type background))))',
         f' (symbol "{sym}_1_1"']
    for i, (name, (x, y, ang)) in enumerate(pins.items()):
        s.append(f'  (pin passive line (at {fmt(x)} {fmt(y)} {ang}) (length {fmt(PIN_LEN)}) '
                 f'(name "{name}" {eff}) (number "{i + 1}" {eff}))')
    s.append(' )')
    s.append(')')
    return "\n".join(s)


def pin_xy(ref, pin):
    for r, sym, cx, cy, _ in PARTS:
        if r == ref:
            _, pins = pin_rows(sym)
            x, y, _ang = pins[pin]
            return round(cx + x, 3), round(cy - y, 3)
    raise KeyError(ref)


def instance(ref, sym, cx, cy, value):
    n, pins = pin_rows(sym)
    h = n * PITCH
    eff = "(effects (font (size 1.27 1.27)))"
    eff_h = "(effects (font (size 1.27 1.27)) (hide yes))"
    s = [f'(symbol (lib_id "J2:{sym}") (at {fmt(cx)} {fmt(cy)} 0) (unit 1)',
         ' (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)',
         f' (uuid "{uid("sym/" + ref)}")',
         f' (property "Reference" "{ref}" (at {fmt(cx)} {fmt(cy - h / 2 - 1.8)} 0) {eff})',
         f' (property "Value" "{value}" (at {fmt(cx)} {fmt(cy + h / 2 + 1.8)} 0) {eff})',
         f' (property "Footprint" "" (at {fmt(cx)} {fmt(cy)} 0) {eff_h})',
         f' (property "Datasheet" "" (at {fmt(cx)} {fmt(cy)} 0) {eff_h})']
    for i in range(len(pins)):
        s.append(f' (pin "{i + 1}" (uuid "{uid(f"pin/{ref}/{i + 1}")}"))')
    s.append(f' (instances (project "{PROJ}" (path "/{ROOT_UUID}" (reference "{ref}") (unit 1))))')
    s.append(')')
    return "\n".join(s)


def wire(key, a, b, color=BLACK):
    col = f" (color {color[0]} {color[1]} {color[2]} 1)" if color else ""
    return (f'(wire (pts (xy {fmt(a[0])} {fmt(a[1])}) (xy {fmt(b[0])} {fmt(b[1])})) '
            f'(stroke (width 0.25) (type default){col}) (uuid "{uid("wire/" + key)}"))')


def text(key, x, y, t, size=1.27):
    return (f'(text "{t}" (exclude_from_sim no) (at {fmt(x)} {fmt(y)} 0) '
            f'(effects (font (size {size} {size})) (justify left)) (uuid "{uid("text/" + key)}"))')


# Leitungen aus docs/schema/verdrahtung-j2.md: Nr., von, nach, Farbe
WIRES = [
    ("W10", ("X1", "L"), ("F1", "1"), BROWN),
    ("W11", ("F1", "2"), ("T1", "L"), BROWN),
    ("W12", ("X1", "N"), ("T1", "N"), BLUE),
    ("W13", ("X1", "PE"), ("T1", "FG"), GREEN),
    ("W1", ("T1", "+V"), ("F2", "1"), RED),
    ("W2", ("F2", "2"), ("A2", "VIN"), RED),
    ("W3", ("T1", "-V"), ("A2", "GND"), BLACK),
    ("W4a", ("A2", "1B"), ("M1", "Sp.1 a"), BLACK),
    ("W4b", ("A2", "1A"), ("M1", "Sp.1 b"), BLACK),
    ("W4c", ("A2", "2A"), ("M1", "Sp.2 a"), BLACK),
    ("W4d", ("A2", "2B"), ("M1", "Sp.2 b"), BLACK),
    ("W5", ("PC1", "USB"), ("A1", "USB"), BLACK),
]

# Beschriftung: Schlüssel, x, y, Text
LABELS = [
    ("w10", 65.0, 62.0, "W10"), ("w11", 100.0, 62.0, "W11"),
    ("w12", 80.0, 67.0, "W12"), ("w13", 80.0, 72.0, "W13"),
    ("w1", 144.0, 62.0, "W1 rot"), ("w2", 179.0, 62.0, "W2 rot"),
    ("w3", 144.0, 67.0, "W3 schwarz"),
    ("w4", 223.0, 61.5, "W4 Motorkabel"),
    ("w5", 172.0, 117.5, "W5 USB"),
    ("h1", 40.0, 50.0, "230-V-SEITE (Entwurf, Opa prüft und gibt frei)"),
    ("h2", 140.0, 50.0, "24-V-SEITE (rot = +24 V, schwarz = 0 V, 1,0 mm²)"),
    ("h3", 140.0, 108.0, "PC-ANSCHLUSS (Logik; Motorstrom nur über die 24-V-Klemme)"),
    ("n1", 40.0, 150.0, "Stand 25.10.2026, Entwurf. Quelle: docs/schema/verdrahtung-j2.md"),
    ("n2", 40.0, 154.0, "Netzteil auf 24,0 V einstellen und 115/230-V-Umschalter auf 230 V, bevor das Shield angeschlossen wird."),
    ("n3", 40.0, 158.0, "Motor nie unter Spannung ein- oder ausstecken. Spulenpaare 1A/1B und 2A/2B mit Multimeter bestimmen."),
    ("n4", 40.0, 162.0, "F1 T 3,15 A reicht für den Prüfstand (ca. 30 W), nicht für den ganzen Arm (Netzteil zieht bis 3,4 A)."),
]


def build():
    lines = ['(kicad_sch (version 20250114) (generator "eeschema") (generator_version "9.0")',
             f'(uuid "{ROOT_UUID}")', '(paper "A4")',
             '(title_block (title "J2-Prüfstand: Verdrahtung") (date "2026-10-25") (rev "Entwurf")'
             ' (comment 1 "24-V-Seite und Motor; 230-V-Seite nur Entwurf"))',
             '(lib_symbols']
    lines += [lib_symbol(s) for s in SYMBOLS]
    lines.append(')')
    for key, a, b, col in WIRES:
        lines.append(wire(key, pin_xy(*a), pin_xy(*b), col))
    for ref, sym, cx, cy, val in PARTS:
        lines.append(instance(ref, sym, cx, cy, val))
    for key, x, y, t in LABELS:
        lines.append(text(key, x, y, t))
    lines.append(')')
    return "\n".join(lines) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{PROJ}.kicad_sch").write_text(build(), encoding="utf-8")
    pro = {"meta": {"filename": f"{PROJ}.kicad_pro", "version": 3}}
    (OUT / f"{PROJ}.kicad_pro").write_text(json.dumps(pro, indent=2), encoding="utf-8")
    print("geschrieben:", OUT)


if __name__ == "__main__":
    main()
