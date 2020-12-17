def output_top_player(type_game, win, n_win):
    '''
    обновляет результаты
    :param type_game: тип игры
    :param win: кто выиграл
    :param n_win: какой счет
    :return:  -
    '''
    if type_game == 'game0':
        out0 = open('text/top_player_game0.txt', 'r')
        game0 = []
        line = out0.readline().strip()
        line = out0.readline().strip()
        while line != '':
            line = line.split(' ')
            game0.append((int(line[3]), line[1]))
            line = out0.readline().strip()
        out0.close()

        out0_w = open('text/top_player_game00.txt', 'w')
        # добавляем результаты игрока
        game0.append((n_win, win))
        # сортируем результаты по счёту игроков
        game0 = sorted(game0, key=lambda x: -x[0])
        out0_w.write('Top players in the single player')
        # записываем рейтинг в тот же файл
        for i in range(len(game0)):
            out0_w.write(f'{i + 1}. {game0[i][1]} --- {game0[i][0]}\n')
        out0_w.close()

    elif type_game == 'game00':
        out00_r = open('text/top_player_game00.txt', 'r')
        game00 = []
        line = out00_r.readline().strip()
        line = out00_r.readline().strip()
        while line != '':
            line = line.split(' ')
            game00.append((int(line[3]), line[1]))
            line = out00_r.readline().strip()
        out00_r.close()

        out00_w = open('text/top_player_game00.txt', 'w')
        # добавляем результаты игрока
        game00.append((n_win, win))
        # сортируем результаты по счёту игроков
        game00 = sorted(game00, key=lambda x: -x[0])
        out00_w.write('Top players in the game together')
        # записываем рейтинг в тот же файл
        for i in range(len(game00)):
            out00_w.write(f'{i + 1}. {game00[i][1]} --- {game00[i][0]}\n')
        out00_w.close()

def input_top_player():
    '''
    выдает результаты в виде 2ух массивов
    :return:
    '''
    out0 = open('text/top_player_game0.txt', 'r')
    game0 = []
    line = out0.readline().strip()
    line = out0.readline().strip()
    while line != '':
        line = line.split(' ')
        game0.append((int(line[3]), line[1]))
        line = out0.readline().strip()
    out0.close()

    out00_r = open('text/top_player_game00.txt', 'r')
    game00 = []
    line = out00_r.readline().strip()
    line = out00_r.readline().strip()
    while line != '':
        line = line.split(' ')
        game00.append((int(line[3]), line[1]))
        line = out00_r.readline().strip()
    out00_r.close()

    return game0, game00