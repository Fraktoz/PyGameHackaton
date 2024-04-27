import mainmenu
import main


def play():
    global run, i
    mainmenu.MainMenu.run = False
    i = main


menu = mainmenu.MainMenu()
menu.initGame()
menu.runGame()



