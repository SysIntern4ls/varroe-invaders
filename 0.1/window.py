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

    def close(self):
        pygame.quit()
        exit()

    def playSound(self, sound):
        pygame.mixer.Sound("0.1\\sounds\\" + sound + ".mp3").play()

    def playMusic(self, music, volume: float = 0.5):
        pygame.mixer.music.load("0.1\\sounds\\" + music + ".mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(volume)
        


