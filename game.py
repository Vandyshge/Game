import pygame
from pygame.draw import *
from random import randint
import numpy as np

from colors import *
from constants import *
from objects import *

class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.p = False


class Game():
    def __init__(self, name, screen):
        global Mouse
        Mouse = Mouse()
        self.name = name
        self.screen = screen

    def game(self):
        self.init_game()

        board = Board(self.screen)

        clock = pg.time.Clock()
        pg.display.update()
        while True:
            clock.tick(FPS)
            # print('2')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.MOUSEMOTION:
                    # запись новых координат мышки(если она подвинулась)
                    Mouse.x, Mouse.y = event.pos
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # кнопка зажата
                    Mouse.p = True
                if event.type == pygame.MOUSEBUTTONUP:
                    # кнопка отжата
                    Mouse.p = False

            board.draw()
            out = game_field.draw()
            if out:
                out1 = game_field.check_ter(gamer)
                print('game', out1)

            pg.display.update()
            self.screen.fill(BLACK)

        return True

    def init_game(self):
        global gamer
        gamer = Gamer(self.name)
        global game_field
        game_field = Game_field(self.screen)
        game_field.init_outpost()
        game_field.init_territorie()


class Board():
    def __init__(self, screen):
        self.screen = screen
        self.x = 50
        self.y = 50

    def draw(self):
        rect(self.screen, RED, (self.x, self.y, 150, 300))

        f0 = pygame.font.Font(None, 24)
        text0 = f0.render(f'player: {gamer.name}', 5, WHITE)
        self.screen.blit(text0, (self.x + 10, self.y + 10))

        i = 25
        for elem in gamer.resources:
            f0 = pygame.font.Font(None, 24)
            text0 = f0.render(f'{elem}: {gamer.resources[elem]}', 5, WHITE)
            self.screen.blit(text0, (self.x + 10, self.y + 10 + i))
            i += 25


class Game_field():
    def __init__(self, screen):
        self.screen = screen
        self.x = 250
        self.y = 100
        self.y0 = 4000
        self.x0 = 461
        self.x_max = 500
        self.y_max = 450
        self.x_min = 0
        self.y_min = 0
        self.n = 10

        self.x3 = 0
        self.y3 = 0
        self.pos = ''

        self.dx = int((self.x_max - self.x_min) / self.n)
        self.dy = int((self.y_max - self.y_min) / self.n)

        self.outpostes = [[0 for j in range(self.n + 1)] for i in range(self.n + 1)]
        self.territories = [[0 for j in range(self.n)] for i in range(self.n)]

    def init_outpost(self):
        for j in range(self.n + 1):
            for i in range(self.n + 1):
                k = self.k_sol(self.x_min + self.dx * i, self.y_min)
                b = self.b_sol(self.x_min + self.dx * i, self.y_min)
                x, y = self.y_x(self.y_min + self.dy * j, k, b), self.y_min + self.dy * j
                x, y = self.xy(self.x + x, self.y + y)
                self.outpostes[i][j] = Outpost(int(x), int(y), self.screen)

    def init_territorie(self):
        for i in range(self.n):
            for j in range(self.n):
                self.territories[i][j] = self.create_obj(j, i)

    def create_obj(self, j, i):
        cells = ['forest', 'golden vein', 'mercenaries', 'enemies', 'farm', 'pie']
        name = cells[randint(0, len(cells) - 1)]
        k = self.k_sol(self.x_min + self.dx * (i + 0.5), self.y_min)
        b = self.b_sol(self.x_min + self.dx * (i + 0.5), self.y_min)
        x, y = self.y_x(self.y_min + self.dy * (j + 0.5), k, b), self.y_min + self.dy * (j + 0.5)
        x, y = self.xy(self.x + x, self.y + y)
        if name == 'forest':
            return Forest(int(x), int(y), self.screen)
        elif name == 'golden vein':
            return GoldVein(int(x), int(y), self.screen)
        elif name == 'mercenaries':
            return Mercenaries(int(x), int(y), self.screen)
        elif name == 'enemies':
            return Enemies(int(x), int(y), self.screen)
        elif name == 'farm':
            return Farm(int(x), int(y), self.screen)
        elif name == 'pie':
            return Pie(int(x), int(y), self.screen)

    def draw(self):
        game_field.draw_outpostes()
        # game_field.grid()
        game_field.game_field()
        return game_field.interaction_with_fied()

    def grid(self):
        # pg.draw.circle(self.screen, RED, (10, 10), 10000)
        for x in range(10, weight + 1, 10):
            line(self.screen, WHITE, [int(x), int(0)], [int(x), int(height)], 1)
        for y in range(10, height + 1, 10):
            line(self.screen, WHITE, [int(0), int(y)], [int(weight), int(y)], 1)

    def game_field(self):
        for x in range(self.x_min, self.x_max + self.dx, self.dx):
            k = self.k_sol(x, self.y_min)
            b = self.b_sol(x, self.y_min)
            x_1, y_1 = self.y_x(self.y_min, k, b), self.y_min
            x_1, y_1 = self.xy(x_1 + self.x, y_1 + self.y)
            x_2, y_2 = self.y_x(self.y_max, k, b), self.y_max
            x_2, y_2 = self.xy(x_2 + self.x, y_2 + self.y)
            pygame.draw.line(self.screen, WHITE, [x_1, y_1], [x_2, y_2], 1)

        k_min, b_min = self.k_sol(self.x_min, self.y_min), self.b_sol(self.x_min, self.y_min)
        k_max, b_max = self.k_sol(self.x_max, self.y_min), self.b_sol(self.x_max, self.y_min)
        for y in range(self.y_min, self.y_max + self.dy, self.dy):
            x_1, y_1 = self.y_x(y, k_min, b_min), y
            x_1, y_1 = self.xy(x_1 + self.x, y_1 + self.y)
            x_2, y_2 = self.y_x(y, k_max, b_max), y
            x_2, y_2 = self.xy(x_2 + self.x, y_2 + self.y)
            pygame.draw.line(self.screen, WHITE, [x_1, y_1], [x_2, y_2], 1)


    def y_x(self, y, k, b):
        return (y - b) / (k + 10**(-3))

    def x_y(self, x, k, b):
        return k * x + b

    def xy(self, x, y):
        return (x, height - y)

    def xy_inv(self, x, y):
        return (x, abs(y - height))

    def k_sol(self, x, y):
        return (self.y0 - y) / (self.x0 - x + 10**(-3))

    def b_sol(self, x, y):
        return (self.x0 * y - self.y0 * x) / (self.x0 - x + 10**(-3))

    def interaction_with_fied(self):
        x0, y0 = self.xy(Mouse.x, Mouse.y)
        x0, y0 = x0 - self.x, y0 - self.y
        k, b = self.k_sol(x0, y0), self.b_sol(x0, y0)
        x, y = self.y_x(self.y_min, k, b), y0
        x3, y3 = int((x / self.dx)//1), int((y / self.dy)//1)
        x33, y33 = int((x / self.dx)//0.25%4), int((y / self.dy)//0.25%4)
        pygame.draw.circle(self.screen, WHITE, (Mouse.x, Mouse.y), 5)

        f0 = pygame.font.Font(None, 36)
        text0 = f0.render('x3 = {}, y3 = {}'.format(x3, y3), 5, WHITE)
        self.screen.blit(text0, (5, 5))

        f0 = pygame.font.Font(None, 36)
        text0 = f0.render('x33 = {}, y33 = {}'.format(x33, y33), 5, WHITE)
        self.screen.blit(text0, (5, 25))

        if x3 >= 0 and x3 <= 10 and y3 >= 0 and y3 <= 10:
            if x33 == 3 and y33 == 3:
                x3 += 1
                y3 += 1
                self.pos = 'Outpost'
            elif x33 == 3 and y33 == 0:
                x3 += 1
                self.pos = 'Outpost'
            elif x33 == 0 and y33 == 3:
                y3 += 1
                self.pos = 'Outpost'
            elif x33 == 0 and y33 == 0:
                self.pos = 'Outpost'
            elif x3 <= 9 and y3 <= 9:
                self.pos = 'Territories'

        if self.pos == 'Territories' and x3 >= 0 and x3 <= 9 and y3 >= 0 and y3 <= 9:
            f0 = pygame.font.Font(None, 36)
            text0 = f0.render('x = {}, y = {}, pos = {}'.format(self.territories[x3][y3].x, self.outpostes[x3][y3].y, 'Outpost'), 5, WHITE)
            self.screen.blit(text0, (300, 5))

        if self.pos == 'Outpost' and x3 >= 0 and x3 <= 10 and y3 >= 0 and y3 <= 10:
            f0 = pygame.font.Font(None, 36)
            text0 = f0.render('x = {}, y = {}, pos = {}'.format(x3, y3, 'Outpost'), 5, WHITE)
            self.screen.blit(text0, (300, 5))

            self.outpostes[x3][y3].draw_information()

            if Mouse.p and self.outpostes[x3][y3].player == '':
                self.outpostes[x3][y3].player = gamer.name
                gamer.resources['gold'] -= self.outpostes[x3][y3].cost
                # voc = gamer.myoutpostes
                # print(gamer.myoutpostes)
                # print('voc', voc, 'voc.ap', voc.append((x3, y3)))
                gamer.myoutpostes.append((x3, y3))
                # print(gamer.myoutpostes)
                return True
        return False

    def draw_outpostes(self):
        for j in range(self.n + 1):
            for i in range(self.n + 1):
                if self.outpostes[i][j].player != '':
                    self.outpostes[i][j].draw()

    def check_neighbors(self, name, graph):
        print('c_n', graph)
        x, y = graph[len(graph) - 1][0], graph[len(graph) - 1][1]
        x0, y0 = graph[len(graph) - 2][0], graph[len(graph) - 2][1]
        print(f'x0, y0 = {x0}, {y0}, x, y = {x}, {y}')
        a = []
        if y + 1 <= 10:
            if self.outpostes[x][y + 1].player == name and (x0, y0) != (x, y + 1):
                print('check_gra_0_2', x, y + 1)
                b = graph[:]
                print('oh', b)
                b.append((x, y + 1))
                a.append(b)
                print('oho', a)
        if y - 1 >= 0:
            if self.outpostes[x][y - 1].player == name and (x0, y0) != (x, y - 1):
                print('check_gra_0_2', x, y - 1)
                b = graph[:]
                print('oh', b)
                b.append((x, y - 1))
                a.append(b)
                print('oho', a)
        if x + 1 >= 0:
            if self.outpostes[x + 1][y].player == name and (x0, y0) != (x + 1, y):
                print('check_gra_0_2', x + 1, y)
                b = graph[:]
                print('oh', b)
                b.append((x + 1, y))
                a.append(b)
                print('oho', a)
        if x - 1 >= 0:
            if self.outpostes[x - 1][y].player == name and (x0, y0) != (x - 1, y):
                print('check_gra_0_2', x - 1, y)
                b = graph[:]
                print('oh', b)
                b.append((x - 1, y))
                a.append(b)
                print('oho', a)
        print('check_gra_0', a)
        return a

    def check_neighbors_0(self, name, x, y):
        a = []
        if y + 1 <= 10:
            print('check_gra_0_1')
            if self.outpostes[x][y + 1].player == name:
                print('check_gra_0_2')
                a.append([(x, y), (x, y + 1)])
        if y - 1 >= 0:
            print('check_gra_0_1')
            if self.outpostes[x][y - 1].player == name:
                print('check_gra_0_2')
                a.append([(x, y), (x, y - 1)])
        if x - 1 >= 0:
            print('check_gra_0_1', self.outpostes[x - 1][y + 1].player)
            if self.outpostes[x - 1][y].player == name:
                print('check_gra_0_2')
                a.append([(x, y), (x - 1, y)])
        if x + 1 >= 0:
            if self.outpostes[x + 1][y].player == name:
                print('check_gra_0_2')
                a.append([(x, y), (x + 1, y)])
        print('check_gra_0', a)
        return a

    def graph(self, x0, y0, name):
        graph0 = []
        for elem_1 in self.check_neighbors_0(name, x0, y0):
            graph0.append(elem_1)
        print('graph_1', graph0)
        if len(graph0) == 0:
            return (False, 0)
        while True:
            graph1 = []
            for elem in graph0:
                for elem_1 in self.check_neighbors(name, elem):
                    graph1.append(elem_1)
                print('for graph1', graph1)
                print()
            print('graph', graph1)
            if graph1 == []:
                print('false')
                return (False, 0)
            graph0 = graph1[:]
            for elem in graph0:
                if elem[len(elem) - 1] == (x0, y0):
                    return (True, elem)

    def check_ter(self, player):
        a = player.myoutpostes
        print('check_ter', a, player.name)
        for x0, y0 in a:
            out = self.graph(x0, y0, player.name)
            print('-------------------------------------------------------------------------------------------')
            print()
            if out[0]:
                print('-------------------------------------------------------------------------------------------')
                return out[1]
        print('-------------------------------------------------------------------------------------------')
        return []






class Gamer():
    def __init__(self, name):
        self.name = name
        self.resources = {'gold': 1000, 'building': 0, 'food': 0, 'army': 0}
        self.myoutpostes = []

class Computer():
    def __init__(self):
        self.name = 'computer'
        self.resources = {'gold': 1000, 'building': 0, 'food': 0, 'army': 0}
        self.myoutpostes = []