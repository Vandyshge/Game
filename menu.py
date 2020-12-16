import pygame as pg
from colors import *
from constants import *

class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.image_menu = pg.image.load('image\menu.jpg').convert_alpha()
        self.image_rule = pg.image.load('image\\rule.jpg').convert_alpha()
        self.image_set = pg.image.load('image\\set.jpg').convert_alpha()
        global Mouse
        Mouse = Mouse()

    def menu(self):
        clock = pg.time.Clock()
        pg.display.update()
        while True:
            clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return True
                if event.type == pg.MOUSEMOTION:
                    # запись новых координат мышки(если она подвинулась)
                    Mouse.x, Mouse.y = event.pos
                if event.type == pg.MOUSEBUTTONDOWN:
                    # кнопка зажата
                    Mouse.p = True
                if event.type == pg.MOUSEBUTTONUP:
                    # кнопка отжата
                    Mouse.p = False
                if event.type == pg.KEYDOWN:
                    # кнопка отжата
                    if event.key == pg.K_RETURN:
                        Mouse.enter = True

            self.screen.blit(self.image_menu, (0, 0))

            pg.draw.circle(self.screen, WHITE, (Mouse.x, Mouse.y), 5)

            if (Mouse.x > 390) and (Mouse.x < 600) and (Mouse.y > 360) and (Mouse.y < 395) and Mouse.p:
                return 'Rule_page'
            if (Mouse.x > 390) and (Mouse.x < 600) and (Mouse.y > 400) and (Mouse.y < 450) and Mouse.p:
                return 'Top_page'
            if (Mouse.x > 390) and (Mouse.x < 600) and (Mouse.y > 460) and (Mouse.y < 495) and Mouse.p:
                return 'Settings_page'

            # self.grid()

            pg.display.update()
            self.screen.fill(BLACK)

    def grid(self):
        # pg.draw.circle(self.screen, RED, (10, 10), 10000)
        for x in range(100, weight + 1, 100):
            pg.draw.line(self.screen, WHITE, [int(x), int(0)], [int(x), int(height)], 1)
        for y in range(100, height + 1, 100):
            pg.draw.line(self.screen, WHITE, [int(0), int(y)], [int(weight), int(y)], 1)

    def rule(self):
        clock = pg.time.Clock()
        pg.display.update()
        name = ''
        # print(pg.font.get_fonts())
        while True:
            clock.tick(FPS)
            self.screen.blit(self.image_rule, (0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return (True, )
                if event.type == pg.MOUSEMOTION:
                    # запись новых координат мышки(если она подвинулась)
                    Mouse.x, Mouse.y = event.pos
                if event.type == pg.MOUSEBUTTONDOWN:
                    # кнопка зажата
                    Mouse.p = True
                if event.type == pg.MOUSEBUTTONUP:
                    # кнопка отжата
                    Mouse.p = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        Mouse.enter = False

                    elif event.key == pg.K_BACKSPACE:
                        name = name[:-1]

                    else:
                        name += event.unicode
            f0 = pg.font.SysFont('arial', 27, bold=True, italic=True)
            text0 = f0.render(name, 5, BLACK)
            self.screen.blit(text0, (250, 110))

            pg.draw.circle(self.screen, WHITE, (Mouse.x, Mouse.y), 5)

            if (Mouse.x > 760) and (Mouse.x < 920) and (Mouse.y > 690) and (Mouse.y < 705) and Mouse.p:
                return ('Game_page', name)
            # self.grid()

            pg.display.update()
            self.screen.fill(BLACK)

    def settings(self):
        clock = pg.time.Clock()
        pg.display.update()
        name = ''
        # print(pg.font.get_fonts())
        while True:
            clock.tick(FPS)
            self.screen.blit(self.image_set, (0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return (True, )
                if event.type == pg.MOUSEMOTION:
                    # запись новых координат мышки(если она подвинулась)
                    Mouse.x, Mouse.y = event.pos
                if event.type == pg.MOUSEBUTTONDOWN:
                    # кнопка зажата
                    Mouse.p = True
                if event.type == pg.MOUSEBUTTONUP:
                    # кнопка отжата
                    Mouse.p = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        Mouse.enter = False

                    elif event.key == pg.K_BACKSPACE:
                        name = name[:-1]

                    else:
                        name += event.unicode
            f0 = pg.font.SysFont('arial', 27, bold=True, italic=True)
            text0 = f0.render(name, 5, BLACK)
            self.screen.blit(text0, (250, 110))

            pg.draw.circle(self.screen, WHITE, (Mouse.x, Mouse.y), 5)

            if (Mouse.x > 760) and (Mouse.x < 920) and (Mouse.y > 690) and (Mouse.y < 705) and Mouse.p:
                return ('Game_page', name)
            # self.grid()

            pg.display.update()
            self.screen.fill(BLACK)


class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.p = False
        self.enter = False