"""Erzeugt den QElectroTech-Stromlaufplan des J2-Prüfstands (docs/schema/verdrahtung-j2.md).

Aufruf: python cad/skripte/qet_j2_schema.py
Ausgabe: cad/qet/j2-pruefstand.qet
Alle Symbole sind selbst gezeichnet und im Plan eingebettet. Masse in QET-Pixeln (Raster 10).
"""
import uuid
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

OUT = Path(__file__).resolve().parents[2] / "cad" / "qet" / "j2-pruefstand.qet"
STYLE = "line-style:normal;line-weight:normal;filling:none;color:black"
FONT = "Liberation Sans,{},-1,5,50,0,0,0,0,0,Regular"
ORI = {"n": 0, "e": 1, "s": 2, "w": 3}
DOCK = {"n": (0, 4), "e": (-4, 0), "s": (0, -4), "w": (4, 0)}  # Andockpunkt liegt 4 px im Element


def U(key):
    return "{" + str(uuid.uuid5(uuid.NAMESPACE_URL, "j2qet/" + key)) + "}"


class Elem:
    """Eine Symbol-Definition; prims = Zeichenelemente, terms = [(Name, x, y, Richtung)]."""

    def __init__(self, name, w, h, title):
        self.name, self.w, self.h, self.title = name, w, h, title
        self.prims, self.terms = [], []

    def rect(self, x, y, w, h):
        self.prims.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" style="{STYLE}" antialias="false"/>')

    def line(self, x1, y1, x2, y2):
        self.prims.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" length1="1.5" length2="1.5" '
                          f'end1="none" end2="none" style="{STYLE}" antialias="false"/>')

    def circle(self, x, y, w, h):
        self.prims.append(f'<ellipse x="{x}" y="{y}" width="{w}" height="{h}" style="{STYLE}" antialias="true"/>')

    def text(self, t, x, y, size=6):
        self.prims.append(f'<text text={quoteattr(t)} x="{x}" y="{y}" rotation="0" '
                          f'font="{FONT.format(size)}" color="#000000"/>')

    def term(self, name, x, y, d):
        self.terms.append((name, x, y, d))

    def xml(self):
        t = [f'<terminal uuid="{U(self.name + "/" + n)}" name={quoteattr(n)} x="{x}" y="{y}" orientation="{d}" type="Generic"/>'
             for n, x, y, d in self.terms]
        body = "\n".join("        " + p for p in self.prims + t)
        return (f'<element name="{self.name}.elmt">\n'
                f'<definition version="0.100.0" type="element" link_type="simple" width="{self.w}" height="{self.h}" '
                f'hotspot_x="{self.w // 2}" hotspot_y="{self.h // 2}">\n'
                f'    <uuid uuid="{U("def/" + self.name)}"/>\n'
                f'    <names><name lang="de">{escape(self.title)}</name><name lang="en">{escape(self.title)}</name></names>\n'
                f'    <informations>J2-Prüfstand, erzeugt aus cad/skripte/qet_j2_schema.py</informations>\n'
                f'    <description>\n{body}\n    </description>\n</definition>\n</element>')


def build_elements():
    el = {}

    e = Elem("netzeingang", 160, 100, "Einbaukaltstecker C14")
    e.rect(-60, -20, 120, 40)
    e.text("X1 Einbaukaltstecker C14", -60, -38, 8)
    e.text("230 V AC", -56, -16, 7)
    for n, x in (("L", -30), ("N", 0), ("PE", 30)):
        e.text(n, x - 3, 4, 7)
        e.term(n, x, 20, "s")
    el["X1"] = e

    e = Elem("sicherung_230", 100, 80, "Feinsicherung T 3,15 A")
    e.rect(-6, -15, 12, 30)
    e.line(0, -15, 0, 15)
    e.text("F1", -76, -14, 8)
    e.text("T 3,15 A 250 V", -76, -3, 7)
    e.text("5 x 20 mm, träge", -76, 8, 7)
    e.term("1", 0, -20, "n")
    e.term("2", 0, 20, "s")
    el["F1"] = e

    e = Elem("netzteil", 200, 160, "Netzteil Mean Well LRS-350-24")
    e.rect(-70, -50, 140, 100)
    e.line(70, -50, -70, 50)
    e.text("~", -62, -42, 14)
    e.text("=", 44, 18, 14)
    for n, x in (("L", -30), ("N", 0), ("FG", 30)):
        e.text(n, x - 5, -46, 7)
        e.term(n, x, -50, "n")
    e.text("+V", 46, -26, 7)
    e.text("-V", 46, 14, 7)
    e.term("+V", 70, -20, "e")
    e.term("-V", 70, 20, "e")
    e.text("T1 Mean Well LRS-350-24", -70, 56, 8)
    e.text("24 V / 14,6 A, Umschalter auf 230 V!", -70, 68, 7)
    el["T1"] = e

    e = Elem("sicherung_24", 100, 80, "Kfz-Flachsicherung 3 A")
    e.rect(-15, -6, 30, 12)
    e.line(-15, 0, 15, 0)
    e.text("F2", -6, -24, 8)
    e.text("Kfz-Sicherung 3 A", -38, 18, 7)
    e.term("1", -20, 0, "w")
    e.term("2", 20, 0, "e")
    el["F2"] = e

    e = Elem("shield", 220, 160, "CNC-Shield mit TMC2209")
    e.rect(-90, -50, 180, 100)
    e.text("A2 CNC-Shield V3 + U1 TMC2209 (X)", -90, -68, 8)
    for n, y in (("VIN", -20), ("GND", 20)):
        e.text(n, -84, y - 5, 7)
        e.term(n, -90, y, "w")
    for n, y in (("1B", -30), ("1A", -10), ("2A", 10), ("2B", 30)):
        e.text(n, 66, y - 5, 7)
        e.term(n, 90, y, "e")
    el["A2"] = e

    e = Elem("motor", 120, 160, "Schrittmotor NEMA 17")
    e.rect(-30, -45, 90, 90)
    e.circle(18, -14, 28, 28)
    e.text("M", 28, -9, 10)
    e.text("M1 NEMA 17, 60 mm", -30, -62, 8)
    for n, y in (("Sp.1 a", -30), ("Sp.1 b", -10), ("Sp.2 a", 10), ("Sp.2 b", 30)):
        e.text(n, -27, y - 5, 7)
        e.term(n, -30, y, "w")
    el["M1"] = e

    e = Elem("pc", 120, 80, "PC")
    e.rect(-40, -20, 80, 40)
    e.text("PC1  PC", -34, -6, 7)
    e.term("USB", 40, 0, "e")
    el["PC1"] = e

    e = Elem("arduino", 140, 80, "Arduino Uno")
    e.rect(-50, -25, 100, 50)
    e.text("A1 Arduino Uno", -44, -6, 7)
    e.term("USB", -50, 0, "w")
    el["A1"] = e
    return el


# Kz., Symbol, Mitte x, Mitte y
PLACE = [("X1", 200, 90), ("F1", 170, 200), ("T1", 200, 360), ("F2", 360, 340),
         ("A2", 580, 360), ("M1", 800, 360), ("PC1", 400, 500), ("A1", 580, 500)]

# Nr., (Kz., Klemme), (Kz., Klemme), Leitungsfarbe (Kurzzeichen), Linienfarbe, Querschnitt
WIRES = [
    ("W10", ("X1", "L"), ("F1", "1"), "BN", "#823c00", ""),
    ("W11", ("F1", "2"), ("T1", "L"), "BN", "#823c00", ""),
    ("W12", ("X1", "N"), ("T1", "N"), "BU", "#0046c8", ""),
    ("W13", ("X1", "PE"), ("T1", "FG"), "GNYE", "#008c00", ""),
    ("W1", ("T1", "+V"), ("F2", "1"), "RD", "#c80000", "1 mm²"),
    ("W2", ("F2", "2"), ("A2", "VIN"), "RD", "#c80000", "1 mm²"),
    ("W3", ("T1", "-V"), ("A2", "GND"), "BK", "#000000", "1 mm²"),
    ("W4a", ("A2", "1B"), ("M1", "Sp.1 a"), "", "#000000", ""),
    ("W4b", ("A2", "1A"), ("M1", "Sp.1 b"), "", "#000000", ""),
    ("W4c", ("A2", "2A"), ("M1", "Sp.2 a"), "", "#000000", ""),
    ("W4d", ("A2", "2B"), ("M1", "Sp.2 b"), "", "#000000", ""),
    ("W5", ("PC1", "USB"), ("A1", "USB"), "", "#000000", ""),
]

# Beschriftungen, die sich sonst überdecken (N- und PE-Leitung sind gleich lang): feste Lage im Plan
LABEL_POS = {"W12": (203, 150), "W13": (233, 175)}

TEXTS = [
    (60, 24, 10, "230-V-SEITE (Entwurf, Elektriker prüft und gibt frei)"),
    (310, 255, 10, "24-V-SEITE (rot = +24 V, schwarz = 0 V, Litze 1,0 mm²)"),
    (310, 440, 10, "PC-ANSCHLUSS (Logik). Motorstrom nur über die 24-V-Klemme."),
    (60, 570, 8, "Quelle: docs/schema/verdrahtung-j2.md, Stand 25.10.2026, Entwurf."),
    (60, 585, 8, "Netzteil vor dem Anschluss des Shields auf 24,0 V einstellen. Motor nie unter Spannung ein- oder ausstecken."),
]


def build():
    elements = build_elements()
    tid = 0
    term_id = {}
    inst = []
    for ref, cx, cy in PLACE:
        e = elements[ref]
        ts = []
        for n, x, y, d in e.terms:
            dx, dy = DOCK[d]
            ts.append(f'<terminal y="{y + dy}" x="{x + dx}" name="" orientation="{ORI[d]}" id="{tid}" number="" nameHidden="0"/>')
            term_id[(ref, n)] = tid
            tid += 1
        inst.append(
            f'<element freezeLabel="false" z="10" y="{cy}" x="{cx}" prefix="" '
            f'type="embed://import/j2/{e.name}.elmt" orientation="0" uuid="{U("inst/" + ref)}">\n'
            f'  <terminals>{"".join(ts)}</terminals>\n  <inputs/>\n'
            f'  <elementInformations><elementInformation show="1" name="label">{ref}</elementInformation></elementInformations>\n'
            f'  <dynamic_texts/>\n  <texts_groups/>\n</element>')
    cond = []
    for num, a, b, code, col, sec in WIRES:
        tx, ty = LABEL_POS.get(num, (0, 0))
        cond.append(
            f'<conductor x="{tx}" y="{ty}" terminal1="{term_id[a]}" terminal2="{term_id[b]}" type="multi" '
            f'num="{num}" displaytext="1" conductor_color="{code}" conductor_section="{sec}" '
            f'color="{col}" color2="#000000" text_color="#000000" bicolor="false" condsize="2" cable="" bus="" '
            f'function="" formula="" tension_protocol="" onetextperfolio="0" vertical-alignment="AlignRight" '
            f'horizontal-alignment="AlignBottom" horizrotatetext="0" vertirotatetext="0" numsize="9" dash-size="1" '
            f'freezeLabel="false">\n  <sequentialNumbers/>\n</conductor>')
    texts = [f'<input x="{x}" y="{y}" rotation="0" font="{FONT.format(s)}" text={quoteattr(t)}/>' for x, y, s, t in TEXTS]
    coll = "\n".join(e.xml() for e in elements.values())
    return (
        '<project title="J2-Pruefstand Stromlaufplan" version="0.100.0">\n'
        '<properties/>\n'
        '<newdiagrams>\n'
        '  <border rowsize="80" rows="8" displaycols="true" cols="17" colsize="60" displayrows="true"/>\n'
        '  <inset displayAt="bottom" folio="%id/%total" indexrev="" plant="" date="null" filename="" author="" '
        'locmach="" title="" version="" auto_page_num=""/>\n'
        '</newdiagrams>\n'
        '<diagram freezeNewElement="false" cols="17" folio="%id/%total" version="0.100.0" indexrev="" date="null" '
        'author="" height="640" freezeNewConductor="false" title="J2-Pruefstand: Stromlaufplan (Entwurf)" '
        'auto_page_num="" displaycols="true" filename="" colsize="60" order="1" displayrows="true" locmach="" '
        'rows="8" plant="" rowsize="80" displayAt="bottom">\n'
        '<defaultconductor condsize="1" cable="" onetextperfolio="0" vertical-alignment="AlignRight" horizrotatetext="0" '
        'bicolor="false" bus="" dash-size="1" numsize="9" horizontal-alignment="AlignBottom" function="" '
        'conductor_color="" conductor_section="" text_color="#000000" color2="#000000" tension_protocol="" '
        'displaytext="0" formula="" vertirotatetext="0" num="" type="multi"/>\n'
        '<elements>\n' + "\n".join(inst) + '\n</elements>\n'
        '<conductors>\n' + "\n".join(cond) + '\n</conductors>\n'
        '<inputs>\n' + "\n".join(texts) + '\n</inputs>\n'
        '</diagram>\n'
        '<collection>\n<category name="import">\n<names><name lang="en">Imported elements</name></names>\n'
        '<category name="j2">\n<names><name lang="de">J2-Pruefstand</name></names>\n'
        + coll + '\n</category>\n</category>\n</collection>\n</project>\n')


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print("geschrieben:", OUT)


if __name__ == "__main__":
    main()
