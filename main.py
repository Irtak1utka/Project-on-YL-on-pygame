import pygame
from utilities import load_image, load_level, terminate, levels, colors, sprites
from Classes import *
from global_variables import *
from screen_window import *

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
pygame.mixer.music.load("sounds/Magical Forest.wav")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)

# jump_sound_r = pygame.mixer.Sound("sounds/Jump.wav")
jump_sound_r.set_volume(0.1)
# jump_sound_g = pygame.mixer.Sound("sounds/Retro Jump 01.wav")
jump_sound_g.set_volume(0.2)


def levels_screen():
    coords = []
    lvl_width, lvl_height = WIDTH // 5, HEIGHT // 3.5
    fon = pygame.transform.scale(load_image('sprites/Background.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.draw.rect(screen, 'white', (10, 10, 50, 50))
    x1, y1 = lvl_width // 2, lvl_height // 2
    font = pygame.font.Font(None, 50)
    string_rendered = font.render('<--', 1, 'black')
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


def generate_level(file_path):
    fon = pygame.transform.scale(load_image('sprites/Background.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    level_map = load_level(file_path)
    print(level_map)
    for g_o in game_object:
        for y, line in enumerate(level_map):
            for x, key in enumerate(line):
                if key == g_o:
                    cls = game_object.get(key, None)
                    if cls is not None:
                        if key == 'R':
                            cls(x * tile_width, y * tile_height, 'sprites/Players/red_dino-export.png', 'r')
                        elif key == 'G':
                            cls(x * tile_width, y * tile_height, 'sprites/Players/green_dino-export.png', 'g')
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
                        elif key in '12345':
                            cls(x, y, colors[key])
                        elif key in '!@№$%':
                            cls(x, y, colors[key])
                        elif key == "m":
                            cls(x, y, "r")
                        elif key == "b":
                            cls(x, y, "g")
                        elif key in "абвгдеёжзийклмноп#":
                            cls(x, y, key)
                        else:
                            cls(x, y)
                            print(key)


def game_screen(file_path):
    pygame.mixer.music.play()
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
        for el in button_group.sprites():
            a = False
            for pl in player_group.sprites():
                if pygame.sprite.collide_rect(pl, el):
                    a = True
                    if el.get_status() is False:
                        el.set_status(True)
                        el.rect.move_ip(0, 4)
            if a is False and el.get_status() is True:
                el.set_status(False)
                el.rect.move_ip(0, -4)
            else:
                for pf in platform_group.sprites():
                    if el.get_color() == pf.get_color() and pf.rect.y > pf.get_coords()[
                        1] * tile_height - tile_height and el.get_status() is True:
                        pf.rect.move_ip(0, -1)
                    elif pf.rect.y < pf.get_coords()[1] * tile_height and el.get_status() is False:
                        pf.rect.move_ip(0, 1)
        font = pygame.font.Font(None, 28)
        seconds = int((pygame.time.get_ticks() - tick) / 1000)
        minutes = seconds // 60
        seconds %= 60
        timer_text = font.render(f"{minutes:02}:{seconds:02}", 1, "White")
        intro_rect = timer_text.get_rect()
        intro_rect.top = 0
        intro_rect.x = 0
        screen.blit(timer_text, intro_rect)
        global end_time
        end_time = f"{minutes:02}:{seconds:02}"
        pygame.display.flip()
        clock.tick(FPS)


def win_screen(file_path):
    pygame.mixer.music.stop()
    win_sound = pygame.mixer.Sound("sounds/Victory.wav")
    win_sound.set_volume(0.1)
    win_sound.play(-1)
    global end_time
    pygame.time.wait(500)
    for sprite in all_sprites:
        sprite.kill()
    fon = pygame.transform.scale(load_image('sprites/Background.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.draw.rect(screen, 'white', (100, 100, 800, 600))
    pygame.draw.rect(screen, (59, 191, 90), (150, 500, 200, 100))
    pygame.draw.rect(screen, (59, 191, 90), (400, 500, 200, 100))
    pygame.draw.rect(screen, (59, 191, 90), (650, 500, 200, 100))
    intro_text = ["                     УРОВЕНЬ ПРОЙДЕН", "", '', '',
                  f"Ваш результат: {end_time}", f"Ваш счёт: {score}"]
    btns_text = ['->', 'Меню', '  Рестарт']
    font = pygame.font.Font(None, 50)
    text_coord = 250
    for s in btns_text:
        string_rendered = font.render(s, 1, 'black')
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 530
        intro_rect.x = text_coord
        screen.blit(string_rendered, intro_rect)
        text_coord += 200
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
                win_sound.stop()
                if 500 <= y <= 600:
                    if 150 <= x <= 350:
                        l = levels.index(file_path) + 1
                        if l <= 6:
                            return game_screen(levels[l])
                        else:
                            return levels_screen()
                    elif 400 <= x <= 600:
                        return levels_screen()
                    elif 650 <= x <= 850:
                        return game_screen(file_path)
        pygame.display.flip()
        clock.tick(FPS)


def death_screen(file_path):
    pygame.time.wait(500)
    pygame.mixer.music.stop()
    end_sound = pygame.mixer.Sound("sounds/GameOver.wav")
    end_sound.play()
    for sprite in all_sprites:
        sprite.kill()
        global move_counter
        move_counter = 0
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
                end_sound.stop()
                if 200 <= x <= 400 and 500 <= y <= 600:
                    return game_screen(file_path)
                elif 600 <= x <= 800 and 500 <= y <= 600:
                    return levels_screen()
        pygame.display.flip()
        clock.tick(FPS)


# Box


# Button


# Platform

# MovePlatform


# Splike


# Diamond


# Door


# AnimatedSprite


game_object = {
    "G": AnimatedSprite,
    'R': AnimatedSprite,
    "r": Spike,
    'g': Spike,
    "#": Box,
    "а": Box,
    "б": Box,
    "в": Box,
    "г": Box,
    "д": Box,
    "е": Box,
    "ё": Box,
    "ж": Box,
    "з": Box,
    "и": Box,
    "й": Box,
    "к": Box,
    "л": Box,
    "м": Box,
    "н": Box,
    "о": Box,
    "п": Box,
    "M": MovePlatform,
    '(': Door,
    ')': Door,
    '1': Button,
    '2': Button,
    '3': Button,
    '4': Button,
    '5': Button,
    '!': Platform,
    '@': Platform,
    '№': Platform,
    '$': Platform,
    '%': Platform,
    "b": Diamond,
    "m": Diamond,
}

if __name__ == '__main__':
    start_screen()
