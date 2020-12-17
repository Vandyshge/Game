import pygame as pg
from colors import *
from player import *
from random import randint


# Класс аванпостов
class Outpost:
    def __init__(self, x, y, screen, x_list, y_list, y_scale=0, side=0, moves=3, cost=100):
        """
        x, y - координаты аванпоста
        built - проверка, построен ли аванпост
        moves - сколько осталось ходов до постройки
        player - какому игроку пренадлежит авапост
        """
        self.x = x
        self.y = y
        self.moves = moves
        self.cost = cost
        self.player = ''
        self.dispute = 0   # ХЗ, зачем, но может понадобиться
        # self.image = im_outpost
        self.screen = screen
        self.exist = True   # надо будет дописать это в основную программу
        self.built = 0
        self.x_list = x_list
        self.y_list = y_list
        self.side = side
        self.y_scale = y_scale

        im_outpost1 = pg.image.load('image/dom1.png')   # загрузка изображения аванпоста
        self.image1 = pg.transform.scale(im_outpost1, (int(50), int(50)))

        im_outpost2 = pg.image.load('image/dom2.png')   # загрузка изображения аванпоста
        self.image2 = pg.transform.scale(im_outpost2, (int(50), int(50)))

    # Рисуем аванпост
    def draw(self):
        if self.moves != 0 and self.side == 1:
            pg.draw.circle(self.screen, BLUE1, (self.x, self.y), 5)
        elif self.moves != 0:
            pg.draw.circle(self.screen, BLUE, (self.x, self.y), 5)
        elif self.side == 1:
            self.screen.blit(self.image2, (self.x - 9, self.y - 24))
        else:
            self.screen.blit(self.image1, (self.x - 9, self.y - 24))
        # pg.screen.blit(self.image, ((self.x - x_size_op/2), (self.y + y_size_op/2)))

    def draw_information(self, x, y, p):
        if self.player == '' and self.exist:
            pg.draw.rect(self.screen, СYAN_BOARD, (self.x, self.y - 45, 60, 45))

            f0 = pg.font.Font(None, 16)
            text0 = f0.render('None', 5, WHITE)
            self.screen.blit(text0, (self.x + 5, self.y - 40))

            f0 = pg.font.Font(None, 16)
            text0 = f0.render('cost: {}'.format(self.cost), 5, WHITE)
            self.screen.blit(text0, (self.x, self.y - 30))

            f0 = pg.font.Font(None, 16)
            text0 = f0.render('moves: {}'.format(self.moves), 5, WHITE)
            self.screen.blit(text0, (self.x, self.y - 20))
            return False
        elif self.moves != 0 and self.exist:
            pg.draw.rect(self.screen, СYAN_BOARD, (self.x, self.y - 45, 60, 45))

            f0 = pg.font.Font(None, 16)
            text0 = f0.render(f'{self.player}', 5, WHITE)
            self.screen.blit(text0, (self.x + 5, self.y - 40))

            f0 = pg.font.Font(None, 16)
            text0 = f0.render('moves: {}'.format(self.moves), 5, WHITE)
            self.screen.blit(text0, (self.x, self.y - 30))

            f0 = pg.font.Font(None, 16)
            text0 = f0.render('ускорить'.format(self.moves), 5, WHITE)
            self.screen.blit(text0, (self.x, self.y - 20))
            if (x > self.x) and (x < self.x + 50) and (y > self.y - 20) and (y < self.y - 10) and p:
                # print('1234')
                return True
            return False
        elif self.exist:
            pg.draw.rect(self.screen, СYAN_BOARD, (self.x, self.y - 30, 60, 30))

            f0 = pg.font.Font(None, 16)
            text0 = f0.render(f'{self.player}', 5, WHITE)
            self.screen.blit(text0, (self.x + 5, self.y - 25))
            return False

    # Уменьшаем количество ходов, оставшихся до постройки
    def build_outposte(self):
        if self.moves > 0:
            self.moves -= 1
            if self.moves == 0:
                return True
            else:
                return False

    # Проверяем, построен ли аванпост
    def check_build(self):
        if self.moves == 0:
            self.built = 1
        else:
            self.built = 0

    # Проверяем, попал ли аванпост в спорную территорию и проводим драчку
    def check_stranger(self, player1, player2, outpost, y0, y):
        print(player1.resources['army'])
        print(player2.resources['army'])
        if self.player != outpost.player and self.moves != 0 and outpost.moves != 0 and \
                (player1.resources['army'] != 0 or player2.resources['army'] != 0):
            self.dispute = 1
            outpost.dispute = 1
            dice = randint(0, 100)
            '''
            Идет сравнение случайного числа с армия1*кпд1/(армия1*кпд1+армия2*кпд2)
            Кпд вычисляется по формуле: -(коорд.п отн своей стороны)**2/150 + 1
            '''
            if self.side == 1:
                d1 = 11 - y0
                d2 = y
                if dice > int(100*player1.resources['army']*((150-d1**2)/150)
                        /(player1.resources['army']*((150-d1**2)/150) + player2.resources['army']*((150-d2**2)/150))):
                    player2.resources['army'] = int(0.9 * player2.resources['army'])
                    player1.resources['army'] = int(0.7 * player1.resources['army'])
                    return False
                else:
                    player1.resources['army'] = int(0.9 * player1.resources['army'])
                    player2.resources['army'] = int(0.7 * player2.resources['army'])
                    return True
            else:
                d1 = y0
                d2 = 11 - y
                if dice > int(100*player1.resources['army']*((150-d1**2)/150)
                        /(player1.resources['army']*((150-d1**2)/150) + player2.resources['army']*((150-d2**2)/150))):
                    player2.resources['army'] = int(0.9 * player2.resources['army'])
                    player1.resources['army'] = int(0.7 * player1.resources['army'])
                    return False
                else:
                    player1.resources['army'] = int(0.9 * player1.resources['army'])
                    player2.resources['army'] = int(0.7 * player2.resources['army'])
                    return True
        return None

# загружаем изображения
im_forest = pg.image.load('image/derevo.png')    # загрузка изображения леса
im_forest = pg.transform.scale(im_forest, (int(40), int(40)))
im_gold_vein = pg.image.load('image/shakhta.png')   # загрузка изображения золотой жилы
im_gold_vein = pg.transform.scale(im_gold_vein, (int(100), int(100)))
im_mercenaries = pg.image.load('image/koster.png')    # загрузка изображения лагеря наемников
im_mercenaries = pg.transform.scale(im_mercenaries, (int(65), int(65)))
im_enemies = pg.image.load('image/dom (1).png')    # загрузка изображения "вражин"
im_enemies = pg.transform.scale(im_enemies, (int(75), int(75)))
im_farm = pg.image.load('image/ferma.png')    # загрузка изображения фермы
im_farm = pg.transform.scale(im_farm, (int(85), int(85)))
im_pie = pg.image.load('image/pechenka.png')   # загрузка изображения "пирожка на полке"
im_pie = pg.transform.scale(im_pie, (int(100), int(100)))
im_wast = pg.image.load('image/pusto.png') 
im_wast = pg.transform.scale(im_wast, (int(100), int(100)))

territories_image = {'forest': im_forest, 'golden_vein': im_gold_vein,
                     'mercenaries': im_mercenaries, 'enemies': im_enemies,
                      'farm': im_farm, 'pie': im_pie, 'wasteland': im_wast}


x_size = 100  # размер изображений клеток по х
y_size = 100  # размер изображений клеток по у


x_size_op = 20  # размер изображений авапоста по х
y_size_op = 20  # размер изображений аванпоста по у

dict_cells = {'forest': '+building -gold', 'golden vein': '+gold', 'mercenaries': '+army -gold',
                   'enemies': '-army +building +money', 'farm': '+food - gold', 'pie': '+food -building'}


territories_resources = {'forest': {'gold': -200, 'building': 500, 'food': 0, 'army': 0},
                         'golden_vein': {'gold': 1000, 'building': 0, 'food': 0, 'army': 0},
                         'mercenaries': {'gold': -200, 'building': 0, 'food': 0, 'army': 500},
                         'enemies': {'gold': 500, 'building': 500, 'food': 0, 'army': -300},
                         'pie': {'gold': 0, 'building': -200, 'food': 100, 'army': 0},
                         'farm': {'gold': -200, 'building': 0, 'food': 100, 'army': 0},
                         'wasteland': {'gold': 0, 'building': 0, 'food': 0, 'army': 0}}


territories_count = {'forest': {'peace': 10, 'war': 50, 'govnilovka': 0},
                     'golden_vein': {'peace': 100, 'war': 20, 'govnilovka': -30},
                     'mercenaries': {'peace': 10, 'war': 60, 'govnilovka': 0},
                     'enemies': {'peace': 60, 'war': 50, 'govnilovka': -10},
                     'farm': {'peace': 50, 'war': 10, 'govnilovka': 0},
                     'pie': {'peace': 50, 'war': 10, 'govnilovka': 0},
                     'wasteland': {'peace': 0, 'war': 0, 'govnilovka': 50}}

cells = ['forest', 'golden_vein', 'mercenaries', 'enemies', 'farm', 'pie']
name = cells[randint(0, len(cells) - 1)]


class Territory():
    def __init__(self, x, y, screen, x_list, y_list, y_scale=0):
        '''
        территории
        :param x: координаты в СО pygame
        :param y:
        :param screen: экран
        :param x_list: В СО массива территорий
        :param y_list:
        :param y_scale: -
        '''
        self.x = x
        self.y = y
        self.screen = screen
        self.player = '' # чья территория

        self.x_list = x_list
        self.y_list = y_list

        self.y_scale = 0
        # генерация рандомной территории при ините и ее параметров
        cells = ['forest', 'golden_vein', 'mercenaries', 'enemies', 'farm', 'pie', 'wasteland', 'wasteland', 'wasteland']
        self.name = cells[randint(0, len(cells) - 1)]
        self.image = territories_image[self.name]
        self.resources = territories_resources[self.name]
        self.give_res = True
        self.count = territories_count[self.name]
        # print(self.count['peace'])

    def draw(self):
        # pass
        # # pg.draw.rect(self.screen, YELLOW, (self.x - 5, self.y - 5, 10, 10))
        # # pg.screen.blit(self.image, ((self.x - x_size/2), (self.y + y_size/2))) 
        # image = self.image.set_colorkey(WHITE)
        # image = pg.transform.scale(self.image, (int(100), int(100)))
        # image_rect = image.get_rect(topleft=(int(x - 63 * k), int(y - 125 * k)))
        self.screen.blit(self.image, (self.x - 18, self.y - 10))

    def draw_information(self):
        pg.draw.rect(self.screen, СYAN_BOARD, (self.x, self.y - 55, 75, 55))

        f0 = pg.font.Font(None, 16)
        text0 = f0.render(f'{self.name}', 5, WHITE)
        self.screen.blit(text0, (self.x + 5, self.y - 50 - 2))

        if self.player != '':
            f0 = pg.font.Font(None, 16)
            text0 = f0.render(f'{self.player}', 5, WHITE)
            self.screen.blit(text0, (self.x + 5, self.y - 40 - 2))
        else:
            f0 = pg.font.Font(None, 16)
            text0 = f0.render('None', 5, WHITE)
            self.screen.blit(text0, (self.x + 5, self.y - 40 - 2))

        i = 0
        for elem in self.resources:
            if self.resources[elem] != 0:
                f0 = pg.font.Font(None, 16)
                text0 = f0.render(f'{elem}:{self.resources[elem]}', 5, WHITE)
                self.screen.blit(text0, (self.x + 5, self.y - 30 - i  - 2))
                i -= 10
