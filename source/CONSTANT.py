import pygame
import os

pygame.init()

# Screen size
WIDTH = 600
HEIGHT = 600

# Board size
ROWS = 8
COLS = 8
SQUARE_SIZE = WIDTH // COLS

# 50-move rule
FIFTY_MOVES = 100

# Highlight effect
HOVER = (180, 180, 180)

# Background color for draw
DRAW_COLOR = (120, 120, 80)
WIN_COLOR = (80, 120, 50)  

# Theme
TAN_LIGHT = (235, 209, 166)
BROWN_WOOD = (165, 117, 80)

WHEAT_LIGHT = (245, 222, 179)
CHOCOLATE_DARK = (139, 69, 19)

OLIVE_LIGHT = (234, 235, 200)
OLIVE_DARK = (119, 154, 88)

COOL_BEIGE  = (229, 228, 200)
STEEL_BLUE = (60, 95, 135)

# Highlight move
YELLOW_HIGHLIGHT = (245, 234, 100)
GOLDEN_HIGHLIGHT = (209, 185, 59)
LIME_LIGHT = (244, 247, 116)
LIME_DARK = (172, 195, 51)
SKY_BLUE = (135, 206, 235)
CYAN = (150, 255, 255)
TEAL = (0, 128, 128)

# Popup
TEXT_COLOR = (255, 255, 255)
BG_COLOR = (50, 50, 50)
BORDER_COLOR = (200, 200, 200)
PROMOTION_COLOR = (165, 117, 80)
PROMOTION_BORDER = (0, 0, 0)
PROMOTION_BOX = pygame.Rect(160, 160, 320, 160)
PIECE_OPTIONS = ['queen', 'rook', 'bishop', 'knight']

# Font
TITLE_FONT = pygame.font.SysFont('Arial', 48, bold=True)
MSG_FONT = pygame.font.SysFont('Arial', 36)
HINT_FONT = pygame.font.SysFont('Arial', 24)
RENDER_TEXT = pygame.font.SysFont('monospace', 18, bold=True)

# Sound
MOVE_SOUND = os.path.join('assets/sounds/move.wav')
CAPTURE_SOUND = os.path.join('assets/sounds/capture.wav')

# Position 
COL_PIECE = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
ROW_PIECE = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}