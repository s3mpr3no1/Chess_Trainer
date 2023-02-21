import pygame
from const import * 
from config import Config

class Help:

    def __init__(self):
        self.config = Config()
                
        self.bg_surf = pygame.image.load('assets/graphics/board_bg.png').convert_alpha()
        self.bg_surf = pygame.transform.scale(self.bg_surf, (WIDTH, HEIGHT))

        self.reset = self.config.help_item.render("r: Reset board", False, (0, 0, 0))
        self.reset_rect = self.reset.get_rect(center = (WIDTH // 2, 100))

        self.flip = self.config.help_item.render("f: Flip board", False, (0, 0, 0))
        self.flip_rect = self.flip.get_rect(center = (WIDTH // 2, 200))

        self.menu = self.config.help_item.render("m: Return to main menu", False, (0, 0, 0))
        self.menu_rect = self.menu.get_rect(center = (WIDTH // 2, 300))

        self.theme = self.config.help_item.render("t: Change the theme", False, (0, 0, 0))
        self.theme_rect = self.theme.get_rect(center = (WIDTH // 2, 400))

    def show_bg(self, surface):
        surface.blit(self.bg_surf, (0,0))
        surface.blit(self.reset, self.reset_rect)
        surface.blit(self.flip, self.flip_rect)
        surface.blit(self.menu, self.menu_rect)
        surface.blit(self.theme, self.theme_rect)

        color = (228, 234, 221)
        rect = (WIDTH, 0, TRUEWIDTH - WIDTH, HEIGHT)
        pygame.draw.rect(surface, color, rect)
        # color = (0,0,0)
        # rect = (WIDTH, 0, 5, HEIGHT)
        # pygame.draw.rect(surface, color, rect)