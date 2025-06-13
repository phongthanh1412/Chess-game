import pygame

from CONSTANT import *
from logicGame import Board
from dragMouse import Dragger
from setting import Config
from square import Square

class ChessGame:
    def __init__(self):
        # Game state
        self.state = {
            'current_player': 'white',  
            'hovered_square': None,     
        }
        self.board = Board()            
        self.dragger = Dragger()        
        self.config = Config()      

    # --- Helper Methods ---

    def _get_square_color(self, row, col, color_map):
        """Determine color for a square based on its position."""
        is_light = (row + col) % 2 == 0
        return color_map['light'] if is_light else color_map['dark']

    def _draw_square(self, surface, row, col, color):
        """Draw a single square on the surface."""
        rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(surface, color, rect)

    def _draw_text(self, surface, text, pos, color):
        """Render and draw text on the surface."""
        label = self.config.font.render(text, True, color)
        surface.blit(label, pos)

    # --- Display Methods ---

    def draw_board(self, surface):
        """Render the chessboard with alternating colors and coordinates."""
        theme = self.config.current_theme
        bg_colors = {'light': theme.bg_light, 'dark': theme.bg_dark}

        for row in range(ROWS):
            for col in range(COLS):
                # Draw board square
                color = self._get_square_color(row, col, bg_colors)
                self._draw_square(surface, row, col, color)

                # Add row number on leftmost column
                if col == 0:
                    text_color = theme.bg_dark if row % 2 == 0 else theme.bg_light
                    self._draw_text(surface, str(ROWS - row), 
                                    (5, 5 + row * SQUARE_SIZE), text_color)

                # Add column letter on bottom row
                if row == 7:
                    text_color = self._get_square_color(row, col, 
                                                        {'light': theme.bg_dark, 'dark': theme.bg_light})
                    self._draw_text(surface, Square.get_alphacol(col), 
                                    (col * SQUARE_SIZE + SQUARE_SIZE - 20, HEIGHT - 20), 
                                    text_color)

    def draw_pieces(self, surface):
        """Display all pieces except the one being dragged."""
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece is not self.dragger.state['piece']:
                        # Load and position piece image
                        piece.set_texture()
                        image = pygame.image.load(piece.texture)
                        image_rect = image.get_rect(center=(
                            col * SQUARE_SIZE + SQUARE_SIZE // 2,
                            row * SQUARE_SIZE + SQUARE_SIZE // 2
                        ))
                        surface.blit(image, image_rect)

    def draw_valid_moves(self, surface):
        """Highlight possible moves for the dragged piece."""
        if self.dragger.state['is_dragging']:
            theme = self.config.current_theme
            move_colors = {'light': theme.move_light, 'dark': theme.move_dark}
            for move in self.dragger.state['piece'].moves:
                color = self._get_square_color(move.final.row, move.final.col, move_colors)
                self._draw_square(surface, move.final.row, move.final.col, color)

    def draw_last_move(self, surface):
        """Mark the initial and final squares of the last move."""
        if self.board.last_move:
            theme = self.config.current_theme
            trace_colors = {'light': theme.trace_light, 'dark': theme.trace_dark}
            for square in [self.board.last_move.initial, self.board.last_move.final]:
                color = self._get_square_color(square.row, square.col, trace_colors)
                self._draw_square(surface, square.row, square.col, color)

    def draw_hover_effect(self, surface):
        """Outline the square under the mouse cursor."""
        if self.state['hovered_square']:
            square = self.state['hovered_square']
            rect = (square.col * SQUARE_SIZE, square.row * SQUARE_SIZE, 
                    SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(surface, HOVER, rect, width=3)

    # --- Game Control Methods ---

    def switch_turn(self):
        """Alternate between white and black players."""
        self.state['current_player'] = ('white' if self.state['current_player'] == 'black' 
                                       else 'black')

    def set_hovered_square(self, row, col):
        """Update the square under the mouse cursor."""
        self.state['hovered_square'] = self.board.squares[row][col]

    def change_theme(self):
        """Cycle through available themes."""
        self.config.switch_theme()

    def play_sound(self, captured=False):
        """Play sound for piece movement or capture."""
        sound = self.config.sounds['capture'] if captured else self.config.sounds['move']
        sound.play()

    def reset_game(self):
        """Restart the game with initial settings."""
        self.state = {
            'current_player': 'white',
            'hovered_square': None,
        }
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()