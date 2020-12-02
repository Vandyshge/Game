import pygame as pg
from colors import *


# загружаем изображения
im_outpost = 1  # загрузка изображения аванпоста
im_forest = 1# загрузка изображения леса
im_gold_vein = 1  # загрузка изображения золотой жилы
im_mercenaries = 1 # загрузка изображения лагеря наемников
im_enemies = 1 # загрузка изображения "вражин"
im_farm = 1 # загрузка изображения фермы
im_pie = 1# загрузка изображения "пирожка на полке"


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
        self.dispute = 0
        self.image = im_outpost
        self.screen = screen


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

    # Проверяем, попал ли аванпост в спорную территорию
    def check_stranger(self, strange_x, strange_y, strange_player, strange_built):
        """
        strange_x, y - координаты другого аванпоста
        stranger_player - владелец другого аванпоста
        strange_built - check на постройку другого аванпоста
        """
        if (strange_player != self.player) and (self.built == 0) and (strange_built == 0):
            if ((self.x - strange_x)**2 + (self.y - strange_y)**2 < 5):
                self.dispute = 1
            else:
                self.dispute = 0


dict_cells = {'forest': '+building -gold', 'golden vein': '+gold', 'mercenaries': '+army -gold',
                   'enemies': '-army +building +money', 'farm': '+food - gold', 'pie': '+food -building'}


class Forest:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.player = ''
        self.image = im_forest

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

    def draw(self):
        pg.draw.rect(self.screen, YELLOW, (self.x - 5, self.y - 5, 10, 10))
        # pg.screen.blit(self.image, ((self.x - x_size/2), (self.y + y_size/2)))
