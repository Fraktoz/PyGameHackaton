import pygame
import pygame_widgets
from pygame.locals import *
from pygame_widgets.button import Button
from pygame_widgets.toggle import Toggle
from win32api import GetSystemMetrics


class MainMenu:

    def __init__(self):
        self.mainText_rect = None
        self.bg = None
        self.font_native = None
        self.mainText = None
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
        self.bg_x = 0
        self.scale_x = self.w / 1920
        self.scale_y = self.h / 1080
        self.text_rect_native = None
        self.text_native = None
        self.MusicOnn = None

    def initGame(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.res, FULLSCREEN, HWSURFACE | DOUBLEBUF | RESIZABLE)
        icon = pygame.image.load('images/icon.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption("SkyKnight")
        self.font = pygame.font.SysFont('arial', 64)
        self.font_native = pygame.font.SysFont('arial', 32)
        self.bg = pygame.transform.scale(pygame.image.load('images/bg.png').convert(), (1920, 1080))
        self.text = self.font.render('', True, (214, 214, 214))
        self.text_native_1 = self.font.render('', True, (214, 214, 214))
        self.text_native_2 = self.font.render('', True, (214, 214, 214))
        self.text_native_3 = self.font.render('', True, (214, 214, 214))
        self.text_native_4 = self.font.render('', True, (214, 214, 214))
        self.text_rect_native_1 = self.text_native_1.get_rect()
        self.text_rect_native_2 = self.text_native_2.get_rect()
        self.text_rect_native_3 = self.text_native_3.get_rect()
        self.text_rect_native_4 = self.text_native_4.get_rect()
        self.text_rect = (500, 200)
        self.mainText = self.font.render('SKY KNIGHT', True, (0, 0, 0))
        self.mainText_rect = self.mainText.get_rect()
        self.mainText_rect.center = (1200, 540)

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
            inactiveColour=(214, 214, 214),
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
            inactiveColour=(214, 214, 214),
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
            inactiveColour=(214, 214, 214),
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
            inactiveColour=(214, 214, 214),
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
            offColour=(214, 79, 0),
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
        self.text = self.font.render('Music', True, (0, 0, 0))
        self.text_native_1 = self.font_native.render('W - JUMP' , True, (0, 0, 0))
        self.text_native_2 = self.font_native.render('D - MOVE RIGHT', True, (0, 0, 0))
        self.text_native_3 = self.font_native.render('A - MOVE LEFT', True, (0, 0, 0))
        self.text_native_4 = self.font_native.render('PRESS  OR TOUCH SPACEBAR - ATTACK', True, (0, 0, 0))
        self.text_rect = self.text.get_rect()
        self.text_rect_native_1 = self.text_native_1.get_rect()
        self.text_rect_native_2 = self.text_native_2.get_rect()
        self.text_rect_native_3 = self.text_native_3.get_rect()
        self.text_rect_native_4 = self.text_native_4.get_rect()
        self.text_rect_native_1.center = (1200, 300)
        self.text_rect_native_2.center = (1200, 450)
        self.text_rect_native_3.center = (1200, 600)
        self.text_rect_native_4.center = (1200, 750)
        self.text_rect.center = (500, 200)
        self.mainText = self.font.render('', True, (0, 0, 0))

    def ClickedBackButton(self):
        global text
        self.BackButton.hide()
        self.OptionsButton.show()
        self.toggle.hide()
        self.PlayButton.show()
        self.text = self.font.render('', True, (214, 214, 214))
        self.text_native_1 = self.font.render('', True, (214, 214, 214))
        self.text_native_2 = self.font.render('', True, (214, 214, 214))
        self.text_native_3 = self.font.render('', True, (214, 214, 214))
        self.text_native_4 = self.font.render('', True, (214, 214, 214))
        self.mainText = self.font.render('SKY KNIGHT', True, (0, 0, 0))


    def runGame(self):
        pygame.mixer.music.load('bgmusic.ogg')
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(loops=50)

        run = True
        while run:
            self.screen.blit(self.bg, (self.bg_x, 0))
            self.screen.blit(self.text_native_1, self.text_rect_native_1)
            self.screen.blit(self.text_native_2, self.text_rect_native_2)
            self.screen.blit(self.text_native_3, self.text_rect_native_3)
            self.screen.blit(self.text_native_4, self.text_rect_native_4)
            self.screen.blit(self.mainText, self.mainText_rect)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            pygame_widgets.update(events)
            pygame.display.update()
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.text, self.text_rect)

            if not self.toggle.getValue():
                pygame.mixer.music.pause()
                pygame.mixer.music.set_volume(0)
            else:
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.unpause()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
