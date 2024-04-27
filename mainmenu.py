import pygame
from pygame.locals import *
from win32api import GetSystemMetrics
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.toggle import Toggle


pygame.init()

# resolution and scale
res = (GetSystemMetrics(0), GetSystemMetrics(1))
w = GetSystemMetrics(0)
h = GetSystemMetrics(1)
scale_x = w / 1920
scale_y = h / 1080

screen = pygame.display.set_mode(res, FULLSCREEN, HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption("Menu")

font = pygame.font.SysFont('arial', 64)

text = font.render('', True, (255, 255, 255))
text_rect = (450, 200)

PlayButton = Button(
    screen,
    350 * scale_x,
    250 * scale_y,
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
    play()  # Функция при нажатии
)
QuitButton = Button(
    screen,
    350 * scale_x,
    750 * scale_y,
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
    quite()  # Функция при нажатии
)
OptionsButton = Button(
    screen,
    350 * scale_x,
    500 * scale_y,
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
    OpenOptionsMenu()  # Функция при нажатии
)
BackButton = Button(
    screen,
    350 * scale_x,
    500 * scale_y,
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
    ClickedBackButton()  # Функция при нажатии
)
toggle = Toggle(
    win=screen,
    x=450,
    y=300,
    width=100,
    height=50,
    startOn=True,
    onColour=(0, 165, 80),
    offColour=(255, 79, 0),
)

toggle.hide()
BackButton.hide()


def quite():
    quit()
    pygame.quit()


def OpenOptionsMenu():
    global text
    global text_rect
    OptionsButton.hide()
    BackButton.show()
    toggle.show()
    PlayButton.hide()
    text = font.render('Music', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (500, 200)


def ClickedBackButton():
    global text
    BackButton.hide()
    OptionsButton.show()
    toggle.hide()
    PlayButton.show()
    text = font.render('', True, (255, 255, 255))


def scale(surface):
    img = surface
    return pygame.transform.scale(img, (img.get_rect().size[0] * scale_x,
                                        img.get_rect().size[1] * scale_y))


def play():
    ...


def toggleMusic():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()

    else:
        pygame.mixer.music.unpause()


def main_menu():
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if toggle.getValue():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        pygame_widgets.update(events)
        pygame.display.update()
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)



main_menu()
