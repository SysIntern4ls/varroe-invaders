import pygame

'''
Sounds sind bis jetzt nur lehre mp3 Dateien, die ich noch austausche
'''

class Window:

    def __init__(self, renderWidth, renderHeight, windowWidth=2560, windowHeight=1440):
        self.renderWidth = renderWidth
        self.renderHeight = renderHeight

        self.screen = pygame.display.set_mode((windowWidth, windowHeight))
        pygame.display.set_caption("Invaders v0.1")

        self.renderSurface = pygame.Surface((renderWidth, renderHeight))

        self.clock = pygame.time.Clock()

    def getMousePos(self):
        currentWidth, currentHeight = self.screen.get_size()
        
        scaleX = currentWidth / self.renderWidth
        scaleY = currentHeight / self.renderHeight

        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX = int(mouseX / scaleX)
        mouseY = int(mouseY / scaleY)
        return mouseX, mouseY
         
    def newFrame(self):
        self.screen.fill((255,255,255))
        self.renderSurface.fill((255,255,255))
            
    def endFrame(self):
        scaledSurface = pygame.transform.smoothscale(self.renderSurface, self.screen.get_size())
        self.screen.blit(scaledSurface, (0, 0))
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

    def isFullscreen(self):
        return bool(pygame.display.get_surface().get_flags() & pygame.FULLSCREEN)
    
    def updateWindow(self, resolution: tuple[int, int], toggleFullscreen: bool):
        if toggleFullscreen:
            if self.isFullscreen():
                self.screen = pygame.display.set_mode(resolution, False) # Resets other flags as well but since there are no others in use its fine
            else:
                self.screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
        else: 
            self.screen = pygame.display.set_mode(resolution)
        


