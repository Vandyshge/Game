from objects import *



def check_neighbors(outpostes, name, graph):
    # print('c_n', graph)
    x, y = graph[len(graph) - 1][0], graph[len(graph) - 1][1]
    x0, y0 = graph[len(graph) - 2][0], graph[len(graph) - 2][1]
    # print(f'x0, y0 = {x0}, {y0}, x, y = {x}, {y}')
    a = []
    if y + 1 <= 10:
        if (x, y + 1) not in graph[1:]:
            if outpostes[x][y + 1].player == name and (x0, y0) != (x, y + 1):
                # print('check_gra_0_2', x, y + 1)
                b = graph[:]
                # print('oh', b)
                b.append((x, y + 1))
                a.append(b)
                # print('oho', a)
    if y - 1 >= 0:
        if (x, y - 1) not in graph[1:]:
            if outpostes[x][y - 1].player == name and (x0, y0) != (x, y - 1):
                # print('check_gra_0_2', x, y - 1)
                b = graph[:]
                # print('oh', b)
                b.append((x, y - 1))
                a.append(b)
                # print('oho', a)
    if x + 1 <= 10:
        if (x + 1, y) not in graph[1:]:
            if outpostes[x + 1][y].player == name and (x0, y0) != (x + 1, y):
                    # print('check_gra_0_2', x + 1, y)
                    b = graph[:]
                    # print('oh', b)
                    b.append((x + 1, y))
                    a.append(b)
                    # print('oho', a)
    if x - 1 >= 0:
        if (x - 1, y) not in graph[1:]:
            if outpostes[x - 1][y].player == name and (x0, y0) != (x - 1, y):
                # print('check_gra_0_2', x - 1, y)
                b = graph[:]
                # print('oh', b)
                b.append((x - 1, y))
                a.append(b)
                # print('oho', a)
    # print('check_gra_0', a)
    return a

def check_neighbors_0(outpostes, name, x, y):
    a = []
    if y + 1 <= 10:
        # print('check_gra_0_1')
        if outpostes[x][y + 1].player == name:
            # print('check_gra_0_2')
            a.append([(x, y), (x, y + 1)])
    if y - 1 >= 0:
        # print('check_gra_0_1')
        if outpostes[x][y - 1].player == name:
            # print('check_gra_0_2')
            a.append([(x, y), (x, y - 1)])
    if x - 1 >= 0:
        # print('check_gra_0_1', outpostes[x - 1][y].player)
        if outpostes[x - 1][y].player == name:
            # print('check_gra_0_2')
            a.append([(x, y), (x - 1, y)])
    if x + 1 <= 10:
        if outpostes[x + 1][y].player == name:
            # print('check_gra_0_2')
            a.append([(x, y), (x + 1, y)])
    # print('check_gra_0', a)
    return a

def graph(x0, y0, outpostes, name):
    graph0 = []
    for elem_1 in check_neighbors_0(outpostes, name, x0, y0):
        graph0.append(elem_1)
    # print('graph_1', graph0)
    if len(graph0) == 0:
        return (False, 0)
    while True:
        graph1 = []
        for elem in graph0:
            for elem_1 in check_neighbors(outpostes, name, elem):
                graph1.append(elem_1)
            # print('for graph1', graph1)
            # print()
        # print('graph', graph1)
        if graph1 == []:
            # print('false')
            return (False, 0)
        graph0 = graph1[:]
        for elem in graph0:
            if elem[len(elem) - 1] == (x0, y0):
                return (True, elem)

def prove_up(cycle, x, y):
    if y > 10:
        return False
    elif (x, y + 1) in cycle and (x + 1, y + 1) in cycle and (x + 1) <= 10 and (y + 1) <= 10:
        # print(x, y)
        # print('-------------------------------------------')
        return True
    else:
        # print(x, y)
        return prove_up(cycle, x, y + 1)

def prove_down(cycle, x, y):
    if y < 0:
        return False
    elif (x, y) in cycle and (x + 1, y) in cycle and (x + 1) <= 10:
        # print(x, y)
        # print('-------------------------------------------')
        return True
    else:
        # print(x, y, '1')
        return prove_down(cycle, x, y - 1)

def prove_left(cycle, x, y):
    if x < 0:
        return False
    elif (x, y) in cycle and (x, y + 1) in cycle and (y + 1) <= 10:
        # print(x, y)
        # print('-------------------------------------------')
        return True
    else:
        # print(x, y)
        return prove_left(cycle, x - 1, y)

def prove_right(cycle, x, y):
    if x > 10:
        return False
    elif (x + 1, y) in cycle and (x + 1, y + 1) in cycle and (x + 1) <= 10 and (y + 1) <= 10:
        # print(x, y)
        # print('-------------------------------------------')
        return True
    else:
        # print(x, y)
        return prove_right(cycle, x + 1, y)

def prove(cycle, x, y):
    if prove_up(cycle, x, y) and prove_down(cycle, x, y) and prove_left(cycle, x, y) and prove_right(cycle, x, y):
        return True
    else:
        return False