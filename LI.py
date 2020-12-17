import pygame
from pygame.draw import *
from random import randint
import numpy as np

from constants import *
from menu import *
from game0 import *
from game00 import *
from output import *


class Labirint_Fantaxiy():
    def __init__(self):
        '''
        Основная функция игры
        '''
        self.screen = pygame.display.set_mode((weight, height))
        self.page = 'Menu_page'
        pygame.init()
        pygame.display.update()
        self.name1 = ''
        self.name2 = ''
        global pages
        pages = Pages(self.screen)
        # print('1')

    def game(self):
        finished = False
        while not finished:
            if self.page == 'Menu_page':
                out = pages.menu()
                # print('111111')
                if out == 'Rule_page':
                    self.page = 'Rule_page'
                elif out == True:
                    finished = True
                # elif out == 'Settings_page':
                #     self.page = 'Settings_page'
                elif out == 'Game_choose':
                    self.page = 'Game_choose'
                elif out =='Top_page':
                    self.page = 'Top_page'

            elif self.page == 'Top_page':
                out = pages.top()
                if out == 'Menu_page':
                    self.page = 'Menu_page'
                elif out == True:
                    finished = True

            elif self.page == 'Rule_page':
                out = pages.rule()
                if out == 'Menu_page':
                    self.page = 'Menu_page'
                elif out == True:
                    finished = True

            elif self.page == 'Game_choose':
                out = pages.game_choose()
                if out == 'Game0_page':
                    self.page = 'Game0_page'
                elif out == True:
                    finished = True
                elif out == 'Game00_page':
                    self.page = 'Game00_page'

            elif self.page == 'Game0_page':
                out = pages.game0()
                if out[0] == 'Game0_game_page':
                    self.page = 'Game0_game_page'
                    self.name1 = out[1]
                elif out[0] == True:
                    finished = True

            elif self.page == 'Game0_game_page':
                game = Game0(self.name1, self.screen)
                out = game.game()
                if out == 'Menu_page':
                    self.page = 'Menu_page'
                elif out == True:
                    finished = True

            elif self.page == 'Game00_page':
                out = pages.game00()
                if out[0] == 'Game00_game_page':
                    self.page = 'Game00_game_page'
                    self.name1 = out[1]
                    self.name2 = out[2]
                elif out[0] == True:
                    finished = True

            elif self.page == 'Game00_game_page':
                game = Game00(self.name1, self.name2, self.screen)
                out = game.game()
                if out[0] == 'Menu_page':
                    self.page = 'Menu_page'
                    if out[1] != 'draw':
                        output_top_player('game00', out[1], out[2])
                elif out[0] == True:
                    finished = True

            elif self.page == 'Settings_page':
                out = pages.settings()
                if out == True:
                    finished = True
                elif out == 'Menu_page':
                    self.page = 'Menu_page'




labirint_fantaxiy = Labirint_Fantaxiy()
labirint_fantaxiy.game()


pygame.quit()