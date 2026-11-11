#!/usr/bin/env python3
"""Laedt eine FluidNC-Konfigurationsdatei per USB (XMODEM) auf den ESP32 und startet FluidNC neu.

Aufruf:  python software/fluidnc_upload.py software/fluidnc/config_j2.yaml [COMx] [Zielname]
Ohne COMx wird der CP210x/CH340-Port automatisch gesucht. Zielname Standard: config.yaml
Benoetigt:  pip install pyserial xmodem
"""
import sys
import time

import serial
import serial.tools.list_ports
from xmodem import XMODEM


def finde_port():
    for p in serial.tools.list_ports.comports():
        if p.vid in (0x10C4, 0x1A86, 0x303A, 0x0403):
            return p.device
    return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    datei = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2].upper().startswith("COM") else finde_port()
    ziel = sys.argv[3] if len(sys.argv) > 3 else "config.yaml"
    if not port:
        print("Kein ESP32-Anschluss gefunden (CP210x-Treiber installiert? Kabel mit Datenleitung?)")
        return 2
    s = serial.Serial()
    s.port = port
    s.baudrate = 115200
    s.timeout = 1.0
    s.dtr = False
    s.rts = False
    s.open()
    time.sleep(0.3)
    s.reset_input_buffer()
    s.write(b"\x18")
    time.sleep(2.0)
    s.reset_input_buffer()
    s.write(f"$Xmodem/Receive={ziel}\n".encode())
    time.sleep(0.5)
    s.reset_input_buffer()

    def getc(size, timeout=1):
        s.timeout = timeout
        return s.read(size) or None

    def putc(data, timeout=1):
        s.write_timeout = timeout
        return s.write(data)

    with open(datei, "rb") as f:
        modem = XMODEM(getc, putc, mode="xmodem")
        ok = modem.send(f)
    print("Upload:", "OK" if ok else "FEHLGESCHLAGEN", f"-> {ziel} auf {port}")
    time.sleep(0.5)
    s.timeout = 0.3
    s.reset_input_buffer()
    if ok:
        s.write(b"$Bye\n")   # FluidNC neu starten, damit die Konfiguration geladen wird
        time.sleep(4.0)
        print(s.read(3000).decode("ascii", "replace")[-1500:])
    s.close()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
