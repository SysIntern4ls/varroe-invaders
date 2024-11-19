import pygame

def clamp(value, minValue, maxValue):
    return max(minValue, min(value, maxValue))

class BaseEntity:
    positonX = 0
    positonY = 0

    isAnimated = False

    def __init__(self, screen: pygame.Surface, imageName: str, imagePath: str = "bilder\\", imageFormat: str = ".png"):
        self.screen = screen
        self.image = pygame.image.load("0.1\\" + imagePath + imageName + imageFormat)

    def show(self, isAnimated: bool = 0, maxFrames: int = 0, frameSize: tuple[int, int] = (0, 0)):
        self.size = frameSize
        if isAnimated:
            if self.isAnimated == False:
                self.isAnimated = True
                self.currentFrame = 0
            
            frameOffset = self.currentFrame * (frameSize[0] + 1)
            self.screen.blit(self.image ,(self.positonX, self.positonY), (frameOffset, 0, frameSize[0], frameSize[1]))

            if self.currentFrame < maxFrames:
                self.currentFrame += 1
            else: 
                self.currentFrame = 0
        else:
            if self.isAnimated == True:
                self.isAnimated = False
            self.screen.blit(self.image ,(self.positonX, self.positonY))



    def move(self, x = 0, y = 0):

        self.positonX = clamp(self.positonX + x, 0, self.screen.get_size()[0] - self.size[0])
        self.positonY = clamp(self.positonY + y, 0, self.screen.get_size()[1] - self.size[1])

    def moveTo(self, x = 0, y = 0):
        self.positonX = x
        self.positonY = y


class BasePlayer(BaseEntity):
    health = 0


    
