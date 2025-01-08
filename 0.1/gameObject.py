import pygame

from gameMath import clamp

class GameObject:

    class State:
        REMOVE_OBJECT = 1 << 0
        ANIMATED = 1 << 1

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
    

    def __init__(self, screen: pygame.Surface, imageName: str, frameSize: tuple[int, int] = (0, 0),  imagePath: str = "bilder\\", imageFormat: str = ".png"):
        self.frameSize = frameSize
        self.screen = screen
        self.image = pygame.image.load("0.1\\" + imagePath + imageName + imageFormat)
        

        #ObjectProperties
        self.currentState = int(0)
        self.setPosition(0,0)
        self.setVelocity(0,0)


    def update(self):
        self.move(self.velocityX, self.velocityY)

    """
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
    def render(self, isAnimated: bool = False, maxFrames: int = 0):
        # Drawing next frame of animated Object
        if isAnimated:
            # setting animated flag of object
            if not self.hasState(self.State.ANIMATED):
                self.addState(self.State.ANIMATED)
                self.currentFrame = 0

            # calculating offset needed for current frame
            frameOffset = self.currentFrame * (self.frameSize[0] + 1)

            # drawing current frame
            self.screen.blit(self.image,
                            (self.positionX, self.positionY),
                            (frameOffset, 0, self.frameSize[0], self.frameSize[1]))
            
            # checking if we have to start over
            if self.currentFrame < maxFrames:
                self.currentFrame += 1
            else: 
                self.currentFrame = 0

        # drawing Object without animation
        else:
            self.screen.blit(self.image, 
                            (self.positionX, self.positionY))

    #TODO: Implement resizing of animated Objects      
    def resize(self, frameSize: tuple[int, int]):
        if self.hasState(self.State.ANIMATED):
            pass
        else:
            self.frameSize = frameSize
            self.image = pygame.transform.smoothscale(self.image, frameSize)


    """
    Moves GameObject

    Parameters:
    -----------
    x: int
        Moves GameObject on x-axis by x-Amount
    y: int
        Moves GameObject on y-axis by y-Amount
    clamp: bool
        Wether x & y should be clamped
    """
    def move(self, x = 0, y = 0, restrictToScreen: bool = True):
        if restrictToScreen:
            self.positionX = clamp(self.positionX + x, 0, self.screen.get_size()[0] - self.frameSize[0])
            self.positionY = clamp(self.positionY + y, 0, self.screen.get_size()[1] - self.frameSize[1])
        else:
            self.positionX += x
            self.positionY += y


    """
    Teleports GameObject to X and Y coordinates
    
    Parameters:
    -----------
    x: int
        Teleports GameObject to x-coordinate
    y: int
        Teleports GameObject to y-coordinate
    clamp: bool
        Wether x & y should be clamped
    """
    def setPosition(self, x = 0, y = 0, restrictToScreen: bool = True):
        if restrictToScreen:
            self.positionX = clamp(x, 0, self.screen.get_size()[0] - self.frameSize[0])
            self.positionY = clamp(y, 0, self.screen.get_size()[1] - self.frameSize[1])
        else:
            self.positionX = x
            self.positionY = y

    def setVelocity(self, x = 0, y = 0):
        self.velocityX = x
        self.velocityY = y

    



