import pygame

from utilities import load_image, load_level, terminate, levels, colors, sprites
from global_variables import *
pygame.init()
# size = WIDTH, HEIGHT = 1000, 800
# tile_width = tile_height = 32
# screen = pygame.display.set_mode(size)
# clock = pygame.time.Clock()
# tick = pygame.time.get_ticks() / 1000
# end_time = ""
# FPS = 30
# move_counter = 0
# score = 100
# jump_sound_r = pygame.mixer.Sound("sounds/Jump.wav")
# jump_sound_g = pygame.mixer.Sound("sounds/Retro Jump 01.wav")
#
#
# all_sprites = pygame.sprite.Group()
# wall_group = pygame.sprite.Group()
# spikes_group = pygame.sprite.Group()
# player_group = pygame.sprite.Group()
# button_group = pygame.sprite.Group()
# platform_group = pygame.sprite.Group()


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, species, *groups):
        super().__init__(all_sprites, wall_group, *groups)
        # self.image = sprites["box"]
        self.image = load_image(f"sprites/Box/Tile_{species}.png")
        # print(f"Tile_{species}")
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height)


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, color, *groups):
        super().__init__(all_sprites, button_group, *groups)
        self.color = color
        self.status = False
        self.x = x
        self.y = y
        self.count = 0
        if self.color == 'r':
            self.image = sprites["r_btn"]
        elif self.color == 'y':
            self.image = sprites["y_btn"]
        elif self.color == 'g':
            self.image = sprites["g_btn"]
        elif self.color == 'b':
            self.image = sprites["b_btn"]
        else:
            self.image = sprites["p_btn"]
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height)

    def set_status(self, b):
        self.status = b

    def get_status(self):
        return self.status

    def get_coords(self):
        return (self.x, self.y)

    def get_color(self):
        return self.color


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, color, *groups):
        super().__init__(all_sprites, wall_group, platform_group, *groups)
        self.color = color
        self.x = x
        self.y = y
        if self.color == 'r':
            self.image = sprites["r_platform"]
        elif self.color == 'y':
            self.image = sprites["y_platform"]
        elif self.color == 'g':
            self.image = sprites["g_platform"]
        elif self.color == 'b':
            self.image = sprites["b_platform"]
        else:
            self.image = sprites["p_platform"]
        self.rect = self.image.get_rect().move(x * tile_width + 14, y * tile_height)

    def get_color(self):
        return self.color

    def get_coords(self):
        return (self.x, self.y)


class MovePlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, way, *groups):
        super().__init__(all_sprites, wall_group, *groups)
        self.image = sprites["move_platform"]
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height)
        self.tile_width = 32
        self.tile_height = 32
        self.start_x = x * tile_width
        self.start_y = y * self.tile_height
        self.vector = 1
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
        self.range = int(way.split()[1])

    def update(self, *args, **kwargs):
        speed = 2
        if self.rect.x > self.start_x + self.range or self.rect.x < self.start_x - self.range or self.rect.y > self.start_y + self.range or self.rect.y < self.start_y - self.range:
            self.vector *= -1
        self.rect.move_ip(speed * self.x_way * self.vector, speed * self.y_way * self.vector)


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


class Diamond(pygame.sprite.Sprite):
    def __init__(self, x, y, color, *groups):
        super().__init__(all_sprites, *groups)
        self.color = color
        if self.color == "r":
            self.image = sprites["water_melon"]
        else:
            self.image = sprites["banana"]
        self.rect = self.image.get_rect().move(x * tile_width, y * tile_height)
        self.start_y = self.rect.y
        self.vector = 1
        self.tick = pygame.time.get_ticks()

    def update(self, *args, **kwargs):
        global score
        if self.rect.y > self.start_y + 5 or self.rect.y < self.start_y - 5:
            self.vector *= -1
        self.rect.move_ip(0, 1 * self.vector)
        for el in player_group:
            if pygame.sprite.collide_rect(self, el):
                if el.get_color() == self.color:
                    score += 300
                    coin_sound = pygame.mixer.Sound("sounds/Retro PickUp Coin StereoUP 04.wav")
                    coin_sound.set_volume(0.1)
                    coin_sound.play()
                    self.kill()


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
        self.win = False
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
            ed = 4
        self.fr = self.frames[st:ed]
        self.cur_frame = (self.cur_frame + 1) % len(self.fr)
        self.image = self.fr[self.cur_frame]
        if not self.jump and w:
            self.jump = True
            self.jumpCount = self.jumpMax
            if self.color == "r":
                jump_sound_r.play()
            else:
                jump_sound_g.play()
        if self.jump:
            self.rect.y -= self.jumpCount
            if self.jumpCount > -self.jumpMax:
                self.jumpCount -= 1
            else:
                self.jump = False
        speed = 2
        self.rect.move_ip(0, self.gravity)
        for el in wall_group.sprites():
            if pygame.sprite.collide_rect(self, el):
                if (((isinstance(el, Spike) and el.get_color() == 'g' and self.color == 'r') or (
                        isinstance(el, Spike) and el.get_color() == 'r' and self.color == 'g'))
                        and self.rect.y + self.tile_height - el.rect.y > 3 and (
                                abs(self.rect.x - el.rect.x - tile_width) > 16 or
                                abs(el.rect.x + tile_width - self.rect.x) > 16)):
                    if not self.death:
                        lose_sound = pygame.mixer.Sound("sounds/SFX_Lose08.ogg")
                        lose_sound.play(0)
                    self.death = True
                elif (isinstance(el, Door) and el.get_color() == 'g' and self.color == 'g') or (
                        isinstance(el, Door) and el.get_color() == 'r' and self.color == 'r'):
                    self.win = True
                else:
                    if self.rect.y + self.tile_height > el.rect.y and self.rect.y < el.rect.y:
                        self.rect.move_ip(0, el.rect.y - (self.rect.y + self.tile_height))
                        self.jump = False
                    if self.rect.x + self.tile_width - el.rect.x <= speed and self.rect.y + self.tile_height - el.rect.y > self.gravity:
                        self.rect.move_ip(-(self.rect.x + self.tile_width - el.rect.x), 0)
                    if isinstance(el,
                                  Platform) and el.rect.x + 6 - self.rect.x <= speed and self.rect.y + self.tile_height - el.rect.y > self.gravity:
                        self.rect.move_ip(el.rect.x + 6 - self.rect.x, 0)
                    elif el.rect.x + tile_width - self.rect.x <= speed and self.rect.y + self.tile_height - el.rect.y > self.gravity:
                        self.rect.move_ip(el.rect.x + tile_width - self.rect.x, 0)
                    if el.rect.y + tile_height - self.rect.y <= self.jumpMax and self.rect.y + self.tile_height > el.rect.y + tile_height:
                        self.rect.move_ip(0, el.rect.y + tile_height - self.rect.y)
        self.rect.move_ip(speed * (d - a), 0)

    def get_death(self):
        return self.death

    def get_win(self):
        return self.win

    def get_color(self):
        return self.color



