import pygame
from const import * 
from config import Config

class Title:
    
    def __init__(self):
        self.config = Config()
        self.bg_surf = pygame.image.load('assets/graphics/board_bg.png').convert_alpha()
        self.bg_surf = pygame.transform.scale(self.bg_surf, (WIDTH, HEIGHT))

        

    def show_bg(self, surface):
        surface.blit(self.bg_surf, (0,0))

        #TODO: Title --> self.config.title_font.render(<>)