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
        '''
        Мышка
        '''
        self.x = 0 # x координата мышки
        self.y = 0 # y координата мышки
        self.p = False # зажата ли кнопка мыши
        self.enter = False # нажат ли Enter


class Game00():
    def __init__(self, name1, name2, screen):
        '''
        игра
        :param screen: экран на который выводиться изображение
        '''
        global Mouse
        Mouse = Mouse()
        self.name1 = name1 # имя игрока
        self.name2 = name2
        self.screen = screen # экран на который выводиться изображение
        self.step_player_outpost = False # поставил ли игрок аванпост в этот ход
        global x_step, y_step
        x_step = 850 # x координата кнопки "закончить ход"
        y_step = 650 # y координата кнопки "закончить ход"

        self.t = 0 # время задержки(сейчас)
        self.t0 = 1*FPS # время задержки(по дефолту)
        self.outpostes_num = 0 # количество занятых аванпостов
        self.win = '' # имя того кто победил
        self.n_win = 0

        self.image_game = pg.image.load('image\game.jpg').convert_alpha()

    def game(self):
        '''
        основная функция игры
        :return: True - нажали на крестик
        '''
        self.init_game()

        clock = pg.time.Clock()
        clock1 = pg.time.Clock()
        pg.display.update()
        i = 1
        while True:
            # clock.tick(1)
            out = self.step_player(clock, gamer1, gamer2)
            if out == 'exit':
                return (True, )
            out2 = self.check_game_over()
            if out2:
                break

            out1 = self.step_player(clock, gamer2, gamer1)
            if out1 == 'exit':
                return (True, )
            out2 = self.check_game_over()
            if out2:
                break

            print('-------------------------------------------------'
                  '---------------------------------------------------------------------')
            if i == 3:
                gamer1.resources['gold'] += 100
                gamer2.resources['gold'] += 100
                i = 0
            else:
                i += 1

        while True:
            out = self.after_game_over(clock)
            if out == 'exit':
                return (True, )
            elif out == 'menu':
                return ('Menu_page', self.win, self.n_win)
            # print('--------------------------------')

        return (True, )

    def init_game(self):
        '''
        инициация игры, всех объектов и тд
        '''
        global gamer1
        gamer1 = Gamer(self.name1)
        global gamer2
        gamer2 = Gamer(self.name2)
        global game_field
        game_field = Game_field(self.screen)
        game_field.init_outpost()
        game_field.init_territorie()
        global board
        board = Board(self.screen)

    def step_player(self, clock, player, player1):
        '''
        ход игрока
        :param clock: объект часов
        :return: "exit" - нажата кнопка выход, "finish" - ход закончен
        '''
        self.step_player_outpost = False
        while True:
            clock.tick(FPS)
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

            self.screen.blit(self.image_game, (0, 0))

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

            board.draw(player)
            board.draw_exchange(player)
            # print('11111')
            out = game_field.draw(player, self.step_player_outpost, player1)
            if out:
                self.step_player_outpost = True
                self.outpostes_num += 1
            print(self.step_player_outpost)
            if (Mouse.x > x_step) and (Mouse.x < x_step + 130) and (Mouse.y > y_step) and (Mouse.y < y_step + 30) and Mouse.p and self.t == 0:
                self.t = self.t0
                break
            if Mouse.enter and self.step_player_outpost:
                break
            pg.display.update()
            self.screen.fill(BLACK)
        print('-------------------------------------------------------------')
        game_field.built_outposts(player)
        cycle = game_field.check_cycle(player)
        if cycle != []:
            player.cycle.append(cycle)
            game_field.change_ter(player.cycle[len(player.cycle) - 1], player)
        game_field.get_resourses(player)
        Mouse.enter = False
        game_field.p_outpost = None

        if player.resources['army'] < 100 * player.resources['food'] and player.resources['food'] > 0:
            player.resources['army'] += int(np.log(player.resources['food']) * 100)

        return 'finish'

    def check_game_over(self):
        '''
        проверка окончания игры
        :return: закончена или нет
        '''
        if self.outpostes_num == 121:
            n_gamer1 = 0
            n_gamer2 = 0
            for i in range(game_field.n):
                for j in range(game_field.n):
                    if game_field.territories[i][j].player == gamer1.name:
                        n_computer += 1
                    elif game_field.territories[i][j].player == '':
                        pass
                    elif game_field.territories[i][j].player == gamer2.name:
                        n_gamer += 1
            if n_gamer2 > n_gamer1:
                self.win = gamer2.name
                self.n_win = n_gamer2
            elif n_gamer2 == n_gamer1:
                self.win = 'draw'
            elif n_gamer2 < n_gamer1:
                self.win = gamer1.name
                self.n_win = n_gamer1
            return True
        return False

    def after_game_over(self, clock):
        '''
        экран игры после окончания
        :param clock: объект часов
        :return: exit - выход из приложения, menu - нажата кнопка "вернуться в меню"
        '''
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

        self.screen.blit(self.image_game, (0, 0))

        out = game_field.draw_game_over()

        f0 = pygame.font.Font(None, 36)
        text0 = f0.render('GAME OVER', 5, WHITE)
        self.screen.blit(text0, (300, 10))

        if self.win != 'draw':
            f0 = pygame.font.Font(None, 36)
            text0 = f0.render(f'Выиграл {self.win}', 5, WHITE)
            self.screen.blit(text0, (300, 40))
        else:
            f0 = pygame.font.Font(None, 36)
            text0 = f0.render('Ничья', 5, WHITE)
            self.screen.blit(text0, (300, 40))

        rect(self.screen, WHITE, (x_step - 5, y_step - 5, 130, 30))
        f0 = pygame.font.Font(None, 24)
        text0 = f0.render('вернуться в меню', 5, MAGENTA)
        self.screen.blit(text0, (x_step, y_step))

        if (Mouse.x > x_step) and (Mouse.x < x_step + 130) and (Mouse.y > y_step) and (Mouse.y < y_step + 30) and Mouse.p:
            return 'menu'

        pg.display.update()
        self.screen.fill(BLACK)






class Board():
    def __init__(self, screen):
        '''
        таблица ресурсов и обмена
        :param screen: экран, на который выводиться
        '''
        self.screen = screen # экран
        self.x = 50 # x координата таблицы
        self.y = 50 # y координата таблицы

        self.g_b = [110, 100] # по первым буквам: g(gold) --> b(building). Курс обмена ресурсов
        self.g_f = [100, 20]
        self.g_a = [100, 90]
        self.b_g = [100, 90]
        self.f_g = [100, 360]
        self.a_g = [100, 90]
        
        self.t0 = 1 * FPS # время задержки(сейчас)
        self.t = 0 # ремя задержки(по дефолту)

    def draw(self, player):
        '''
        рисует таблицу
        :param player: игрок
        '''
        rect(self.screen, СYAN_BOARD, (self.x, self.y, 220, 320))

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
        '''
        рисует обмен ресурсов и производит обмен
        :param player: объект-игрок
        '''
        f0 = pygame.font.Font(None, 24)
        text0 = f0.render(f'{self.g_b[0]}*gold --> {self.g_b[1]}*building', 5, WHITE)
        self.screen.blit(text0, (self.x + 10, self.y + 160))

        f0 = pygame.font.Font(None, 24)
        text0 = f0.render(f'{self.g_f[0]}*gold --> {self.g_f[1]}*food', 5, WHITE)
        self.screen.blit(text0, (self.x + 10, self.y + 185))

        f0 = pygame.font.Font(None, 24)
        text0 = f0.render(f'{self.g_a[0]}*gold --> {self.g_a[1]}*army', 5, WHITE)
        self.screen.blit(text0, (self.x + 10, self.y + 210))

        f0 = pygame.font.Font(None, 24)
        text0 = f0.render(f'{self.b_g[0]}*building --> {self.b_g[1]}*gold', 5, WHITE)
        self.screen.blit(text0, (self.x + 10, self.y + 235))

        f0 = pygame.font.Font(None, 24)
        text0 = f0.render(f'{self.f_g[0]}*food --> {self.f_g[1]}*gold', 5, WHITE)
        self.screen.blit(text0, (self.x + 10, self.y + 260))

        f0 = pygame.font.Font(None, 24)
        text0 = f0.render(f'{self.a_g[0]}*army --> {self.a_g[1]}*gold', 5, WHITE)
        self.screen.blit(text0, (self.x + 10, self.y + 285))

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
            if (Mouse.x > self.x + 10) and (Mouse.x < self.x + 10 + 150) and (Mouse.y > self.y + 235) and (Mouse.y < self.y + 235 + 20) and Mouse.p and player.resources['gold'] >= self.b_g[0]:
                self.exchange_building_gold(player)
                self.t = self.t0
            if (Mouse.x > self.x + 10) and (Mouse.x < self.x + 10 + 150) and (Mouse.y > self.y + 260) and (Mouse.y < self.y + 260 + 20) and Mouse.p and player.resources['gold'] >= self.f_g[0]:
                self.exchange_food_gold(player)
                self.t = self.t0
            if (Mouse.x > self.x + 10) and (Mouse.x < self.x + 10 + 150) and (Mouse.y > self.y + 285) and (Mouse.y < self.y + 285 + 20) and Mouse.p and player.resources['gold'] >= self.a_g[0]:
                self.exchange_army_gold(player)
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

    def exchange_building_gold(self, player):
        player.resources['gold'] += self.b_g[0]
        player.resources['building'] -= self.b_g[1]

    def exchange_food_gold(self, player):
        player.resources['gold'] += self.b_f[0]
        player.resources['food'] -= self.b_f[1]

    def exchange_army_gold(self, player):
        player.resources['gold'] += self.a_g[0]
        player.resources['army'] -= self.a_g[1]


class Game_field():
    def __init__(self, screen):
        '''
        игровое поле
        :param screen: экран
        '''
        self.screen = screen # экран
        self.x = 250 # x координата нижней левой точки в Нормальной СО
        self.y = 100 # y координата нижней левой точки в Нормальной СО
        self.y0 = 2000 # y координата точки Перспектива в Нормальной СО
        self.x0 = 461 # x координата точки Перспектива в Нормальной СО
        self.x_max = 500 # параметры поля
        self.y_max = 450
        self.x_min = 0
        self.y_min = 0
        self.n = 10 # кол-во полей

        self.p_outpost = None # у какого аванпоста фиксируется информация
        self.t0 = 1*FPS # время задерки(дефолтное)
        self.t = 0 # время задержки(сейчас)
        self.t1 = 0 # время задержки(сейчас)

        self.x3 = 0 # координаты объекта на оторый наводиться мышка
        self.y3 = 0
        self.pos = '' # тип этого объека

        self.dx = int((self.x_max - self.x_min) / self.n) # параметры поля
        self.dy = int((self.y_max - self.y_min) / self.n)

        self.outpostes = [[0 for j in range(self.n + 1)] for i in range(self.n + 1)] # массив с аванпостами(объектами)
        self.territories = [[0 for j in range(self.n)] for i in range(self.n)] # массив с территориями(объектами)

    def init_outpost(self):
        '''
        инициализиркуется массив аванпостов
        '''
        for j in range(self.n + 1):
            for i in range(self.n + 1):
                k = self.k_sol(self.x_min + self.dx * i, self.y_min)
                b = self.b_sol(self.x_min + self.dx * i, self.y_min)
                x, y = self.y_x(self.y_min + self.dy * j, k, b), self.y_min + self.dy * j
                x, y = self.xy(self.x + x, self.y + y)
                self.outpostes[i][j] = Outpost(int(x), int(y), self.screen, i, j)

    def init_territorie(self):
        '''
        инициализируется массив аванпостов
        '''
        for i in range(self.n):
            for j in range(self.n):
                self.territories[i][j] = self.create_obj(j, i)

    def create_obj(self, j, i):
        '''
        создаеться территория и считаються ее координаты в СО pygame
        :param j: x координата территории
        :param i: y координата территории
        :return: объект-территория
        '''
        k = self.k_sol(self.x_min + self.dx * (i + 0.5), self.y_min)
        b = self.b_sol(self.x_min + self.dx * (i + 0.5), self.y_min)
        x, y = self.y_x(self.y_min + self.dy * (j + 0.5), k, b), self.y_min + self.dy * (j + 0.5)
        x, y = self.xy(self.x + x, self.y + y)
        return Territory(x, y, self.screen, i, j)

    def draw(self, player, step_player_outpost, player1):
        '''
        рисуется поле, аванпосты, территории и обрабатываеться ход
        :param player: игрок делающий ход
        :param step_player_outpost: поставил ли игрок аванпост
        :param player1: противник
        :return: построен аванпост или нет
        '''
        game_field.game_field()
        game_field.draw_outpostes()
        # game_field.grid()
        game_field.draw_territories()
        return game_field.interaction_with_fied(player, step_player_outpost, player1)

    def draw_game_over(self):
        '''
        рисуется поле, аванпосты, территории и обрабатывается ход после завершения игры
        '''
        game_field.game_field()
        game_field.draw_outpostes()
        # game_field.grid()
        game_field.draw_territories()
        game_field.interaction_with_fied_game_over()

    def grid(self):
        '''
        рабочая функция, рисуется сетка, по которой можно считать координаты
        '''
        # pg.draw.circle(self.screen, RED, (10, 10), 10000)
        for x in range(10, weight + 1, 10):
            line(self.screen, WHITE, [int(x), int(0)], [int(x), int(height)], 1)
        for y in range(10, height + 1, 10):
            line(self.screen, WHITE, [int(0), int(y)], [int(weight), int(y)], 1)

    def game_field(self):
        '''
        рисует поле по заданным параметрам
        '''
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
        '''
        решает линейное уравнение y = kx + b по y
        :return: x
        '''
        return (y - b) / (k + 10**(-3))

    def x_y(self, x, k, b):
        '''
        решает линейное уравнение y = kx + b по x
        :return: y
        '''
        return k * x + b

    def xy(self, x, y):
        '''
        конвертирует x, y из СО pygame в нормальное СО
        :return: x, y
        '''
        return (x, height - y)

    def xy_inv(self, x, y):
        '''
        конвертирует x, y из нормальное СО в СО pygame
        :return: x, y
        '''
        return (x, abs(y - height))

    def k_sol(self, x, y):
        '''
        решает линейное уравнение y = kx + b по координатам 2ух точек, одна из которых точка Перспектива
        :return: k
        '''
        return (self.y0 - y) / (self.x0 - x + 10**(-3))

    def b_sol(self, x, y):
        '''
        решает линейное уравнение y = kx + b по координатам 2ух точек, одна из которых точка Перспектива
        :return: b
        '''
        return (self.x0 * y - self.y0 * x) / (self.x0 - x + 10**(-3))

    def interaction_with_fied(self, player, step_player_outpost, player1):
        '''
        взаимодействие с полем: вывод информации, постройка аванпота(битва за территорию)
        :param player: игрок
        :param step_player_outpost: постороен ли уже аванпост в этот ход
        :param player1: противник
        :return: построен аванпост или нет
        '''
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
            text0 = f0.render('x = {}, y = {}, pos = {}'.format(self.territories[x3][y3].x_list, self.outpostes[x3][y3].y_list, 'Territories'), 5, WHITE)
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
            text0 = f0.render('x = {}, y = {}, pos = {}'.format(self.outpostes[x3][y3].x_list, self.outpostes[x3][y3].y_list, 'Outpost'), 5, WHITE)
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
                    if (abs(x3 - x) == 1 or abs(x3 - x) == 0) and (abs(y3 - y) == 1 or abs(y3 - y) == 0):
                        print(x, y)
                        out = self.outpostes[x3][y3].check_stranger(player, player1, self.outpostes[x][y], y3, y)
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

    def interaction_with_fied_game_over(self):
        '''
        взаимодействие с полем после завершения игры: вывод информации и тд
        '''
        x0, y0 = self.xy(Mouse.x, Mouse.y)
        x0, y0 = x0 - self.x, y0 - self.y
        k, b = self.k_sol(x0, y0), self.b_sol(x0, y0)
        x, y = self.y_x(self.y_min, k, b), y0
        x3, y3 = int((x / self.dx)//1), int((y / self.dy)//1)
        x33, y33 = int((x / self.dx)//0.25%4), int((y / self.dy)//0.25%4)
        pygame.draw.circle(self.screen, WHITE, (Mouse.x, Mouse.y), 5)

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
            # f0 = pygame.font.Font(None, 36)
            # text0 = f0.render('x = {}, y = {}, pos = {}'.format(self.territories[x3][y3].x_list, self.outpostes[x3][y3].y_list, 'Territories'), 5, WHITE)
            # self.screen.blit(text0, (300, 5))

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
            # f0 = pygame.font.Font(None, 36)
            # text0 = f0.render('x = {}, y = {}, pos = {}'.format(self.outpostes[x3][y3].x_list, self.outpostes[x3][y3].y_list, 'Outpost'), 5, WHITE)
            # self.screen.blit(text0, (300, 5))

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

    def draw_outpostes(self):
        '''
        рисование аванпостов
        '''
        for x, y in gamer1.myoutpostes:
            self.outpostes[x][y].draw()
        for x, y in gamer1.myoutpostes_build:
            self.outpostes[x][y].draw()
        for x, y in gamer2.myoutpostes:
            self.outpostes[x][y].draw()
        for x, y in gamer2.myoutpostes_build:
            self.outpostes[x][y].draw()

    def draw_territories(self):
        '''
        рисование территорий
        '''
        for j in range(self.n):
            for i in range(self.n):
                self.territories[i][j].draw()

    def check_cycle(self, player):
        '''
        ищет новые циклы среди аванпостов игрока
        :param player: игрок
        :return: [] - если нет циклов или cycle - если нашла цикл
        '''
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
        '''
        изменяет территории и аванпосты находящиеся в цикле
        :param cycle: новый цикл
        :param player: игрок
        '''
        for i in range(self.n):
            for j in range(self.n):
                if self.territories[i][j].player == '':
                    if prove(cycle, i, j):
                        # print(cycle)
                        self.territories[i][j].player = player.name
                        self.change_near_out(i, j)
        self.change_cycle_out(player, cycle)

    def change_near_out(self, x, y):
        '''
        захватывает все аванпосты вокруг захваченной территории
        :param x: координаты территории
        :param y:
        '''
        self.outpostes[x][y].player = 'occupied'
        self.outpostes[x + 1][y].player = 'occupied'
        self.outpostes[x + 1][y + 1].player = 'occupied'
        self.outpostes[x][y + 1].player = 'occupied'

    def change_cycle_out(self, player, cycle):
        '''
        изменяет названия всех аванпостов в цикле
        :param player: игрок
        :param cycle: цикл
        '''
        for x, y in cycle:
            self.outpostes[x][y].player = player.name

    def built_outposts(self, player):
        '''
        строит все аванпосты игрока за один ход
        :param player: игрок
        '''
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
        '''
        дает игроку ресурсы с захваченных территорий
        :param player: игрок
        '''
        for x in range(self.n):
            for y in range(self.n):
                if self.territories[x][y].player == player.name and self.territories[x][y].give_res:
                    print('33333333333333333333333333333')
                    resources_i = {}
                    for elem in player.resources:
                        resources_i[elem] = player.resources[elem] + self.territories[x][y].resources[elem]
                    player.resources = resources_i
                    self.give_res = False
