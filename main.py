import os
import sys

import pygame

pygame.init()
size = WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 30
move_counter = 0

all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

levels = ['levels/level1.txt', 'levels/level2.txt', 'levels/level3.txt', 'levels/level4.txt', 'levels/level5.txt',
          'levels/level6.txt']


def terminate():
    pygame.quit()
    sys.exit()


def rot_center(image, angle):
    """rotate a Surface, maintaining position."""
    loc = image.get_rect().center  # rot_image is not defined
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite
    # or return tuple: (Surface, Rect)
    # return rot_sprite, rot_sprite.get_rect()


def levels_screen():
    coords = []
    lvl_width, lvl_height = WIDTH // 5, HEIGHT // 3.5
    fon = pygame.transform.scale(load_image('sprites/Background.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.draw.rect(screen, 'white', (10, 10, 50, 50))
    x1, y1 = lvl_width // 2, lvl_height // 2
    font = pygame.font.Font(None, 50)
    string_rendered = font.render('<--', 1, 'black')
    intro_rect = string_rendered.get_rect()
    screen.blit(string_rendered, (10, 10))
    for i in range(6):
        coords.append((x1, y1))
        pygame.draw.rect(screen, 'white', (x1, y1, lvl_width, lvl_height))
        string_rendered = font.render(str(i + 1), 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = y1 + lvl_height // 2
        intro_rect.x = x1 + lvl_width // 2
        screen.blit(string_rendered, intro_rect)
        x1 += round(lvl_width * 1.5)
        if i == 2:
            y1 += round(lvl_height * 1.5)
            x1 = lvl_width // 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i in range(len(coords)):
                    if coords[i][0] <= x <= coords[i][0] + lvl_width and coords[i][1] <= y <= coords[i][1] + lvl_height:
                        return game_screen(levels[i])
                    elif 10 <= x <= 60 and 10 <= y <= 60:
                        return start_screen()
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ["                       ОГОНЬ И ЗЕМЛЯ", "", '', '',
                  "Ваша задача - вместе решать головоломки.",
                  "Зеленый динозаврик не может наступать на",
                  "красные области,",
                  "а красный - на зелёные.",
                  ""]

    fon = pygame.transform.scale(load_image('sprites/Background.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.draw.rect(screen, 'white', (100, 100, 800, 600))
    pygame.draw.rect(screen, (59, 191, 90), (400, 550, 200, 100))
    font = pygame.font.Font(None, 50)
    text_coord = 110
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 120
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    string_rendered = font.render('Играть', 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 590
    intro_rect.x = 440
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and 400 <= event.pos[0] <= 600 and 550 <= event.pos[1] <= 650:
                return levels_screen()
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(file_path: str):
    with open(file_path) as e:
        level_map = [line.strip() for line in e]

    h = len(level_map)
    if h > 0:
        # w = max(level_map, key=len)
        w = max(map(len, level_map))
    else:
        raise ValueError("Файл пустой!")

    level_map = list(map(lambda x: x.ljust(w, '.'), level_map))
    return level_map


sprites = {
    "box": load_image('sprites/Box/ground.png'),
    "water": load_image("sprites/Spikes/water.png"),
    "lava": load_image("sprites/Spikes/lava.png"),
    'move_platform': load_image('sprites/Box/Tile_07.png'),
    'r_door': load_image('sprites/Doors/red_door.png'),
    'g_door': load_image('sprites/Doors/green_door.png')
}


def generate_level(file_path):
    fon = pygame.transform.scale(load_image('sprites/Background.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    level_map = load_level(file_path)
    for g_o in game_object:
        for y, line in enumerate(level_map):
            for x, key in enumerate(line):
                if key == g_o:
                    cls = game_object.get(key, None)
                    if cls is not None:
                        if key == 'R':
                            cls(x * tile_width, y * tile_height, 'sprites/Players/red_dino.png', 'r')
                        elif key == 'G':
                            cls(x * tile_width, y * tile_height, 'sprites/Players/green_dino.png', 'g')
                        elif key == 'r' or key == '(':
                            cls(x, y, 'r')
                        elif key == 'g' or key == ')':
                            cls(x, y, 'g')
                        elif key == "M":
                            global move_counter
                            with open("Moves.txt", "r", encoding="Utf-8") as e:
                                r = e.readlines()[move_counter]
                            cls(x, y, r)
                            move_counter += 1
                        else:
                            cls(x, y)


def game_screen(file_path):
    generate_level(file_path)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and player_group.sprites() and not player_group.sprites()[0].get_death():
                player_group.update()
            elif player_group.sprites() and (
                    player_group.sprites()[0].get_death() or player_group.sprites()[1].get_death()):
                return death_screen(file_path)
            elif player_group.sprites() and player_group.sprites()[0].get_win() and player_group.sprites()[1].get_win():
                return win_screen(file_path)
        fon = pygame.transform.scale(load_image('sprites/Background.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        # player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def win_screen(file_path):
    pygame.time.wait(500)
    for sprite in all_sprites:
        sprite.kill()
    fon = pygame.transform.scale(load_image('sprites/Background.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.draw.rect(screen, 'white', (100, 100, 800, 600))
    intro_text = ["                        УРОВЕНЬ ПРОЙДЕН", "", '', '',
                  "Ваш результат:"]  # потом будет когда таймер добавим
    font = pygame.font.Font(None, 50)
    text_coord = 250
    for line in intro_text:
        string_rendered = font.render(line, 1, 'black')
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def death_screen(file_path):
    pygame.time.wait(500)
    for sprite in all_sprites:
        sprite.kill()
    fon = pygame.transform.scale(load_image('sprites/Background.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.draw.rect(screen, 'white', (100, 100, 800, 600))
    pygame.draw.rect(screen, (59, 191, 90), (200, 500, 200, 100))
    pygame.draw.rect(screen, (59, 191, 90), (600, 500, 200, 100))
    intro_text = ["                        ВЫ ПРОИГРАЛИ", "", '', '',
                  "Не забывайте, что зеленый динозаврик",
                  "не может ходить по лаве, а красный",
                  "не может ходить по воде."]
    btns_text = ['Рестарт', 'Меню']
    font = pygame.font.Font(None, 50)
    text_coord = 250
    for s in btns_text:
        string_rendered = font.render(s, 1, 'black')
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 530
        intro_rect.x = text_coord
        screen.blit(string_rendered, intro_rect)
        text_coord += 400
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, 'black')
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 200 <= x <= 400 and 500 <= y <= 600:
                    return game_screen(file_path)
                elif 600 <= x <= 800 and 500 <= y <= 600:
                    return levels_screen()
        pygame.display.flip()
        clock.tick(FPS)


tile_width = tile_height = 32


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(all_sprites, wall_group, *groups)
        self.image = sprites["box"]
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height)


class MovePlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, way, *groups):
        super().__init__(all_sprites, wall_group, *groups)
        self.image = sprites["move_platform"]
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height)
        if way.split()[0] == "W":
            self.x_way = 0
            self.y_way = 1
        elif way.split()[0] == "A":
            self.x_way = -1
            self.y_way = 0
        elif way.split()[0] == "D":
            self.x_way = 1
            self.y_way = 0
        elif way.split()[0] == "S":
            self.x_way = 0
            self.y_way = -1
        self.range = int(way.split()[1]) * 2
        self.move_counter = 0

    def update(self, *args, **kwargs):
        speed = 2
        if self.move_counter <= self.range // 2:
            vector = 1
        elif self.move_counter > self.range:
            self.move_counter = 0
            vector = 1
        else:
            vector = -1
        self.rect.move_ip(speed * self.x_way * vector, speed * self.y_way * vector)
        self.move_counter += 1


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, color, *groups):
        super().__init__(all_sprites, wall_group, *groups)
        self.color = color
        if color == 'r':
            self.image = sprites["lava"]
            print('lava')
        else:
            self.image = sprites['water']
            print('water')
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height)

    def get_color(self):
        return self.color


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, color, *groups):
        super().__init__(all_sprites, wall_group, *groups)
        self.color = color
        if self.color == 'r':
            self.image = sprites['r_door']
        else:
            self.image = sprites['g_door']
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height)

    def get_color(self):
        return self.color


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, fn, color, *groups):
        super().__init__(all_sprites, player_group, *groups)
        self.frames = []
        self.cut_sheet(load_image(fn), 24, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.death = False
        self.win = False

        self.jump = False
        self.jumpCount = 0
        self.jumpMax = 13
        self.vector = 1
        self.color = color
        self.gravity = 4

    def cut_sheet(self, sheet, columns, rows):
        self.tile_height = sheet.get_height() // rows
        self.tile_width = sheet.get_width() // columns
        self.rect = pygame.Rect(0, 0, self.tile_width,
                                self.tile_height)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.color == 'r':
            w = pressed_keys[pygame.K_UP]
            d = pressed_keys[pygame.K_RIGHT]
            a = pressed_keys[pygame.K_LEFT]
        else:
            w = pressed_keys[pygame.K_w]
            d = pressed_keys[pygame.K_d]
            a = pressed_keys[pygame.K_a]
        if a and not (w and d):
            st = 2
            ed = 6
            if self.vector == 1:
                self.frames = [pygame.transform.flip(i, True, False) for i in self.frames]
                self.vector = -1
        elif w and not (a or d):
            st = 6
            ed = 10
        elif d and not (a or w):
            st = 2
            ed = 6
            if self.vector == -1:
                self.frames = [pygame.transform.flip(i, True, False) for i in self.frames]
                self.vector = 1
        else:
            st = 0
            ed = 2
        self.fr = self.frames[st:ed]
        self.cur_frame = (self.cur_frame + 1) % len(self.fr)
        self.image = self.fr[self.cur_frame]
        if not self.jump and w:
            self.jump = True
            self.jumpCount = self.jumpMax
        if self.jump:
            self.rect.y -= self.jumpCount
            if self.jumpCount > -self.jumpMax:
                self.jumpCount -= 1
            else:
                self.jump = False
        speed = 2
        self.rect.move_ip(0, self.gravity)
        for el in wall_group.sprites():
            if isinstance(el, Box) or isinstance(el, MovePlatform) or (isinstance(el, Spike) and (
                    (el.get_color() == 'r' and self.color == 'r') or (el.get_color() == 'g' and self.color == 'g'))):
                if pygame.sprite.collide_rect(self, el):
                    if self.rect.y + self.tile_height > el.rect.y and self.rect.y < el.rect.y:
                        self.rect.move_ip(0, el.rect.y - (self.rect.y + self.tile_height))
                        self.jump = False
                    if self.rect.x + self.tile_width - el.rect.x <= speed:
                        self.rect.move_ip(-(self.rect.x + self.tile_width - el.rect.x), 0)
                    if el.rect.x + tile_width - self.rect.x <= speed and self.rect.y + self.tile_height - el.rect.y > self.gravity:
                        self.rect.move_ip(el.rect.x + tile_width - self.rect.x, 0)
                    if el.rect.y + tile_height - self.rect.y <= self.jumpMax and self.rect.y + self.tile_height > el.rect.y + tile_height:
                        self.rect.move_ip(0, el.rect.y + tile_height - self.rect.y)
            if (isinstance(el, Spike) and el.get_color() == 'g' and self.color == 'r') or (
                    isinstance(el, Spike) and el.get_color() == 'r' and self.color == 'g'):
                if pygame.sprite.collide_rect(self, el):
                    self.death = True
            if (isinstance(el, Door) and el.get_color() == 'g' and self.color == 'g') or (
                    isinstance(el, Door) and el.get_color() == 'r' and self.color == 'r'):
                if pygame.sprite.collide_rect(self, el):
                    self.win = True
                else:
                    self.win = False
        self.rect.move_ip(speed * (d - a), 0)

    def get_death(self):
        return self.death

    def get_win(self):
        return self.win


game_object = {
    "G": AnimatedSprite,
    'R': AnimatedSprite,
    "r": Spike,
    'g': Spike,
    "#": Box,
    "M": MovePlatform,
    '(': Door,
    ')': Door
}

start_screen()
