import pygame
import ctypes
import os

from game import Game

#----------------  Game ----------------
#TODO: Add a way to change the resolution of the game
#TODO: Add some kind of levels to the game
#TODO: Add mask collision checking

#----------------  PowerPoint ----------------
#TODO: Slide mit diagramm von den verschiedenen Klassen
#TODO: Slide mit chatgpt verwendung (verwendung für research bezüglich pygame praktisch statt die ducumentation zu lesen)
#      - chatgpt nur die nötigen Veränderungen sagen lassen weil komplette integration nie richtig funktioniert

os.environ["SDL_VIDEO_HIGHDPI"] = "1"

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()

    

 