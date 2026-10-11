"""Zentrale Parameter des Arms. Namen und Werte entsprechen docs/parameter.md.

Längen in Metern, Massen in Kilogramm, Winkel in Grad, Momente in Nm.
"""

from dataclasses import dataclass

# Geometrie
H_SCHULTER = 0.170  # Tischfläche -> Achse J2
L_OBERARM = 0.200  # Achse J2 -> Achse J3
L_UNTERARM = 0.190  # Achse J3 -> Handgelenkmitte
L_HAND = 0.060  # Handgelenkmitte -> Flanschfläche

# Gelenkbereiche (min, max) in Grad; Nullstellung = Arm senkrecht nach oben
GELENKBEREICH = (
    (-170.0, 170.0),  # J1
    (-90.0, 90.0),  # J2, Capstan-Halbscheibe
    (-135.0, 135.0),  # J3, Capstan-Vollscheibe
    (-180.0, 180.0),  # J4
    (-110.0, 110.0),  # J5
    (-180.0, 180.0),  # J6
)


@dataclass(frozen=True)
class Antrieb:
    name: str
    untersetzung: float
    motormoment: float  # nutzbares Moment bei Betriebsdrehzahl, nicht Haltemoment
    wirkungsgrad: float
    motordrehzahl: float = 400.0  # U/min, bis hier gilt motormoment etwa

    @property
    def abtriebsmoment(self) -> float:
        return self.motormoment * self.untersetzung * self.wirkungsgrad

    @property
    def gelenkgeschwindigkeit(self) -> float:
        """Grad pro Sekunde bei motordrehzahl."""
        return self.motordrehzahl * 6.0 / self.untersetzung


# Motormomente sind Annahmen (ca. 70 % des Haltemoments), bis sie am
# Prüfstand gemessen sind. J1, J3, J4: vorhandene 17CS04A-170E (40 mm);
# J2: NEMA 17 60 mm; J5: NEMA 17 34 mm; J6: NEMA 14.
ANTRIEBE = (
    Antrieb("J1", 20, 0.28, 0.85),
    Antrieb("J2", 72, 0.45, 0.65),  # drei Riemenstufen 3,6 x 4 x 5
    Antrieb("J3", 60, 0.28, 0.65),
    Antrieb("J4", 20, 0.28, 0.85),
    Antrieb("J5", 18.75, 0.18, 0.85),  # 5 x 3,75
    Antrieb("J6", 8, 0.08, 0.90),
)


@dataclass(frozen=True)
class Masse:
    name: str
    glied: int  # 1..6: bewegt sich mit dem Glied hinter Gelenk <glied>
    ort: tuple[float, float, float]  # im Koordinatensystem dieses Glieds
    kg: float


# Massenmodell (Schätzung vor dem CAD; wird mit Fusion-Massen nachgeführt).
# Ursprung Glied 2 = Schulterachse, Glied 3/4 = Ellbogenachse,
# Glied 5 = Handgelenkmitte, Glied 6 = Flanschfläche. z zeigt zum Werkzeug.
MASSEN = (
    Masse("Oberarm Struktur", 2, (0, 0, 0.100), 0.30),
    Masse("Motor J3 (nahe Schulter)", 2, (0, 0, 0.030), 0.30),
    Masse("Vorstufe + Riemen J3", 2, (0, 0, 0.100), 0.10),
    Masse("Ellbogen Scheibe + Lager", 2, (0, 0, 0.200), 0.20),
    Masse("Unterarm Struktur", 3, (0, 0, 0.080), 0.20),
    Masse("Motor J4 + Stufe", 3, (0, 0, 0.030), 0.38),
    Masse("Motor J5", 4, (0, 0, 0.060), 0.22),
    Masse("Stufe J5", 4, (0, 0, 0.150), 0.08),
    Masse("Handgelenk Gehäuse", 5, (0, 0, 0.000), 0.12),
    Masse("Motor J6 + Stufe", 5, (0, 0, 0.020), 0.18),
    Masse("Reserve Wechsler + Kamera", 6, (0, 0, 0.000), 0.15),
    Masse("Greifer", 6, (0, 0, 0.040), 0.15),
    Masse("Verkleidung + Kabel Oberarm", 2, (0, 0, 0.100), 0.18),
    Masse("Verkleidung + Kabel Unterarm", 3, (0, 0, 0.090), 0.15),
    Masse("Verkleidung + Kabel Hand", 5, (0, 0, 0.010), 0.07),
)

# Schwerpunkt der Nutzlast im Flansch-Koordinatensystem (30 mm seitlich versetzt,
# damit auch J4 und J6 belastet werden)
ORT_NUTZLAST = (0.030, 0.0, 0.080)
