import pygame
import sys
import random
from time import monotonic

pygame.init()
button_sound = pygame.mixer.Sound("Надёжная ладонь .wav")


class Game():
    def __init__(self):
        self.screen_width = 720
        self.screen_height = 720

        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)
        self.white = pygame.Color(255, 255, 255)
        self.brown = pygame.Color(162, 42, 42)
        self.run = True
        self.score = 0
        self.fps_controller = pygame.time.Clock()
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("SEGAm")

    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def print_text(self, message, x, y, font_color=(255, 255, 255), font_size=30):
        font_type = pygame.font.Font("C:/Users/semen/PycharmProjects/gameabc/19888.ttf", font_size)
        text = font_type.render(message, True, font_color)
        self.play_surface.blit(text, (x, y))

    def pause(self):
        paused = True
        while paused:
            self.print_text('Please choose your color', 160, 100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            button = Button(50, 50, pygame.Color(255, 0, 0), pygame.Color(255, 255, 255))
            button2 = Button(50, 50, pygame.Color(0, 255, 0), pygame.Color(255, 255, 255))
            if button.choose(200, 200, "red"):
                hero = Red()
                return hero
            elif button2.choose(270, 200, "green"):
                hero = Green()
                return hero

            if button.choosed:
                paused = False
            pygame.display.update()
            pygame.time.delay(100)

    def refresh_screen(self):
        pygame.display.flip()
        self.fps_controller.tick(23)


game = Game()


class Button:
    def __init__(self, width, height, inactive_color, active_color):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.choosed = False

    def choose(self, x, y, text):
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                pygame.draw.rect(game.play_surface, self.active_color, (x, y, self.width, self.height))
                if click[0] == 1:
                    pygame.mixer.Sound.play(button_sound)
                    pygame.time.delay(300)
                    self.choosed = True
                    return True
        else:
            pygame.draw.rect(game.play_surface, self.inactive_color, (x, y, self.width, self.height))

bullets = []
class Bullet:
    def __init__(self, color, pos, speed):
        self.color = color
        self.x = pos[0]
        self.y= pos[1]
        self.mouse = pygame.mouse.get_pos()
        self.end = True
        a = self.mouse[0]-self.x
        b= self.mouse[1]-self.y
        c = (a*a+b*b)**0.5
        sin = a/c
        cos = b/c
        self.speedx = sin*10
        self.speedy = cos*10
        print(a,b)

    def shooting(self):
        pygame.draw.circle(game.play_surface, self.color, (self.x, self.y), 10)

        self.x = self.x+self.speedx
        self.y = self.y+self.speedy

    def waiting(self):
        if self.x > 720 or self.x < 0:
            if self.y > 720 or self.y < 0:
                self.end = False

class Red():
    def __init__(self):
        self.color = pygame.Color(255, 0, 0)
        self.pos = [100, 50]
        self.speed = 10
        self.timing = 0
    def moving(self):

        keys = pygame.key.get_pressed()
        click = pygame.mouse.get_pressed()
        if keys[pygame.K_LEFT]:
            self.pos[0] = self.pos[0] - self.speed
        if keys[pygame.K_RIGHT]:
            self.pos[0] = self.pos[0] + self.speed
        if keys[pygame.K_UP]:
            self.pos[1] = self.pos[1] - self.speed
        if keys[pygame.K_DOWN]:
            self.pos[1] = self.pos[1] + self.speed
        if click[0] == 1:

            if len(bullets)<5 and monotonic()-self.timing>10:
                bullets.append(Bullet(self.color,self.pos,7))
            self.timing = monotonic()






class Green():
    def __init__(self):
        self.color = pygame.Color(0, 255, 0)
        self.pos = [100, 50]
        self.speed = 5

    def moving(self):   
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.pos[0] = self.pos[0] - self.speed
        if keys[pygame.K_RIGHT]:
            self.pos[0] = self.pos[0] + self.speed
        if keys[pygame.K_UP]:
            self.pos[1] = self.pos[1] - self.speed
        if keys[pygame.K_DOWN]:
            self.pos[1] = self.pos[1] + self.speed


def play(hero):
    while game.run:
        game.control()
        hero.moving()
        game.play_surface.fill((0, 0, 0))
        pygame.draw.rect(game.play_surface, hero.color, (hero.pos[0], hero.pos[1], 50, 60))
        for bullet in bullets:
            bullet.waiting()
            if bullet.end:
                bullet.shooting()
            else:
                bullets.pop(bullets.index(bullet))
        game.refresh_screen()
hero = game.pause()
play(hero)
