import pygame
import random

from window     import Window
from gameObject import GameObject
from enemy      import Enemy
from player     import Player
from gameMath   import getDistance


class Game:
    def __init__(self):
        #Initialising pygame
        self.window = Window(1280, 720)

        #TODO: Change image to un watermarked version
        self.prop = GameObject(self.window.screen, "bienenstock", (1200, 1094))
        #Setting position and size of prop
        self.prop.setPosition(-330, -50, False)
        self.prop.resize((self.prop.frameSize[0] /1.4, self.prop.frameSize[1] /1.4))

        #Things happening on gamestart
        self.player = Player(self.window.screen, "biene-sprite-sheet", (100, 100))
        self.player.setPosition(90, 500)

        self.enemies = [Enemy(self.window.screen, "varroa", (35, 50))]
        self.lastEnemySpawnTime = 0

        self.running = True
        self.window.playMusic("bienensummen")

        
    def handleInputs(self):
        #Checking for keypresses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.player.move(0, 10)
        if keys[pygame.K_UP]:
            self.player.move(0, -10)
        if keys[pygame.K_SPACE]:
            self.player.shoot()

        # Checking if we want to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.window.close()

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                #TODO: Add pause menu
                print("Escape")

    def update(self):
        self.player.update()

        # Update all enemies
        for enemy in self.enemies:
            enemy.update()

        # Not realy the most efficient way to do this but looks way nicer and is easier to understand
        self.enemies = [enemy for enemy in self.enemies if not enemy.hasState(GameObject.State.REMOVE_OBJECT)]

        #TODO: Rework enemy spawning
        if len(self.enemies) < 5 and pygame.time.get_ticks() - self.lastEnemySpawnTime >= 500:
            self.enemies.append(Enemy(self.window.screen, "varroa", (35, 50)))
            self.lastEnemySpawnTime = pygame.time.get_ticks()

        for bullet in self.player.bullets:
            for enemy in self.enemies:
                if getDistance(bullet.positionX, bullet.positionY, enemy.positionX, enemy.positionY) < bullet.frameSize[0] + enemy.frameSize[0]:
                    bullet.addState(GameObject.State.REMOVE_OBJECT)
                    enemy.addState(GameObject.State.REMOVE_OBJECT)
                    self.window.playSound("enemy-hit")

        
        

    def render(self):
        self.window.newFrame()

        self.prop.render(False)               
        self.player.render(True, 5)

        for enemy in self.enemies:
            enemy.render(False)

        self.window.endFrame()

    def run(self):
        while self.running:
            self.handleInputs()
            self.update()
            self.render()
            self.window.clock.tick(30)