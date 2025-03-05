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

        self.running = True
        self.paused = False
        self.gameOver = False
        self.isSaved = False

        self.playerScore = 0
        self.ui = UI(self.window, self.saveManager, self.resume, self.restart, self.quit)

        windowWidth, windowHeight = self.ui.resolutions[int(self.saveManager.saveData.get("resolution", 0))]
        self.window.updateWindow((windowWidth, windowHeight), int(self.saveManager.saveData.get("fullscreen", False)))
        self.gameStartTime = pygame.time.get_ticks()

        self.window.playMusic("bienensummen")
        
    def resume(self):
        self.paused = False

        # if you are bad at the game but still want to be the best
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

        if self.gameOver or self.paused:
            if not self.isSaved:
                self.saveManager.saveData["playerHighScore"] = max(int(self.saveManager.saveData.get("playerHighScore", "0")), self.playerScore)
                self.saveManager.save("gameData")
                self.isSaved = True
            return

        self.player.update()

        # Update all enemies
        for enemy in self.enemies:
            enemy.update()

        # add score for every frame
        self.playerScore += 1

        # Remove Enemies that are marked for removal
        # Backwards iteration to avoid index errors
        for i in range(len(self.enemies) - 1, -1, -1):
            if self.enemies[i].hasState(Enemy.State.OFFSCREEN) or self.enemies[i].hasState(Enemy.State.WASHIT):
                if self.enemies[i].hasState(Enemy.State.OFFSCREEN):
                    self.playerScore -= 50
                self.enemies.pop(i)

        # Spawn new enemies
        if len(self.enemies) < 5 and pygame.time.get_ticks() - self.lastEnemySpawnTime >= 500:
            self.enemies.append(Enemy(self.window.renderSurface, "varroa", (35, 50)))
            self.lastEnemySpawnTime = pygame.time.get_ticks()

        # Checking for collisions between enemies and bullets
        for bullet in self.player.bullets:
            for enemy in self.enemies:
                if pygame.sprite.collide_mask(bullet, enemy):
                    bullet.addState(Bullet.State.WASHIT)
                    enemy.addState(Enemy.State.WASHIT)
                    self.window.playSound("enemy-hit")
                    self.playerScore += 150
        
        # Checking for collisions between enemies and player
        for enemy in self.enemies:
            if pygame.sprite.collide_mask(self.player, enemy):
                self.window.playSound("player-hit")
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
