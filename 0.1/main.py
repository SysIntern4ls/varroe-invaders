import pygame
import ctypes
import os

from game import Game

#----------------  PowerPoint ----------------
#TODO: Slide mit diagramm von den verschiedenen Klassen
#TODO: Slide mit chatgpt verwendung (verwendung für research bezüglich pygame praktisch statt die ducumentation zu lesen)
#      - chatgpt nur die nötigen Veränderungen sagen lassen weil komplette integration nie richtig funktioniert
#TODO: Sprites sind falsch gemacht, deshalb +1 bei frameOffset -> deswegen funktioniert dann die mask auch nicht richtig sprite sheet = 604 pixel width und nicht 600 bzw 606
#TODO: Slide mit sprite mask detection


os.environ["SDL_VIDEO_HIGHDPI"] = "1"

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()


 