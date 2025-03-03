from gameObject import GameObject

class Bullet(GameObject):
    def __init__(self, screen, positionX, positionY, velocityX = 10, velocityY = 0):
        super().__init__(screen, "honigtropfen", (10, 10))
        self.setPosition(positionX, positionY, False)
        self.setVelocity(velocityX, velocityY)

    def update(self):
        super().update()
        # Remove bullet if it goes off-screen
        if self.positionX >= self.screen.get_size()[0] - self.frameSize[0]:
            self.addState(self.State.OFFSCREEN)