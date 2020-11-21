# Класс аванпостов
class Outpost():
    def __Init__(self, x, y, player):
        """
        x, y - координаты аванпоста
        built - проверка, построен ли аванпост
        moves - сколько осталось ходов до постройки
        player - какому игроку пренадлежит авапост
        dispute - проверка, начинается ли спор за территорию
        """
        self.x = x
        self.y = y
        self.moves = 3
        self.built = 0
        self.player = player
        self.dispute = 0

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

    # Проверяем, попал ли аванпост в спорную территорию !!!может стоит реализовать по-другому!!!
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
