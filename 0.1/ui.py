import pygame
import pygame.freetype

from window import Window
from saveManager import SaveManager

class UI:
    def __init__(self, window: Window, saveManager : SaveManager, resumeCallback, restartCallback, quitCallback):
        self.saveManager = saveManager
        self.saveManager.load("gameData")

        self.window = window
        self.font = pygame.font.Font("0.1\\fonts\\Roboto_Condensed-Regular.ttf", 24)
        self.largeFont = pygame.font.Font("0.1\\fonts\\Roboto_Condensed-Regular.ttf", 50)
        self.wasButtonClicked = False

        self.buttonWidth, self.buttonHeight = 250, 60
        self.buttonSpacing = 20

        self.currResolution = 0 if self.saveManager.saveData.get("resolution") == None else int(self.saveManager.saveData.get("resolution"))
        self.resolutions = [(1280, 720), (1920, 1080), (2560, 1440), (3840, 2160)]

        self.resumeCallback = resumeCallback
        self.restartCallback = restartCallback
        self.quitCallback = quitCallback

    def render(self, playerScore, bulletsRemaining, gameTime, paused=False, gameOver=False):
        # Render HUD
        if not paused and not gameOver:
            self._renderHud(playerScore, bulletsRemaining, gameTime)
            return

        # Render Pause Menu
        if paused:
            self._renderPauseMenu()
            return
            
        # Render Game Over Screen
        if gameOver:
            self._renderGameOverScreen()
            return
    
    def __renderBackgroundTransparent(self):
        #DEBUG: Dont make background transparent if collision dbg enabled for ez screenshots
        if int(self.saveManager.saveData.get("showCollisions", 0)) == True:
            return

        screenWidth, screenHeight = self.window.renderSurface.get_size()

        # Create a blurred background using multiple scaled smooth surfaces for better quality
        screenCopy = pygame.Surface((screenWidth, screenHeight))
        screenCopy.blit(self.window.renderSurface, (0, 0))  # Copy current screen

        for _ in range(3):  # Multiple blurs for a smoother effect
            screenCopy = pygame.transform.smoothscale(screenCopy, (screenWidth // 2, screenHeight // 2))
            screenCopy = pygame.transform.smoothscale(screenCopy, (screenWidth, screenHeight))

        # Create a semi-transparent overlay to darken the background
        overlay = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Dark overlay for better contrast

        # Draw the blurred background and overlay
        self.window.renderSurface.blit(screenCopy, (0, 0))
        self.window.renderSurface.blit(overlay, (0, 0))

    def _renderHud(self, playerScore, bulletsRemaining, gameTime):
        # Render Score
        score_text = self.font.render(f"Score: {playerScore}", True, (0, 0, 0))
        self.window.renderSurface.blit(score_text, (10, 10))

        # Render Bullets
        bullets_text = self.font.render(f"Bullets: {bulletsRemaining}", True, (0, 0, 0))
        self.window.renderSurface.blit(bullets_text, (10, 40))

        # Render Time
        time_text = self.font.render(f"Time: {gameTime//1000}", True, (0, 0, 0))
        self.window.renderSurface.blit(time_text, (10, 70))


    def __renderButton(self, color: tuple[int, int, int], text: str, position: tuple[int, int], size: tuple[int, int], font: pygame.freetype.Font):
        mouseX, mouseY = self.window.getMousePos()

        if position[0] <= mouseX <= position[0] + size[0] and position[1] <= mouseY <= position[1] + size[1]:
            isHovered = True
        else:
            isHovered = False

        buttonColor = tuple(max(0, x - 50) for x in color) if isHovered else color

        pygame.draw.rect(self.window.renderSurface, buttonColor, (position[0], position[1], size[0], size[1]), border_radius=15)
        text = font.render(text, True, (255, 255, 255))
        rect = text.get_rect(center=(position[0] + size[0] // 2, position[1] + size[1] // 2))
        self.window.renderSurface.blit(text, rect)

        if pygame.mouse.get_pressed()[0]:
            if isHovered and not self.wasButtonClicked:
                self.wasButtonClicked = True
                return True
        else:
            self.wasButtonClicked = False
        return False

    def _renderPauseMenu(self):
        screenWidth, screenHeight = self.window.renderSurface.get_size()

        self.__renderBackgroundTransparent()

        # Render highest Score
        playerHighScore = 0 if self.saveManager.saveData.get("playerHighScore") == None else int(self.saveManager.saveData.get("playerHighScore"))
        score_text = self.font.render(f"Highest achieved score: {playerHighScore}", True, (0, 0, 0))
        self.window.renderSurface.blit(score_text, (10, 10))

        # Resolution Buttons
        arrowButtonSize = (40, 40)
        arrowButtonColor = (255, 70, 70)

        if self.currResolution > 0:
            if self.__renderButton(arrowButtonColor,
                                "<",
                                (screenWidth // 2 - self.buttonWidth // 2, screenHeight // 2 - self.buttonHeight * 2 - self.buttonSpacing * 1.5),
                                arrowButtonSize,
                                self.font):
                self.currResolution -= 1
                self.window.updateWindow(self.resolutions[self.currResolution], False)
                self.saveManager.saveData["resolution"] = self.currResolution

        if self.__renderButton((100, 100, 100),
                            str(self.resolutions[self.currResolution][0]) + " x " + str(self.resolutions[self.currResolution][1]),
                            (screenWidth // 2 - self.buttonWidth // 2 + arrowButtonSize[0] + self.buttonSpacing // 2, screenHeight // 2 - self.buttonHeight * 2 - self.buttonSpacing * 1.5),
                            (self.buttonWidth - 2 * arrowButtonSize[0] - self.buttonSpacing, arrowButtonSize[1]),
                            self.font):
            pass
        
        if self.currResolution < len(self.resolutions) - 1:
            if self.__renderButton(arrowButtonColor,
                                ">",
                                (screenWidth // 2 + self.buttonWidth // 2 - arrowButtonSize[0], screenHeight // 2 - self.buttonHeight * 2 - self.buttonSpacing * 1.5),
                                arrowButtonSize,
                                self.font):
                self.currResolution += 1
                self.window.updateWindow(self.resolutions[self.currResolution], False)
                self.saveManager.saveData["resolution"] = self.currResolution

        # Fullscreen Button
        if self.__renderButton((100, 100, 100),
                            "Toggle Fullscreen",
                            (screenWidth // 2 - self.buttonWidth // 2, screenHeight // 2 - self.buttonHeight - self.buttonSpacing * 2),
                            (self.buttonWidth, self.buttonHeight), 
                            self.font):
            self.window.updateWindow(self.resolutions[self.currResolution], True)
            self.saveManager.saveData["fullscreen"] = int(self.window.isFullscreen())


        # Resume Button
        if self.__renderButton((255, 70, 70),
                            "Resume",
                            (screenWidth // 2 - self.buttonWidth // 2, screenHeight // 2 - self.buttonHeight // 2), 
                            (self.buttonWidth, self.buttonHeight), 
                            self.font):
            self.resumeCallback()

        # Quit Button
        if self.__renderButton((100, 100, 100), 
                            "Quit", 
                            (screenWidth // 2 - self.buttonWidth // 2, screenHeight // 2 + self.buttonHeight // 2 + self.buttonSpacing // 2), 
                            (self.buttonWidth, self.buttonHeight), 
                            self.font):
            self.quitCallback()

    def _renderGameOverScreen(self):
        self.__renderBackgroundTransparent()

        screenWidth, screenHeight = self.window.renderSurface.get_size()

        # Render "Game Over" Text
        gameOverText = self.largeFont.render("GAME OVER", True, (255, 70, 70))
        gameOverRect = gameOverText.get_rect(center=(screenWidth // 2, screenHeight // 2 - 100))
        self.window.renderSurface.blit(gameOverText, gameOverRect)
        
        # Restart Button
        if self.__renderButton((255, 70, 70),
                            "Restart", 
                            (screenWidth // 2 - self.buttonWidth // 2, screenHeight // 2 - self.buttonHeight // 2), 
                            (self.buttonWidth, self.buttonHeight), 
                            self.font):
            self.restartCallback()

        # Quit Button
        
        if self.__renderButton((100, 100, 100), 
                            "Quit", 
                            (screenWidth // 2 - self.buttonWidth // 2, screenHeight // 2 + self.buttonHeight // 2 + self.buttonSpacing), 
                            (self.buttonWidth, self.buttonHeight), 
                            self.font):
            self.quitCallback()