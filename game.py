import pygame
from pygame.draw import *
from random import randint
import numpy as np

from colors import *
from constants import *
from objects import *
from ter import *
from player import *

class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.p = False
        self.enter = False
        self.cycle = []



class Game():
    def __init__(self, name, screen):
        global Mouse
        Mouse = Mouse()
        self.name = name
        self.screen = screen
        self.step_gamer_outpost = False
        self.step_gamer_finish = False
        self.step_computer_outpost = False
        self.step_computer_finish = False
        global x_step, y_step
        x_step = 850
        y_step = 650

        self.t = 0
        self.t0 = 1*FPS

    def game(self):
        self.init_game()

        clock = pg.time.Clock()
        clock1 = pg.time.Clock()
        pg.display.update()
        i = 1
        while True:
            # clock.tick(1)
            out = self.step_gamer(clock)
            if out == 'exit':
                return True
            out1 = self.step_computer(clock)
            if out1 == 'exit':
                return True
            print('----------------------------------------------------------------------------------------------------------------------')
            if i == 3:
                gamer.resources['gold'] += 300
                computer.resources['gold'] += 300
                i = 0
            else:
                i += 1

            # print('--------------------------------')

        return True

    def init_game(self):
        global gamer
        gamer = Gamer(self.name)
        global computer
        computer = Computer()
        global game_field
        game_field = Game_field(self.screen)
        game_field.init_outpost()
        game_field.init_territorie()
        global board
        board = Board(self.screen)

    def step_gamer(self, clock):
        self.step_gamer_outpost = False
        self.step_gamer_finish = False
        while True:
            clock.tick(FPS)
            # print(gamer.myoutpostes, gamer.myoutpostes_build)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'
                if event.type == pygame.MOUSEMOTION:
                    # запись новых координат мышки(если она подвинулась)
                    Mouse.x, Mouse.y = event.pos
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # кнопка зажата
                    Mouse.p = True
                if event.type == pygame.MOUSEBUTTONUP:
                    # кнопка отжата
                    Mouse.p = False
                if event.type == pygame.KEYDOWN:
                    # кнопка отжата
                    if event.key == pygame.K_RETURN:
                        Mouse.enter = True

            if self.t > 0:
                self.t -= 1

            rect(self.screen, WHITE, (x_step - 5, y_step - 5, 130, 30))
            f0 = pygame.font.Font(None, 24)
            text0 = f0.render('закончить ход', 5, MAGENTA)
            self.screen.blit(text0, (x_step, y_step))

            if game_field.t1 > 0:
                f0 = pygame.font.Font(None, 24)
                text0 = f0.render('Вы проиграли бой', 5, MAGENTA)
                self.screen.blit(text0, (400, 100))

            board.draw(gamer)
            board.draw_exchange(gamer)
            # print('11111')
            out = game_field.draw(gamer, self.step_gamer_outpost, computer)
            if out:
                self.step_gamer_outpost = True
            print(self.step_gamer_outpost)
            if (Mouse.x > x_step) and (Mouse.x < x_step + 130) and (Mouse.y > y_step) and (Mouse.y < y_step + 30) and Mouse.p and self.t == 0:
                self.t = self.t0
                break
            if Mouse.enter and self.step_gamer_outpost:
                break
            pg.display.update()
            self.screen.fill(BLACK)
        print('-------------------------------------------------------------')
        game_field.built_outposts(gamer)
        cycle = game_field.check_cycle(gamer)
        if cycle != []:
            gamer.cycle.append(cycle)
            game_field.change_ter(gamer.cycle[len(gamer.cycle) - 1], gamer)
        game_field.get_resourses(gamer)
        Mouse.enter = False
        game_field.p_outpost = None

        if gamer.resources['army'] < 1000 * gamer.resources['food'] and gamer.resources['food'] > 0:
            gamer.resources['army'] += int(np.log(gamer.resources['food']) * 100)

        return 'finish'


    def step_computer(self, clock):
        self.step_computer_outpost = False
        self.step_computer_finish = False
        while True:
            clock.tick(FPS)
            # print(computer.myoutpostes, computer.myoutpostes_build)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'
                if event.type == pygame.MOUSEMOTION:
                    # запись новых координат мышки(если она подвинулась)
                    Mouse.x, Mouse.y = event.pos
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # кнопка зажата
                    Mouse.p = True
                if event.type == pygame.MOUSEBUTTONUP:
                    # кнопка отжата
                    Mouse.p = False
                if event.type == pygame.KEYDOWN:
                    # кнопка отжата
                    if event.key == pygame.K_RETURN:
                        Mouse.enter = True

            if self.t > 0:
                self.t -= 1

            print(self.t)

            rect(self.screen, WHITE, (x_step - 5, y_step - 5, 130, 30))
            f0 = pygame.font.Font(None, 24)
            text0 = f0.render('закончить ход', 5, MAGENTA)
            self.screen.blit(text0, (x_step, y_step))

            if game_field.t1 > 0:
                f0 = pygame.font.Font(None, 24)
                text0 = f0.render('Вы проиграли бой', 5, MAGENTA)
                self.screen.blit(text0, (400, 100))

            board.draw(computer)
            board.draw_exchange(computer)
            # print('11111')
            out = game_field.draw(computer, self.step_computer_outpost, gamer)
            if out:
                self.step_computer_outpost = True
            # print(self.step_gamer_outpost)
            if (Mouse.x > x_step) and (Mouse.x < x_step + 130) and (Mouse.y > y_step) and (Mouse.y < y_step + 30) and Mouse.p and self.t == 0:
                self.t = self.t0
                break
            if Mouse.enter and self.step_computer_outpost:
                break
            pg.display.update()
            self.screen.fill(BLACK)
        print('-------------------------------------------------------------')
        game_field.built_outposts(computer)
        cycle = game_field.check_cycle(computer)
        if cycle != []:
            computer.cycle.append(cycle)
            game_field.change_ter(computer.cycle[len(computer.cycle) - 1], computer)
        game_field.get_resourses(computer)
        Mouse.enter = False
        game_field.p_outpost = None

        if computer.resources['army'] < 1000 * computer.resources['food'] and computer.resources['food'] > 0:
            computer.resources['army'] += int(np.log(computer.resources['food']) * 100)

        return 'finish'

    def check_game_over(self):
        pass


class Board():
    def __init__(self, screen):
        self.screen = screen
        self.x = 50
        self.y = 50

        self.g_b = [100, 100]
        self.g_f = [100, 100]
        self.g_a = [100, 100]

        self.t0 = 1 * FPS
        self.t = 0

    def draw(self, player):
        rect(self.screen, RED, (self.x, self.y, 150, 300))

        f0 = pygame.font.Font(None, 24)
        text0 = f0.render(f'player: {player.name}', 5, WHITE)
        self.screen.blit(text0, (self.x + 10, self.y + 10))

        i = 25
        for elem in player.resources:
            f0 = pygame.font.Font(None, 24)
            text0 = f0.render(f'{elem}: {player.resources[elem]}', 5, WHITE)
            self.screen.blit(text0, (self.x + 10, self.y + 10 + i))
            i += 25

    def draw_exchange(self, player):
        f0 = pygame.font.Font(None, 24)
        text0 = f0.render(f'{self.g_b[0]}*gold --> {self.g_b[1]}*building', 5, WHITE)
        self.screen.blit(text0, (self.x + 10, self.y + 160))

        f0 = pygame.font.Font(None, 24)
        text0 = f0.render(f'{self.g_f[0]}*gold --> {self.g_f[1]}*food', 5, WHITE)
        self.screen.blit(text0, (self.x + 10, self.y + 185))

        f0 = pygame.font.Font(None, 24)
        text0 = f0.render(f'{self.g_a[0]}*gold --> {self.g_a[1]}*army', 5, WHITE)
        self.screen.blit(text0, (self.x + 10, self.y + 210))

        if self.t == 0:
            if (Mouse.x > self.x + 10) and (Mouse.x < self.x + 10 + 150) and (Mouse.y > self.y + 160) and (Mouse.y < self.y + 160 + 20) and Mouse.p and player.resources['gold'] >= self.g_b[0]:
                self.exchange_gold_building(player)
                self.t = self.t0
            if (Mouse.x > self.x + 10) and (Mouse.x < self.x + 10 + 150) and (Mouse.y > self.y + 185) and (Mouse.y < self.y + 185 + 20) and Mouse.p and player.resources['gold'] >= self.g_f[0]:
                self.exchange_gold_food(player)
                self.t = self.t0
            if (Mouse.x > self.x + 10) and (Mouse.x < self.x + 10 + 150) and (Mouse.y > self.y + 210) and (Mouse.y < self.y + 210 + 20) and Mouse.p and player.resources['gold'] >= self.g_a[0]:
                self.exchange_gold_army(player)
                self.t = self.t0
        else:
            self.t -= 1


    def exchange_gold_building(self, player):
        player.resources['gold'] -= self.g_b[0]
        player.resources['building'] += self.g_b[1]

    def exchange_gold_food(self, player):
        player.resources['gold'] -= self.g_f[0]
        player.resources['food'] += self.g_f[1]

    def exchange_gold_army(self, player):
        player.resources['gold'] -= self.g_a[0]
        player.resources['army'] += self.g_a[1]



class Game_field():
    def __init__(self, screen):
        self.screen = screen
        self.x = 250
        self.y = 100
        self.y0 = 2000
        self.x0 = 461
        self.x_max = 500
        self.y_max = 450
        self.x_min = 0
        self.y_min = 0
        self.n = 10

        self.p_outpost = None
        self.t0 = 1*FPS
        self.t = 0
        self.t1 = 0

        self.x3 = 0
        self.y3 = 0
        self.pos = ''

        # self.no = False

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
        k = self.k_sol(self.x_min + self.dx * (i + 0.5), self.y_min)
        b = self.b_sol(self.x_min + self.dx * (i + 0.5), self.y_min)
        x, y = self.y_x(self.y_min + self.dy * (j + 0.5), k, b), self.y_min + self.dy * (j + 0.5)
        x, y = self.xy(self.x + x, self.y + y)
        return Territory(x, y, self.screen)
        

    def draw(self, player, step_player_outpost, player1):
        game_field.game_field()
        game_field.draw_outpostes()
        # game_field.grid()
        game_field.draw_territories()
        return game_field.interaction_with_fied(player, step_player_outpost, player1)

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

    def interaction_with_fied(self, player, step_player_outpost, player1):
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

            self.territories[x3][y3].draw_information()

        if self.p_outpost != None:
            out = self.outpostes[self.p_outpost[0]][self.p_outpost[1]].draw_information(Mouse.x, Mouse.y, Mouse.p)
            if out and self.t == 0 and self.outpostes[self.p_outpost[0]][self.p_outpost[1]].player == player.name and player.resources['building'] >= 100:
                self.outpostes[self.p_outpost[0]][self.p_outpost[1]].moves -= 1
                if self.outpostes[self.p_outpost[0]][self.p_outpost[1]].moves == 0:
                    player.myoutpostes_build.remove((x3, y3))
                    player.myoutpostes.append((x3, y3))
                    self.outpostes[x3][y3].check_build()
                player.resources['building'] -= 100
                self.t = self.t0
        if self.t > 0:
            self.t -= 1
        if self.t1 > 0:
            self.t1 -= 1
        # if self.t2 > 0:
        #     self.t2 -= 1
        # print(self.p_outpost)
        if self.pos == 'Outpost' and x3 >= 0 and x3 <= 10 and y3 >= 0 and y3 <= 10:
            f0 = pygame.font.Font(None, 36)
            text0 = f0.render('x = {}, y = {}, pos = {}'.format(x3, y3, 'Outpost'), 5, WHITE)
            self.screen.blit(text0, (300, 5))

            if self.p_outpost == None:
                self.outpostes[x3][y3].draw_information(Mouse.x, Mouse.y, Mouse.p)
            # print(self.p_outpost)
            if self.p_outpost == (x3, y3) and Mouse.p and self.t == 0:
                print('------------------------------------------------')
                self.p_outpost = None
                self.t = self.t0
            if Mouse.p and self.t == 0:
                self.p_outpost = (x3, y3)
                self.t = self.t0

            if Mouse.p and self.outpostes[x3][y3].player == '' and not step_player_outpost and self.outpostes[x3][y3].cost <= player.resources['gold']:
                for x, y in player1.myoutpostes_build:
                    print(x, y)
                    if abs(x3 - x) == 1 or abs(y3 - y) == 1:
                        print(x, y)
                        out = self.outpostes[x3][y3].check_stranger(player, player1, self.outpostes[x][y])
                        if out == None:
                            break
                        elif out:
                            self.outpostes[x][y].exist = False
                            print(x, y)
                            player1.myoutpostes_build.remove((x, y))
                            print('1111111111111111111111111111111111111111111111111111111111111111')
                            break
                        else:
                            self.outpostes[x3][y3].exist = False
                            print('2222222222222222222222222222222222222222222222222222222222222222')
                            self.t1 = self.t0
                            return True
                self.outpostes[x3][y3].player = player.name
                player.resources['gold'] -= self.outpostes[x3][y3].cost
                # voc = player.myoutpostes
                # print(player.myoutpostes)
                # print('voc', voc, 'voc.ap', voc.append((x3, y3)))
                player.myoutpostes_build.append((x3, y3))
                # print(player.myoutpostes)
                return True
        return False

    def draw_outpostes(self):
        for x, y in gamer.myoutpostes:
            self.outpostes[x][y].draw()
        for x, y in gamer.myoutpostes_build:
            self.outpostes[x][y].draw()
        for x, y in computer.myoutpostes:
            self.outpostes[x][y].draw()
        for x, y in computer.myoutpostes_build:
            self.outpostes[x][y].draw()


    def draw_territories(self):
        for j in range(self.n):
            for i in range(self.n):
                self.territories[i][j].draw()

    def check_cycle(self, player):
        a = player.myoutpostes[:]
        # print(player.cycle)
        b = []
        for elem in player.cycle:
            for ele in elem:
                b.append(ele)
        b = set(b)
        # print(a, player.myoutpostes_build)
        for x0, y0 in a[::-1]:
            if (x0, y0) not in b:
                out = graph(x0, y0, self.outpostes, player.name, a)
                # print('-------------------------------------------------------------------------------------------')
                # print()
                if out[0]:
                    k = 0
                    for elem in player.cycle:
                        if set(out[1]) == set(elem):
                            k = 1
                    if len(out[1]) != (len(set(out[1])) + 1):
                        k = 1
                    if k == 0:
                        # print('-------------------------------------------------------------------------------------------')
                        return out[1]
        # print('-------------------------------------------------------------------------------------------')
        return []

    def change_ter(self, cycle, player):
        for i in range(self.n):
            for j in range(self.n):
                if self.territories[i][j].player == '':
                    if prove(cycle, i, j):
                        # print(cycle)
                        self.territories[i][j].player = player.name
                        self.change_near_out(player, i, j)
        self.change_cycle_out(player, cycle)

    def change_near_out(self, player, x, y):
        self.outpostes[x][y].player = 'occupied'
        self.outpostes[x + 1][y].player = 'occupied'
        self.outpostes[x + 1][y + 1].player = 'occupied'
        self.outpostes[x][y + 1].player = 'occupied'

    def change_cycle_out(self, player, cycle):
        for x, y in cycle:
            self.outpostes[x][y].player = player.name

    def built_outposts(self, player):
        outpostes = player.myoutpostes_build[:]
        for x, y in outpostes:
            # print(x, y)
            out = self.outpostes[x][y].build_outposte()
            # print(x, y, self.outpostes[x][y].moves)
            if out:
                player.myoutpostes_build.remove((x, y))
                player.myoutpostes.append((x, y))
                self.outpostes[x][y].check_build()

    def get_resourses(self, player):
        for x in range(self.n):
            for y in range(self.n):
                if self.territories[x][y].player == player.name:
                    print('33333333333333333333333333333')
                    player.resources = {**player.resources, **self.territories[x][y].resources}
