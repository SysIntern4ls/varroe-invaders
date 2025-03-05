import pygame
import ctypes
import os

from game import Game

#----------------  Game ----------------
#TODO: Add some kind of levels to the game
#TODO: Add mask collision checking

#----------------  PowerPoint ----------------
#TODO: Slide mit diagramm von den verschiedenen Klassen
#TODO: Slide mit chatgpt verwendung (verwendung für research bezüglich pygame praktisch statt die ducumentation zu lesen)
#      - chatgpt nur die nötigen Veränderungen sagen lassen weil komplette integration nie richtig funktioniert
#TODO: Sprites sind falsch gemacht, deshalb +1 bei frameOffset -> deswegen funktioniert dann die mask auch nicht richtig und daher hab ich da es am leichtesten ist einfach an des sprite die fehlenden pixel drangehängt damit ich keinen error bekomme des sprite sheet hat halt z.b. 604 pixel insgesamt und des ergibt halt bei 604/6 nicht so viel sinn
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

    

 