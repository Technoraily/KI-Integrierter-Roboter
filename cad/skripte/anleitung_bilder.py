exec(open(r'C:/Claude/KI-Integrierter Roboter/cad/skripte/anleitung_helfer.py', encoding='utf-8').read())
import math
ZIEL = r'C:/Claude/KI-Integrierter Roboter/docs/bauanleitung/schritte/'
HELL = ['Wange_Links','Wange_Rechts','Quertraeger_unten_links','Quertraeger_unten_rechts','Quertraeger_oben_links','Quertraeger_oben_rechts','Motor']
RIEMEN = ['Riemen_GT2_200','Riemen_3M_252','Riemen_5M_525']
RAHMEN = ['Wange_Links','Quertraeger_unten_links','Quertraeger_unten_rechts','Quertraeger_oben_links','Quertraeger_oben_rechts']
S = []  # (datei, [neue Teile], Kamera-Variante)
def s(d, neu, cam='links'): S.append((d, neu, cam))
s('00_ausgangslage', [])
s('01_motor', ['Motor','Ritzel_GT2_Z20'])
s('02_lager_links', ['Lager_A_links','Lager_B_links','Lager_O_links'])
s('03a_A_distanzring_links', ['Distanzring_A_links'])
s('03b_A_scheibe_z72', ['Scheibe_GT2_Z72'])
s('03c_A_ritzel_3m', ['Ritzel_3M_Z16'])
s('03d_A_distanzring_rechts', ['Distanzring_A_rechts'])
s('03e_A_welle', ['Welle_A'])
s('04e_B_welle', ['Welle_B'])
s('04b_B_ritzel_5m', ['Ritzel_5M_Z18'])
s('04f_B_scheibe_m8', ['Scheibe_M8_Ritzel'])
s('04c_B_scheibe_z64', ['Scheibe_3M_Z64'])
s('04d_B_distanzring_rechts', ['Distanzring_B_rechts'])
s('05a_O_scheibe_z90', ['Scheibe_5M_Z90'])
s('05b_O_welle', ['Welle_O'])
s('06_rolle_3m', ['Schraube_Rolle_3M','Huelse_3M_links','Lager_Rolle3M_1','Lager_Rolle3M_2','Huelse_3M_rechts'])
s('07_rolle_5m', ['Schraube_Rolle_5M','Huelse_5M_links','Lager_Rolle5M_1','Spannrolle_5M','Lager_Rolle5M_2','Huelse_5M_mitte','Huelse_5M_rechts'])
s('08a_riemen_gt2', ['Riemen_GT2_200'])
s('08b_riemen_3m', ['Riemen_3M_252'])
s('08c_riemen_5m', ['Riemen_5M_525'])
s('09_rechte_wange', ['Wange_Rechts','Lager_A_rechts','Lager_B_rechts','Lager_O_rechts'], 'rechts')
s('10_lasthebel', ['Lasthebel'], 'hoch')
s('11_messzeiger', ['Messzeiger'], 'hoch')
s('12_messuhrhalter', ['Messuhrhalter'], 'hoch')
# Gruppe 'Huelse_5M_mitte' o.ae. existiert evtl. nicht -> nur vorhandene
bereits = []
log = []
sichern()
dunkel = farbe('Anl_Riemen',(45,45,50)); hell = farbe('Anl_Hell',(226,230,236)); mittel = farbe('Anl_Mittel',(135,146,163)); neu_f = farbe('Anl_Neu',(255,110,0))
CAMS = {'links': ((-30,14,48),(0,11,2),36), 'rechts': ((-30,14,48),(0,11,2),36), 'hoch': ((-34,19,62),(0,18,6),58)}
platz = list(RAHMEN)
for datei, neu, cam in S:
    neu = [n for n in neu if n in BODY]
    sichtbar = set(platz) | set(neu)
    for o in OCC.values(): o.isLightBulbOn = True
    for n, b in BODY.items():
        b.isLightBulbOn = n in sichtbar
        b.opacity = 1.0
        if n in neu: b.appearance = neu_f
        elif n in HELL: b.appearance = hell
        elif n in RIEMEN: b.appearance = dunkel
        else: b.appearance = mittel
    if cam != 'links' and 'Wange_Rechts' in sichtbar and 'Wange_Rechts' not in neu:
        BODY['Wange_Rechts'].opacity = 0.35
    if datei.startswith('09'):
        BODY['Wange_Rechts'].opacity = 0.45
    e, z, br = CAMS[cam]
    kamera(eye=e, ziel=z, breite=br)
    ok = bild(ZIEL+datei+'.png', 1600, 1200)
    log.append((datei, ok, sorted(neu)))
    platz += neu
wiederherstellen()
'\n'.join(str(l) for l in log)
