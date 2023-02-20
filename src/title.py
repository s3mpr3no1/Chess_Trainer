import pygame
from const import * 
from config import Config

class Title:
    
    def __init__(self):
        self.config = Config()
                
        self.bg_surf = pygame.image.load('assets/graphics/board_bg.png').convert_alpha()
        self.bg_surf = pygame.transform.scale(self.bg_surf, (WIDTH, HEIGHT))

        self.title_message = self.config.title_font.render("Chess Trainer", False, (0, 0, 0))
        self.title_message_rect = self.title_message.get_rect(center = ((WIDTH // 2), (HEIGHT // 8)))

        self.study_message = self.config.menu_item_font.render("Study", False, (0, 0, 0))
        self.study_message_rect = self.study_message.get_rect(center = ((WIDTH // 2), 275))

        self.study_message_hover = self.config.menu_item_font_hover.render("Study", False, (0, 0, 0))
        self.study_message_rect_hover = self.study_message_hover.get_rect(center = ((WIDTH // 2), 275))

        self.add_message = self.config.menu_item_font.render("Add Drills", False, (0, 0, 0))
        self.add_message_rect = self.add_message.get_rect(center = ((WIDTH // 2), 400))

        self.add_message_hover = self.config.menu_item_font_hover.render("Add Drills", False, (0, 0, 0))
        self.add_message_rect_hover = self.add_message_hover.get_rect(center = ((WIDTH // 2), 400))

        self.custom_message = self.config.menu_item_font.render("Custom", False, (0, 0, 0))
        self.custom_message_rect = self.custom_message.get_rect(center = ((WIDTH // 2), 525))

        self.custom_message_hover = self.config.menu_item_font_hover.render("Custom", False, (0, 0, 0))
        self.custom_message_rect_hover = self.custom_message_hover.get_rect(center = ((WIDTH // 2), 525))

        self.help_message = self.config.menu_item_font.render("Help", False, (0, 0, 0))
        self.help_message_rect = self.help_message.get_rect(center = ((WIDTH // 2), 650))

        self.help_message_hover = self.config.menu_item_font_hover.render("Help", False, (0, 0, 0))
        self.help_message_rect_hover = self.help_message_hover.get_rect(center = ((WIDTH // 2), 650))

    def show_bg(self, surface):
        surface.blit(self.bg_surf, (0,0))

        mouse_pos = pygame.mouse.get_pos()
        #print(mouse_pos)
        
        surface.blit(self.title_message, self.title_message_rect)
        if self.study_message_rect.collidepoint(mouse_pos):
            surface.blit(self.study_message_hover, self.study_message_rect_hover)
            surface.blit(self.add_message, self.add_message_rect)
            surface.blit(self.custom_message, self.custom_message_rect)
            surface.blit(self.help_message, self.help_message_rect)

        elif self.add_message_rect.collidepoint(mouse_pos):
            surface.blit(self.study_message, self.study_message_rect)
            surface.blit(self.add_message_hover, self.add_message_rect_hover)
            surface.blit(self.custom_message, self.custom_message_rect)
            surface.blit(self.help_message, self.help_message_rect)

        elif self.custom_message_rect.collidepoint(mouse_pos):
            surface.blit(self.study_message, self.study_message_rect)
            surface.blit(self.add_message, self.add_message_rect)
            surface.blit(self.custom_message_hover, self.custom_message_rect_hover)
            surface.blit(self.help_message, self.help_message_rect)

        elif self.help_message_rect.collidepoint(mouse_pos):
            surface.blit(self.study_message, self.study_message_rect)
            surface.blit(self.add_message, self.add_message_rect)
            surface.blit(self.custom_message, self.custom_message_rect)
            surface.blit(self.help_message_hover, self.help_message_rect_hover)
        
        else: 
            surface.blit(self.study_message, self.study_message_rect)
            surface.blit(self.add_message, self.add_message_rect)
            surface.blit(self.custom_message, self.custom_message_rect)
            surface.blit(self.help_message, self.help_message_rect)

        color = (255, 255, 255)
        rect = (WIDTH, 0, TRUEWIDTH - WIDTH, HEIGHT)
        pygame.draw.rect(surface, color, rect)
        color = (0,0,0)
        rect = (WIDTH, 0, 5, HEIGHT)
        pygame.draw.rect(surface, color, rect)
        
    
    def get_collision(self, pos):
        """
        These four codes correspond to the different possible modes
        """
        if self.study_message_rect.collidepoint(pos):
            return STUDY
        elif self.add_message_rect.collidepoint(pos):
            return ADD_DRILL
        elif self.custom_message_rect.collidepoint(pos):
            return CUSTOM
        elif self.help_message_rect.collidepoint(pos):
            return HELP
        else:
            return TITLE_SCREEN

        


        
        
