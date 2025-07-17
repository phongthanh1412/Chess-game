import pygame
from CONSTANT import *

class Config:
    def __init__(self):
        # Font for rendering text
        self.font = RENDER_TEXT
        # Available themes
        self._themes = self._create_themes()
        self._current_theme_index = 0
        self.current_theme = self._themes[self._current_theme_index]

    def switch_theme(self):
        self._current_theme_index = (self._current_theme_index + 1) % len(self._themes)
        self.current_theme = self._themes[self._current_theme_index]

    def _create_themes(self):
        """Define and return a list of available themes."""
        theme_configs = [
            {  # Brown theme
                'bg': (TAN_LIGHT, BROWN_WOOD),
                'moves': (YELLOW_HIGHLIGHT, GOLDEN_HIGHLIGHT),
                'trace': (YELLOW_HIGHLIGHT, GOLDEN_HIGHLIGHT)
            },
            {  # Dark brown theme
                'bg': (WHEAT_LIGHT, CHOCOLATE_DARK),
                'moves': (YELLOW_HIGHLIGHT, GOLDEN_HIGHLIGHT),
                'trace': (YELLOW_HIGHLIGHT, GOLDEN_HIGHLIGHT)
            },
            {  # Green theme
                'bg': (OLIVE_LIGHT, OLIVE_DARK),
                'moves': (LIME_LIGHT, LIME_DARK),
                'trace': (LIME_LIGHT, LIME_DARK)
            },                   
            {  # Blue theme
                'bg': (COOL_BEIGE , STEEL_BLUE),
                'moves': (CYAN, TEAL),     
                'trace': (SKY_BLUE, SKY_BLUE)        
            }      
        ]
        return [Theme(**config) for config in theme_configs]

class Sound:
    def __init__(self, file_path):
        self._sound = pygame.mixer.Sound(file_path)

    def play(self):
        self._sound.play()

class Theme:
    def __init__(self, bg, moves, trace):
        self.bg_light, self.bg_dark = bg
        self.move_light, self.move_dark = moves
        self.trace_light, self.trace_dark = trace