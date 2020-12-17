from objects import *
from game0 import *
from player import *


'''Суть алгоритма: в зависимости от стратегии компьютера клеткам присваивается разная ценность;
Для постановки выбирается аванпост с наибольшей ценностью соседних клеткок'''



class Alforithm():
    def __init__(self, game_field, board, computer):
        self.game_field = game_field
        self.board = board
        self.computer = computer

    def updade(self, game_field, board, computer):
        self.game_field = game_field
        self.board = board
        self.computer = computer

    # Мирный режим - режим самого начала игры. Основная задача - накопить денег и еды (чтобы позже была армия)
    def peace(self, game_field, board, computer):
        m = 0   # Счетчики для нахождения наибольшего элемента множества
        m_i = 0
        m_j = 0
        for i in range(1, 11):
            for j in range(7, 11):   # Ограничение на область, считающейся "домашней"
                if self.game_field.territories[i][j].player == '':   # Считаем ценность только незанятых клеток
                    k = self.v(i, j, 'peace')
                else:
                    k = 0
                if self.game_field.outpostes[i-1][j].player == 'computer' or self.game_field.outpostes[i+1][j].player == 'computer' or\
                        self.game_field.outpostes[i][j-1].player == 'computer' or self.game_field.outpostes[i][j+1].player == 'computer':
                    sosedi = 100   # Увеличиваем ценность пересечения, если одно из соседних пренадлежит компьютеру
                else:
                    sosedi = 0   # Нужно, чтобы компьютер захватывал территории
                counter = self.v(i-1, j-1, 'peace') + self.v(i, j-1, 'peace') + self.v(i-1, j, 'peace') + k + sosedi   # Возможно, нужно учесть еще что-нибудь
                if m < counter and self.game_field.outpost[i][j].player == '':   # Проверка на максимум и на то, что аванпост ничей
                    m = counter
                    m_i = i
                    m_j = j
        if m != 0:
            self.game_field.outpost[m_i][m_j].player = 'computer'   # Присвиваем аванпост
        if self.computer.resources['gold'] > 2000:   # Покупаем еду, если есть излишки золота
            self.board.exchange_gold_food(computer)


    # Режим говнаря - режим тактической бомбардировки территории игрока. Активируется, если игрок сам начинает говнить
    def govnilovka(self):
        m = 1000   # Счетчики для нахождения наименьшего элемента
        m_i = 0
        m_j = 0
        if computer.resources['gold'] > 500:   # Проверка, достаточно ли ресурсов, чтобы можно было говнить без ущерба для себя
            for i in range(1, 11):
                for j in range(1, 3):   # Ограничение на домашнюю территорию игрока
                    if game_field.territories[i][j].player == '':   # Считаем ценность только незанятых клеток
                        k = v(i, j, govnilovka)
                    else:
                        k = 0
                    if game_field.outpostes[i-1][j].player == 'computer' or game_field.outpostes[i+1][j].player == 'computer'\
                            or game_field.outpostes[i][j-1].player == 'computer' or game_field.outpostes[i][j+1].player == 'computer':
                        sosedi = 100   # Учитываем соседей, но на этот раз в минус
                    else:
                        sosedi = 0
                    counter = v(i-1, j-1, govnilovka) + v(i, j-1, govnilovka) + v(i-1, j, govnilovka) + k + sosedi
                    if m > counter and game_field.outpost[i][j].player == '':   # Проверка на минимум и на то, что аванпост ничей
                        m = counter
                        m_i = i
                        m_j = j
            game_field.outpost[m_i][m_j].player = 'computer'
        else:
            war()   # Если ресурсов мало, добываем еще


    # Режим войны, активируется, если ресурсов на домашней территории осталось мало
    def war(self):
        m = 0
        for i in range(1, 11):   # проверяем, достаточно ли ресурсов на домашней территории
            for j in range(7, 11):   # Ограничиваем домашнюю территорию
                if game_field.territories[i][j].player == '':   # Учитываем только незанятые клетки
                    v = game_field.territories[i][j].count[peace]
                else:
                    v = 0
                counter = v(i-1, j-1, peace) + v(i, j-1, peace) + v(i-1, j, peace) + v   # При подсчете смотрим только на ресурсы
                if m < counter and game_field.outpost[i][j].player == '':   # Проверка на максимум и незанятость
                    m = counter
        if m > 100:   # Граница, достаточной ценности клеток
            peace()
        else:
            sosedi = 0
            m = 0   # Счетчики для нахождения наибольшего элемента множества
            m_i = 0
            m_j = 0
            for i in range(1, 11):
                for j in range(3, 7):   # Граница спорной территории
                    if game_field.territories[i][j].player == None:   # Учитываем только незанятые клетки
                        v = game_field.territories[i][j].count[peace]
                    else:
                        v = 0
                    if game_field.outpostes[i - 1][j].player == 'computer' or game_field.outpostes[i + 1][j].player == 'computer'\
                            or game_field.outpostes[i][j - 1].player == 'computer' or game_field.outpostes[i][j + 1].player == 'computer':
                        sosedi = 100   # Увеличиваем ценность пересечения, если одно из соседних пренадлежит компьютеру
                    counter = v(i-1, j-1, peace) + v(i, j-1, peace) + v(i-1, j, peace) + k + sosedi
                    if m < counter and game_field.outpost[i][j].player == None:   # Проверка на максимум и незанятость
                        m = counter
                        m_i = i
                        m_j = j
            outpost[m_i][m_j].player = 'computer'   # Присваиваем аванпост
            if computer.resources['building'] > 100:   # Ускоряем строительство
                computer.resources['building'] -= 100
                outpost[m_i][m_j].build_outposte()
            if computer.resources['building'] > 500:   # Если достаточно ресурсов, ускоряем еще раз
                computer.resources['building'] -= 100
                outpost[m_i][m_j].build_outposte()
            if computer.resources['gold'] > 500:   # Покупаем армию
                board.exchange_gold_army()
                board.exchange_gold_building()

    def v(self, x, y, type_alg):
        self.game_field.territories[x][y].count[type_alg]