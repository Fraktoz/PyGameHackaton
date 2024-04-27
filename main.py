import pygame
from win32api import GetSystemMetrics
from pygame.locals import *
from classes import Enemy, Player

pygame.init()
res = (GetSystemMetrics(0), GetSystemMetrics(1))
w = GetSystemMetrics(0)
h = GetSystemMetrics(1)
scale_x = w / 1920
scale_y = h / 1080
screen = pygame.display.set_mode(res, FULLSCREEN, HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption('PygamePlatformer')
# icon = pygame.image.load('icon.png')
# pygame.display.set_icon(icon)
clock = pygame.time.Clock()
gameplay = True
gravity = 10
is_jumping = False
label = pygame.font.SysFont('Arial', 50)
lose_label = label.render('Game Over', False, (0, 0, 0))
restart_label = label.render('Restart', True, (0, 0, 0))
restart_label_rect = restart_label.get_rect(topleft=(100, 100))


def scale(surface):
    img = surface
    return pygame.transform.scale(img, (50, 50))


    def move(self):
        if self.direction == 'right':
            self.rect.x += self.speed
            # Если враг достиг правой границы, меняем направление на лево
            if self.rect.right >= 1800:
                self.direction = 'left'
        elif self.direction == 'left':
            self.rect.x -= self.speed
            # Если враг достиг левой границы, меняем направление на право
            if self.rect.left <= 400:
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



player = Player(100, 350, 15, 301, 493)
enemies = [Enemy(650, 350, 301, 493, 7), Enemy(900, 350, 301, 493, 25)]

bg_x = 0
bg = pygame.transform.scale(pygame.image.load('images/bg.png').convert(), (1920, 1080))

running = True
while running:

    if gameplay:
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + w * scale_x, 0))

        keys = pygame.key.get_pressed()
        player_rect = player.rect
        if len(enemies) >= 1:
            for i in range(len(enemies)):
                if player.rect.colliderect(enemies[i].rect):
                    gameplay = False

        if keys[K_a] and player.rect.left > 0:
            player.stay = False
            player.move(-player.speed, 0)
            player.direction = 'left'
        else:
            player.stay = True

        if keys[K_d] and player.rect.right < w:
            player.stay = False
            player.move(player.speed, 0)
            player.direction = 'right'

        if keys[K_w] and player.rect.top > 0:
            if not is_jumping:
                if keys[pygame.K_w]:
                    is_jumping = True

        if keys[K_SPACE]:
            if player.direction == 'left':
                sword_hitbox = pygame.Rect(player.rect.midleft[0] - 50, player.rect.midleft[1], 50, 50)
            if player.direction == 'right':
                sword_hitbox = pygame.Rect(player.rect.midright[0] + 50, player.rect.midright[1], 50, 50)

        if player.is_attacking:
                if sword_hitbox.colliderect(Enemy.rect) and Enemy.alive:
                    # Уничтожаем врага
                    Enemy.kill()

        if is_jumping:
            if gravity >= -10:
                if gravity > 0:
                    player.rect.y -= (gravity ** 2) / 2
                else:
                    player.rect.y += (gravity ** 2) / 2
                gravity -= 1
            else:
                is_jumping = False
                gravity = 10

        if keys[K_SPACE]:
            player.attack()
        else:
            player.stop_attack()
        for Enemy in enemies:
            Enemy.move()
            Enemy.draw(screen)
            Enemy.update()
            # Если противник мертв, удаляем его из списка
            if not Enemy.alive:
                enemies.remove(Enemy)
        player.update()
        player.draw(screen)
        pygame.display.update()

    else:
        pygame.display.update()
        screen.fill((255, 255, 255))
        screen.blit(lose_label, (50, 50))
        screen.blit(restart_label, restart_label_rect)
        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player.rect.x = 100
            enemies = [Enemy(650, 350, 301, 493, 7), Enemy(900, 350, 301, 493, 25)]


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    clock.tick(15)


"""e_walk_right = [
    pygame.transform.scale(pygame.image.load('images/enemy/walk_right/1.png').convert_alpha(), (40, 70)),
    pygame.transform.scale(pygame.image.load('images/enemy/walk_right/2.png').convert_alpha(), (40, 70)),
    pygame.transform.scale(pygame.image.load('images/enemy/walk_right/3.png').convert_alpha(), (40, 70)),
    pygame.transform.scale(pygame.image.load('images/enemy/walk_right/4.png').convert_alpha(), (40, 70)),
]

e_walk_left = [
    pygame.transform.scale(pygame.image.load('images/enemy/walk_left/1.png').convert_alpha(), (40, 70)),
    pygame.transform.scale(pygame.image.load('images/enemy/walk_left/2.png').convert_alpha(), (40, 70)),
    pygame.transform.scale(pygame.image.load('images/enemy/walk_left/3.png').convert_alpha(), (40, 70)),
    pygame.transform.scale(pygame.image.load('images/enemy/walk_left/4.png').convert_alpha(), (40, 70)),
]

e_stay = pygame.transform.scale(pygame.image.load('images/enemy/stay/1.png').convert_alpha(), (50, 70))

bg_x = 0
player_anim_count = 0
enemy_anim_count = 0

player_speed = 10
player_x = 150
player_y = 220
is_jumping = False
gravity = 8

enemy_x = 650
enemy_y = 220
enemy_speed = 10

label = pygame.font.SysFont('Arial', 50)
lose_label = label.render('Game Over', False, (0, 0, 0))
restart_label = label.render('Restart', True, (0, 0, 0))
restart_label_rect = restart_label.get_rect(topleft=(100, 100))
sword_width = 32
sword_height = 32
sword_hitbox = pygame.Rect(0, 0, sword_width, sword_height)

gameplay = True
running = True
killed = False
while running:

    if gameplay:
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 700, 0))
        keys = pygame.key.get_pressed()
        player_rect = p_walk_left[0].get_rect(topleft=(player_x, player_y))
        enemy_rect = e_walk_left[0].get_rect(topleft=(enemy_x, enemy_y))

        if player_rect.colliderect(enemy_rect):
            gameplay = False



        if enemy_x == 450:
            flag = True
        if enemy_x == 650:
            flag = False
        if flag:
            screen.blit(e_walk_right[enemy_anim_count], (enemy_x, enemy_y))
            enemy_x += enemy_speed
        else:
            screen.blit(e_walk_left[enemy_anim_count], (enemy_x, enemy_y))
            enemy_x -= enemy_speed

        if keys[pygame.K_d]:
            screen.blit(p_walk_right[player_anim_count], (player_x, player_y))
            if keys[pygame.K_SPACE]:
                sword_hitbox.topleft = (player_x + 30, player_y)
        elif keys[pygame.K_a]:
            screen.blit(p_walk_left[player_anim_count], (player_x, player_y))
            if keys[pygame.K_SPACE]:
                sword_hitbox.topleft = (player_x - 30, player_y)
        else:
            screen.blit(p_stay, (player_x, player_y))

        if keys[pygame.K_a] and player_x > 10:
            player_x -= player_speed
        elif keys[pygame.K_d] and player_x < 690:
            player_x += player_speed

        if enemy_anim_count == 3:
            enemy_anim_count = 0
        else:
            enemy_anim_count += 1

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        if not is_jumping:
            if keys[pygame.K_w]:
                is_jumping = True
        else:
            if gravity >= -8:
                if gravity > 0:
                    player_y -= (gravity ** 2) / 2
                else:
                    player_y += (gravity ** 2) / 2
                gravity -= 1
            else:
                is_jumping = False
                gravity = 8

        bg_x -= 2

        if bg_x == - 700:
            bg_x = 0
    else:
        pygame.display.update()
        screen.fill((255, 255, 255))
        screen.blit(lose_label, (50, 50))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    clock.tick(15)"""
