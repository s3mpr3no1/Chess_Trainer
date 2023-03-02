import pygame 
import os

from sound import Sound
from theme import Theme


class Config:

    def __init__(self):
        self.themes = []
        self._add_themes()
        self.idx = 1
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.title_font = pygame.font.SysFont('impact', 100)
        
        self.menu_item_font = pygame.font.SysFont('impact', 75)
        self.menu_item_font_hover = pygame.font.SysFont('impact', 80)

        self.help_item = pygame.font.SysFont('impact', 50)
        self.help_item_hover = pygame.font.SysFont('impact', 55)
        self.move_font = pygame.font.SysFont('MONOSPACE', 25)
        self.move_sound = Sound(os.path.join('assets/sounds/move.mp3'))
        self.capture_sound = Sound(os.path.join('assets/sounds/capture.mp3'))

        self.study_wrong = (255, 0, 0)
        self.study_right = (0, 255, 0)
        self.study_neutral = (255, 255, 255)

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), (150, 150, 150), (150, 150, 150))
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), (150, 150, 150), (150, 150, 150))
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), (150, 150, 150), (150, 150, 150))
        gray = Theme((120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 102, 128), (150, 150, 150), (150, 150, 150))

        self.themes = [green, brown, blue, gray]
