import pygame
from pygame.draw import *
from random import randint
import numpy as np

from objects import *
from colors import *
from constants import *
from menu import *
from game import *


class Labirint_Fantaxiy():
    def __init__(self):
        self.screen = pygame.display.set_mode((weight, height))
        self.page = 'Menu_page'
        pygame.init()
        pygame.display.update()
        # print('1')

    def game(self):
        finished = False
        while not finished:
            if self.page == 'Menu_page':
                pass
                menu = Menu(self.screen)
                out = menu.menu()
                print('111111')
                if out == 'Game_page':
                    self.page = 'Game_page'
                elif out == True:
                    finished = True
            elif self.page == 'Game_page':
                game = Game('georgii', self.screen)
                out = game.game()
                if out == 'Menu_page':
                    self.page = 'Menu_page'
                elif out == True:
                    finished = True




labirint_fantaxiy = Labirint_Fantaxiy()
labirint_fantaxiy.game()


pygame.quit()