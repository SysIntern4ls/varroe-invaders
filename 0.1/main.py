import pygame
import ctypes
import os

from game import Game


#TODO: Add a way to change the resolution of the game
#TODO: Add a way to change the volume of the Sound and Music
#TODO: Add some kind of levels to the game


os.environ["SDL_VIDEO_HIGHDPI"] = "1"

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()

    

 