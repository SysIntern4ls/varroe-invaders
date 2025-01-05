# Importieren u. initialisieren der Pygame-Bibliothek
import pygame
from pygame.locals import *
import random
import math
pygame.init()

# Variablen/KONSTANTEN setzen
W, H = 800, 600
FPS  = 30
SCHWARZ = ( 0, 0, 0)
WEISS   = ( 255, 255, 255)

spielaktiv = True

spieler = pygame.image.load("bilder/biene-sprite-sheet.png")
bereich = ['','','','','','']
bereich[0] = (0,0,100,100)
bereich[1] = (101,0,100,100)
bereich[2] = (202,0,100,100)
bereich[3] = (303,0,100,100)
bereich[4] = (404,0,100,100)
bereich[5] = (505,0,100,100) 
animbereich = 0

spielerposY = 300
spielerbewegung = 0 

# Gegner
# gegnerBild = pygame.image.load("bilder/varroa.png")
# gegnerX = random.randint(W/2, W-50)
# gegnerY = random.randint(50, H-50)
# gegnerbewegung = 5

gegnerBild = []
gegnerX = []
gegnerY = []
gegnerbewegung = []

anzahlgegner = 5

for x in range(anzahlgegner):
    gegnerBild.append(pygame.image.load("bilder/varroa.png"))
    gegnerX.append(random.randint(int(W/2), int(W-50)))
    gegnerY.append(random.randint(50, int(H-50)))
    gegnerbewegung.append(5)

# Kugel
kugelBild = pygame.image.load("bilder/honigtropfen.png")
kugelX = 0
kugelY = 0
kugelXbewegung = 12
kugelstatus = False

siegpunkte = 0

# Definieren und Öffnen eines neuen Fensters
fenster = pygame.display.set_mode((W, H))
pygame.display.set_caption("Varroa Invaders")
clock = pygame.time.Clock()

# für Textausgabe
font = pygame.font.Font(None, 36)

# Musik/Soundeffekte einrichten
pygame.mixer.music.load('sound/bienensummen.mp3')
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(.4)

def gegner(nr, x, y):
    fenster.blit(gegnerBild[nr], (x, y))

def kugelfliegt(x, y):
    fenster.blit(kugelBild, (x, y))

def kollisionskontrolle(kugelX, kugelY, gegnerX, gegnerY):
    abstand = int( math.sqrt(math.pow(kugelX-gegnerX,2) + math.pow(kugelY-gegnerY,2)) )
    # print("Abstand zwichen Kugel und Gegner: ", abstand)

    if abstand < 25:
        return True
    else:
        return False

# Schleife Hauptprogramm
while spielaktiv:
    # Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        # Beenden bei [ESC] oder [X]
        if event.type==QUIT:
            spielaktiv = False

        if event.type == KEYDOWN:
            # print("Spieler hat Taste gedrückt")

            # Taste für Spieler 1
            if event.key == K_UP:
                # print("Spieler hat Pfeiltaste hoch gedrückt")
                spielerbewegung = -6
            elif event.key == K_DOWN:
                # print("Spieler hat Pfeiltaste runter gedrückt")
                spielerbewegung = 6
            elif event.key == K_ESCAPE:
                spielaktiv = False

            elif event.key == K_SPACE:
                # print("Kugel abfeuern")
                # nur möglich, wenn keine Kugel sichtbar ist
                if kugelstatus == False:
                    kugelstatus = True
                    kugelX = 200
                    kugelY = spielerposY+50

        if event.type == KEYUP:
            # print("Spieler stoppt bewegung")
            spielerbewegung = 0

    # Spiellogik
    if spielerbewegung  != 0:
        spielerposY += spielerbewegung 

    if spielerposY < 0:
        spielerposY = 0
        spielerbewegung = 0 

    if spielerposY > H - 90:
        spielerposY = H - 90
        spielerbewegung = 0 

    for x in range(len(gegnerBild)):
        gegnerY[x] += gegnerbewegung[x]

        if gegnerY[x] < 10:
            gegnerbewegung[x] *= -1
            gegnerX[x] -= 30

        if gegnerY[x] > H - 50:
            gegnerbewegung[x] *= -1
            gegnerX[x] -= 30

    if kugelstatus == True:
        kugelX += kugelXbewegung

        durchgang = 0
        for x in gegnerBild:
            if kollisionskontrolle(kugelX-30,kugelY-25,gegnerX[durchgang], gegnerY[durchgang]) == True:
                # Kugel hat getroffen
                # print("Kugel hat getroffen")
                siegpunkte += 1
                print("aktueller Stand der Siegpunkte: ", siegpunkte)
                kugelstatus = False

                #del gegnerNr[durchgang]
                del gegnerBild[durchgang]
                del gegnerX[durchgang]
                del gegnerY[durchgang]
                del gegnerbewegung[durchgang]

            durchgang += 1

        if kugelX > W:
            kugelstatus = False

     # Kontrolle auf gewonnen!#TODO: war mal gegnerNr versteh aber den sinn nicht
    if len(gegnerBild) == 0:
        print("Gewonnen!")
        spielaktiv = False

     # Spielfeld löschen
    fenster.fill(WEISS)

    # Siegpunkte ausgeben
    inhalt = "Punkte: {}".format(siegpunkte)
    text = font.render(inhalt, 1, SCHWARZ)
    fenster.blit(text, (20,20))

    # Spielfeld/figuren zeichnen
    animbereich  += 1

    if animbereich  > 5:
        animbereich  = 0

    fenster.blit(spieler, (100, spielerposY), bereich[animbereich])    

    if kugelstatus == True:
        kugelfliegt(kugelX,kugelY)

    for x in range(len(gegnerBild)):
        gegner(x, gegnerX[x], gegnerY[x])

    # Fenster aktualisieren
    pygame.display.flip()
    clock.tick(FPS)