# Importieren u. initialisieren der Pygame-Bibliothek
import pygame
from pygame.locals import *
import random
import math

'''Spiel Init'''

## initialisieren
pygame.init()

# Variablen/KONSTANTEN setzen
W, H = 800, 600
FPS  = 30
SCHWARZ = ( 0, 0, 0)
WEISS   = ( 255, 255, 255)

siegpunkte = 0
spielaktiv = True

'''Spiel Init'''

'''Biene Init'''

spieler = pygame.image.load("0.1/bilder/biene-sprite-sheet.png")
bereich = ['','','','','','']
bereich[0] = (0,0,100,100)
bereich[1] = (101,0,100,100)
bereich[2] = (202,0,100,100)
bereich[3] = (303,0,100,100)
bereich[4] = (404,0,100,100)
bereich[5] = (505,0,100,100)
spielerAnimFrame = 0

spielerposY = 300
spielerbewegung = 0

'''Biene Init'''

'''Gegner Init'''

gegnerBild = []
gegnerX = []
gegnerY = []
gegnerbewegung = []

anzahlgegner = 5

for x in range(anzahlgegner):
    gegnerBild.append(pygame.image.load("0.1/bilder/varroa.png"))
    gegnerX.append(random.randint(int(W/2), int(W-50)))
    gegnerY.append(random.randint(50, int(H-50)))
    gegnerbewegung.append(5)

'''Gegner Init'''

'''Kugel Init'''

# Kugel
kugelBild = pygame.image.load("0.1/bilder/honigtropfen.png")
kugelX = 0
kugelY = 0
kugelXbewegung = 12
kugelstatus = False

'''Kugel Init'''


'''Pygame Init'''

# Definieren und Öffnen eines neuen Fensters
fenster = pygame.display.set_mode((W, H))
pygame.display.set_caption("Varroa Invaders")
clock = pygame.time.Clock()

# für Textausgabe
font = pygame.font.Font(None, 36)

# Musik/Soundeffekte einrichten
pygame.mixer.music.load('0.1/sounds/bienensummen.mp3')
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(.4)

'''Pygame Init'''


'''Funktionen'''

# Funktion um Gegner zu zeichnen
def gegner(nr, x, y):
    fenster.blit(gegnerBild[nr], (x, y))

# Funktion um Kugel zu zeichnen
def kugelfliegt(x, y):
    fenster.blit(kugelBild, (x, y))

# Funktion um Kollision zu überprüfen
def kollisionskontrolle(kugelX, kugelY, gegnerX, gegnerY, size = 25):
    abstand = int( math.sqrt(math.pow(kugelX - gegnerX,2) + math.pow(kugelY-gegnerY,2)) )

    if abstand < size:
        return True
    else:
        return False

'''Funktionen'''

# Schleife Hauptprogramm
while spielaktiv:

    '''Spiel Kontrolle nach Aktion'''

    # Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        # Beenden bei [ESC] oder [X]
        if event.type == QUIT:
            spielaktiv = False

        if event.type == KEYDOWN:
           
            # Taste für Spieler 1
            if event.key == K_UP:
                spielerbewegung = -6

            elif event.key == K_DOWN:
                spielerbewegung = 6

            elif event.key == K_ESCAPE:
                spielaktiv = False

            elif event.key == K_SPACE:
                # nur möglich, wenn keine Kugel sichtbar ist
                if kugelstatus == False:
                    kugelstatus = True
                    kugelX = 200
                    kugelY = spielerposY + 50

        if event.type == KEYUP:
            spielerbewegung = 0

        '''Spiel Kontrolle nach Aktion'''

    '''Spieler Bewegung'''
    
    if spielerbewegung  != 0:
        spielerposY += spielerbewegung 

    if spielerposY < 0:
        spielerposY = 0
        spielerbewegung = 0 

    if spielerposY > H - 90:
        spielerposY = H - 90
        spielerbewegung = 0 

    '''Spieler Bewegung'''

    '''Gegner Bewegung'''

    for x in range(len(gegnerBild)):
        gegnerY[x] += gegnerbewegung[x]

        if gegnerY[x] < 10:
            gegnerbewegung[x] *= -1
            gegnerX[x] -= 30

        if gegnerY[x] > H - 50:
            gegnerbewegung[x] *= -1
            gegnerX[x] -= 30

    '''Gegner Bewegung'''

    '''Kugel Bewegung'''

    if kugelstatus == True:
        kugelX += kugelXbewegung

        '''Kugel Bewegung'''

        '''Kollisionskontrolle zwischen Kugel und Gegner'''

        i = 0
        while i < len(gegnerBild):

            if kollisionskontrolle(kugelX-30,kugelY-25,gegnerX[i], gegnerY[i]) == True:
                # Kugel hat getroffen
                siegpunkte += 1
                print("aktueller Stand der Siegpunkte: ", siegpunkte)
                kugelstatus = False

                del gegnerBild[i]
                del gegnerX[i]
                del gegnerY[i]
                del gegnerbewegung[i]

            else:
                i += 1

        '''Kollisionskontrolle zwischen Kugel und Gegner'''

        '''Kugel ausserhalb des Spielfeldes'''

        if kugelX > W:
            kugelstatus = False

        '''Kugel ausserhalb des Spielfeldes'''

    '''Spiel Kontrolle auf gewonnen/verloren'''

    if len(gegnerBild) == 0:
        print("Gewonnen!")
        spielaktiv = False

    for x in range(len(gegnerBild)):
        if kollisionskontrolle(200, spielerposY, gegnerX[x], gegnerY[x]) == True:
                print("Verloren!")
                spielaktiv = False

    '''Spiel Kontrolle auf gewonnen/verloren'''

    '''Spiel Spielfeld löschen'''
    
    fenster.fill(WEISS)

    '''Spiel Spielfeld löschen'''

    '''Spiel Spielfeld/figuren zeichnen'''

    # Siegpunkte ausgeben
    inhalt = "Punkte: {}".format(siegpunkte)
    text = font.render(inhalt, 1, SCHWARZ)
    fenster.blit(text, (20,20))

    spielerAnimFrame  += 1
    if spielerAnimFrame  > 5:
        spielerAnimFrame  = 0

    fenster.blit(spieler, (100, spielerposY), bereich[spielerAnimFrame])  

    # draw collision circle
    pygame.draw.circle(fenster, SCHWARZ, (kugelX + 30 // 2, kugelY + 25 // 2), 12.5, 2)
    for x in range(len(gegnerBild)):
        pygame.draw.circle(fenster, SCHWARZ, (gegnerX[x], gegnerY[x]), 12.5, 2)

    if kugelstatus == True:
        kugelfliegt(kugelX,kugelY)

    for x in range(len(gegnerBild)):
        gegner(x, gegnerX[x], gegnerY[x])

    # Fenster aktualisieren
    pygame.display.flip()
    clock.tick(5)

    '''Spiel Spielfeld/figuren zeichnen'''