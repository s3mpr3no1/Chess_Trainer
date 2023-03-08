import pygame
from const import * 
from config import Config

class DrillComplete:
    
    def __init__(self):
        self.config = Config()

        # self.bg_surf = pygame.image.load('assets/graphics/board_bg.png').convert_alpha()
        # self.bg_surf = pygame.transform.scale(self.bg_surf, (WIDTH, HEIGHT))

        self.bg_rect = (0, 0, TRUEWIDTH, HEIGHT)

        self.msg = self.config.help_item.render("Drills Complete", False, self.config.theme_blue)
        self.msg_rect = self.msg.get_rect(center = (TRUEWIDTH // 2, HEIGHT // 2))

    def show_bg(self, surface):
        pygame.draw.rect(surface, self.config.theme_bg, self.bg_rect)
        # surface.blit(self.bg_surf, (0,0))
        surface.blit(self.msg, self.msg_rect)
        # color = (228, 234, 221)
        # rect = (WIDTH, 0, TRUEWIDTH - WIDTH, HEIGHT)
        # pygame.draw.rect(surface, color, rect)