import pygame
from const import * 
from config import Config

class Help:

    def __init__(self):
        self.config = Config()
                
        self.bg_color = (37, 34, 44)
        self.bg_rect = (0, 0, TRUEWIDTH, HEIGHT)

        # self.bg_surf = pygame.image.load('assets/graphics/board_bg.png').convert_alpha()
        # self.bg_surf = pygame.transform.scale(self.bg_surf, (WIDTH, HEIGHT))

        self.reset = self.config.help_item.render("r: Reset board", False, self.config.theme_blue)
        self.reset_rect = self.reset.get_rect(center = (TRUEWIDTH // 2, 100))

        self.flip = self.config.help_item.render("f: Flip board", False, self.config.theme_blue)
        self.flip_rect = self.flip.get_rect(center = (TRUEWIDTH // 2, 200))

        self.menu = self.config.help_item.render("m: Return to main menu", False, self.config.theme_blue)
        self.menu_rect = self.menu.get_rect(center = (TRUEWIDTH // 2, 300))

        self.theme = self.config.help_item.render("t: Change the theme", False, self.config.theme_blue)
        self.theme_rect = self.theme.get_rect(center = (TRUEWIDTH // 2, 400))

    def show_bg(self, surface):
        # surface.blit(self.bg_surf, (0,0))
        pygame.draw.rect(surface, self.bg_color, self.bg_rect)
        surface.blit(self.reset, self.reset_rect)
        surface.blit(self.flip, self.flip_rect)
        surface.blit(self.menu, self.menu_rect)
        surface.blit(self.theme, self.theme_rect)

        # color = (228, 234, 221)
        # rect = (WIDTH, 0, TRUEWIDTH - WIDTH, HEIGHT)
        # pygame.draw.rect(surface, color, rect)
        # color = (0,0,0)
        # rect = (WIDTH, 0, 5, HEIGHT)
        # pygame.draw.rect(surface, color, rect)