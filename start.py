import mainmenu
import main


def play():
    global game
    game = main.MainGame()
    game.initGame()
    game.runGame()


menu = mainmenu.MainMenu()
menu.initGame()
menu.runGame()



