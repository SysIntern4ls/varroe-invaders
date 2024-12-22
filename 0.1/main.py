import pygame

from window     import Window
from gameObject import GameObject

window = Window(1000, 1000)

localPlayer = GameObject(window.screen, "biene-sprite-sheet", (100, 100))
localPlayer.moveTo(50, 500)

enemy = GameObject(window.screen, "varroa", (35, 50))
enemy.moveTo(700, 500)
while True:

    for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

    enemy.move(-7)

    #enemy.move(20, 0)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:  
        localPlayer.move(0, 10)
    if keys[pygame.K_UP]:
        localPlayer.move(0, -10)

    window.newFrame()
                       
    localPlayer.render(True, 5,)
    enemy.render(False)

    window.endFrame()



