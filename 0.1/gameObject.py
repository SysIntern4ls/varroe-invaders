import pygame
from gameMath import clamp

class GameObject:

    class State:
        ANIMATED = 1 << 0

    """
    Object state system using bitmasks
    """
    def hasState(self, state: int):
        return (self.currentState & state) != 0
    
    def addState(self, state: int):
        self.currentState |= state
    
    def removeState(self, state: int):
        self.currentState &= ~state
    
    def toggleState(self, state: int):
        self.currentState ^= state
    

    def __init__(self, screen: pygame.Surface, imageName: str, imagePath: str = "bilder\\", imageFormat: str = ".png"):
        self.screen = screen
        self.image = pygame.image.load("0.1\\" + imagePath + imageName + imageFormat)

        #ObjectProperties
        self.currentState = 0
        self.positionX = 0
        self.positionY = 0


    """
    TODO: does currently not support changing from animated to not animated and vice versa

    Rendering of both static aswell as animated objects.

    Parameters:
    -----------
    isAnimated: bool
        Bool to specifie if object should be animated.
    maxFrames: int
        Total Frames to be drawn.
    frameSize: tuple[int, int]
        Size of a singular frame.
    """
    def render(self, isAnimated: bool = False, maxFrames: int = 0, frameSize: tuple[int, int] = (0, 0)):
        self.frameSize = frameSize
        # Drawing next frame of animated Object
        if isAnimated:
            # setting animated flag of object
            if not self.hasState(self.State.ANIMATED):
                self.addState(self.State.ANIMATED)
                self.currentFrame = 0

            # calculating offset needed for current frame
            frameOffset = self.currentFrame * (frameSize[0] + 1)

            # drawing current frame
            self.screen.blit(self.image ,
                            (self.positionX, self.positionY), 
                            (frameOffset, 0, frameSize[0], frameSize[1]))
            
            # checking if we have to start over
            if self.currentFrame < maxFrames:
                self.currentFrame += 1
            else: 
                self.currentFrame = 0

        # drawing Object without animation
        else:
            self.screen.blit(self.image, 
                            (self.positionX, self.positionY))
    
    


    """
    Moves GameObject

    Parameters:
    -----------
    x: int
        Moves GameObject on x-axis by x-Amount
    y: int
        Moves GameObject on y-axis by y-Amount
    """
    def move(self, x = 0, y = 0):
        self.positionX = clamp(self.positionX + x, 0, self.screen.get_size()[0] - self.frameSize[0])
        self.positionY = clamp(self.positionY + y, 0, self.screen.get_size()[1] - self.frameSize[1])

    """
    Teleports GameObject to X and Y coordinates
    
    Parameters:
    -----------
    x: int
        Teleports GameObject to x-coordinate
    y: int
        Teleports GameObject to y-coordinate
    """
    def moveTo(self, x = 0, y = 0):
        self.positionX = x
        self.positionY = y


