import pygame

class BaseEntity:
    PositonX = 0
    PositonY = 0

    IsAnimated = False

    def __init__(self, Screen: pygame.Surface, ImageName: str, ImagePath: str = "bilder\\", ImageFormat: str = ".png"):
        self.Screen = Screen
        self.Image = pygame.image.load(ImagePath + ImageName + ImageFormat)

    def show(self, IsAnimated: bool = 0, MaxFrames: int = 0, FrameSize: tuple[int, int] = (0, 0)):
        if IsAnimated:
            if self.IsAnimated == False:
                self.IsAnimated = True
                self.CurrentFrame = 0
            
            FrameOffset = self.CurrentFrame * (FrameSize[0] + 1)
            self.Screen.blit(self.Image ,(self.PositonX, self.PositonY), (FrameOffset, 0, FrameSize[0], FrameSize[1]))

            if self.CurrentFrame < MaxFrames:
                self.CurrentFrame += 1
            else: 
                self.CurrentFrame = 0

        else:
            if self.IsAnimated == True:
                self.IsAnimated = False
            self.Screen.blit(self.Image ,(self.PositonX, self.PositonY))



    def move(self, x = 0, y = 0):
        self.PositonX += x
        self.PositonY += y

    def moveTo(self, x = 0, y = 0):
        self.PositonX = x
        self.PositonY = y

class BasePlayer(BaseEntity):
    health = 0

    
