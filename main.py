import os
import sys

import pygame

pygame.init()
size = WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 30

all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


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


def start_screen():
    intro_text = ["                       ОГОНЬ И ЗЕМЛЯ", "", '', '',
                  "Ваша задача - вместе решать головоломки.",
                  "Зеленый динозаврик не может наступать на",
                  "красные области,",
                  "а красный - на зелёные.",
                  ""]

    fon = pygame.transform.scale(load_image('sprites/Background.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return game_screen("level1.txt")
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
    "lava": load_image("sprites/Spikes/lava.png")
}


def generate_level(file_path):
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
                            cls(x * tile_width, y * tile_height, 'sprites/Players/dino.png', 'g')
                        elif key == 'r':
                            cls(x, y, 'r')
                        elif key == 'g':
                            cls(x, y, 'g')
                        else:
                            cls(x, y)


def game_screen(file_path):
    generate_level("level1.txt")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                player_group.update()
        fon = pygame.transform.scale(load_image('sprites/Background.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        # player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


tile_width = tile_height = 50


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(all_sprites, wall_group, *groups)
        self.image = sprites["box"]
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height)


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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, fn, color):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.cut_sheet(load_image(fn), 24, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

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
            if isinstance(el, Box) or (isinstance(el, Spike) and el.get_color() == 'r' and self.color == 'r') or (
                    isinstance(el, Spike) and el.get_color() == 'g' and self.color == 'g'):
                if pygame.sprite.collide_rect(self, el):
                    if self.rect.y + self.tile_height > el.rect.y and self.rect.y < el.rect.y:
                        self.rect.move_ip(0, el.rect.y - (self.rect.y + self.tile_height))
                        print("Up")
                        self.jump = False
                    if self.rect.x + self.tile_width - el.rect.x <= speed:
                        self.rect.move_ip(-(self.rect.x + self.tile_width - el.rect.x), 0)
                        print("left")
                    if el.rect.x + tile_width - self.rect.x <= speed and self.rect.y + self.tile_height - el.rect.y > self.gravity:
                        self.rect.move_ip(el.rect.x + tile_width - self.rect.x, 0)
                        print("right")
                    if el.rect.y + tile_height - self.rect.y <= self.jumpMax and self.rect.y + self.tile_height > el.rect.y + tile_height:
                        self.rect.move_ip(0, el.rect.y + tile_height - self.rect.y)
                        print("Down")
            elif (isinstance(el, Spike) and el.get_color() == 'g' and self.color == 'r') or (
                isinstance(el, Spike) and el.get_color() == 'r' and self.color == 'g'):
                if pygame.sprite.collide_rect(self, el):
                    terminate()
        self.rect.move_ip(speed * (d - a), 0)


game_object = {
    "G": AnimatedSprite,
    'R': AnimatedSprite,
    "r": Spike,
    'g': Spike,
    "#": Box,
}

start_screen()
