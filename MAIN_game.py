import pygame
import sys
import time
from math import fabs

WIDTH = 1000
HEIGHT = 750
FPS = 30

# Задаем цвета
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
all_heroes = pygame.sprite.Group()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, color, x, y, speed, damage=10, unthrough=True,huge =10):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((huge, huge))
        self.image.fill(color)
        self.through = []
        self.rect = self.image.get_rect(center=(x, y))
        self.color = color
        self.mouse = pygame.mouse.get_pos()
        self.end = True
        self.unthrough = unthrough
        a = self.mouse[0] - self.rect.x
        b = self.mouse[1] - self.rect.y
        c = (a * a + b * b) ** 0.5
        sin = a / c
        cos = b / c
        self.speedx = sin * speed
        self.speedy = cos * speed
        self.damage = damage

    def update(self):

        self.rect.x = self.rect.x + self.speedx
        self.rect.y = self.rect.y + self.speedy
        if 0 > self.rect.x > 720 or 0 > self.rect.y > 720:
            self.kill()
        for hero in all_heroes:

            if hero.rect.x - hero.rect.width // 2 < self.rect.x < hero.rect.x + hero.rect.width // 2:
                if hero.rect.y - hero.rect.height // 2 < self.rect.y < hero.rect.y + hero.rect.height // 2:

                    if hero.color != self.color and hero not in self.through:

                        hero.health -= self.damage
                        if self.unthrough:
                            self.kill()
                        else:
                            self.through.append(hero)
                        print(hero.health)


global choosing
choosing = True
player_color = (0, 0, 0)
all_bullets = pygame.sprite.Group()


class Buttons(pygame.sprite.Sprite):
    def __init__(self, color, active_color, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 30))
        self.color = color
        self.image.fill(color)
        self.active_color = active_color
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, y)

    def update(self):
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        if self.rect.x < mouse[0] < self.rect.x + self.rect.width:
            if self.rect.y < mouse[1] < self.rect.y + self.rect.height:
                self.image.fill(self.active_color)
                if click[0] == 1:
                    if self.color == GREEN:
                        globals()['player_color'] = GREEN
                    elif self.color == RED:
                        globals()['player_color'] = RED
                    elif self.color == YELLOW:
                        globals()['player_color'] = YELLOW
                    globals()['choosing'] = False

        else:
            self.image.fill(self.color)


all_buttons = pygame.sprite.Group()


class Text(pygame.sprite.Sprite):
    def __init__(self, text, color, width=100, height=70, size=30):
        # Call th   e parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.SysFont("C:/Users/semen/PycharmProjects/gameabc/19888.ttf", size)
        self.textSurf = self.font.render(text, True, color)
        self.image = pygame.Surface((width, height))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [width / 2 - W / 2, height / 2 - H / 2])

    def update(self):
        pass


all_textes = pygame.sprite.Group()


def print_text(message, x, y, font_color=(255, 255, 255), font_type="C:/Users/semen/PycharmProjects/gameabc/19888.ttf",
               font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))

class Gr_ability(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((7,7))
        self.image.fill(GREEN)
        self.color = GREEN
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.speed = 9
        self.damage = 9
        self.rangehero = [x, y]
    def search(self):
        for hero in all_heroes:
            if (abs(hero.rect.x - self.rangehero[0]) + abs(hero.rect.y - self.rangehero[1])) >  0 and hero.color != GREEN:
                self.rangehero[0] = hero.rect.x
                self.rangehero[1] = hero.rect.y
    def update(self):
        a = self.rangehero[0] - self.rect.x
        b = self.rangehero[1] - self.rect.y
        c = (a * a + b * b) ** 0.5 or 1
        sin = a / c
        cos = b / c
        self.speedx = sin * self.speed
        self.speedy = cos * self.speed
        self.rect.x = self.rect.x + self.speedx
        self.rect.y = self.rect.y + self.speedy
        if 0 > self.rect.x > 720 or 0 > self.rect.y > 720:
            self.kill()
        for hero in all_heroes:
            if hero.rect.x - hero.rect.width // 2 < self.rect.x < hero.rect.x + hero.rect.width // 2:
                if hero.rect.y - hero.rect.height // 2 < self.rect.y < hero.rect.y + hero.rect.height // 2:
                    if hero.color != self.color :
                        hero.health -= self.damage
                        self.kill()
all_abil = pygame.sprite.Group()

class Green(pygame.sprite.Sprite):
    def __init__(self, order=2):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.color = GREEN
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / order, HEIGHT / order)
        self.speed = 5
        self.timerbul = 0
        self.timerabil = 0
        self.damage = 30
        self.health = 100

    def update(self):
        if self.health <= 0:
            all_textes.add(Text(("death"), WHITE))
            self.kill()  # осуждаю
        keys = pygame.key.get_pressed()
        click = pygame.mouse.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x = self.rect.x - self.speed
        if keys[pygame.K_d]:
            self.rect.x = self.rect.x + self.speed
        if keys[pygame.K_w]:
            self.rect.y = self.rect.y - self.speed
        if keys[pygame.K_s]:
            self.rect.y = self.rect.y + self.speed
        if click[1] == 1:
            if self.timerbul == 0:
                all_bullets.add(Bullet(GREEN, self.rect.x, self.rect.y, 20, damage=self.damage))
                self.timerbul = time.time()
            else:
                if time.time() - self.timerbul > 2:
                    self.timerbul = time.time()
                    bullet = Bullet(GREEN, self.rect.x, self.rect.y, 20, damage=self.damage)

                    all_bullets.add(bullet)
        ability = (Gr_ability(self.rect.x, self.rect.y))
        ability.search()
        if self.timerabil == 0:
            all_abil.add(ability)
            self.timerabil = time.time()
        else:
            if time.time() -self.timerabil >1.75:
                self.timerabil = time.time()
                all_abil.add(ability)
class Red(pygame.sprite.Sprite):
    def __init__(self, order=2, clon_x=0):
        pygame.sprite.Sprite.__init__(self)
        self.clon_x= clon_x
        self.color = RED
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        if self.clon_x == 0:
            self.rect.center = (WIDTH / order, HEIGHT / order)
        else:
            self.rect.center = (clon_x,HEIGHT / order)
        self.speed = 10
        self.i = 0
        self.health = 80

    def ability(self):
         clon = Red(clon_x=self.rect.x-10)
         all_heroes.add(clon)
    def update(self):
        if self.health <= 0:
            print_text("game over", 360, 360)
            self.kill()  # осуждаю
        keys = pygame.key.get_pressed()
        click = pygame.mouse.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x = self.rect.x - self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x = self.rect.x + self.speed
        if keys[pygame.K_UP]:
            self.rect.y = self.rect.y - self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y = self.rect.y + self.speed
        if keys[pygame.K_r]:
            if self.clon_x ==0:

                self.ability()
        if click[0] == 1:
            if self.i == 0:
                all_bullets.add(Bullet(RED, self.rect.x, self.rect.y, 10))
                self.i = time.time()
            else:
                if time.time() - self.i > 1.5:
                    self.i = time.time()
                    all_bullets.add(
                        Bullet(RED, self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2, 10))


class Yellow(pygame.sprite.Sprite):
    def __init__(self, order=2):
        pygame.sprite.Sprite.__init__(self)

        self.color = YELLOW
        self.image = pygame.Surface((50, 50))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // order, HEIGHT / order)
        self.speed = 8
        self.timerbul = 0
        self.timerabil = 0
        self.health = 120
        self.damage = 10

    def update(self):
        if self.health <= 0:
            print_text("game over", 360, 360)
            self.kill()  # осуждаю
        keys = pygame.key.get_pressed()
        click = pygame.mouse.get_pressed()
        if keys[pygame.K_y]:
            self.rect.x = self.rect.x - self.speed
        if keys[pygame.K_i]:
            self.rect.x = self.rect.x + self.speed
        if keys[pygame.K_7]:
            self.rect.y = self.rect.y - self.speed
        if keys[pygame.K_u]:
            self.rect.y = self.rect.y + self.speed
        if keys[pygame.K_SPACE]:
            if self.timerbul == 0:
                all_bullets.add(Bullet(YELLOW, self.rect.x, self.rect.y, self.speed, damage=self.damage, unthrough=False))
                self.timerbul = time.time()
            else:
                if time.time() - self.timerbul > 0.75:
                    self.timerbul = time.time()
                    all_bullets.add(
                        Bullet(YELLOW, self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2,  self.speed,
                               damage=self.damage, unthrough=False))
        if keys[pygame.K_f]:
            if self.timerabil == 0:
                all_bullets.add(Bullet(YELLOW, self.rect.x, self.rect.y, 8, damage=self.damage-7,huge=5))
                self.timerabil = time.time()
            else:
                if time.time() - self.timerabil > 0.3:
                    self.timerabil=time.time()
                    all_bullets.add(Bullet(YELLOW, self.rect.x, self.rect.y, 8, damage=self.damage - 7, huge=5))

clock = pygame.time.Clock()
all_buttons.add(Buttons(RED, pygame.Color(255, 150, 150), 400))
all_buttons.add(Buttons(GREEN, pygame.Color(150, 255, 150), 200))
all_buttons.add(Buttons(YELLOW, pygame.Color(255, 215, 150), 600))
while globals()['choosing']:

    clock.tick(FPS)
    screen.fill(WHITE)
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    all_buttons.update()
    all_buttons.draw(screen)
    print_text("Choose a hero", 360, 350, font_color=BLACK)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            choosing = False
    pygame.display.flip()

if player_color == RED:

    player = Red()
    all_heroes.add(player)
elif player_color == GREEN:
    player = Green()
    all_heroes.add(player)
elif player_color == YELLOW:
    player = Yellow(order=3)
    all_heroes.add(player)
all_heroes.add(Green())
all_heroes.add(Red(1))
# Цикл игры
running = True
while running:

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_heroes.update()
    all_bullets.update()
    all_textes.update()
    all_abil.update()
    # Рендеринг
    screen.fill(BLACK)
    all_heroes.draw(screen)
    all_bullets.draw(screen)
    all_abil.draw(screen)
    print_text(str(all_heroes), 0, 0, font_color=WHITE)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
