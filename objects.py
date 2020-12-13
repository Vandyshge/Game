import pygame as pg
from colors import *
from player import *
from random import randint

# загружаем изображения
im_outpost = 1  # загрузка изображения аванпоста
im_forest = 1   # загрузка изображения леса
im_gold_vein = 1  # загрузка изображения золотой жилы
im_mercenaries = 1   # загрузка изображения лагеря наемников
im_enemies = 1   # загрузка изображения "вражин"
im_farm = 1   # загрузка изображения фермы
im_pie = 1   # загрузка изображения "пирожка на полке"
im_wast = 1
territories_image = {'forest': im_forest, 'golden vein': im_gold_vein,
                     'mercenaries': im_mercenaries, 'enemies': im_enemies,
                      'farm': im_farm, 'pie': im_pie, 'wasteland': im_wast}


x_size = 100  # размер изображений клеток по х
y_size = 100  # размер изображений клеток по у


x_size_op = 20  # размер изображений авапоста по х
y_size_op = 20  # размер изображений аванпоста по у


# Класс аванпостов
class Outpost:
    def __init__(self, x, y, screen, moves=3, cost=100):
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
        self.image = im_outpost
        self.screen = screen
        self.exist = True   # надо будет дописать это в основную программу
        self.built = 0

    # Рисуем аванпост
    def draw(self):
        if self.moves != 0 and self.player == 'computer':
            pg.draw.circle(self.screen, BLUE1, (self.x, self.y), 5)
        elif self.moves != 0:
            pg.draw.circle(self.screen, BLUE, (self.x, self.y), 5)
        elif self.player == 'computer':
            pg.draw.circle(self.screen, MAGENTA, (self.x, self.y), 5)
        else:
            pg.draw.circle(self.screen, GREEN, (self.x, self.y), 5)
        # pg.screen.blit(self.image, ((self.x - x_size_op/2), (self.y + y_size_op/2)))

    def draw_information(self, x, y, p):
        if self.player == '':
            pg.draw.rect(self.screen, RED, (self.x, self.y - 45, 60, 45))

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
            pg.draw.rect(self.screen, RED, (self.x, self.y - 45, 60, 45))

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
                print('1234')
                return True
            return False
        elif self.exist:
            pg.draw.rect(self.screen, RED, (self.x, self.y - 30, 60, 30))

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
            if player1.name == 'computer':
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


dict_cells = {'forest': '+building -gold', 'golden vein': '+gold', 'mercenaries': '+army -gold',
                   'enemies': '-army +building +money', 'farm': '+food - gold', 'pie': '+food -building'}


territories_resources = {'forest': {'gold': -100, 'building': 500, 'food': 0, 'army': 0},
                         'golden vein': {'gold': 1000, 'building': 0, 'food': 0, 'army': 0},
                         'mercenaries': {'gold': -100, 'building': 0, 'food': 0, 'army': 500},
                         'enemies': {'gold': 500, 'building': 500, 'food': 0, 'army': -300},
                         'farm': {'gold': -100, 'building': 0, 'food': 200, 'army': 0},
                         'pie': {'gold': 0, 'building': -300, 'food': 300, 'army': 0},
                         'farm': {'gold': -100, 'building': 0, 'food': 100, 'army': 0},
                         'pie': {'gold': 0, 'building': -300, 'food': 100, 'army': 0},
                         'wasteland': {'gold': 0, 'building': 0, 'food': 0, 'army': 0}}

cells = ['forest', 'golden vein', 'mercenaries', 'enemies', 'farm', 'pie']
name = cells[randint(0, len(cells) - 1)]


class Territory():
    def __init__(self, x, y, screen, get_resources):
        self.x = x
        self.y = y
        self.screen = screen
        self.player = ''
        self.get_resources = get_resources   # Хз, правильно ли поняла тебя

        cells = ['forest', 'golden vein', 'mercenaries', 'enemies', 'farm', 'pie', 'wasteland']
        self.name = cells[randint(0, len(cells) - 1)]
        self.image = territories_image[self.name]
        self.resources = territories_resources[self.name]
        self.give_res = True

    def draw(self):
        pass
        # pg.draw.rect(self.screen, YELLOW, (self.x - 5, self.y - 5, 10, 10))
        # pg.screen.blit(self.image, ((self.x - x_size/2), (self.y + y_size/2)))

    def draw_information(self):
        pg.draw.rect(self.screen, RED, (self.x, self.y - 55, 50, 55))

        f0 = pg.font.Font(None, 16)
        text0 = f0.render(f'{self.name}', 5, WHITE)
        self.screen.blit(text0, (self.x + 5, self.y - 50))

        if self.player != '':
            f0 = pg.font.Font(None, 16)
            text0 = f0.render(f'{self.player}', 5, WHITE)
            self.screen.blit(text0, (self.x + 5, self.y - 40))
        else:
            f0 = pg.font.Font(None, 16)
            text0 = f0.render('None', 5, WHITE)
            self.screen.blit(text0, (self.x + 5, self.y - 40))

        i = 0
        for elem in self.resources:
            if self.resources[elem] != 0:
                f0 = pg.font.Font(None, 16)
                text0 = f0.render(f'{elem}:{self.resources[elem]}', 5, WHITE)
                self.screen.blit(text0, (self.x + 5, self.y - 30 - i))
                i -= 10
