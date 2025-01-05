import pygame

from gameObject import GameObject
from bullet     import Bullet

class Player(GameObject):
    def __init__(self, screen, image, frameSize):
        super().__init__(screen, image, frameSize)
        self.setPosition(0, 0, False)
        self.setVelocity(0, 0)
        self.bullets = []
        
    def update(self):
        super().update()

        for bullet in self.bullets:
            bullet.update()

        self.bullets = [bullet for bullet in self.bullets if not bullet.hasState(GameObject.State.REMOVE_OBJECT)]

    def render(self, isAnimated = False, maxFrames = 0):
        super().render(isAnimated, maxFrames)
        
        for bullet in self.bullets:
            bullet.render()

    def shoot(self):
        if not hasattr(self, "lastBulletSpawnTime"):
            self.lastBulletSpawnTime = 0
        if len(self.bullets) >= 3 or self.lastBulletSpawnTime + 500 >= pygame.time.get_ticks():
            return
        bullet = Bullet(self.screen, self.positionX + self.frameSize[0], self.positionY + self.frameSize[1] / 2)
        self.bullets.append(bullet)
        self.lastBulletSpawnTime = pygame.time.get_ticks()
