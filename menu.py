import pygame as pg
from colors import *
from constants import *

class Menu():
    def __init__(self, screen):
        self.screen = screen
        global Mouse
        Mouse = Mouse()

    def menu(self):
        # t = FPS * 0.5
        # clock = pg.time.Clock()
        # pg.draw.circle(self.screen, WHITE, (10, 10), 10000)
        # pg.display.update()
        # while t > 0:
        #     clock.tick(FPS)
        #     t -= 1
        #     # if t % 50 == 0:
        #     print('1')
        #     pg.draw.circle(self.screen, WHITE, (10, 10), 5)

        return 'Game_page'

class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.p = False