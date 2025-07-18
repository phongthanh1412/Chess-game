import pygame
from CONSTANT import *

class Square:
    COLS = 'abcdefgh'

    def __init__(self, row, col, piece=None):
        self.row, self.col, self.piece = row, col, piece
        self.alphacol = Square.COLS[col]

    def __eq__(self, other):
        return (self.row, self.col) == (other.row, other.col)

    def has_piece(self):
        return self.piece is not None

    def isempty(self):
        return self.piece is None

    def has_team_piece(self, color):
        return self.piece and self.piece.color == color

    def has_enemy_piece(self, color):
        return self.piece and self.piece.color != color

    def isempty_or_enemy(self, color):
        return not self.piece or self.piece.color != color
    
    def draw(self, screen, board, theme=None):
        
        if theme:
            color = theme.bg_light if (self.row + self.col) % 2 == 0 else theme.bg_dark
        else:
            color = WHITE_SQUARE if (self.row + self.col) % 2 == 0 else DARK_SQUARE

        pygame.draw.rect(screen, color, (self.col * SQUARE_SIZE, self.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def in_range(*args):
        return all(0 <= arg <= 7 for arg in args)

    def get_alphacol_white(col):
        return Square.COLS[col]
    
    def get_alphacol_black(col):
        return Square.COLS[7 - col]