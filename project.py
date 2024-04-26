####################################################################################
# Данный код представляет собой каркас для игры в жанре платформер                 #
# В нем определены: классы главного героя, врагов, собираемых предметов и платформ #
# управление с помощью клавиатуры, проверка коллизий объектов                      #
# Проект можно запустить для демонстрации функционала                              #
####################################################################################


################################################################
# При запуске:                                                  #
# синие элементы - платформы,                                  #
# красный элемент - враг,                                      #
# зеленый элемент - игрок,                                     #
# желтый элемент - собираемый предмет                          #
#                                                              #
# Управление: стрелки клавиатуры для движения, пробел для прыжка#
################################################################

# подключние бибилиотек
import pygame
import random

# инициализация Pygame
pygame.init()

# константы-параметры окна
WIDTH = 800
HEIGHT = 600
# константы-цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)


# класс для игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # создание изображения для спрайта
        self.image = pygame.Surface((32, 32))
        self.image.fill(GREEN)

        # создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # компоненты скорости по оси X и Y
        self.x_velocity = 0
        self.y_velocity = 0

        # переменная-флаг для отслеживания в прыжке ли спрайт
        self.on_ground = False

    def update(self):
        # Обновление позиции игрока
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity


# класс для патрулирующих врагов
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # создание изображения для спрайта
        self.image = pygame.Surface((32, 32))
        self.image.fill(RED)

        # начальная позиция по Х, нужна для патрулирования
        self.x_start = x
        # выбор направления начального движения
        self.direction = random.choice([-1, 1])

        # создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # компоненты скорости по оси Х и Y
        self.x_velocity = 1
        self.y_velocity = 0

    def update(self):
        # если расстояние от начальной точки превысило 50
        # то меняем направление
        if abs(self.x_start - self.rect.x) > 50:
            self.direction *= -1

        # движение спрайта по оси Х
        self.rect.x += self.x_velocity * self.direction


# класс для поднимаемых предметов
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # создание изображения для спрайта
        self.image = pygame.Surface((16, 16))
        self.image.fill(GOLD)

        # создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# класс для платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # создание изображения для спрайта
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)

        # создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# функция для проверки коллизий c платформой
def check_collision_platforms(object, platform_list):
    # перебираем все платформы из списка (не группы спрайтов)
    for platform in platform_list:
        if object.rect.colliderect(platform.rect):
            if object.y_velocity > 0:  # Если спрайт падает
                # меняем переменную-флаг
                object.on_ground = True
                # ставим его поверх платформы и сбрасываем скорость по оси Y
                object.rect.bottom = platform.rect.top
                object.y_velocity = 0
            elif object.y_velocity < 0:  # Если спрайт движется вверх
                # ставим спрайт снизу платформы
                object.rect.top = platform.rect.bottom
                object.y_velocity = 0
            elif object.x_velocity > 0:  # Если спрайт движется вправо
                # ставим спрайт слева от платформы
                object.rect.right = platform.rect.left
            elif object.x_velocity < 0:  # Если спрайт движется влево
                # ставим спрайт справа от платформы
                object.rect.left = platform.rect.right


# функция проверки коллизии выбранного объекта с объектами Enemies
def check_collision_enemies(object, enemies_list):
    # running делаем видимой внутри функции чтобы было возможно
    # завершить игру
    global running
    # в списке проверяем
    for enemy in enemies_list:
        # при коллизии
        if object.rect.colliderect(enemy.rect):
            # объект пропадает из всех групп спрайтов и игра заканчивается
            object.kill()
            running = False


# проверка
def check_collision_collectibles(object):
    # делаем видимыми объекты для подбора в игре и очки
    global collectibles_list
    global score
    # если object касается collictible
    for collectible in collectibles_list:
        if object.rect.colliderect(collectible.rect):
            # убираем этот объект из всех групп
            collectible.kill()
            # убираем этот объект из списка (чтобы не было проверки коллизии)
            collectibles_list.remove(collectible)
            # прибавляем одно очко
            score += 1


# создаем экран, счетчик частоты кадров и очков
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
score = 0

# создаем игрока, платформы, врагов и то, что будем собирать в игре
player = Player(50, 50)
platforms_list = [Platform(0, HEIGHT - 25, WIDTH, 50), Platform(50, 150, 100, 20), Platform(100, 350, 100, 20),
                  Platform(250, 170, 100, 20)]
enemies_list = [Enemy(120, 315)]
collectibles_list = [Collectible(280, 135)]

# счёт игры
font = pygame.font.Font(None, 36)  # создание объекта, выбор размера шрифта
score_text = font.render("Счёт: 0", True, BLACK)  # выбор цвета и текст
score_rect = score_text.get_rect()  # создание хитбокса текста
score_rect.topleft = (WIDTH // 2, 100)  # расположение хитбокса\текста на экране

# создаем групп спрайтов
player_and_platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

# в трех циклах добавляем объекты в соответствующие группы
for i in enemies_list:
    enemies.add(i)

for i in platforms_list:
    player_and_platforms.add(i)

for i in collectibles_list:
    collectibles.add(i)

# отдельно добавляем игрока
player_and_platforms.add(player)

# игровой цикл
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # проверяем нажатие на клавиши для перемещения
    keys = pygame.key.get_pressed()
    player.x_velocity = 0
    if keys[pygame.K_a]:
        player.x_velocity = -5
    if keys[pygame.K_d]:
        player.x_velocity = 5
    # условие прыжка более сложное
    if keys[pygame.K_w] and player.on_ground == True:
        player.y_velocity = -9
        player.on_ground = False
    # гравитация для игрока
    player.y_velocity += 0.3

    # обновляем значения атрибутов игрока и врагов
    player.update()
    enemies.update()

    # отрисовываем фон, платформы, врагов и собираемые предметы
    screen.fill(WHITE)
    player_and_platforms.draw(screen)
    enemies.draw(screen)
    collectibles.draw(screen)

    # проверяем все возможные коллизии
    check_collision_platforms(player, platforms_list)
    check_collision_enemies(player, enemies_list)
    check_collision_collectibles(player)

    # обновление счёта на экране
    score_text = font.render("Счёт: " + str(score), True, BLACK)
    screen.blit(score_text, score_rect)

    # обновление экрана и установка частоты кадров
    pygame.display.update()
    clock.tick(60)

pygame.quit()

'''Пока так'''