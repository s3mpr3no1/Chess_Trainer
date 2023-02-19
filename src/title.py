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
        self.study_message_rect = self.study_message.get_rect(center = ((WIDTH // 2), 300))

        self.study_message_hover = self.config.menu_item_font_hover.render("Study", False, (0, 0, 0))
        self.study_message_rect_hover = self.study_message_hover.get_rect(center = ((WIDTH // 2), 300))

        self.add_message = self.config.menu_item_font.render("Add Drills", False, (0, 0, 0))
        self.add_message_rect = self.add_message.get_rect(center = ((WIDTH // 2), 450))

        self.add_message_hover = self.config.menu_item_font_hover.render("Add Drills", False, (0, 0, 0))
        self.add_message_rect_hover = self.add_message_hover.get_rect(center = ((WIDTH // 2), 450))

        self.custom_message = self.config.menu_item_font.render("Custom", False, (0, 0, 0))
        self.custom_message_rect = self.custom_message.get_rect(center = ((WIDTH // 2), 600))

        self.custom_message_hover = self.config.menu_item_font_hover.render("Custom", False, (0, 0, 0))
        self.custom_message_rect_hover = self.custom_message_hover.get_rect(center = ((WIDTH // 2), 600))

    def show_bg(self, surface):
        surface.blit(self.bg_surf, (0,0))

        mouse_pos = pygame.mouse.get_pos()
        #print(mouse_pos)
        
        surface.blit(self.title_message, self.title_message_rect)
        if self.study_message_rect.collidepoint(mouse_pos):
            surface.blit(self.study_message_hover, self.study_message_rect_hover)
            surface.blit(self.add_message, self.add_message_rect)
            surface.blit(self.custom_message, self.custom_message_rect)

        elif self.add_message_rect.collidepoint(mouse_pos):
            surface.blit(self.study_message, self.study_message_rect)
            surface.blit(self.add_message_hover, self.add_message_rect_hover)
            surface.blit(self.custom_message, self.custom_message_rect)

        elif self.custom_message_rect.collidepoint(mouse_pos):
            surface.blit(self.study_message, self.study_message_rect)
            surface.blit(self.add_message, self.add_message_rect)
            surface.blit(self.custom_message_hover, self.custom_message_rect_hover)

        else: 
            surface.blit(self.study_message, self.study_message_rect)
            surface.blit(self.add_message, self.add_message_rect)
            surface.blit(self.custom_message, self.custom_message_rect)
        
    
    def get_collision(self, pos):
        if self.study_message_rect.collidepoint(pos):
            return STUDY
        elif self.add_message_rect.collidepoint(pos):
            return ADD_DRILL
        elif self.custom_message_rect.collidepoint(pos):
            return CUSTOM
        else:
            return TITLE_SCREEN

        


        
        
