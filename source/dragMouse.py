import pygame

from CONSTANT import *

class Dragger:
    def __init__(self):
        self.state = {
            'piece': None,           
            'is_dragging': False,   
            'mouse_x': 0,            
            'mouse_y': 0,            
            'start_row': 0,          
            'start_col': 0           
        }

    def render(self, surface):
        """Draw the dragged piece at mouse position."""
        if self.state['is_dragging']:
            piece = self.state['piece']
            piece.set_texture()
            img = pygame.image.load(piece.texture)
            img_rect = img.get_rect(center=(self.state['mouse_x'], self.state['mouse_y']))
            surface.blit(img, img_rect)

    def set_mouse_pos(self, pos):
        self.state['mouse_x'], self.state['mouse_y'] = pos

    def set_start_square(self, pos):
        self.state['start_row'] = pos[1] // SQUARE_SIZE
        self.state['start_col'] = pos[0] // SQUARE_SIZE

    def start_dragging(self, piece):
        self.state['piece'] = piece
        self.state['is_dragging'] = True

    def stop_dragging(self):
        self.state['piece'] = None
        self.state['is_dragging'] = False