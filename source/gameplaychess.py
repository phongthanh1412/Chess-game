import pygame
from CONSTANT import *
from logicGame import Board
from dragMouse import Dragger
from setting import Config
from square import Square
from chess import Move

class ChessGame:
    def __init__(self, flipped=False):
        self.flipped = flipped
        self.state = {
            'current_player': 'white',
            'hovered_square': None,
        }
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    def _get_square_color(self, row, col, color_map):
        is_light = (row + col) % 2 == 0
        return color_map['light'] if is_light else color_map['dark']

    def _draw_square(self, surface, row, col, color):
        rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(surface, color, rect)

    def _draw_text(self, surface, text, pos, color):
        label = self.config.font.render(text, True, color)
        surface.blit(label, pos)

    def _flip(self, row, col):
        """Return flipped (row, col) if game.flipped is True"""
        if self.flipped:
            return 7 - row, 7 - col
        return row, col

    def draw_board(self, surface):
        theme = self.config.current_theme
        bg_colors = {'light': theme.bg_light, 'dark': theme.bg_dark}

        for row in range(ROWS):
            for col in range(COLS):
                draw_row, draw_col = self._flip(row, col)
                self.board.squares[row][col].draw(surface, self.board, theme)

                if draw_col == 0:
                    text_color = bg_colors['dark'] if (row + col) % 2 == 0 else bg_colors['light']
                    self._draw_text(surface, str(ROWS - row),
                         (5, draw_row * SQUARE_SIZE + 5), text_color)

                if draw_row == 7:
                    text_color = self._get_square_color(row, col,
                       {'light': theme.bg_dark, 'dark': theme.bg_light})
                    self._draw_text(surface, Square.get_alphacol(col),
                      (draw_col * SQUARE_SIZE + SQUARE_SIZE - 20, HEIGHT - 20), text_color)

    def draw_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece is not self.dragger.state['piece']:
                        piece.set_texture()
                        image = pygame.image.load(piece.texture)
                        image = pygame.transform.scale(image, (80, 80))
                        draw_row, draw_col = self._flip(row, col)
                        center = (
                            draw_col * SQUARE_SIZE + SQUARE_SIZE // 2,
                            draw_row * SQUARE_SIZE + SQUARE_SIZE // 2
                        )
                        rect = image.get_rect(center=center)
                        surface.blit(image, rect)

    def draw_valid_moves(self, surface):
        if self.dragger.state['is_dragging']:
            theme = self.config.current_theme
            move_colors = {'light': theme.move_light, 'dark': theme.move_dark}
            for move in self.dragger.state['piece'].moves:
                row, col = move.final.row, move.final.col
                draw_row, draw_col = self._flip(row, col)
                color = self._get_square_color(row, col, move_colors)
                self._draw_square(surface, draw_row, draw_col, color)

    def draw_last_move(self, surface):
        if self.board.last_move:
            theme = self.config.current_theme
            trace_colors = {'light': theme.trace_light, 'dark': theme.trace_dark}
            for square in [self.board.last_move.initial, self.board.last_move.final]:
                row, col = square.row, square.col
                draw_row, draw_col = self._flip(row, col)
                color = self._get_square_color(row, col, trace_colors)
                self._draw_square(surface, draw_row, draw_col, color)

    def switch_turn(self):
        self.state['current_player'] = 'black' if self.state['current_player'] == 'white' else 'white'

    def change_theme(self):
        self.config.switch_theme()

    def play_sound(self, captured=False, castled=False):
        if castled:
            sound = self.config.sounds['castle']
        elif captured:
            sound = self.config.sounds['capture']
        else:
            sound = self.config.sounds['move']
        sound.play()

    def reset_game(self):
        self.state = {
            'current_player': 'white',
            'hovered_square': None,
        }
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    def update_from_server(self, board_state):
        self.state['current_player'] = board_state['current_player']
        for r in range(ROWS):
            for c in range(COLS):
                self.board.squares[r][c].piece = board_state['squares'][r][c]
        self.board.last_move = Move(
            Square(board_state['last_move']['start_row'], board_state['last_move']['start_col']),
            Square(board_state['last_move']['end_row'], board_state['last_move']['end_col'])
        ) if board_state['last_move'] else None
