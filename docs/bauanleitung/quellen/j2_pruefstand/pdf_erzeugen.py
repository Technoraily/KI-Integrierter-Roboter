"""Erzeugt die Bauanleitung des J2-Prüfstands als eine PDF-Datei.

Aufruf:  python docs/bauanleitung/quellen/j2_pruefstand/pdf_erzeugen.py
Ergebnis: docs/bauanleitung/Bauanleitung_J2_Pruefstand.pdf
Text steht hier im Skript. Bilder: cad/renders/J2_Pruefstand_*.png (Fusion), docs/bilder/pruefstand_befestigung.png,
bilder/wellen.png (wellen_zeichnen.py). Masse und Teile: cad/skripte/j2_pruefstand.py, docs/pruefstand-j2.md,
docs/stuecklisten/pruefstand-j2.md, cad/export/stl/J2_Pruefstand/Druckeinstellungen.md.
Braucht: pip install reportlab pillow
"""

from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, ListFlowable, ListItem, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

HIER = Path(__file__).parent
BILDER = HIER / "bilder"
REPO = HIER.parents[3]
ZIEL = HIER.parents[1] / "Bauanleitung_J2_Pruefstand.pdf"
STAND = "20.10.2026"

pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", "ariali.ttf"))
pdfmetrics.registerFont(TTFont("Arial-BoldItalic", "arialbi.ttf"))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic",
                              boldItalic="Arial-BoldItalic")

BLAU = colors.HexColor("#2a5d8f")
GRAU = colors.HexColor("#e8ecf1")
WARN = colors.HexColor("#fff1e0")

TEXT = ParagraphStyle("Text", fontName="Arial", fontSize=10.5, leading=14.5, spaceAfter=5)
KLEIN = ParagraphStyle("Klein", parent=TEXT, fontSize=9, leading=12, textColor=colors.HexColor("#555555"))
TITEL = ParagraphStyle("Titel", parent=TEXT, fontName="Arial-Bold", fontSize=24, leading=29,
                       textColor=BLAU, spaceAfter=6)
UNTERTITEL = ParagraphStyle("Untertitel", parent=TEXT, fontSize=13, leading=17, spaceAfter=14)
H1 = ParagraphStyle("H1", parent=TEXT, fontName="Arial-Bold", fontSize=15, leading=19, textColor=BLAU,
                    spaceBefore=12, spaceAfter=6)
ZELLE = ParagraphStyle("Zelle", parent=TEXT, fontSize=9.5, leading=12.5, spaceAfter=0)
ZELLE_FETT = ParagraphStyle("ZelleFett", parent=ZELLE, fontName="Arial-Bold")
BILDTEXT = ParagraphStyle("Bildtext", parent=KLEIN, alignment=TA_CENTER, spaceAfter=8)
BREITE = A4[0] - 40 * mm


def bild(datei, breite=BREITE, max_hoehe=105 * mm, text=None):
    w, h = PILImage.open(datei).size
    b = breite
    hoehe = b * h / w
    if hoehe > max_hoehe:
        hoehe, b = max_hoehe, max_hoehe * w / h
    teile = [Image(str(datei), width=b, height=hoehe)]
    if text:
        teile.append(Paragraph(text, BILDTEXT))
    return KeepTogether(teile)


def tabelle(zeilen, spalten):
    daten = [[Paragraph(z, ZELLE_FETT if i == 0 else ZELLE) for z in zeile] for i, zeile in enumerate(zeilen)]
    t = Table(daten, colWidths=[BREITE * s for s in spalten], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GRAU),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b8c0cc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def kasten(text):
    t = Table([[Paragraph(text, TEXT)]], colWidths=[BREITE])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), WARN),
                           ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#e0a050")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return t


def liste(punkte, nummeriert=True):
    return ListFlowable([ListItem(Paragraph(p, TEXT), leftIndent=14) for p in punkte],
                        bulletType="1" if nummeriert else "bullet", bulletFontName="Arial",
                        bulletFontSize=10, leftIndent=14, start=1 if nummeriert else None)


def fusszeile(canvas, doc):
    canvas.saveState()
    canvas.setFont("Arial", 8.5)
    canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawString(20 * mm, 12 * mm, f"Bauanleitung J2-Prüfstand – Stand {STAND}")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"Seite {doc.page}")
    canvas.restoreState()


RENDER = REPO / "cad/renders"

s = []

# ---------------------------------------------------------------- Titel
s += [Paragraph("Bauanleitung J2-Prüfstand", TITEL),
      Paragraph("Schultergelenk in Originalgrösse mit drei Riemenstufen (72:1) – misst Umkehrspiel, Steifigkeit, "
                "Kriechen und Erwärmung", UNTERTITEL),
      bild(RENDER / "J2_Pruefstand_iso.png", max_hoehe=100 * mm,
           text="Fertiger Prüfstand: zwei Wangen, Lasthebel, Messuhrhalter; Motor aussen an der linken Wange"),
      Paragraph(
          "Der Prüfstand zeigt, bevor der Arm konstruiert wird, ob die Riemenstufen das Moment von 11,8 Nm ohne "
          "zu viel Spiel und Nachgiebigkeit übertragen. Diese Anleitung beschreibt den Aufbau. Die Messungen "
          "(Umkehrspiel, Steifigkeit, Haltetest, Rücklauf) stehen in <b>docs/pruefstand-j2.md</b>; alle Teile und "
          "Preise in <b>docs/stuecklisten/pruefstand-j2.md</b>.", TEXT),
      Spacer(1, 4),
      tabelle([
          ["Stufe", "Riemen", "Übersetzung", "Wo"],
          ["1", "GT2, 10 mm breit, 200 mm", "Ritzel 20 Z → Scheibe 72 Z", "Motor → Welle A"],
          ["2", "HTD-3M, 15 mm, 252 mm", "Ritzel 16 Z → Scheibe 64 Z", "Welle A → Welle B"],
          ["3", "HTD-5M, 15 mm, 525 mm", "Ritzel 18 Z → Scheibe 90 Z", "Welle B → Abtrieb O mit Lasthebel"],
      ], (0.10, 0.30, 0.34, 0.26)),
      PageBreak()]

# ---------------------------------------------------------------- Überblick
s += [Paragraph("Was du brauchst", H1),
      tabelle([
          ["Gruppe", "Teil", "Menge"],
          ["Druckteile", "22 Teile, STL in <b>cad/export/stl/J2_Pruefstand/</b> (je ca. 0,4 kg PETG und PLA)", "22"],
          ["Riemen, Ritzel", "Ritzel GT2 20 Z, HTD-3M 16 Z, HTD-5M 18 Z (alle mit Nabe und Bordscheiben); drei "
                             "geschlossene Riemen", "3 + 3"],
          ["Lager, Wellen", "Rillenkugellager 608 · Stahlwelle 8 mm auf 70 mm · Sechskantschraube M8 × 90 mit Schaft, "
                            "Mutter M8 selbstsichernd, 2 Scheiben je Schraube", "10 · 3 · 2"],
          ["Schrauben", "M3 × 8 (1), × 10 (2), × 12 (4), × 16 (26), × 20 (4), × 25 (4), × 30 (2); M4 × 16 (2)", "45"],
          ["Einschmelzgewinde", "M3, Messing, Ø 5 × 4 mm", "41"],
          ["Antrieb", "NEMA 17, 60 mm, TMC2209 mit Kühlkörper, Arduino Uno mit CNC-Shield, Netzteil 24 V (oder "
                      "12 V für Messungen im Stillstand)", "–"],
          ["Messen", "Messuhr 0,01 mm (Schaft Ø 8 mm) mit Stativ, Kofferwaage, Gewichte 1,07 / 5,9 / 6,3 kg, "
                     "Multimeter, Schieblehre", "–"],
          ["Aufstellung", "Brett 220 × 200 × 12 mm, 2 Schraubzwingen (Spannweite ab 60 mm), weiche Unterlage", "–"],
          ["Werkzeug", "Lötkolben, Inbus 1,5 / 2 / 2,5 (Kugelkopf) / 3 mm, Gabelschlüssel 13 mm (2×), Säge, "
                       "Feile, Bohrer 3,0 · 3,5 · 4,0 · 6,5 · 8,0 · 10 mm", "–"],
      ], (0.17, 0.66, 0.17)),
      Spacer(1, 6),
      Paragraph("Die vollständige Liste mit Positionsnummern, Suchbegriffen und Status steht in "
                "docs/stuecklisten/pruefstand-j2.md.", KLEIN)]

s += [Paragraph("Schritt 0: Gekaufte Ritzel nachmessen", H1),
      Paragraph("Das CAD nimmt Masse der Ritzel an. <b>Bevor die drei Scheiben gedruckt werden</b> (Z72, Z64, Z90), "
                "misst du die gelieferten Ritzel mit der Schieblehre nach:", TEXT),
      tabelle([
          ["Ritzel", "Annahme im CAD", "Wenn es abweicht"],
          ["5M, 18 Z", "Nabe Ø 20 × 8 mm, zwei Gewindestifte im Winkel von 90°, Mitte 3,75 mm vom Nabenende; "
                       "Gewinde M4", "Hülse der Z64-Scheibe anpassen (Nabenlänge, M4 oder M5, Lage der Stifte)"],
          ["3M, 16 Z", "Gesamtlänge 24,5 mm (Zahnbreite 16,5, zwei Bordscheiben, Nabe 6 mm)",
           "Fehlt die Nabe, sitzen die Stifte im Zahnbereich: nur den Distanzring anpassen"],
          ["GT2, 20 Z", "Bohrung 5 mm, Nabe 6 mm, zwei Stifte", "Stifte müssen auf die Abflachung der Motorwelle drücken"],
      ], (0.16, 0.50, 0.34)),
      Spacer(1, 4),
      Paragraph("Auch der Motor: die Gewindetiefe der M3-Löcher messen (M3 × 12 greift 4 mm ein).", TEXT)]

# ---------------------------------------------------------------- Schritt 1 Druck
s += [Paragraph("Schritt 1: Teile drucken", H1),
      Paragraph("Drucker BambuLab A1, Düse 0,4 mm, Bambu Studio. Grundlage ist das Profil "
                "<b>«0.20mm Standard @BBL A1»</b>; geändert wird nur, was hier steht. Gemeinsam für alle Teile: "
                "Schichthöhe 0,20 mm, obere / untere Schichten 5 / 4, Infill Gyroid, <b>Stützen aus</b>, Brim aus "
                "(ausser angegeben), Textured PEI (bei Smooth PEI mit Klebestift). Alle Werte sind Startwerte.", TEXT),
      tabelle([
          ["Teil (STL)", "Mat.", "Lage auf dem Bett", "Wände", "Infill"],
          ["Wange_Links_Lager22-20", "PETG", "flach, Lagertaschen (Innenseite) oben; Brim 5 mm", "4", "30 %"],
          ["Wange_Rechts_Lager22-20", "PLA", "flach, Lagertaschen (Innenseite) oben", "4", "30 %"],
          ["Quertraeger (4×)", "PLA", "liegend", "4", "40 %"],
          ["Scheibe_GT2_Z72", "PETG", "Zahnkranz unten, Nabe oben", "4", "40 %"],
          ["Scheibe_3M_Z64", "PETG", "Zahnkranz unten, Hülse oben", "5", "40 %"],
          ["Scheibe_5M_Z90", "PETG", "Hebelseite unten", "4", "30 %"],
          ["Lasthebel", "PLA", "flach, Nabenbund oben", "5", "40 %"],
          ["Messzeiger", "PLA", "flach, Tastklotz oben", "4", "40 %"],
          ["Messuhrhalter", "PLA", "auf dem Rücken", "4", "40 %"],
          ["Spannrolle_5M_Lager22-20", "PETG", "stehend", "4", "<b>100 %</b>"],
          ["Distanzringe (4×), Hülsen (5×)", "PETG", "stehend", "3", "<b>100 %</b>"],
      ], (0.34, 0.09, 0.39, 0.08, 0.10)),
      Spacer(1, 4),
      Paragraph("Dieselben Angaben mit Hinweisen je Teil stehen in <b>cad/export/stl/J2_Pruefstand/"
                "Druckeinstellungen.md</b>. Reihenfolge: erst die kleinen Teile und ein Zahnsegment der 90er-Scheibe "
                "zur Passprobe (Flankenspiel an der 90er-Scheibe wirkt direkt: 0,2 mm sind 0,16°), dann der Rest. "
                "Elefantenfuss-Kompensation bei den Scheiben prüfen: Die untersten Zähne dürfen nicht aufquellen.", TEXT),
      Paragraph("Grösstes Teil ist der Lasthebel mit 240 mm (A1-Bett 256 mm). Filament: PETG 0,35–0,45 kg, "
                "PLA 0,35–0,45 kg, Reserve 0,2 kg.", KLEIN)]

# ---------------------------------------------------------------- Schritt 2 Nachbearbeiten
s += [Paragraph("Schritt 2: Nachbearbeiten", H1),
      Paragraph("Fäden und Reste aus Bohrungen, Langlöchern und Zahnlücken entfernen. Danach die Bohrungen nach "
                "folgender Tabelle auf Mass bringen. Lagersitz und Einschmelzbohrung sind im Toleranztest gemessen; "
                "die Wellen- und Mitnahmebohrungen sind noch Startwerte.", TEXT),
      tabelle([
          ["Stelle", "Gedruckt", "Aufreiben auf"],
          ["Lagersitze 608 (Wangen, Spannrolle 5M)", "Ø 22,20 mm (gemessen im Toleranztest 18.10.2026)",
           "nichts – Lager sollen sich von Hand eindrücken lassen"],
          ["Naben Wellen A und B (Z72, Z64, Distanzringe)", "Ø 8,15 mm", "nur falls Welle nicht gleitet"],
          ["Nabe Abtrieb (Z90, Lasthebel)", "Ø 8,05 mm, <b>stramm</b>", "mit 8,0-mm-Bohrer von Hand, bis die Welle "
                                                                          "ohne Spiel gleitet"],
          ["Mitnahmebohrungen Z64-Hülse (4)", "Ø 3,9 mm", "die M4-Schraube geht saugend ohne Spiel durch; kein "
                                                           "Gewinde im Kunststoff"],
          ["Blockierbohrungen Z72 (4)", "Ø 3,0 mm", "saugend mit 3,0-mm-Bohrer"],
          ["Messuhrhalter, Schaftbohrung", "Ø 8,0 mm, stramm", "mit 8,0-mm-Bohrer auf den Schaft der Messuhr"],
          ["Hülsen (5)", "Ø 8,3 mm", "nicht aufbohren (M8-Schraube)"],
      ], (0.34, 0.31, 0.35)),
      Spacer(1, 6),
      Paragraph("<b>41 Einschmelzgewinde M3</b> (Bohrung Ø 4,0 mm, im Test mit Lötkolben am besten; 4,2 hält "
                "schlechter, 4,4 gar nicht) mit dem Lötkolben setzen. Spitze auf etwa 220 °C "
                "(PLA) bzw. 240 °C (PETG) heizen, Einsatz gerade und ohne Druck von Hand einschmelzen lassen, bis er "
                "bündig sitzt; nicht tiefer. Die Temperaturen sind übliche Richtwerte.", TEXT),
      tabelle([
          ["Teil", "Anzahl", "Zweck"],
          ["Quertraeger (4×)", "16", "je 2 pro Ende, Verschraubung mit den Wangen"],
          ["Untere Quertraeger", "4", "von unten, fürs Grundbrett"],
          ["Scheibe Z90", "8", "Hebel 6, Messzeiger 2"],
          ["Scheibe Z72", "2", "Gewindestifte auf Welle A"],
          ["Lasthebel (Nabe)", "1", "Gewindestift auf Abtriebswelle"],
          ["Wange links", "3", "Blockierstift 1, Stellschrauben 2"],
          ["Wange rechts", "6", "Stellschrauben 2, Messuhrhalter 4"],
          ["Messuhrhalter", "1", "Klemmschraube"],
          ["<b>Summe</b>", "<b>41</b>", ""],
      ], (0.40, 0.12, 0.48))]

# ---------------------------------------------------------------- Schritt 3 Wellen
s += [Paragraph("Schritt 3: Wellen vorbereiten", H1),
      bild(BILDER / "wellen.png", max_hoehe=88 * mm, text="Aufbau der drei Wellen (z-Lagen aus dem CAD)"),
      liste(["Die drei Wellen mit der Metallsäge auf <b>70 mm</b> ablängen (am besten im Schraubstock), beide Enden "
             "entgraten.",
             "Auf jeder Welle Flächen für die Gewindestifte anfeilen, etwa 8 bis 10 mm lang und 0,5 mm tief: "
             "<b>Welle A</b> zwei Flächen für die Stifte der 72er-Scheibe (31 mm vom linken Wellenende) und zwei "
             "für das 3M-Ritzel; <b>Welle B</b> zwei Flächen im Winkel von 90° für die M4-Schrauben (33 mm vom "
             "linken Ende); <b>Abtriebswelle</b> eine Fläche für den Gewindestift der Hebelnabe (53 mm vom linken "
             "Ende).",
             "Die Lagen sind aus dem CAD gerechnet. Beim Zusammenbau trotzdem am Teil anzeichnen: Stift anlegen, "
             "Welle drehen, Fläche genau dort anfeilen."])]

# ---------------------------------------------------------------- Schritt 4..
s += [Paragraph("Schritt 4: Motor an die linke Wange", H1),
      bild(RENDER / "J2_Pruefstand_offen.png", max_hoehe=75 * mm,
           text="Baugruppe ohne rechte Wange: Wellen, Scheiben, Ritzel und Querträger"),
      kasten("<b>Reihenfolge:</b> Die Montagereihenfolge unten ist ein Vorschlag aus dem CAD und noch nicht am "
             "echten Teil durchgespielt. Weicht etwas ab, bitte notieren, die Anleitung wird danach nachgeführt."),
      Spacer(1, 6),
      liste(["Motor mit der Welle nach oben auf den Tisch stellen. Links und rechts davon zwei gleich hohe Klötze "
             "(60 mm, z. B. Brettstapel).",
             "Die linke Wange mit der <b>Aussenseite nach unten</b> auflegen: Der runde Bund (Ø 22 mm) des Motors "
             "steckt im Langloch, die Wange liegt auf Motor und Klötzen.",
             "Vier M3 × 12 von der Innenseite durch die Langlöcher in den Motor drehen, <b>noch nicht festziehen</b>. "
             "Den Motor ganz zur Welle A hin schieben (= entspannt). Zwei der Schrauben liegen später dicht am "
             "GT2-Riemen; sie lassen sich dann nur noch durch die Löcher der rechten Wange anziehen.",
             "Ritzel GT2 20 Z auf die Motorwelle stecken, <b>Nabenunterkante 1 mm über der Innenfläche der Wange</b>, "
             "und die Gewindestifte auf die Abflachung der Welle anziehen (Schraubensicherung mittelfest, falls "
             "vorhanden)."])]

s += [Paragraph("Schritt 5: Lager, Wellen und Scheiben", H1),
      Paragraph("Alle Teile werden von der Innenseite der linken Wange her gestapelt; die Reihenfolge je Welle "
                "steht im Bild bei Schritt 3.", TEXT),
      liste(["Je ein Lager 608 in die drei Lagertaschen der linken Wange drücken (6 Lager insgesamt, drei davon "
             "kommen später rechts).",
             "<b>Welle A:</b> Distanzring A links auf das Lager, darauf die Scheibe Z72 (Zahnkranz unten), dann das "
             "3M-Ritzel 16 Z (Nabe nach oben), dann Distanzring A rechts. Welle von oben durchstecken; Stifte der "
             "72er-Scheibe (M3 × 10) und des Ritzels auf die Flächen anziehen.",
             "<b>Welle B:</b> Distanzring B links, 5M-Ritzel 18 Z (Nabe nach oben), darüber die Scheibe Z64 mit der "
             "Hülse über die Nabe, Distanzring B rechts. Die zwei M4 × 16 durch die Mitnahmebohrungen der Hülse und "
             "die Gewinde der Ritzelnabe auf die Welle schrauben (ersetzen die Gewindestifte des Ritzels); die "
             "Köpfe liegen nicht auf.",
             "<b>Abtriebswelle O:</b> Scheibe Z90 (Zahnkranz unten) auf das Lager; Lasthebel und Messzeiger noch "
             "<b>nicht</b> aufschrauben.",
             "Jede Welle so ausrichten, dass sie unten bündig mit dem Lager abschliesst (Wellenende auf einem 61 mm "
             "hohen Klotz unter der Wange abstützen).",
             "Handprobe: Alle drei Wellen müssen sich leicht drehen; die Zahnscheiben dürfen nirgends streifen."])]

s += [Paragraph("Schritt 6: Spannrollen und Riemen", H1),
      bild(RENDER / "J2_Pruefstand_Riementrieb.png", max_hoehe=88 * mm,
           text="Riemenverlauf (rechte Wange ausgeblendet): unten rechts der Motor, oben die 90er-Scheibe"),
      Paragraph("Jede Spannrolle läuft auf einer <b>M8 × 90</b> in Langlöchern beider Wangen (±8 mm). Die Schraube "
                "steckt mit Scheibe von aussen durch die linke Wange; die Mutter M8 (selbstsichernd) sitzt aussen an "
                "der rechten Wange.", TEXT),
      tabelle([
          ["Rolle", "Aufbau auf der M8-Schraube (von links nach rechts)"],
          ["5M (Stufe 3), bei −54,9 / 90",
           "Hülse 5M links · Lager 608 · Hülse 5M mitte · Lager 608 · Hülse 5M rechts; die Lager sitzen in der "
           "gedruckten Rolle Ø 32 mm"],
          ["3M (Stufe 2), bei 10 / 23,2",
           "Hülse 3M links (bleibt 12 mm dick) · 2 Lager 608 blank nebeneinander (14 mm, Riemen 15 mm) · "
           "Hülse 3M rechts"],
      ], (0.28, 0.72)),
      Spacer(1, 6),
      liste(["Die M8-Schrauben mit Scheibe von aussen durch die linke Wange stecken und die Teile jeder Rolle "
             "aufziehen; die Mutter vorläufig lose aufdrehen, damit nichts herausrutscht.",
             "Die drei Riemen jetzt auflegen, solange noch keine rechte Wange da ist: GT2 um Motorritzel und "
             "Z72, HTD-3M um 3M-Ritzel, Z64 und Rolle (die Rolle drückt auf den Riemenrücken), HTD-5M um 5M-Ritzel, "
             "Z90 und Rolle (ebenfalls auf dem Rücken)."])]

s += [Paragraph("Schritt 7: Querträger, rechte Wange", H1),
      liste(["Die vier Querträger mit je 4 Schrauben M3 × 16 an die linke Wange schrauben (zwei Schrauben je Ende; "
             "die oberen Träger sind zugleich die Endanschläge des Hebels).",
             "Rechte Wange aufsetzen: Wellenenden, Lager (3 in die rechten Taschen drücken), Rollen-Schrauben und "
             "Querträger müssen zugleich fassen. Mit den restlichen M3 × 16 verschrauben.",
             "Mutter M8 mit Scheibe auf die Rollen-Schrauben, <b>nur handfest (etwa 1 Nm)</b>: Fester Anzug würde "
             "die gedruckten Hülsen zerdrücken.",
             "Handprobe: Wellen drehen, Riemen laufen lassen."]),
      bild(RENDER / "J2_Pruefstand_rechts.png", max_hoehe=88 * mm,
           text="Ansicht von rechts: Zugangsbohrungen zu Hebelschrauben und Blockierstift, Messuhrhalter oben links")]

s += [Paragraph("Schritt 8: Riemen spannen", H1),
      Paragraph("In dieser Reihenfolge, damit sich nichts gegenseitig verstellt: <b>Stufe 3, Stufe 2, Stufe 1</b>.", TEXT),
      tabelle([
          ["Stufe", "So wird gespannt", "Schraube"],
          ["3 (5M)", "M3-Stellschraube in der Nische an der linken Kante der Wangen (je Wange eine) stützt die "
                     "M8-Schraube gegen den Riemenzug; damit spannen. Dann Mutter M8 handfest.", "2 × M3 × 30"],
          ["2 (3M)", "Stellschrauben kommen von unten; sie ragen gespannt rund 9 mm aus den Wangen (entspannt bis "
                     "17 mm). Dann Mutter M8 handfest.", "2 × M3 × 25"],
          ["1 (GT2)", "Motor in den Langlöchern (±3 mm) von der Welle A wegschieben, dann die vier Motorschrauben "
                      "durch die Löcher der rechten Wange festziehen.", "4 × M3 × 12"],
      ], (0.12, 0.68, 0.20)),
      Spacer(1, 6),
      Paragraph("Spannung als Richtwert: Der Riemen soll straff sein und sich in der Mitte des freien Trums mit dem "
                "Finger nur etwa 1 bis 2 mm eindrücken lassen (kein gemessener Wert). Alle Stufen so spannen, dass "
                "die Wellen noch leicht laufen.", TEXT),
      Paragraph("Die 3M-Stellschrauben ragen unten aus dem Prüfstand: Das Grundbrett bekommt dafür zwei Löcher "
                "Ø 10 mm, und es wird gespannt, bevor das Brett am Tisch festgezwungen ist.", KLEIN)]

s += [Paragraph("Schritt 9: Hebel, Messzeiger, Messuhrhalter", H1),
      liste(["<b>Lasthebel</b> mit 6 × M3 × 16 auf die 90er-Scheibe schrauben (Zugang durch die Zugangsbohrungen "
             "der rechten Wange), Hebelarm in der Grundstellung nach oben. Gewindestift M3 × 8 in der Hebelnabe auf "
             "die Fläche der Abtriebswelle.",
             "<b>Messzeiger</b> mit 2 × M3 × 16 auf die 90er-Scheibe, dem Hebel entgegen. Der Tastklotz am Ende hat "
             "zwei ebene Flächen; wenn nötig mit Schleifpapier K400 plan abziehen.",
             "<b>Messuhrhalter</b> mit 2 × M3 × 16 aussen an die rechte Wange (links für «Hebel waagrecht nach "
             "rechts», rechts für «Hebel waagrecht nach links»). Messuhr in die geschlitzte Bohrung stecken und "
             "mit der M3 × 25 nur leicht klemmen.",
             "Von der Unterkante des Halters bis zur Tastfläche sind es 15 mm. Das Gehäuse der Messuhr darf "
             "von der Schaftachse aus höchstens 17 mm zur rechten Wange und 17 mm zur Scheibe hin auftragen."])]

s += [PageBreak(),
      Paragraph("Schritt 10: Auf das Grundbrett", H1),
      bild(REPO / "docs/bilder/pruefstand_befestigung.png", max_hoehe=135 * mm),
      liste(["Brett 220 × 200 × 12 mm nach dem Bohrbild bohren: vier Löcher Ø 3,5 mm, von unten Ø 6,5 mm "
             "3,5 mm tief angesenkt (Schraubenköpfe dürfen nicht vorstehen), dazu zwei Löcher Ø 10 mm für die "
             "Stellschrauben der 3M-Rolle.",
             "Prüfstand aufsetzen und mit 4 × M3 × 20 von unten in die Einschmelzgewinde der unteren Querträger "
             "schrauben.",
             "Brett <b>bündig an die Tischkante</b>, Wangen quer zur Kante, mit zwei Zwingen links und rechts vom "
             "Prüfstand festspannen. Ohne Zwingen kippt der Aufbau: Die Last hängt 78,5 mm ausserhalb der Kante.",
             "Für die Gegenrichtung (Hebel nach links) das Brett um 180° drehen und neu spannen."])]

s += [Paragraph("Schritt 11: Elektrik", H1),
      Paragraph("Arduino Uno mit CNC-Shield, Treiber TMC2209 mit Kühlkörper, Motor NEMA 17, Netzteil 24 V "
                "(für Messungen im Stillstand genügt das vorhandene 12 V / 4 A). Verdrahtung wie bei der Motorvermessung "
                "(docs/verdrahtung.md).", TEXT),
      kasten("<b>Offen:</b> Der Treiberstrom (Vref) für den 60-mm-Motor mit dem TMC2209 ist noch nicht eingestellt "
             "und dokumentiert; das geschieht beim ersten Aufbau mit dem Multimeter und wird hier nachgetragen. "
             "Stecker nie unter Spannung ziehen oder stecken."),
      Spacer(1, 6),
      Paragraph("Schritt 12: Prüfen vor der ersten Messung", H1),
      liste(["Alle Wellen von Hand drehen: leichtgängig, kein Streifen der Scheiben am Riemen oder an den Wangen.",
             "Spalt am Endanschlag offen: Bei waagrechtem Hebel bleiben rund 10 mm über dem Querträger (Papierstreifen). "
             "Liegt der Hebel auf, ist die Messung ungültig.",
             "Stellschrauben und Motorschrauben fest, M8-Muttern nur handfest.",
             "Gewicht an einer <b>kurzen Schlaufe</b> höchstens 30 mm über einer weichen Unterlage oder mit "
             "Fangschnur; Hände nie unter dem Hebel. Der Antrieb ist rückdrehbar: Ohne Motorstrom oder bei "
             "Schrittverlust fällt der Hebel bis zum Anschlag."]),
      Paragraph("Weiter geht es mit den Messungen in <b>docs/pruefstand-j2.md</b>: Umkehrspiel unter Wechsellast "
                "±2 Nm (Gewicht 1,07 kg), Steifigkeit, Haltetest mit 5,9 kg (11 Nm) und Rücklauftest ohne Strom.",
                TEXT)]



def schritte_zusammenhalten(fluss):
    """Jede Überschrift samt Inhalt bis zur nächsten Überschrift auf einer Seite halten."""
    neu, gruppe = [], []
    for f in fluss:
        ist_kopf = isinstance(f, Paragraph) and f.style.name == "H1"
        if ist_kopf or isinstance(f, PageBreak):
            if gruppe:
                neu.append(KeepTogether(gruppe))
            gruppe = []
            if isinstance(f, PageBreak):
                neu.append(f)
                continue
        gruppe.extend(f._content if isinstance(f, KeepTogether) else [f])
    if gruppe:
        neu.append(KeepTogether(gruppe))
    return neu


s = schritte_zusammenhalten(s)
doc = SimpleDocTemplate(str(ZIEL), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                        bottomMargin=20 * mm, title="Bauanleitung J2-Prüfstand",
                        author="Projekt KI-Integrierter Roboterarm")
doc.build(s, onFirstPage=fusszeile, onLaterPages=fusszeile)
print(ZIEL)
