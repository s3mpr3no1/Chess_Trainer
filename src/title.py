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
        title_message = self.config.title_font.render("Chess Trainer", False, (0, 0, 0))
        title_message_rect = title_message.get_rect(center = ((WIDTH // 2), (HEIGHT // 8)))
        surface.blit(title_message, title_message_rect)
        # game_name = test_font.render("Pixel Runner", False, (111, 196, 169))
        # game_name_rect = game_name.get_rect(center = (400, 80))
        # screen.blit(game_message, game_message_rect)
