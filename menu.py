import pygame as pg
from colors import *
from constants import *
from output import *

class Pages():
    def __init__(self, screen):
        self.screen = screen
        self.image_menu = pg.image.load('image\menu.jpg').convert_alpha()
        # self.image_rule = pg.image.load('image\\rule.jpg').convert_alpha()
        self.image_game0 = pg.image.load('image\game0.jpg').convert_alpha()
        self.image_game00 = pg.image.load('image\game00.jpg').convert_alpha()
        self.image_game_choose = pg.image.load('image\game_choose.jpg').convert_alpha()
        self.vol = 5
        self.music = True
        self.image_set_on = pg.image.load('image\set_on.jpg').convert_alpha()
        self.image_set_off = pg.image.load('image\set_off.jpg').convert_alpha()
        self.image_top = pg.image.load('image\\top.jpg').convert_alpha()
        global Mouse
        Mouse = Mouse()
        self.T0 = 1 * FPS
        self.T = 0

    def menu(self):
        clock = pg.time.Clock()
        pg.display.update()
        # pg.mixer.music.load('all.mp3')
        # pg.mixer.music.play()
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

            if self.T > 0:
                self.T -= 1

            self.screen.blit(self.image_menu, (0, 0))

            pg.draw.circle(self.screen, WHITE, (Mouse.x, Mouse.y), 5)

            if (Mouse.x > 390) and (Mouse.x < 600) and (Mouse.y > 305) and (Mouse.y < 340) and Mouse.p and self.T == 0:
                self.T = self.T0
                return 'Game_choose'
            if (Mouse.x > 390) and (Mouse.x < 600) and (Mouse.y > 350) and (Mouse.y < 395) and Mouse.p and self.T == 0:
                self.T = self.T0
                return 'Top_page'
            if (Mouse.x > 390) and (Mouse.x < 600) and (Mouse.y > 404) and (Mouse.y < 445) and Mouse.p and self.T == 0:
                self.T = self.T0
                return 'Menu_page'
            if (Mouse.x > 390) and (Mouse.x < 600) and (Mouse.y > 455) and (Mouse.y < 495) and Mouse.p and self.T == 0:
                self.T = self.T0
                return 'Settings_page'

            if Mouse.enter:
                pygame.mixer.music.pause()

            self.grid()

            pg.display.update()
            self.screen.fill(BLACK)

    def top(self):
        clock = pg.time.Clock()
        pg.display.update()
        t0 = int(0.5 * FPS)
        t = 0
        # print(pg.font.get_fonts())
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

            self.screen.blit(self.image_top, (0, 0))

            game0, game00 = input_top_player()

            k_r = 0
            for i in range(len(game0)):
                f0 = pg.font.SysFont('arial', 27, bold=True, italic=True)
                text6 = f0.render('{}. {} --- {}'.format(i + 1, game0[i][1], game0[i][0]), 20, NAMES)
                self.screen.blit(text6, (125, 130 + k_r * 27))
                k_r += 1
                if k_r > 10:
                    break

            k_r = 0
            for i in range(len(game00)):
                f0 = pg.font.SysFont('arial', 27, bold=True, italic=True)
                text6 = f0.render('{}. {} --- {}'.format(i + 1, game00[i][1], game00[i][0]), 20, NAMES)
                self.screen.blit(text6, (575, 130 + k_r * 27))
                k_r += 1
                if k_r > 10:
                    break

            if self.T > 0:
                self.T -= 1

            pg.draw.circle(self.screen, WHITE, (Mouse.x, Mouse.y), 5)

            if (Mouse.x > 860) and (Mouse.x < 930) and (Mouse.y > 690) and (Mouse.y < 705) and Mouse.p and self.T == 0:
                self.T = self.T0
                return 'Menu_page'
            self.grid()

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

            # if (Mouse.x > 760) and (Mouse.x < 920) and (Mouse.y > 690) and (Mouse.y < 705) and Mouse.p:
            #     return 'Game_page'
            # self.grid()

            pg.display.update()
            self.screen.fill(BLACK)

    def game_choose(self):
        clock = pg.time.Clock()
        pg.display.update()
        print(self.T)
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

            if self.T > 0:
                self.T -= 1

            self.screen.blit(self.image_game_choose, (0, 0))

            pg.draw.circle(self.screen, WHITE, (Mouse.x, Mouse.y), 5)

            if (Mouse.x > 390) and (Mouse.x < 570) and (Mouse.y > 300) and (Mouse.y < 340) and Mouse.p and self.T == 0:
                self.T = self.T0
                return 'Game0_page'
            if (Mouse.x > 390) and (Mouse.x < 570) and (Mouse.y > 350) and (Mouse.y < 390) and Mouse.p and self.T == 0:
                self.T = self.T0
                return 'Game00_page'
            self.grid()

            pg.display.update()
            self.screen.fill(BLACK)

    def game0(self):
        clock = pg.time.Clock()
        pg.display.update()
        name = ''
        # print(pg.font.get_fonts())
        while True:
            clock.tick(FPS)
            self.screen.blit(self.image_game0, (0, 0))
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

            if self.T > 0:
                self.T -= 1

            f0 = pg.font.SysFont('arial', 27, bold=True, italic=True)
            text0 = f0.render(name, 5, NAMES)
            self.screen.blit(text0, (443, 277))

            pg.draw.circle(self.screen, WHITE, (Mouse.x, Mouse.y), 5)

            if (Mouse.x > 760) and (Mouse.x < 920) and (Mouse.y > 690) and (Mouse.y < 705) and Mouse.p and self.T == 0:
                self.T = self.T0
                return ('Game0_game_page', name)
            self.grid()

            pg.display.update()
            self.screen.fill(BLACK)

    def game00(self):
        clock = pg.time.Clock()
        pg.display.update()
        name1 = ''
        name2 = ''
        next_name = False
        while True:
            clock.tick(FPS)
            self.screen.blit(self.image_game00, (0, 0))
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
                        Mouse.enter = True

                    elif event.key == pg.K_BACKSPACE:
                        if not next_name:
                            name1 = name1[:-1]
                        else:
                            name2 = name2[:-1]

                    else:
                        if not next_name:
                            name1 += event.unicode
                        else:
                            name2 += event.unicode

            if self.T > 0:
                self.T -= 1

            f0 = pg.font.SysFont('arial', 28, bold=True, italic=True)
            text0 = f0.render(name1, 5, NAMES)
            self.screen.blit(text0, (580, 277))

            f0 = pg.font.SysFont('arial', 28, bold=True, italic=True)
            text0 = f0.render(name2, 5, NAMES)
            self.screen.blit(text0, (617, 363))

            pg.draw.circle(self.screen, WHITE, (Mouse.x, Mouse.y), 5)

            if Mouse.enter:
                next_name = True


            if (Mouse.x > 760) and (Mouse.x < 920) and (Mouse.y > 690) and (Mouse.y < 705) and Mouse.p and self.T == 0:
                self.T = self.T0
                return ('Game00_game_page', name1, name2)
            self.grid()

            pg.display.update()
            self.screen.fill(BLACK)

    def settings(self):
        clock = pg.time.Clock()
        pg.display.update()
        t0 = int(0.5 * FPS)
        t = 0
        # print(pg.font.get_fonts())
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
            if self.music:
                self.screen.blit(self.image_set_off, (0, 0))
            else:
                self.screen.blit(self.image_set_on, (0, 0))

            if self.T > 0:
                self.T -= 1

            pg.draw.circle(self.screen, WHITE, (Mouse.x, Mouse.y), 5)
            
            if t > 0:
                t -= 1            

            for i in range(int(self.vol)):
                pg.draw.rect(self.screen, BLACK, (460 + i * 17, 207, 10, 23))
            # print(self.vol)
            if (Mouse.x > 396) and (Mouse.x < 401) and (Mouse.y > 205) and (Mouse.y < 225) and Mouse.p and t == 0 and self.T == 0:
                if self.vol > 0 and self.vol <= 10:
                    self.vol -= 1
                    t = t0
            if (Mouse.x > 405) and (Mouse.x < 440) and (Mouse.y > 205) and (Mouse.y < 225) and Mouse.p and t == 0 and self.T == 0:
                if self.vol >= 0 and self.vol < 10:
                    self.vol += 1
                    t = t0

            if (Mouse.x > 396) and (Mouse.x < 505) and (Mouse.y > 270) and (Mouse.y < 397) and Mouse.p and t == 0 and self.T == 0:
                if self.music:
                    self.music = False
                    t = t0
                else:
                    self.music = True
                    t = t0

            if (Mouse.x > 860) and (Mouse.x < 930) and (Mouse.y > 690) and (Mouse.y < 705) and Mouse.p and self.T == 0:
                self.T = self.T0
                return 'Menu_page'
            self.grid()

            pg.display.update()
            self.screen.fill(BLACK)


class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.p = False
        self.enter = False