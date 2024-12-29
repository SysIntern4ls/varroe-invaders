import pygame
import random

from gameMath import clamp
from gameObject import GameObject

class Enemy(GameObject):
    def __init__(self, screen, image, frameSize):
        super().__init__(screen, image, frameSize)
        
        self.setVelocity(-5, 9)
        self.setPosition(self.screen.get_size()[0] + self.frameSize[0]
                        ,random.randint(0, self.screen.get_size()[1]))
        
    def move(self, x = 0, y = 0, restrictToScreen: bool = True):
        x = clamp(self.positionX + x, -self.frameSize[0], self.screen.get_size()[0] - self.frameSize[0])
        y = clamp(self.positionY + y, 0, self.screen.get_size()[1] - self.frameSize[1])
        self.setPosition(x, y, False)

    def update(self):
        super().update()

        # Bounce off upper and lower screen borders
        if self.positionY == 0 or self.positionY >= self.screen.get_size()[1] - self.frameSize[1]:
            self.setVelocity(self.velocityX, -self.velocityY)
        
        if self.positionX == -self.frameSize[0]:
            self.addState(self.State.REMOVE_OBJECT)
        