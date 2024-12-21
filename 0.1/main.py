import pygame

from window     import Window
from gameObject import GameObject

window = Window(1000, 1000)

localPlayer = GameObject(window.screen, "biene-sprite-sheet")

while True:
    window.newFrame()


    for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

                
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:  
        localPlayer.move(0, 10)
    if keys[pygame.K_UP]:
        localPlayer.move(0, -10)
    if keys[pygame.K_RIGHT]:
        localPlayer.move(10, 0)
    if keys[pygame.K_LEFT]:
        localPlayer.move(-10, 0)


   
                    
                    

              

    localPlayer.render(True, 5, (100, 100))

    window.endFrame()


'''
    
'''