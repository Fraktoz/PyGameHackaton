import pygame
import pygame_widgets
from pygame.locals import *
from pygame_widgets.button import Button
from pygame_widgets.toggle import Toggle
from win32api import GetSystemMetrics



class MainMenu:

    def __init__(self):
        self.run = None
        self.toggle = None
        self.BackButton = None
        self.OptionsButton = None
        self.QuitButton = None
        self.PlayButton = None
        self.text_rect = None
        self.text = None
        self.font = None
        self.screen = None
        self.res = (GetSystemMetrics(0), GetSystemMetrics(1))
        self.w = GetSystemMetrics(0)
        self.h = GetSystemMetrics(1)
        self.scale_x = self.w / 1920
        self.scale_y = self.h / 1080

    def initGame(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.res, FULLSCREEN, HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption("PygamePlatformer")
        self.font = pygame.font.SysFont('arial', 64)

        self.text = self.font.render('', True, (255, 255, 255))
        self.text_rect = (450, 200)
        self.PlayButton = Button(
            self.screen,
            350 * self.scale_x,
            250 * self.scale_y,
            300,
            150,
            imageHAlign='centre',
            imageVAlign='centre',
            text='Play',
            fontSize=50,
            margin=20,
            inactiveColour=(255, 255, 255),
            hoverColour=(150, 0, 0),
            pressedColour=(0, 200, 20),
            radius=20,
            onClick=lambda:
            self.ClPlay()  # Функция при нажатии
        )
        self.QuitButton = Button(
            self.screen,
            350 * self.scale_x,
            750 * self.scale_y,
            300,
            150,
            imageHAlign='centre',
            imageVAlign='centre',
            text='Quit',
            fontSize=50,
            margin=20,
            inactiveColour=(255, 255, 255),
            hoverColour=(150, 0, 0),
            pressedColour=(0, 200, 20),
            radius=20,
            onClick=lambda:
            self.quite()  # Функция при нажатии
        )
        self.OptionsButton = Button(
            self.screen,
            350 * self.scale_x,
            500 * self.scale_y,
            300,
            150,
            imageHAlign='centre',
            imageVAlign='centre',
            text='Options',
            fontSize=50,
            margin=20,
            inactiveColour=(255, 255, 255),
            hoverColour=(150, 0, 0),
            pressedColour=(0, 200, 20),
            radius=20,
            onClick=lambda:
            self.OpenOptionsMenu()  # Функция при нажатии
        )
        self.BackButton = Button(
            self.screen,
            350 * self.scale_x,
            500 * self.scale_y,
            300,
            150,
            imageHAlign='centre',
            imageVAlign='centre',
            text='Back',
            fontSize=50,
            margin=20,
            inactiveColour=(255, 255, 255),
            hoverColour=(150, 0, 0),
            pressedColour=(0, 200, 20),
            radius=20,
            onClick=lambda:
            self.ClickedBackButton()  # Функция при нажатии
        )
        self.toggle = Toggle(
            win=self.screen,
            x=450,
            y=300,
            width=100,
            height=50,
            startOn=True,
            onColour=(0, 165, 80),
            offColour=(255, 79, 0),
        )

        self.toggle.hide()
        self.BackButton.hide()

    def ClPlay(self):
        from start import play
        self.run = False
        play()

    @staticmethod
    def quite():
        quit()
        pygame.quit()

    def OpenOptionsMenu(self):
        global text
        global text_rect
        self.OptionsButton.hide()
        self.BackButton.show()
        self.toggle.show()
        self.PlayButton.hide()
        self.text = self.font.render('Music', True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (500, 200)

    def ClickedBackButton(self):
        global text
        self.BackButton.hide()
        self.OptionsButton.show()
        self.toggle.hide()
        self.PlayButton.show()
        self.text = self.font.render('', True, (255, 255, 255))

    def toggleMusic(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

        else:
            pygame.mixer.music.unpause()

    def runGame(self):
        run = True
        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if self.toggle.getValue():
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
            pygame_widgets.update(events)
            pygame.display.update()
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.text, self.text_rect)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
