import pygame
import random

from window     import Window
from gameObject import GameObject


class Game:
    def __init__(self):
        #Initialising pygame
        self.window = Window(1280, 720)

        #TODO: Change image to un watermarked version
        self.prop = GameObject(self.window.screen, "bienenstock", (1200, 1094))
        self.prop.moveTo(-330, -50, False)
        self.prop.reSize((self.prop.frameSize[0] /1.4, self.prop.frameSize[1] /1.4))

        #Things happening on gamestart
        self.player = GameObject(self.window.screen, "biene-sprite-sheet", (100, 100))
        self.player.moveTo(90, 500)

        self.enemy = GameObject(self.window.screen, "varroa", (35, 50))
        self.enemy.moveTo(random.randint(100, self.window.windowWidth)
                        ,random.randint(0, self.window.windowHeight))
        self.enemy.setVelocity(-5, 9)
        
        self.running = True
        
    def handleEvents(self):
        # Checking if we want to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.player.move(0, 10)
        if keys[pygame.K_UP]:
            self.player.move(0, -10)

    def update(self):

        #TODO:
        #-Remove X for final version(only for fun)
        #-Move Y to better Spot (maybe Collision manager)
        if self.enemy.positionY == 0 or self.enemy.positionY >= self.window.windowHeight - self.enemy.frameSize[1]:
            self.enemy.setVelocity(self.enemy.velocityX, -self.enemy.velocityY)
        if self.enemy.positionX == 0 or self.enemy.positionX >= self.window.windowWidth - self.enemy.frameSize[0]:
            self.enemy.setVelocity(-self.enemy.velocityX, self.enemy.velocityY)

        self.enemy.update()

    def render(self):
        self.window.newFrame()

        self.prop.render(False)               
        self.player.render(True, 5,)
        self.enemy.render(False)

        self.window.endFrame()

    def run(self):
        while self.running:
            self.handleEvents()
            self.update()
            self.render()