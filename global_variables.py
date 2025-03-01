import pygame

pygame.init()
size = WIDTH, HEIGHT = 1000, 800
tile_width = tile_height = 32
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
tick = pygame.time.get_ticks() / 1000
end_time = ""
FPS = 30
move_counter = 0
score = 100
jump_sound_r = pygame.mixer.Sound("sounds/Jump.wav")
jump_sound_g = pygame.mixer.Sound("sounds/Retro Jump 01.wav")


all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()

