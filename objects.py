import pygame as pg
from colors import *
from random import randint

# загружаем изображения
im_outpost = 1  # загрузка изображения аванпоста
im_forest = 1   # загрузка изображения леса
im_gold_vein = 1  # загрузка изображения золотой жилы
im_mercenaries = 1   # загрузка изображения лагеря наемников
im_enemies = 1   # загрузка изображения "вражин"
im_farm = 1   # загрузка изображения фермы
im_pie = 1   # загрузка изображения "пирожка на полке"


x_size = 40  # размер изображений клеток по х
y_size = 40  # размер изображений клеток по у


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

    # Рисуем аванпост
    def draw(self):
        pg.draw.circle(self.screen, GREEN, (self.x, self.y), 5)
        # pg.screen.blit(self.image, ((self.x - x_size_op/2), (self.y + y_size_op/2)))

    def draw_information(self):
        pg.draw.rect(self.screen, RED, (self.x, self.y - 50, 50, 50))

        f0 = pg.font.Font(None, 16)
        text0 = f0.render(f'{self.player}', 5, WHITE)
        self.screen.blit(text0, (self.x + 5, self.y - 45))

        f0 = pg.font.Font(None, 16)
        text0 = f0.render('cost: {}'.format(self.cost), 5, WHITE)
        self.screen.blit(text0, (self.x, self.y - 30))

        f0 = pg.font.Font(None, 16)
        text0 = f0.render('moves: {}'.format(self.moves), 5, WHITE)
        self.screen.blit(text0, (self.x, self.y - 10))

    # Уменьшаем количество ходов, оставшихся до постройки
    def minus_move(self):
        if self.moves > 0:
            self.moves -= 1

    # Проверяем, построен ли аванпост
    def check_built(self):
        if self.moves == 0:
            self.built = 1
        else:
            self.built = 0

    # Проверяем, попал ли аванпост в спорную территорию и проводим драчку
    def check_stranger(self, stranger):
        if ((self.x - stranger.x)**2 == 1 or (self.y - stranger.y)**2 == 1)\
                and self.player != stranger.player and self.built == 0 and stranger.built == 0:
            self.dispute = 1
            stranger.dispute = 1
            dice = randint(0, 100)
            if self.player == name:
                # формулу стоит изменить на что-нибудь поумнее
                if dice > int(100*gamer.army/(gamer.army + computer.army)):   # ХЗ, как нормально обратиться к армии
                    self.exist = False
                else:
                    stranger.exist = False
            else:
                if dice > int(100*computer.army/(gamer.army + computer.army)):
                    stranger.exist = False
                else:
                    self.exist = False


dict_cells = {'forest': '+building -gold', 'golden vein': '+gold', 'mercenaries': '+army -gold',
                   'enemies': '-army +building +money', 'farm': '+food - gold', 'pie': '+food -building'}


class Forest:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.player = ''
        self.image = im_forest
        self.resources = {'gold': -100, 'building': 500, 'food': 0, 'army': 0}   # потом поменять значения на нормальные

    def draw(self):
        pg.draw.rect(self.screen, YELLOW, (self.x - 5, self.y - 5, 10, 10))
        # pg.screen.blit(self.image, ((self.x - x_size/2), (self.y + y_size/2)))


class GoldVein:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.player = ''
        self.image = im_gold_vein
        self.resources = {'gold': 1000, 'building': 0, 'food': 0, 'army': 0}

    def draw(self):
        pg.draw.rect(self.screen, YELLOW, (self.x - 5, self.y - 5, 10, 10))
        # pg.screen.blit(self.image, ((self.x - x_size/2), (self.y + y_size/2)))


class Mercenaries:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.player = ''
        self.image = im_mercenaries
        self.resources = {'gold': -200, 'building': 0, 'food': 0, 'army': 500}

    def draw(self):
        pg.draw.rect(self.screen, YELLOW, (self.x - 5, self.y - 5, 10, 10))
        # pg.screen.blit(self.image, ((self.x - x_size/2), (self.y + y_size/2)))


class Enemies:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.player = ''
        self.image = im_enemies
        self.resources = {'gold': 500, 'building': 500, 'food': 0, 'army': -300}

    def draw(self):
        pg.draw.rect(self.screen, YELLOW, (self.x - 5, self.y - 5, 10, 10))
        # pg.screen.blit(self.image, ((self.x - x_size/2), (self.y + y_size/2)))


class Farm:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.player = ''
        self.image = im_farm
        self.resources = {'gold': -200, 'building': 0, 'food': 200, 'army': 0}

    def draw(self):
        pg.draw.rect(self.screen, YELLOW, (self.x - 5, self.y - 5, 10, 10))
        # pg.screen.blit(self.image, ((self.x - x_size/2), (self.y + y_size/2)))


class Pie:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.player = ''
        self.image = im_pie
        self.resources = {'gold': 0, 'building': -300, 'food': 300, 'army': 0}

    def draw(self):
        pg.draw.rect(self.screen, YELLOW, (self.x - 5, self.y - 5, 10, 10))
        # pg.screen.blit(self.image, ((self.x - x_size/2), (self.y + y_size/2)))
