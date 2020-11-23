# загружаем изображения
im_outpost = pg.image.load('')  # загрузка изображения аванпоста
im_forest = pg.image.load('')  # загрузка изображения леса
im_gold_vein = pg.image.load('')  # загрузка изображения золотой жилы
im_mercenaries = pg.image.load('')  # загрузка изображения лагеря наемников
im_enemies = pg.image.load('')  # загрузка изображения "вражин"
im_farm = pg.image.load('')  # загрузка изображения фермы
im_pie = pg.image.load('')  # загрузка изображения "пирожка на полке"


x_size = 40  # размер изображений клеток по х
y_size = 40  # размер изображений клеток по у


x_size_op = 20  # размер изображений авапоста по х
y_size_op = 20  # размер изображений аванпоста по у


# Класс аванпостов
class Outpost:
    def __Init__(self, x, y, player):
        """
        x, y - координаты аванпоста
        built - проверка, построен ли аванпост
        moves - сколько осталось ходов до постройки
        player - какому игроку пренадлежит авапост
        """
        self.x = x
        self.y = y
        self.moves = 3
        self.built = 0
        self.player = player
        self.dispute = 0
        self.image = im_outpost

    # Рисуем аванпост
    def draw(self):
        pg.screen.blit(self.image, ((self.x - x_size_op/2), (self.y + y_size_op/2)))

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


dict_cells = dict({'forest': '+building -gold', 'golden vein': '+gold', 'mercenaries': '+army -gold',
                   'enemies': '-army +building +money', 'farm': '+food - gold', 'pie': '+food -building'})


class Forest:
    def __Init__(self, x, y):
        self.x = x
        self.y = y
        self.image = im_forest

    def draw(self):
        pg.screen.blit(self.image, ((self.x - x_size/2), (self.y + y_size/2)))


class GoldVein:
    def __Init__(self, x, y):
        self.x = x
        self.y = y
        self.image = im_gold_vein

    def draw(self):
        pg.screen.blit(self.image, ((self.x - x_size/2), (self.y + y_size/2)))


class Mercenaries:
    def __Init__(self, x, y):
        self.x = x
        self.y = y
        self.image = im_mercenaries

    def draw(self):
        pg.screen.blit(self.image, ((self.x - x_size/2), (self.y + y_size/2)))


class Enemies:
    def __Init__(self, x, y):
        self.x = x
        self.y = y
        self.image = im_enemies

    def draw(self):
        pg.screen.blit(self.image, ((self.x - x_size/2), (self.y + y_size/2)))


class Farm:
    def __Init__(self, x, y):
        self.x = x
        self.y = y
        self.image = im_farm

    def draw(self):
        pg.screen.blit(self.image, ((self.x - x_size/2), (self.y + y_size/2)))


class Pie:
    def __Init__(self, x, y):
        self.x = x
        self.y = y
        self.image = im_pie

    def draw(self):
        pg.screen.blit(self.image, ((self.x - x_size/2), (self.y + y_size/2)))
