import pygame
from pygame.draw import *
from random import randint
import numpy as np
pygame.init()


WHITE = (250, 250, 250)
BLACK = (0, 0, 0)

class Game():
    def __init__(self):
        self.weight = 1000
        self.height = 750
        self.screen = pygame.display.set_mode((self.weight, self.height))
        self.x = 0
        self.y = 0
        self.y0 = 2000
        self.x0 = 461
        self.x_max = 500
        self.y_max = 450
        self.x_min = 0
        self.y_min = 0
        self.n = 10

    def game_screen(self):
        # for x in range(10, self.weight + 1, 10):
        #     pygame.draw.line(self.screen, WHITE, [int(x), int(0)], [int(x), int(self.height)], 1)
        # for y in range(10, self.height + 1, 10):
        #     pygame.draw.line(self.screen, WHITE, [int(0), int(y)], [int(self.weight), int(y)], 1)

        dx = int((self.x_max - self.x_min) / self.n)
        dy = int((self.y_max - self.y_min) / self.n)
        for x in range(self.x_min, self.x_max + dx, dx):
            k = self.k_sol(x, 0)
            b = self.b_sol(x, 0)
            x_1, y_1 = self.y_x(self.y_min, k, b), self.y_min
            x_1, y_1 = self.xy(x_1, y_1)
            x_2, y_2 = self.y_x(self.y_max, k, b), self.y_max
            x_2, y_2 = self.xy(x_2, y_2)
            pygame.draw.line(self.screen, WHITE, [x_1, y_1], [x_2, y_2], 1)

        k_min, b_min = self.k_sol(self.x_min, self.y_min), self.b_sol(self.x_min, self.y_min)
        k_max, b_max = self.k_sol(self.x_max, self.y_min), self.b_sol(self.x_max, self.y_min)
        for y in range(self.y_min, self.y_max + dy, dy):
            x_1, y_1 = self.y_x(y, k_min, b_min), y
            x_1, y_1 = self.xy(x_1, y_1)
            x_2, y_2 = self.y_x(y, k_max, b_max), y
            x_2, y_2 = self.xy(x_2, y_2)
            pygame.draw.line(self.screen, WHITE, [x_1, y_1], [x_2, y_2], 1)


        x0, y0 = self.xy(Mouse.x, Mouse.y)
        k, b = self.k_sol(x0, y0), self.b_sol(x0, y0)
        x, y = self.y_x(self.y_min, k, b), y0
        x3, y3 = ((x / dx)//1) * 10, ((y / dy)//1) * 10
        x33, y33 = (x / dx)//0.25%4, (y / dy)//0.25%4
        pygame.draw.circle(Game.screen, WHITE, (Mouse.x, Mouse.y), 5)
        # pygame.draw.circle(Game.screen, WHITE, self.xy_inv(Mouse.x, Mouse.y), 20)
        # pygame.draw.circle(Game.screen, WHITE, self.xy_inv(x3, y3), 10)

        f0 = pygame.font.Font(None, 36)
        text0 = f0.render('x = {}, y = {}'.format(x3, y3), 5, WHITE)
        self.screen.blit(text0, (5, 5))

        # image = pygame.image.load('dom.png').convert_alpha()
        # self.screen.blit(image, (100, 100))

        # image  = pygame.image.load('pechenka.png')  
        # image.set_colorkey(WHITE)
        # image = pygame.transform.scale(image, (1, 1))
        # # image_rect=image.get_rect(topleft=(int(x - 63 * k), int(y - 125 * k)))
        # self.screen.blit(image, (200, 600))




        # pygame.draw.circle(self.screen, WHITE, (100, 100), 10)

    # def trance(self, x, y):
    #     return (x - y*self.alfa, y)

    # def trance_inv(self, x, y):
    #     return (self.x + x + y*self.alfa, self.y + y)

    def y_x(self, y, k, b):
        return (y - b) / k

    def x_y(self, x, k, b):
        return k * x + b

    def xy(self, x, y):
        return (x, self.height - y)

    def xy_inv(self, x, y):
        return (x, abs(y - self.height))

    def k_sol(self, x, y):
        return (self.y0 - y) / (self.x0 - x + 10**(-3))

    def b_sol(self, x, y):
        return (self.x0 * y - self.y0 * x) / (self.x0 - x + 10**(-3))


class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.p = False




Game = Game()
Mouse = Mouse()

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    # clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEMOTION:
            # запись новых координат мышки(если она подвинулась)
            Mouse.x, Mouse.y = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            # кнопка зажата
            Mouse.p = True
        if event.type == pygame.MOUSEBUTTONUP:
            # кнопка отжата
            Mouse.p = False

    Game.game_screen()

    pygame.display.update()
    Game.screen.fill(BLACK)

pygame.quit()