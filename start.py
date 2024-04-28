import mainmenu
import main
import pygame


def play():
    global gamed
    game = main.MainGame()
    game.initGame()
    game.runGame()


icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('SkyKnight')
menu = mainmenu.MainMenu()
menu.initGame()
menu.runGame()
