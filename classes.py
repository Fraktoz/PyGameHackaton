import pygame
import time, datetime


class Enemy:
    def __init__(self, x, y, width, height, speed, point_1, point_2):
        global count
        count = 0
        self.point_1 = point_1
        self.point_2 = point_2
        self.alive = True
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.direction = 'right'  # Начальное направление движения врага
        self.frame_index = 0
        self.walk_right = [
            pygame.image.load('images/enemy/walk_right/1.png').convert_alpha(),
            pygame.image.load('images/enemy/walk_right/2.png').convert_alpha(),
            pygame.image.load('images/enemy/walk_right/3.png').convert_alpha(),
        ]
        self.walk_left = [
            pygame.image.load('images/enemy/walk_left/1.png').convert_alpha(),
            pygame.image.load('images/enemy/walk_left/2.png').convert_alpha(),
            pygame.image.load('images/enemy/walk_left/3.png').convert_alpha(),
        ]

    def move(self):
        if self.direction == 'right':
            self.rect.x += self.speed
            # Если враг достиг правой границы, меняем направление на лево
            if self.rect.right >= self.point_1:
                self.direction = 'left'
        elif self.direction == 'left':
            self.rect.x -= self.speed
            # Если враг достиг левой границы, меняем направление на право
            if self.rect.left <= self.point_2:
                self.direction = 'right'

    def animation(self):
        if self.direction == 'right':
            self.frame_index = (self.frame_index + 1) % len(self.walk_right)
        elif self.direction == 'left':
            self.frame_index = (self.frame_index + 1) % len(self.walk_left)

    def draw(self, screen):

        if self.direction == 'right':
            screen.blit(self.walk_right[self.frame_index], (self.rect.x, self.rect.y))
        elif self.direction == 'left':
            screen.blit(self.walk_left[self.frame_index], (self.rect.x, self.rect.y))

    def kill(self):
        # Метод для уничтожения врага
        self.alive = False

    def update(self):
        self.animation()


class Player:
    def __init__(self, player_x, player_y, player_speed, width, height):
        self.startedtimer = False
        self.is_attacking = False
        self.timer = None
        self.rect = pygame.Rect(player_x, player_y, width, height)
        self.speed = player_speed
        self.y_velocity = 0
        self.jump_speed = 0
        self.x = player_x
        self.y = player_y
        self.max_velocity = player_speed * 2
        self.direction = 'right'
        self.stay = True
        self.frame_index = 0
        self.attack_index = 0
        self.on_ground = False
        self.walk_right = [
            pygame.image.load('images/player/walk_right/1.png').convert_alpha(),
            pygame.image.load('images/player/walk_right/2.png').convert_alpha(),
            pygame.image.load('images/player/walk_right/3.png').convert_alpha(),
        ]
        self.walk_left = [
            pygame.image.load('images/player/walk_left/1.png').convert_alpha(),
            pygame.image.load('images/player/walk_left/2.png').convert_alpha(),
            pygame.image.load('images/player/walk_left/3.png').convert_alpha(),
        ]
        self.right_attack = [
            pygame.image.load(('images/player/right_attack/1.png')).convert_alpha(),
            pygame.image.load(('images/player/right_attack/2.png')).convert_alpha(),
            pygame.image.load(('images/player/right_attack/3.png')).convert_alpha(),
        ]
        self.left_attack = [
            pygame.image.load(('images/player/left_attack/1.png')).convert_alpha(),
            pygame.image.load(('images/player/left_attack/2.png')).convert_alpha(),
            pygame.image.load(('images/player/left_attack/3.png')).convert_alpha(),
        ]

    def speedup(self, time_stop):
        self.timer = time_stop
        self.speed = self.max_velocity

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def attack(self):
        self.is_attacking = True

    def stop_attack(self):
        self.is_attacking = False

    def animation(self):
        if self.stay:
            self.frame_index = 1
        else:
            if self.direction == 'right':
                self.frame_index = (self.frame_index + 1) % len(self.walk_right)
            else:
                self.frame_index = (self.frame_index + 1) % len(self.walk_left)

    def draw(self, screen):
        if self.direction == 'right':
            screen.blit(self.walk_right[self.frame_index], (self.rect.x, self.rect.y))
        else:
            screen.blit(self.walk_left[self.frame_index], (self.rect.x, self.rect.y))

    def draw_attack(self, screen):
        if self.direction == 'right' and self.is_attacking == True:
            screen.blit(self.right_attack[self.attack_index], (self.rect.x, self.rect.y))
        elif self.direction == 'left' and self.is_attacking == True:
            screen.blit(self.left_attack[self.attack_index], (self.rect.x, self.rect.y))

    def update(self):
        self.animation()
        self.rect.y += self.y_velocity
        if self.startedtimer:
            if datetime.datetime.utcnow() > self.timer:
                self.speed = self.speed / 2
                self.startedtimer = False


class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load('images/platform.png').convert_alpha()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

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
                elif object.speed > 0:  # Если спрайт движется вправо
                    # ставим спрайт слева от платформы
                    object.rect.right = platform.rect.left
                elif object.speed < 0:  # Если спрайт движется влево
                    # ставим спрайт справа от платформы
                    object.rect.left = platform.rect.right


class Collectible:
    def __init__(self, x, y, width, height):
        self.cnt_text_rect = None
        self.cnt_text = None
        self.font = None
        self.cnt_image = None
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.frame_index = 0
        self.image = [
            pygame.image.load('images/coins/monetka1.png').convert_alpha(),
            pygame.image.load('images/coins/monetka2.png').convert_alpha(),
            pygame.image.load('images/coins/monetka3.png').convert_alpha(),
            pygame.image.load('images/coins/monetka4.png').convert_alpha(),
            pygame.image.load('images/coins/monetka5.png').convert_alpha(),
            pygame.image.load('images/coins/monetka6.png').convert_alpha(),
        ]

    def check_collision_collectibles(object, collectibles_list):
        global count

        # если object касается collictible
        for collectible in collectibles_list:
            if object.rect.colliderect(collectible.rect):
                # убираем этот объект из списка (чтобы не было проверки коллизии)
                collectibles_list.remove(collectible)
                count += 1
                object.startedtimer = False

                Player.speedup(object, time_stop=datetime.datetime.utcnow() + datetime.timedelta(seconds=3))
                object.startedtimer = True

    def counter(self):
        self.font = pygame.font.SysFont('arial', 32)
        self.cnt_image = pygame.image.load('images/coins/monetka1.png').convert_alpha()
        self.cnt_image_rect = self.cnt_image.get_rect()
        self.cnt_image_rect.center = (1800, 100)
        self.cnt_text = self.font.render(f'{count}', True, (0, 0, 0))
        self.cnt_text_rect = self.cnt_text.get_rect()
        self.cnt_text_rect.center = (1800, 150)

    def restart(self):
        global count
        count = 0

    def update(self, screen):
        self.frame_index = (self.frame_index + 1) % len(self.image)
        self.counter()
        screen.blit(self.cnt_image, self.cnt_image_rect)
        screen.blit(self.cnt_text, self.cnt_text_rect)
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.image[self.frame_index], self.rect)


class Portal:
    def __init__(self, x, y, width, height):
        self.image = pygame.image.load('images/portal.png')
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Super_Platform:
    def __init__(self, x, y, width, height, speed, point_1, point_2):
        self.x = x
        self.y = y
        self.direction = 'right'
        self.point_1 = point_1
        self.point_2 = point_2
        self.speed = speed
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load('images/platform.png').convert_alpha()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        if self.direction == 'right':
            self.rect.x += self.speed
            if self.rect.right >= self.point_1:
                self.direction = 'left'
        elif self.direction == 'left':
            self.rect.x -= self.speed
            if self.rect.left <= self.point_2:
                self.direction = 'right'

    def check_collision_platforms(object, super_platforms):
        for s_platform in super_platforms:
            if object.rect.colliderect(s_platform.rect):
                if object.y_velocity > 0:  # Если спрайт падает
                    # меняем переменную-флаг
                    object.on_ground = True
                    # ставим его поверх платформы и сбрасываем скорость по оси Y
                    object.rect.bottom = s_platform.rect.top
                    object.y_velocity = 0
                elif object.y_velocity < 0:  # Если спрайт движется вверх
                    # ставим спрайт снизу платформы
                    object.rect.top = s_platform.rect.bottom
                    object.y_velocity = 0
                elif object.speed > 0:  # Если спрайт движется вправо
                    # ставим спрайт слева от платформы
                    object.rect.right = s_platform.rect.left
                elif object.speed < 0:  # Если спрайт движется влево
                    # ставим спрайт справа от платформы
                    object.rect.left = s_platform.rect.right
