import pygame
#define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
AQUA = (67, 223, 245)
PINK = (245, 134, 189)

#define screen size
WIDTH = 1024
HEIGHT = 768

FPS = 60
TITLE = "Demo Project"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

PLAYER_SPEED = 50.0
PLAYER_ROTATION_SPEED = 250.0

ENEMY_SPEED = 300

def collideHitbox(one, two):
    return one.hitbox.colliderect(two.rect)
