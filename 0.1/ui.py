import pygame
import pygame.freetype

from window import Window

class UI:
    def __init__(self, window: Window, resumeCallback, restartCallback, quitCallback):
        self.window = window
        self.font = pygame.font.Font("0.1\\fonts\\Roboto_Condensed-Regular.ttf", 24)
        self.largeFont = pygame.font.Font("0.1\\fonts\\Roboto_Condensed-Regular.ttf", 50)
        self.wasButtonClicked = False

        self.buttonWidth, self.buttonHeight = 250, 60
        self.buttonSpacing = 20

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

    
    def _renderHud(self, player_score, bullets_remaining, game_time):
        # Render Score
        score_text = self.font.render(f"Score: {player_score}", True, (0, 0, 0))
        self.window.renderSurface.blit(score_text, (10, 10))

        # Render Bullets
        bullets_text = self.font.render(f"Bullets: {bullets_remaining}", True, (0, 0, 0))
        self.window.renderSurface.blit(bullets_text, (10, 40))

        # Render Time
        time_text = self.font.render(f"Time: {game_time//1000}", True, (0, 0, 0))
        self.window.renderSurface.blit(time_text, (10, 70))

    def __renderBackgroundTransparent(self):
        # Get screen dimensions
        screenWidth, screenHeight = self.window.renderSurface.get_size()

        # Create a blurred background using multiple scaled smooth surfaces for better quality
        screenCopy = pygame.Surface((screenWidth, screenHeight))
        screenCopy.blit(self.window.renderSurface, (0, 0))  # Copy current screen

        for _ in range(3):  # Multiple blurs for a smoother effect
            screenCopy = pygame.transform.smoothscale(screenCopy, (screenWidth // 2, screenHeight // 2))
            screenCopy = pygame.transform.smoothscale(screenCopy, (screenWidth, screenHeight))

        # Create a semi-transparent overlay to darken the background
        overlay = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Dark overlay for better contrast (alpha=180)

        # Draw the blurred background and overlay
        self.window.renderSurface.blit(screenCopy, (0, 0))
        self.window.renderSurface.blit(overlay, (0, 0))

    def __renderButton(self, color: tuple[int, int, int], text: str, position: tuple[int, int], size: tuple[int, int], font: pygame.freetype.Font):
        mouseX, mouseY = self.window.getMousePos()

        if position[0] <= mouseX <= position[0] + size[0] and position[1] <= mouseY <= position[1] + size[1]:
            isHovered = True
        else:
            isHovered = False

        buttonColor = tuple(x - 50 for x in color) if isHovered else color

        pygame.draw.rect(self.window.renderSurface, buttonColor, (position[0], position[1], size[0], size[1]), border_radius=15)
        text = font.render(text, True, (255, 255, 255))
        rect = text.get_rect(center=(position[0] + size[0] // 2, position[1] + size[1] // 2))
        self.window.renderSurface.blit(text, rect)

        if not self.wasButtonClicked:
            if isHovered and pygame.mouse.get_pressed()[0]:
                self.wasButtonClicked = True
                return True
        self.wasButtonClicked = False
        return False

    def _renderPauseMenu(self):
        self.__renderBackgroundTransparent()

        screenWidth, screenHeight = self.window.renderSurface.get_size()
        if self.__renderButton((255, 70, 70),
                            "Resume",
                            (screenWidth // 2 - self.buttonWidth // 2, screenHeight // 2 - self.buttonHeight // 2), 
                            (self.buttonWidth, self.buttonHeight), 
                            self.font):
            self.resumeCallback()

    def _renderGameOverScreen(self):
        self.__renderBackgroundTransparent()

        screenWidth, screenHeight = self.window.renderSurface.get_size()

        # Render "Game Over" Text
        gameOverText = self.largeFont.render("GAME OVER", True, (255, 70, 70))
        gameOverRect = gameOverText.get_rect(center=(screenWidth // 2, screenHeight // 2 - 100))
        self.window.renderSurface.blit(gameOverText, gameOverRect)
        
        # Render Buttons
        if self.__renderButton((255, 70, 70),
                            "Restart", 
                            (screenWidth // 2 - self.buttonWidth // 2, screenHeight // 2 - self.buttonHeight // 2), 
                            (self.buttonWidth, self.buttonHeight), 
                            self.font):
            self.restartCallback()
        if self.__renderButton((100, 100, 100), 
                            "Quit", 
                            (screenWidth // 2 - self.buttonWidth // 2, screenHeight // 2 + self.buttonHeight // 2 + self.buttonSpacing), 
                            (self.buttonWidth, self.buttonHeight), 
                            self.font):
            self.quitCallback()