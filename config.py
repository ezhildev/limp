import os
import sys
from lib.funcs import *
from lib.inputhandler import InputHandler

pygame.init()

TITLE = 'limp'
TILE_SIZE = 16
GRID_SIZE = 32

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 576
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_CENTER = tuple([x//2 for x in WINDOW_SIZE])

FPS = 60


BG_COLOR = '#392830'

FONT_L = load_font('./src/fonts/ThaleahFat.ttf', 96)
FONT_M = load_font('./src/fonts/ThaleahFat.ttf', 64)
FONT_S = load_font('./src/fonts/ThaleahFat.ttf', 32)

# ICON = pygame.image.load('./scr/image/FNF.ico')


SCREEN_FADER = load_surface(WINDOW_SIZE)
SCREEN_FADER.fill(BG_COLOR)
SCREEN_FADER.set_alpha(255)

INPUT = InputHandler()
INPUT.left.map = [pygame.K_a, pygame.K_LEFT]
INPUT.right.map = [pygame.K_d, pygame.K_RIGHT]
INPUT.up.map = [pygame.K_w, pygame.K_UP]
INPUT.down.map = [pygame.K_s, pygame.K_DOWN]
INPUT.enter.map = [pygame.K_SPACE, pygame.K_RETURN]
INPUT.exit.map = [pygame.K_ESCAPE]
INPUT.restart.map = [pygame.K_r]

	