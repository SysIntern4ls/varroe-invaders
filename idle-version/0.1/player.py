import pygame

from gameObject import GameObject
from bullet     import Bullet

class Player(GameObject):
    def __init__(self, screen, image, frameSize, velocityX = 0, velocityY = 0):
        super().__init__(screen, image, frameSize)
        self.setPosition(0, 0, False)
        self.setVelocity(velocityX, velocityY)

        # Bullets
        self.bullets = []
        self.lastBulletSpawnTime = 0
        self.maxBullets = 3
        
    def update(self):
        super().update()

        for bullet in self.bullets:
            bullet.update()

        for i in range(len(self.bullets) - 1, -1, -1):
            if self.bullets[i].hasState(GameObject.State.OFFSCREEN):
                self.bullets.pop(i)

    def render(self, isAnimated = False, maxFrames = 0):
        super().render(isAnimated, maxFrames)
        
        for bullet in self.bullets:
            bullet.render()

    def shoot(self):
        if len(self.bullets) >= self.maxBullets or self.lastBulletSpawnTime + 500 >= pygame.time.get_ticks():
            return
        bullet = Bullet(self.screen, self.positionX + self.frameSize[0], self.positionY + self.frameSize[1] / 2)
        self.bullets.append(bullet)
        self.lastBulletSpawnTime = pygame.time.get_ticks()
