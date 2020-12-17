from colors import *


class Gamer():
    def __init__(self, name, side=0):
        self.name = name
        self.resources = {'gold': 1000, 'building': 0, 'food': 0, 'army': 100}
        self.myoutpostes_build = []
        self.myoutpostes = []
        self.cycle = []
        self.side = side

class Computer():
    def __init__(self):
        self.name = 'computer'
        self.resources = {'gold': 1000, 'building': 0, 'food': 0, 'army': 100}
        self.myoutpostes = []
        self.myoutpostes_build = []
        self.cycle = []
