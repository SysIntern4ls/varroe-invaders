import pygame
import random

from window         import Window
from gameObject     import GameObject
from enemy          import Enemy
from player         import Player
from ui             import UI
from saveManager    import SaveManager
from bullet         import Bullet


class Game:
    def __init__(self):
        self.saveManager = SaveManager("game")

        #Initialising pygame
        self.saveManager.load("gameData")
        self.window = Window(1280, 720)

        #Things happening on gamestart
        self.player = Player(self.window.renderSurface, "biene-sprite-sheet", (100, 100))
        self.player.setPosition(90, 500)

        self.enemies = [Enemy(self.window.renderSurface, "varroa", (35, 50))]
        self.lastEnemySpawnTime = 0
        self.maxEnemieCount = 5

        self.running = True
        self.paused = False
        self.gameOver = False
        self.isSaved = False

        self.playerScore = 0
        self.ui = UI(self.window, self.saveManager, self.resume, self.restart, self.quit)

        windowWidth, windowHeight = self.ui.resolutions[int(self.saveManager.saveData.get("resolution", 0))]
        self.window.updateWindow((windowWidth, windowHeight), int(self.saveManager.saveData.get("fullscreen", False)))
        self.gameStartTime = pygame.time.get_ticks()
        
    def resume(self):
        self.paused = False

        # cheats
        if self.gameOver:
            if pygame.mouse.get_pressed()[1] or hasattr(self, "godMode"):
                self.gameOver = False
                self.godMode = True

    def restart(self):
        self.saveManager.save("gameData")
        self.isSaved = False
        self.__init__()
        self.gameStartTime = pygame.time.get_ticks()

    def quit(self):
        self.saveManager.save("gameData")
        self.running = False
        self.window.close()
        exit()

        
    def handleInputs(self):
        #Checking for keypresses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            if not (self.gameOver or self.paused):
                self.player.move(0, 10)
        if keys[pygame.K_UP]:
            if not (self.gameOver or self.paused):
                self.player.move(0, -10)
        if keys[pygame.K_SPACE]:
            if not (self.gameOver or self.paused):
                self.player.shoot()

        # Checking if we want to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused


    def update(self):
        # Stop updating if the game is over or paused
        if self.gameOver or self.paused:
            if not self.isSaved:
                self.saveManager.saveData["playerHighScore"] = max(int(self.saveManager.saveData.get("playerHighScore", "0")), self.playerScore)
                self.saveManager.save("gameData")
                self.isSaved = True
            return

        # Update opjects
        self.player.update()

        # Update all enemies
        for enemy in self.enemies:
            enemy.update()

        # add score for every frame that the player survives
        self.playerScore += 1

        # change amount of total enemies based on score
        self.maxEnemieCount = 5 + self.playerScore // 1000 
        self.player.maxBullets = 3 + self.playerScore // 10000

        # Backwards iteration to avoid index errors
        for i in range(len(self.enemies) - 1, -1, -1):
            # Remove Enemies that are marked for removal
            if self.enemies[i].hasState(Enemy.State.OFFSCREEN) or self.enemies[i].hasState(Enemy.State.WAS_HIT):
                if self.enemies[i].hasState(Enemy.State.OFFSCREEN):
                    self.playerScore -= 50
                self.enemies.pop(i)

        # Spawn new enemies
        if len(self.enemies) < self.maxEnemieCount and pygame.time.get_ticks() - self.lastEnemySpawnTime >= 500:

            self.enemies.append(Enemy(self.window.renderSurface, "varroa", (35, 50)))

            self.lastEnemySpawnTime = pygame.time.get_ticks()

        # Checking for collisions between enemies and bullets
        for bullet in self.player.bullets:
            for enemy in self.enemies:
                if pygame.sprite.collide_mask(bullet, enemy):
                    bullet.addState(Bullet.State.WAS_HIT)
                    enemy.addState(Enemy.State.WAS_HIT)
                    self.playerScore += 150
        
        # Checking for collisions between enemies and player
        for enemy in self.enemies:
            if pygame.sprite.collide_mask(self.player, enemy):
                if hasattr(self, "godMode"):
                    return
                self.gameOver = True

    def render(self):
        self.window.newFrame()

        self.player.render(True, 6)

        for enemy in self.enemies:
            enemy.render(False)

        self.ui.render(
            playerScore = self.playerScore,
            bulletsRemaining = self.player.maxBullets - len(self.player.bullets),
            gameTime = pygame.time.get_ticks() - self.gameStartTime,
            paused = self.paused,
            gameOver = self.gameOver
        )

        #DEBUG: Draw collision masks of player, bullets and enemies
        if int(self.saveManager.saveData.get("showCollisions", 0)) == True:
            for x in range(self.player.mask.get_size()[0]):
                    for y in range(self.player.mask.get_size()[1]):
                        if self.player.mask.get_at((x, y)):
                            self.window.renderSurface.set_at((int(x + self.player.positionX), int(y + self.player.positionY)), (0,255,0))

            for bullet in self.player.bullets:
                for x in range(bullet.mask.get_size()[0]):
                    for y in range(bullet.mask.get_size()[1]):
                        if bullet.mask.get_at((x, y)):
                            self.window.renderSurface.set_at((int(x + bullet.positionX), int(y + bullet.positionY)), (0,255,0))
            for enemy in self.enemies:
                    for x in range(enemy.mask.get_size()[0]):
                        for y in range(enemy.mask.get_size()[1]):
                            if enemy.mask.get_at((x, y)):
                                self.window.renderSurface.set_at((int(x + enemy.positionX), int(y + enemy.positionY)), (0,255,0))

        self.window.endFrame()

    def run(self):
        while True:
            self.handleInputs()

            self.update()

            self.render()

            self.window.clock.tick(30)

            if not self.running:
                self.quit()
                break
