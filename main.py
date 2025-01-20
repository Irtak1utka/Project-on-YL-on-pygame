import sys

import pygame

import os

pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 60

all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


sprites = {
    "fire": load_image("fire.png"),
    "water": load_image("fail_water.png")
}


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = sprites["fire"]
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self, *args, **kwargs):
        pressed_keys = pygame.key.get_pressed()
        w = pressed_keys[pygame.K_w]
        d = pressed_keys[pygame.K_d]
        s = pressed_keys[pygame.K_s]
        a = pressed_keys[pygame.K_a]
        speed = 2
        self.rect.move_ip(speed * (d - a), speed * (s - w))
        if pygame.sprite.collide_rect(fire, water):
            fire.kill()
            print("You fail")


class Water(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = sprites["water"]
        self.rect = self.image.get_rect().move(pos_x, pos_y)


fire = Player(0, 0)
water = Water(100, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if pygame.key.get_pressed():
        player_group.update()
    screen.fill("black")
    all_sprites.draw(screen)
    all_sprites.update()
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
