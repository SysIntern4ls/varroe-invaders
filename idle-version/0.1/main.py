import pygame
import ctypes
import os

from game import Game

os.environ["SDL_VIDEO_HIGHDPI"] = "1"

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()


 
