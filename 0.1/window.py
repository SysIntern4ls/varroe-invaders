import pygame



class Window:

    def __init__(self, windowWidth, windowHeight):
         self.windowWidth = windowWidth
         self.windowHeight = windowHeight
         
         self.screen = pygame.display.set_mode((windowWidth, windowHeight))
         pygame.display.set_caption("Invaders v0.1")

         self.clock = pygame.time.Clock()


         
    def newFrame(self):
        self.screen.fill((255,255,255))

            

    def endFrame(self):
        pygame.display.flip()
        


