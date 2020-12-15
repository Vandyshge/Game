from objects import *
from game import *


'''Суть алгоритма: в зависимости от стратегии компьютера клеткам присваивается разная ценность;
Для постановки выбирается аванпост с наибольшей ценностью соседних клеткок'''


# Мирный режим - режим самого начала игры. Основная задача - накопить денег и еды (чтобы позже была армия)
def peace():
    m = 0   # Счетчики для нахождения наибольшего элемента множества
    m_i = 0
    m_j = 0
    for i in range(0, 10):
        for j in range(7, 10):   # Ограничение на область, считающейся "домашней"
            if game_field.territories[i][j].player == None:   # Считаем ценность только незанятых клеток
                k[i][j] = game_field.territories[i][j].count[peace]
            else:
                k[i][j] = 0
            if game_field.outpostes[i-1][j].player == 'computer' or game_field.outpostes[i+1][j].player == 'computer' or\
                    game_field.outpostes[i][j-1].player == 'computer' or game_field.outpostes[i][j+1].player == 'computer':
                sosedi = 100   # Увеличиваем ценность пересечения, если одно из соседних пренадлежит компьютеру
            else:
                sosedi = 0   # Нужно, чтобы компьютер захватывал территории
            counter[i][j] = k[i-1][j-1] + k[i][j-1] + k[i-1][j] + k[i][j] + sosedi   # Возможно, нужно учесть еще что-нибудь
            if m < counter[i][j] and game_field.outpost[i][j].player == None:   # Проверка на максимум и на то, что аванпост ничей
                m = counter[i][j]
                m_i = i
                m_j = j
    game_field.outpost[m_i][m_j].player = 'computer'   # Присвиваем аванпост
    if computer.resources['gold'] > 2000:   # Покупаем еду, если есть излишки золота
        board.exchange_gold_food()


# Режим говнаря - режим тактической бомбардировки территории игрока. Активируется, если игрок сам начинает говнить
def govnilovka():
    m = 1000   # Счетчики для нахождения наименьшего элемента
    m_i = 0
    m_j = 0
    if computer.resources['gold'] > 500:   # Проверка, достаточно ли ресурсов, чтобы можно было говнить без ущерба для себя
        for i in range(0, 10):
            for j in range(0, 3):   # Ограничение на домашнюю территорию игрока
                if game_field.territories[i][j].player == None:   # Считаем ценность только незанятых клеток
                    k[i][j] = game_field.territories[i][j].count[govnilovka]
                else:
                    k[i][j] = 0
                if game_field.outpostes[i-1][j].player == 'computer' or game_field.outpostes[i+1][j].player == 'computer'\
                        or game_field.outpostes[i][j-1].player == 'computer' or game_field.outpostes[i][j+1].player == 'computer':
                    sosedi = 100   # Учитываем соседей, но на этот раз в минус
                else:
                    sosedi = 0
                counter[i][j] = k[i-1][j-1] + k[i][j-1] + k[i-1][j] + k[i][j] + sosedi
                if m > counter[i][j] and game_field.outpost[i][j].player == None:   # Проверка на минимум и на то, что аванпост ничей
                    m = counter[i][j]
                    m_i = i
                    m_j = j
        game_field.outpost[m_i][m_j].player = 'computer'
    else:
        war()   # Если ресурсов мало, добываем еще


# Режим войны, активируется, если ресурсов на домашней территории осталось мало
def war():
    m = 0
    for i in range(0, 10):   # проверяем, достаточно ли ресурсов на домашней территории
        for j in range(7, 10):   # Ограничиваем домашнюю территорию
            if game_field.territories[i][j].player == None:   # Учитываем только незанятые клетки
                k[i][j] = game_field.territories[i][j].count[peace]
            else:
                k[i][j] = 0
            counter[i][j] = k[i-1][j-1] + k[i][j-1] + k[i-1][j] + k[i][j]   # При подсчете смотрим только на ресурсы
            if m < counter[i][j] and game_field.outpost[i][j].player == None:   # Проверка на максимум и незанятость
                m = counter[i][j]
    if m > 100:   # Граница, достаточной ценности клеток
        peace()
    else:
        sosedi = 0
        m = 0   # Счетчики для нахождения наибольшего элемента множества
        m_i = 0
        m_j = 0
        for i in range(0, 10):
            for j in range(3, 7):   # Граница спорной территории
                if game_field.territories[i][j].player == None:   # Учитываем только незанятые клетки
                    k[i][j] = game_field.territories[i][j].count[peace]
                else:
                    k[i][j] = 0
                if game_field.outpostes[i - 1][j].player == 'computer' or game_field.outpostes[i + 1][j].player == 'computer'\
                        or game_field.outpostes[i][j - 1].player == 'computer' or game_field.outpostes[i][j + 1].player == 'computer':
                    sosedi = 100   # Увеличиваем ценность пересечения, если одно из соседних пренадлежит компьютеру
                counter[i][j] = k[i-1][j-1] + k[i][j-1] + k[i-1][j] + k[i][j] + sosedi
                if m < counter[i][j] and game_field.outpost[i][j].player == None:   # Проверка на максимум и незанятость
                    m = counter[i][j]
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
