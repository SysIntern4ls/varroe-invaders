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


        # Remove Enemies that are marked for removal
        # Backwards iteration to avoid index errors
        for i in range(len(self.enemies) - 1, -1, -1):
            if self.enemies[i].hasState(GameObject.State.REMOVE_OBJECT):
                self.enemies.pop(i)
                
            

        # Spawn new enemies
        if len(self.enemies) < 5 and pygame.time.get_ticks() - self.lastEnemySpawnTime >= 500:
            self.enemies.append(Enemy(self.window.screen, "varroa", (35, 50)))
            self.lastEnemySpawnTime = pygame.time.get_ticks()

        # Collision checking
        for bullet in self.player.bullets:
            for enemy in self.enemies:
                if getDistance(bullet.positionX, bullet.positionY, enemy.positionX, enemy.positionY) < bullet.frameSize[0] / 2 + enemy.frameSize[0] / 2:
                    bullet.addState(GameObject.State.REMOVE_OBJECT)
                    enemy.addState(GameObject.State.REMOVE_OBJECT)
                    self.window.playSound("enemy-hit")
        
        for enemy in self.enemies:
            if getDistance(enemy.positionX, enemy.positionY, self.player.positionX, self.player.positionY) < enemy.frameSize[0] / 2 + self.player.frameSize[0] / 2:
                self.window.playSound("player-hit")
                self.running = False



    def render(self):
        self.window.newFrame()

        self.player.render(True, 6)

        for enemy in self.enemies:
            enemy.render(False)

        if not self.running:
            self.drawEndScreen()

        self.window.endFrame()

    def run(self):
        while True:
            self.handleInputs()
            self.update()
            self.render()
            self.window.clock.tick(30)

            if not self.running:
                while True:
                    pass
