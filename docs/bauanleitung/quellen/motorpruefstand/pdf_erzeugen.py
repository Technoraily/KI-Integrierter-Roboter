"""Erzeugt die Bauanleitung des Motorprüfstands als eine PDF-Datei.

Aufruf:  python docs/bauanleitung/quellen/motorpruefstand/pdf_erzeugen.py
Ergebnis: docs/bauanleitung/Bauanleitung_Motorpruefstand.pdf
Text steht hier im Skript; Bilder aus bilder/ (Fusion: cad/skripte/motorpruefstand_bilder.py,
Verdrahtung: verdrahtung_zeichnen.py) und cad/renders/Motorpruefstand_iso.png.
Braucht: pip install reportlab
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
ZIEL = HIER.parents[1] / "Bauanleitung_Motorpruefstand.pdf"
STAND = "14.10.2026"

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
    canvas.drawString(20 * mm, 12 * mm, f"Bauanleitung Motorprüfstand NEMA 17 – Stand {STAND}")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"Seite {doc.page}")
    canvas.restoreState()


s = []
s += [Paragraph("Bauanleitung Motorprüfstand", TITEL),
      Paragraph("Für die vorhandenen NEMA-17-Motoren (17CS04A-170E) – ohne Kaufteile", UNTERTITEL),
      bild(REPO / "cad/renders/Motorpruefstand_iso.png", max_hoehe=95 * mm,
           text="Fertiger Prüfstand: Motorhalter mit Wiege, Niederhalter und Waagebalken"),
      Paragraph(
          "Mit diesem Prüfstand misst du das Moment deiner Motoren: das Haltemoment am Waagebalken, das "
          "Moment bei Drehzahl mit der Seiltrommel und ob unter Last Schritte verloren gehen. Als Last dient "
          "eine Wasserflasche an einer Schnur, gewogen wird mit der Küchenwaage. Diese Anleitung beschreibt "
          "den Aufbau; die Messungen selbst stehen in <b>docs/motorvermessung.md</b>.", TEXT),
      Spacer(1, 4),
      tabelle([
          ["Teil", "Was es tut"],
          ["<b>Motorhalter</b>", "Grundplatte 200 × 110 mm mit Wiege. Der Motor wird nur eingelegt; die Wiege hält "
                                 "das Gegenmoment über seine Kanten."],
          ["<b>Niederhalter</b>", "Wird oben eingesteckt, damit der Motor nicht herausspringt."],
          ["<b>Waagebalken</b>", "Symmetrischer Hebel mit Schnurlöchern genau 100 mm von der Welle (Test A)."],
          ["<b>Seiltrommel</b>", "Zwei Stufen mit 20 und 10 mm Wickelradius (Tests B und C)."],
      ], (0.22, 0.78)),
      PageBreak()]

s += [Paragraph("Was du brauchst", H1),
      tabelle([
          ["Gruppe", "Teil", "Status"],
          ["Druckteile", "Motorhalter, Niederhalter, Waagebalken, Seiltrommel (ca. 110 g PLA)", "drucken"],
          ["Schrauben", "1–2 × M3 × 16 mit Mutter; optional 4 × M3 × 8–10", "vorhanden"],
          ["Elektrik", "NEMA 17, Arduino Uno mit GRBL, CNC-Shield, A4988, Netzteil 12 V / 4 A", "vorhanden"],
          ["", "Motorkabel, USB-Kabel, G-Code-Sender auf dem PC (Universal Gcode Sender oder Candle, kostenlos)",
           "nachsehen"],
          ["Messen", "Küchenwaage, Multimeter, Handy mit Wasserwaage-App", "Waage vorhanden"],
          ["Haushalt", "2 PET-Flaschen 1,5 l, eine Tasche, ca. 2 m Schnur (1 mm), Klebeband, Tuch", "Haushalt"],
          ["Aufstellung", "Schraubzwinge oder mindestens 4 kg Bücher", "nachsehen"],
          ["Werkzeug", "Inbus bzw. Schraubendreher für M3, kleiner Schraubendreher für das Poti", "nachsehen"],
      ], (0.17, 0.63, 0.20)),
      Spacer(1, 6),
      Paragraph("Die vollständige Liste mit allen Positionen: docs/stuecklisten/motorpruefstand.md.", KLEIN)]

s += [Paragraph("Schritt 1: Teile drucken", H1),
      bild(BILDER / "01_teile.png", max_hoehe=68 * mm, text="Die vier Druckteile"),
      Paragraph("Drucker BambuLab A1, Düse 0,4 mm, Bambu Studio. Grundlage ist das Profil "
                "<b>«0.20mm Standard @BBL A1»</b>; geändert wird nur, was hier steht.", TEXT),
      tabelle([
          ["Für alle Teile gleich", "Wert"],
          ["Material", "PLA (Bambu PLA Basic oder Generic PLA), Temperaturen laut Filamentprofil"],
          ["Schichthöhe", "0,20 mm"],
          ["Obere / untere Schichten", "5 / 4"],
          ["Infill-Muster", "Gyroid"],
          ["Stützen", "<b>aus</b>"],
          ["Brim", "aus (beim Motorhalter einschalten, falls die Ecken sich lösen)"],
          ["Druckplatte", "Textured PEI oder Smooth PEI, vorher fettfrei"],
      ], (0.36, 0.64)),
      Spacer(1, 6),
      tabelle([
          ["Datei (cad/export/stl/ Motorpruefstand/)", "Lage auf dem Druckbett", "Wände", "Infill"],
          ["Motorhalter.stl", "Grundplatte unten (wie exportiert)", "3", "30 %"],
          ["Niederhalter.stl", "<b>im Slicer umdrehen</b>: Platte unten, Zapfen oben", "3", "<b>100 %</b>"],
          ["Waagebalken.stl", "flach, Nabe oben (wie exportiert)", "4", "40 %"],
          ["Seiltrommel.stl", "Aussenflansch unten (wie exportiert); Kegel 45°, ohne Stützen", "4", "40 %"],
      ], (0.30, 0.46, 0.10, 0.14)),
      Spacer(1, 4),
      Paragraph("Filament gesamt ca. 110 g PLA. Dieselben Angaben liegen als Druckeinstellungen.md im "
                "STL-Ordner.", KLEIN),
      Spacer(1, 4),
      Paragraph("Danach Fäden und Reste aus Schlitzen, Taschen und Bohrungen entfernen. Die 5,1-mm-Bohrung der "
                "Naben muss sich leicht auf die Motorwelle schieben lassen; sonst mit einem 5-mm-Bohrer von Hand "
                "nachdrehen.", TEXT)]

s += [Paragraph("Schritt 2: Klemmung an den Naben vorbereiten", H1),
      bild(BILDER / "02_klemmnabe.png", max_hoehe=55 * mm, text="Klemmnabe am Waagebalken: Schlitz und Mutterfalle"),
      Paragraph("Jede Nabe hat einen Schlitz und quer dazu ein Loch für die M3-Schraube.", TEXT),
      liste(["Die M3-Mutter seitlich in die rechteckige Tasche schieben.",
             "Die M3 × 16 von der Gegenseite durchstecken und zwei, drei Umdrehungen eindrehen. "
             "<b>Noch nicht anziehen.</b>"]),
      Paragraph("Bei der Seiltrommel genauso.", TEXT)]

s += [Paragraph("Schritt 3: Motor einlegen", H1),
      bild(BILDER / "03_motor_einlegen.png", max_hoehe=62 * mm, text="Motor von oben in die Wiege legen"),
      liste(["Der Kabelstecker zeigt nach hinten, zur offenen Seite der Wiege.",
             "Der runde Bund vorne am Motor steckt im Schlitz der Stirnwand; die Stirnfläche liegt an der Wand an.",
             "Optional mit vier M3 × 8–10 durch die Löcher der Stirnwand in den Motor schrauben. Nötig ist das "
             "nicht."], nummeriert=False)]

s += [Paragraph("Schritt 4: Niederhalter aufstecken", H1),
      bild(BILDER / "04_niederhalter.png", max_hoehe=62 * mm, text="Niederhalter mit zwei Zapfen"),
      Paragraph("Den Niederhalter mit den zwei Zapfen oben in die Löcher der Seitenwände stecken. Er liegt auf dem "
                "Motor und verhindert, dass der Motor herausspringt.", TEXT)]

s += [Paragraph("Schritt 5: Waagebalken aufstecken", H1),
      bild(BILDER / "05_waagebalken.png", max_hoehe=62 * mm, text="Waagebalken auf die Motorwelle"),
      liste(["Den Waagebalken auf die Welle schieben, mit der flachen Seite des Balkens zur Stirnwand. "
             "<b>1–2 mm Luft</b> zur Stirnwand lassen, damit nichts schleift.",
             "Hat die Welle eine Abflachung, gehört der Schlitz der Nabe darüber.",
             "Die M3-Schraube anziehen, bis sich der Balken von Hand nicht mehr auf der Welle verdreht. "
             "Nicht mit Gewalt, sonst reisst die Nabe."])]

s += [PageBreak(),
      Paragraph("Schritt 6: Verdrahten", H1),
      bild(BILDER / "08_verdrahtung.png", max_hoehe=95 * mm),
      kasten("<b>Alles nur ohne Strom stecken.</b> Den Motorstecker nie ziehen oder stecken, solange Spannung "
             "anliegt – das zerstört den A4988."),
      Spacer(1, 6),
      liste(["Das CNC-Shield auf den Uno stecken.",
             "Unter Steckplatz X alle drei Mikroschritt-Jumper stecken (1/16-Schritt).",
             "Den A4988 in Steckplatz X setzen, richtig herum nach Aufdruck (Pin EN zu EN). Falsch herum "
             "zerstört ihn das beim Einschalten.",
             "Das Motorkabel an den 4-Pin-Stecker X.",
             "Das Netzteil 12 V an die Schraubklemme des Shields. <b>Plus und Minus prüfen.</b>",
             "USB vom Uno zum PC."])]

s += [Paragraph("Schritt 7: Strom einstellen und Wärmetest", H1),
      liste(["Das Netzteil einschalten.",
             "Mit dem Multimeter die Spannung zwischen dem Poti des A4988 und GND messen (Vref).",
             "Mit einem kleinen Schraubendreher auf den Wert für <b>1,0 A</b> drehen. Welcher Wert das ist, hängt "
             "vom Widerstand ab, der auf dem Treiber aufgedruckt ist:"]),
      tabelle([["Aufdruck auf dem Treiber", "Vref für 1,0 A"],
               ["R100", "0,80 V"], ["R050", "0,40 V"], ["R200", "1,60 V"]], (0.5, 0.5)),
      Spacer(1, 6),
      Paragraph("<b>Wärmetest:</b> Im G-Code-Sender verbinden (115200 Baud), dann <b>$1=255</b> senden und "
                "<b>G91 G0 X1</b>. Der Motor bleibt jetzt bestromt. 5 Minuten warten. Wird der A4988 so heiss, "
                "dass man ihn nicht anfassen kann, oder lässt der Motor zwischendurch los, braucht es einen "
                "Kühlkörper oder Lüfter.", TEXT)]

s += [PageBreak(),
      Paragraph("Schritt 8: Aufstellen", H1),
      bild(BILDER / "06_test_a.png", max_hoehe=72 * mm, text="Aufstellung an der Tischkante, Test A"),
      liste(["Die Grundplatte so auf den Tisch legen, dass ihre Vorderkante (Seite mit Welle und Balken) "
             "<b>20 mm über die Tischkante</b> ragt.",
             "Hinten mit der <b>Schraubzwinge</b> durch eines der zwei Löcher festmachen. Ohne Zwinge: mindestens "
             "4 kg Bücher hinten auf die Platte legen und zusätzlich mit der Hand drücken.",
             "Ein Tuch oder einen Karton unter die Stelle legen, wo die Flasche hängt."])]

s += [Paragraph("Schritt 9: Last anhängen", H1),
      Paragraph("<b>Test A (Haltemoment):</b> eine Schnurschlaufe durch das Loch am Ende des Waagebalkens "
                "(100 mm von der Welle) und die Flasche fest am Hals anbinden.", TEXT),
      Paragraph("<b>Tests B und C (Seilwinde):</b> den Waagebalken abnehmen und die Seiltrommel genauso aufklemmen "
                "(Schritt 5). Die Schnur durch das radiale Loch der gewünschten Stufe und das axiale Loch nach "
                "aussen fädeln, unter dem Aussenflansch verknoten und <b>einlagig nebeneinander</b> aufwickeln.",
                TEXT),
      bild(BILDER / "07_test_b.png", max_hoehe=72 * mm, text="Seiltrommel mit Flasche, Test B"),
      Paragraph("Der Prüfstand ist fertig. Weiter geht es mit den Messungen in docs/motorvermessung.md "
                "(Test A, B und C mit Protokoll).", TEXT)]



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
                        bottomMargin=20 * mm, title="Bauanleitung Motorprüfstand",
                        author="Projekt KI-Integrierter Roboterarm")
doc.build(s, onFirstPage=fusszeile, onLaterPages=fusszeile)
print(ZIEL)
