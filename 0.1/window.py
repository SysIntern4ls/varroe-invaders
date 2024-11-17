import pygame



class Window:

    def __init__(self, WindowWidth, WindowHeight):
         self.WindowWidth = WindowWidth
         self.WindowHeight = WindowHeight
         
         self.Screen = pygame.display.set_mode((WindowWidth, WindowHeight))
         pygame.display.set_caption("Invaders v0.1")

         self.clock = pygame.time.Clock()


         
    def newFrame(self):
        self.Screen.fill((255,255,255))

            

    def endFrame(self):
        pygame.display.flip()
        self.clock.tick(60)
        
