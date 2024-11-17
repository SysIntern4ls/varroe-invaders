import pygame

from window     import Window
from baseEntity import BaseEntity, BasePlayer

window = Window(1000, 1000)

localPlayer = BasePlayer(window.Screen, "biene-sprite-sheet")

while True:
    window.newFrame()

    for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()




    localPlayer.show(False, 5, (100, 100))

    window.endFrame()