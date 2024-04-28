import pygame
from win32api import GetSystemMetrics
from pygame.locals import *
from classes import *


class MainGame:

    def __init__(self):
        self.super_platforms = None
        self.res = (GetSystemMetrics(0), GetSystemMetrics(1))
        self.w = GetSystemMetrics(0)
        self.h = GetSystemMetrics(1)
        self.scale_x = self.w / 1920
        self.scale_y = self.h / 1080
        self.gameplay = True
        self.gravity = 10
        self.is_jumping = False

    def initGame(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.res, FULLSCREEN, HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption('SkyKnight')
        icon = pygame.image.load('images/icon.png')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.label = pygame.font.SysFont('Arial', 50)
        self.lose_label = self.label.render('Game Over', False, (0, 0, 0))
        self.lose_label_rect = self.lose_label.get_rect()
        self.lose_label_rect.center = (self.w//2, self.h // 2 - 100)
        self.restart_label = self.label.render('Restart', True, (0, 0, 0))
        self.restart_label_rect = self.restart_label.get_rect()
        self.restart_label_rect.center = (self.w//2, self.h//2)
        self.win_label = self.label.render('Спасибо за прохождение нашей игры!', False, (0, 0, 0))
        self.win_label_rect = self.win_label.get_rect()
        self.win_label_rect.center = (self.w//2, self.h // 2 - 100)
        self.quit_label = self.label.render('Quit', True, (0, 0, 0))
        self.quit_label_rect = self.quit_label.get_rect()
        self.quit_label_rect.center = (self.w//2, self.h//2)

        self.player = Player(70, 400, 15, 112, 112)
        self.enemies = [Enemy(680, 540, 112, 112, 3, 940, 420),
                        Enemy(1700, 790, 112, 112, 3, 1920, 1180)]
        self.platforms = [Platform(0, 800, 260, 60), Platform(420, 650, 260, 60),
                          Platform(680, 650, 260, 60),
                          Platform(1180, 500, 260, 60),
                          Platform(1180, 900, 260, 60),
                          Platform(1440, 900, 260, 60),
                          Platform(1700, 900, 260, 60)]
        self.collectibles_list = [Collectible(665, 590, 32, 32),
                                  Collectible(1295, 440, 32, 32),
                                  Collectible(1555, 840, 32, 32)]
        self.portal = Portal(1700, 700, 128, 128)

        self.bg = pygame.transform.scale(pygame.image.load('images/bg.png').convert(), (1920, 1080))


    def runGame(self):
        global final_lvl
        self.running = True
        curr_lvl = 1
        bg_x = 0
        winning = False
        final_lvl = False
        while self.running:

            bg_x -= 2
            if bg_x == -self.w:
                bg_x = 0

            if self.gameplay and  not winning:
                self.screen.blit(self.bg, (bg_x, 0))
                self.screen.blit(self.bg, (bg_x + self.w * self.scale_x, 0))

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

                if keys[K_w] and self.player.on_ground:
                    self.player.y_velocity = -14
                    self.player.on_ground = False

                self.player.y_velocity += 0.5

                if keys[K_SPACE]:
                    if self.player.direction == 'left':
                        self.sword_hitbox = pygame.Rect(self.player.rect.midleft[0] - 30, self.player.rect.midleft[1],
                                                        25, 25)
                    if self.player.direction == 'right':
                        self.sword_hitbox = pygame.Rect(self.player.rect.midright[0] + 30, self.player.rect.midright[1],
                                                        25, 25)

                if self.player.is_attacking:
                    if len(self.enemies) >= 1:
                        for self.Enemy in self.enemies:
                            if self.sword_hitbox.colliderect(self.Enemy.rect) and self.Enemy.alive:
                                # Уничтожаем врага
                                self.Enemy.kill()
                                self.enemies.pop(self.enemies.index(self.Enemy))
                                break
                for self.Collectible in self.collectibles_list:
                    self.Collectible.update(self.screen)
                Collectible.check_collision_collectibles(self.player, self.collectibles_list)
                if self.super_platforms is not None:
                    for self.Super_Platform in self.super_platforms:
                        self.Super_Platform.draw(self.screen)
                        self.Super_Platform.move()
                        Super_Platform.check_collision_platforms(self.player, self.super_platforms)

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
                self.portal.draw(self.screen)
                self.player.update()
                self.player.draw(self.screen)
                self.player.draw_attack(self.screen)
                for self.Platform in self.platforms:
                    self.Platform.draw(self.screen)
                pygame.display.update()
                Platform.check_collision_platforms(self.player, self.platforms)

                if self.player.rect.colliderect(self.portal.rect):
                    if len(self.collectibles_list) == 0 and len(self.enemies) == 0:
                        match curr_lvl:
                            case 1:
                                curr_lvl += 1
                                self.player = Player(70, 200, 15, 112, 112)
                                self.enemies = [Enemy(560, 490, 112, 112, 3, 660, 420),
                                                Enemy(980, 490, 112, 112, 3, 1080, 840),
                                                Enemy(1400, 490, 112, 112, 3, 1500, 1260)]
                                self.collectibles_list = [Collectible(545, 525, 32, 32),
                                                          Collectible(965, 525, 32, 32),
                                                          Collectible(1385, 525, 32, 32)]
                                self.platforms = [Platform(0, 600, 260, 60),
                                                  Platform(420, 600, 260, 60),
                                                  Platform(840, 600, 260, 60),
                                                  Platform(1260, 600, 260, 60),
                                                  Platform(1680, 600, 260, 60)]
                                self.portal = Portal(1780, 450, 128, 128)
                            case 2:
                                final_lvl = True
                                curr_lvl += 1
                                self.player = Player(70, 300, 15, 112, 112)
                                self.enemies = [Enemy(580, 840, 112, 112, 3, 680, 420),
                                                Enemy(1560, 740, 112, 112, 3, 1660, 1400), ]
                                self.collectibles_list = [Collectible(535, 890, 32, 32),
                                                          Collectible(1515, 790, 32, 32)]
                                self.platforms = [Platform(0, 700, 260, 60),
                                                  Platform(420, 950, 260, 60),
                                                  Platform(1400, 850, 260, 60),
                                                  Platform(1650, 725, 260, 60)]
                                self.portal = Portal(1720, 575, 128, 128)
                                self.super_platforms = [Super_Platform(780, 950, 260, 60, 5, 1400, 780)]

                            case 3:
                                final_lvl = False
                                winning = True





                if self.player.rect.y > self.h:
                    self.gameplay = False

            elif not self.gameplay and not winning:
                pygame.display.update()
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.lose_label, self.lose_label_rect)
                self.screen.blit(self.restart_label, self.restart_label_rect)
                mouse = pygame.mouse.get_pos()
                if self.restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    self.gameplay = True
                    self.player = Player(70, 400, 15, 112, 112)
                    self.enemies = [Enemy(680, 540, 112, 112, 3, 940, 420),
                                    Enemy(1700, 790, 112, 112, 3, 1920, 1180)]
                    self.collectibles_list = [Collectible(665, 590, 32, 32),
                                              Collectible(1295, 440, 32, 32),
                                              Collectible(1555, 840, 32, 32)]
                    self.platforms = [Platform(0, 800, 260, 60), Platform(420, 650, 260, 60),
                                      Platform(680, 650, 260, 60),
                                      Platform(1180, 500, 260, 60),
                                      Platform(1180, 900, 260, 60),
                                      Platform(1440, 900, 260, 60),
                                      Platform(1700, 900, 260, 60)]
                    self.portal = Portal(1700, 700, 128, 128)
                    self.super_platforms = None
                    final_lvl = False
                    curr_lvl = 1
            elif self.gameplay and winning:
                pygame.display.update()
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.win_label, self.win_label_rect)
                self.screen.blit(self.quit_label, self.quit_label_rect)
                mouse = pygame.mouse.get_pos()
                if self.quit_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    quit(0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

            self.clock.tick(30)
