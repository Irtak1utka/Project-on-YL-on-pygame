import pygame
import sys
import os


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
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
        w = max(map(len, level_map))
    else:
        raise ValueError("Файл пустой!")

    level_map = list(map(lambda x: x.ljust(w, '.'), level_map))
    return level_map


levels = ['levels/level1.txt', 'levels/level2.txt', 'levels/level3.txt', 'levels/level4.txt', 'levels/level5.txt',
          'levels/level6.txt']

colors = {
    '1': 'r',
    '!': 'r',
    '2': 'y',
    '@': 'y',
    '3': 'g',
    '№': 'g',
    '4': 'b',
    '$': 'b',
    '5': 'p',
    '%': 'p'
}

sprites = {
    "box": load_image('sprites/Box/ground.png'),
    "water": load_image("sprites/Spikes/water.png"),
    "lava": load_image("sprites/Spikes/lava.png"),
    'move_platform': load_image('sprites/Box/Tile_07.png'),
    'r_door': load_image('sprites/Doors/red_door.png'),
    'g_door': load_image('sprites/Doors/green_door.png'),
    'r_btn': load_image('sprites/Buttons/red_button.png'),
    'y_btn': load_image('sprites/Buttons/yellow_button.png'),
    'g_btn': load_image('sprites/Buttons/green_button.png'),
    'b_btn': load_image('sprites/Buttons/blue_button.png'),
    'p_btn': load_image('sprites/Buttons/pink_button.png'),
    'r_platform': load_image('sprites/Box/red_platform.png'),
    'y_platform': load_image('sprites/Box/yellow_platform.png'),
    'g_platform': load_image('sprites/Box/green_platform.png'),
    'b_platform': load_image('sprites/Box/blue_platform.png'),
    'p_platform': load_image('sprites/Box/pink_platform.png'),
    "banana": load_image("sprites/Diamonds/banana.png"),
    "water_melon": load_image("sprites/Diamonds/Wmelon.png")
}
