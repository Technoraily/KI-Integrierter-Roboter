"""Rechnet die GRBL-Einstellungen des J2-Prüfstands und erzeugt die Testprogramme.

Aufruf: python software/j2_testprogramme.py
Schreibt docs/gcode/*.nc. Werte und Begründung: docs/grbl-j2.md.
X ist in Grad am Abtrieb (Hebel), 0 = Hebel waagrecht, positiv = Hebel nach oben.
"""

from pathlib import Path

# Antrieb (docs/parameter.md, J2)
UEBERSETZUNG = 3.6 * 4 * 5  # GT2 20:72, 3M 16:64, 5M 18:90
VOLLSCHRITTE = 200  # 1,8 Grad
MIKROSCHRITT = 16  # alle Jumper am CNC-Shield gesteckt
STEP_RATE_MAX = 30000  # Schritte/s, Grenze von GRBL auf dem Arduino Uno

# Bewegungsgrenzen am Prüfstand (docs/pruefstand-j2.md, Endanschläge)
L_HEBEL = 190.0  # mm, Achse -> Lastbohrung
SPALT_ABWAERTS = 22.0  # mm, so weit sinkt die Lastbohrung aus der Waagrechten bis zum Anschlag
WINKEL_ABWAERTS_MAX = 6.65  # Grad, = asin(22/190)

STEPS_PRO_GRAD = VOLLSCHRITTE * MIKROSCHRITT * UEBERSETZUNG / 360
STEPS_PRO_GRAD_MOTOR = VOLLSCHRITTE * MIKROSCHRITT / 360  # Motor allein, X = Grad an der Welle

# Prüfdrehzahlen wie in docs/motorvermessung.md (Motor U/min -> Grad/s am Abtrieb)
DREHZAHLEN = (60, 120, 240, 360)


def grad_pro_s(motor_rpm: float) -> float:
    return motor_rpm * 6.0 / UEBERSETZUNG


def schrittrate(grad_s: float) -> float:
    return grad_s * STEPS_PRO_GRAD


def kopf(titel: str, einstellungen: str, hinweise: list[str]) -> list[str]:
    zeilen = [f"(J2 {titel})", f"(Einstellungen: {einstellungen})"]
    zeilen += [f"({h})" for h in hinweise]
    zeilen += ["G21 (mm bzw. Grad)", "G91 (relativ)", "G94 (Vorschub pro Minute)"]
    return zeilen


def hin_zurueck(winkel: float, f: float, n: int) -> list[str]:
    zeilen = []
    for _ in range(n):
        zeilen += [f"G1 X{winkel:g} F{f:g}", f"G1 X{-winkel:g} F{f:g}"]
    return zeilen


def programme() -> dict[str, list[str]]:
    sicher = "Hebel von Hand waagrecht stellen, BEVOR der Strom eingeschaltet wird: dort ist X0"
    prog = {}

    prog["j2-00-motor-allein"] = kopf(
        "Test 0: Motor allein auf der Wange, ohne Riemen und Ritzelstufen",
        f"$100={STEPS_PRO_GRAD_MOTOR:.3f} $110=45000 $120=500 (X = Grad an der Motorwelle)",
        [
            "Markierung mit Klebeband auf die Welle; 1 Umdrehung = 360",
            "Prüft Verdrahtung, Drehrichtung, Vref und dass keine Schritte fehlen",
        ],
    )
    prog["j2-00-motor-allein"] += [
        "(10 Umdrehungen vor, 10 zurück, 60 U/min; Marke muss wieder am Start stehen)",
        "G1 X3600 F21600",
        "G1 X-3600 F21600",
        "(5 Umdrehungen bei 120 U/min)",
        "G1 X1800 F43200",
        "G1 X-1800 F43200",
        "M30",
    ]

    prog["j2-01-abtrieb-kurz"] = kopf(
        "Test 1: Abtrieb ohne Last, kurze Wege",
        f"$100={STEPS_PRO_GRAD:.0f} $110=1800 $120=20",
        [sicher, "Hebel ohne Gewicht. Richtung prüfen: X+ muss den Hebel nach oben bewegen,",
         "sonst $3=1 setzen (nicht den Motorstecker umstecken).",
         f"Nach unten höchstens {WINKEL_ABWAERTS_MAX} Grad (22 mm an der Lastbohrung); hier nur -3"],
    )
    prog["j2-01-abtrieb-kurz"] += [
        "G1 X2 F300 (2 Grad = 6,6 mm an der Lastbohrung, 5 Grad/s)",
        "G4 P2",
        "G1 X-2 F300",
        "G1 X5 F300",
        "G1 X-5 F300",
        "G1 X-3 F300 (unter Waagrechte)",
        "G1 X3 F300",
        "M30",
    ]

    prog["j2-02-schrittverlust"] = kopf(
        "Test 2: Wiederholgenauigkeit / Schrittverlust",
        f"$100={STEPS_PRO_GRAD:.0f} $110=1800 $120=20",
        [sicher, "Kante des Hebels vor dem Start am Rahmen oder Messuhrhalter markieren",
         "Amplitude 5 Grad = 5,6 mm am Tastklotz (64 mm Radius), passt in den Messbereich 0-10 mm",
         "Messuhr vor und nach 20 Zyklen in Position X0 ablesen und vergleichen",
         "Mit Last erst wiederholen, wenn ohne Last die Anzeige zurückkehrt"],
    )
    prog["j2-02-schrittverlust"] += hin_zurueck(5, 600, 20) + ["M30"]

    prog["j2-03-geschwindigkeit"] = kopf(
        "Test 3: Drehzahlstufen wie Motorvermessung",
        f"$100={STEPS_PRO_GRAD:.0f} $110=1800 $120=20",
        [sicher, "Je 3 Zyklen 0 -> +15 -> 0 bei Motordrehzahl 60 / 120 / 240 / 360 U/min",
         "Aufsteigend; stehen bleiben oder Brummen = Grenze gefunden, Programm mit Reset abbrechen",
         "Messuhr vorher abnehmen: 15 Grad sind 17 mm am Tastklotz, mehr als ihr Messbereich",
         "Hebel ohne Gewicht, dann mit 1,07 kg (2 Nm)"],
    )
    for rpm in DREHZAHLEN:
        f = grad_pro_s(rpm) * 60
        prog["j2-03-geschwindigkeit"] += [f"({rpm} U/min Motor = {grad_pro_s(rpm):.1f} Grad/s Abtrieb)"]
        prog["j2-03-geschwindigkeit"] += hin_zurueck(15, round(f), 3)
    prog["j2-03-geschwindigkeit"] += ["M30"]

    prog["j2-04-dauerlauf"] = kopf(
        "Test 4: Dauerlauf (Erwärmung)",
        f"$100={STEPS_PRO_GRAD:.0f} $110=1800 $120=20",
        [sicher, "100 Zyklen 0 -> +15 -> 0 bei 10 Grad/s (120 U/min), etwa 5 Minuten", "Messuhr abnehmen",
         "Danach Motor, Treiber und Wange mit der Hand prüfen und Temperatur notieren"],
    )
    prog["j2-04-dauerlauf"] += hin_zurueck(15, 600, 100) + ["M30"]
    return prog


def grbl_sicher(zeile: str) -> str:
    """GRBL kennt keine verschachtelten Klammern und liest nur ASCII sicher."""
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("Ä", "Ae"), ("Ö", "Oe"), ("Ü", "Ue"), ("ß", "ss")):
        zeile = zeile.replace(a, b)
    code, klammer, kommentar = zeile.partition("(")
    if not klammer:
        return zeile
    inner = kommentar[:-1] if kommentar.endswith(")") else kommentar
    return f"{code}({inner.replace('(', '[').replace(')', ']')})"


def main() -> None:
    ziel = Path(__file__).resolve().parents[1] / "docs" / "gcode"
    ziel.mkdir(exist_ok=True)
    for name, zeilen in programme().items():
        (ziel / f"{name}.nc").write_text("\n".join(grbl_sicher(z) for z in zeilen) + "\n", encoding="ascii")
        print("geschrieben:", name)

    print(f"\nSchritte pro Grad am Abtrieb: {STEPS_PRO_GRAD:.1f}")
    print(f"Winkel pro Mikroschritt: {1 / STEPS_PRO_GRAD:.5f} Grad")
    print(f"Weg an der Lastbohrung pro Mikroschritt: {L_HEBEL * 3.14159265 / 180 / STEPS_PRO_GRAD:.5f} mm")
    for rpm in DREHZAHLEN:
        print(f"{rpm} U/min: {grad_pro_s(rpm):.2f} Grad/s = {grad_pro_s(rpm) * 60:.0f} Grad/min,"
              f" {schrittrate(grad_pro_s(rpm)):.0f} Schritte/s")
    max_gs = STEP_RATE_MAX / STEPS_PRO_GRAD
    print(f"Grenze Arduino ({STEP_RATE_MAX} Schritte/s): {max_gs:.1f} Grad/s = {max_gs * UEBERSETZUNG / 6:.0f} U/min Motor")


if __name__ == "__main__":
    main()
