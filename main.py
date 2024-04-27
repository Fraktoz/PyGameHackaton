import pygame
from win32api import GetSystemMetrics
from pygame.locals import *

import classes
from classes import *


class MainGame:

    def __init__(self):
        self.Enemy = None
        self.sword_hitbox = None
        self.player_rect = None
        self.running = None
        self.bg = None
        self.enemies = None
        self.player = None
        self.restart_label_rect = None
        self.restart_label = None
        self.lose_label = None
        self.label = None
        self.screen = None
        self.clock = None
        self.res = (GetSystemMetrics(0), GetSystemMetrics(1))
        self.w = GetSystemMetrics(0)
        self.h = GetSystemMetrics(1)
        self.scale_x = self.w / 1920
        self.scale_y = self.h / 1080
        self.bg_x = 0
        self.gameplay = True
        self.gravity = 10
        self.is_jumping = False

    def initGame(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.res, FULLSCREEN, HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption('PygamePlatformer')
        # icon = pygame.image.load('icon.png')
        # pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.label = pygame.font.SysFont('Arial', 50)
        self.lose_label = self.label.render('Game Over', False, (0, 0, 0))
        self.restart_label = self.label.render('Restart', True, (0, 0, 0))
        self.restart_label_rect = self.restart_label.get_rect(topleft=(100, 100))

        self.player = Player(100, 350, 15, 301, 493)
        self.enemies = [classes.Enemy(650, 350, 301, 493, 7), classes.Enemy(900, 350, 301, 493, 25)]

        self.bg = pygame.transform.scale(pygame.image.load('images/bg.png').convert(), (1920, 1080))

    def runGame(self):
        self.running = True
        while self.running:

            if self.gameplay:
                self.screen.blit(self.bg, (self.bg_x, 0))
                self.screen.blit(self.bg, (self.bg_x + self.w * self.scale_x, 0))

                keys = pygame.key.get_pressed()
                self.player_rect = self.player.rect
                if len(self.enemies) >= 1:
                    for i in range(len(self.enemies)):
                        if self.player.rect.colliderect(self.enemies[i].rect):
                            self.gameplay = False

                if keys[K_a] and self.player.rect.left > 0:
                    self.player.stay = False
                    self.player.move(-self.player.speed, 0)
                    self.player.direction = 'left'
                else:
                    self.player.stay = True

                if keys[K_d] and self.player.rect.right < self.w:
                    self.player.stay = False
                    self.player.move(self.player.speed, 0)
                    self.player.direction = 'right'

                if keys[K_w] and self.player.rect.top > 0:
                    if not self.is_jumping:
                        if keys[pygame.K_w]:
                            self.is_jumping = True

                if keys[K_SPACE]:
                    if self.player.direction == 'left':
                        self.sword_hitbox = pygame.Rect(self.player.rect.midleft[0] - 50, self.player.rect.midleft[1],
                                                        50, 50)
                    if self.player.direction == 'right':
                        self.sword_hitbox = pygame.Rect(self.player.rect.midright[0] + 50, self.player.rect.midright[1],
                                                        50, 50)

                if self.player.is_attacking:
                    if self.sword_hitbox.colliderect(self.Enemy.rect) and self.Enemy.alive:
                        # Уничтожаем врага
                        self.Enemy.kill()
                        self.enemies.pop(self.enemies.index(self.Enemy))

                if self.is_jumping:
                    if self.gravity >= -10:
                        if self.gravity > 0:
                            self.player.rect.y -= (self.gravity ** 2) / 2
                        else:
                            self.player.rect.y += (self.gravity ** 2) / 2
                        self.gravity -= 1
                    else:
                        self.is_jumping = False
                        self.gravity = 10

                if keys[K_SPACE]:
                    self.player.attack()

                else:
                    self.player.stop_attack()
                for self.Enemy in self.enemies:
                    self.Enemy.move()
                    self.Enemy.draw(self.screen)
                    self.Enemy.update()
                    # Если противник мертв, удаляем его из списка
                    if not self.Enemy.alive:
                        self.enemies.remove(self.Enemy)
                self.player.update()
                self.player.draw(self.screen)
                self.player.draw_attack(self.screen)
                pygame.display.update()

            else:
                pygame.display.update()
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.lose_label, (50, 50))
                self.screen.blit(self.restart_label, self.restart_label_rect)
                mouse = pygame.mouse.get_pos()
                if self.restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    self.gameplay = True
                    self.player.rect.x = 100
                    for self.Enemy in self.enemies:
                        self.Enemy.kill()
                    self.enemies = [(classes.Enemy(650, 350, 301, 493, 7)), (classes.Enemy(900, 350, 301, 493, 25))]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

            self.clock.tick(15)
