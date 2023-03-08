import pygame
from const import * 
from config import Config

class Title:
    
    def __init__(self):
        self.config = Config()
                
        # self.bg_surf = pygame.image.load('assets/graphics/board_bg.png').convert_alpha()
        # self.bg_surf = pygame.transform.scale(self.bg_surf, (WIDTH, HEIGHT))
        self.bg_color = (37, 34, 44)
        self.bg_rect = (0, 0, TRUEWIDTH, HEIGHT)
        self.option_color = (30, 174, 228)
        
        self.hover_color = (14, 46, 68)

        self.dragonfly_surf = pygame.image.load('assets/graphics/dragonfly.png').convert_alpha()
        # self.dragonfly_surf = pygame.transform.scale(self.dragonfly_surf, (250, 250))
        self.dragonfly_rect = self.dragonfly_surf.get_rect(center = (TRUEWIDTH // 2, (HEIGHT // 2) + 87))

        # self.dragonfly_surf.set_alpha(100)

        # self.study_hover_surf = pygame.image.load('assets/graphics/hover.png').convert_alpha()
        # self.study_hover_rect = self.study_hover_surf.get_rect(topleft = (30, 30))
        

        # self.title_message = self.config.title_font.render("Chess Trainer", False, (0, 0, 0))
        # self.title_message_rect = self.title_message.get_rect(center = ((WIDTH // 2), (HEIGHT // 8)))

        self.study_message = self.config.menu_item_font.render("Study", False, self.option_color)
        # self.study_message = pygame.image.load('assets/graphics/study.png').convert_alpha()
        # self.study_message = pygame.transform.scale(self.study_message, (400, 300))
        self.study_message_rect = self.study_message.get_rect(center = ((TRUEWIDTH // 4), (HEIGHT // 4)))

        # self.study_message_hover = self.config.menu_item_font_hover.render("Study", False, self.option_color)
        # self.study_message_rect_hover = self.study_message_hover.get_rect(center = ((TRUEWIDTH // 4), (HEIGHT // 4)))

        self.add_message = self.config.menu_item_font.render("Add  Drills", False, self.option_color)
        self.add_message_rect = self.add_message.get_rect(center = (3 * (TRUEWIDTH // 4), (HEIGHT // 4)))

        # self.add_message_hover = self.config.menu_item_font_hover.render("Add Drills", False, self.option_color)
        # self.add_message_rect_hover = self.add_message_hover.get_rect(center = (3 * (TRUEWIDTH // 4), (HEIGHT // 4)))

        self.custom_message = self.config.menu_item_font.render("Custom", False, self.option_color)
        self.custom_message_rect = self.custom_message.get_rect(center = ((TRUEWIDTH // 4), 3 * (HEIGHT // 4)))

        # self.custom_message_hover = self.config.menu_item_font_hover.render("Custom", False, self.option_color)
        # self.custom_message_rect_hover = self.custom_message_hover.get_rect(center = ((TRUEWIDTH // 4), 3 * (HEIGHT // 4)))

        self.help_message = self.config.menu_item_font.render("Help", False, self.option_color)
        self.help_message_rect = self.help_message.get_rect(center = (3 * (TRUEWIDTH // 4), 3 * (HEIGHT // 4)))

        # self.help_message_hover = self.config.menu_item_font_hover.render("Help", False, self.option_color)
        # self.help_message_rect_hover = self.help_message_hover.get_rect(center = (3 * (TRUEWIDTH // 4), 3 * (HEIGHT // 4)))

        ###################

        self.study_hover_rect = pygame.Rect(30, 30, (TRUEWIDTH // 2) - 60, (HEIGHT // 2) - 60)
        self.add_hover_rect = pygame.Rect((TRUEWIDTH // 2) + 30, 30, (TRUEWIDTH // 2) - 60, (HEIGHT // 2) - 60)
        self.custom_hover_rect = pygame.Rect(30, (HEIGHT // 2) + 30, (TRUEWIDTH // 2) - 60, (HEIGHT // 2) - 60)
        self.help_hover_rect = pygame.Rect((TRUEWIDTH // 2) + 30, (HEIGHT // 2) + 30, (TRUEWIDTH // 2) - 60, (HEIGHT // 2) - 60)



        

    def show_bg(self, surface):

        mouse_pos = pygame.mouse.get_pos()
        # surface.blit(self.bg_surf, (0,0))
        pygame.draw.rect(surface, self.bg_color, self.bg_rect)
        
        if self.study_hover_rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.study_hover_rect, border_radius=50)
        elif self.add_hover_rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.add_hover_rect, border_radius=50)
        elif self.custom_hover_rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.custom_hover_rect, border_radius=50)
        elif self.help_hover_rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.help_hover_rect, border_radius=50)
        # surface.blit(self.study_hover_surf, self.study_hover_rect)
        surface.blit(self.dragonfly_surf, self.dragonfly_rect)

        mouse_pos = pygame.mouse.get_pos()
        #print(mouse_pos)
        surface.blit(self.study_message, self.study_message_rect)
        surface.blit(self.add_message, self.add_message_rect)
        surface.blit(self.custom_message, self.custom_message_rect)
        surface.blit(self.help_message, self.help_message_rect)
        
        # # surface.blit(self.title_message, self.title_message_rect)
        # if self.study_message_rect.collidepoint(mouse_pos):
        #     surface.blit(self.study_message_hover, self.study_message_rect_hover)
        #     surface.blit(self.add_message, self.add_message_rect)
        #     surface.blit(self.custom_message, self.custom_message_rect)
        #     surface.blit(self.help_message, self.help_message_rect)

        # elif self.add_message_rect.collidepoint(mouse_pos):
        #     surface.blit(self.study_message, self.study_message_rect)
        #     surface.blit(self.add_message_hover, self.add_message_rect_hover)
        #     surface.blit(self.custom_message, self.custom_message_rect)
        #     surface.blit(self.help_message, self.help_message_rect)

        # elif self.custom_message_rect.collidepoint(mouse_pos):
        #     surface.blit(self.study_message, self.study_message_rect)
        #     surface.blit(self.add_message, self.add_message_rect)
        #     surface.blit(self.custom_message_hover, self.custom_message_rect_hover)
        #     surface.blit(self.help_message, self.help_message_rect)

        # elif self.help_message_rect.collidepoint(mouse_pos):
        #     surface.blit(self.study_message, self.study_message_rect)
        #     surface.blit(self.add_message, self.add_message_rect)
        #     surface.blit(self.custom_message, self.custom_message_rect)
        #     surface.blit(self.help_message_hover, self.help_message_rect_hover)
        
        # else: 
        #     surface.blit(self.study_message, self.study_message_rect)
        #     surface.blit(self.add_message, self.add_message_rect)
        #     surface.blit(self.custom_message, self.custom_message_rect)
        #     surface.blit(self.help_message, self.help_message_rect)

        # color = (228, 234, 221)
        # rect = (WIDTH, 0, TRUEWIDTH - WIDTH, HEIGHT)
        # pygame.draw.rect(surface, color, rect)
        # color = (0,0,0)
        # rect = (WIDTH, 0, 5, HEIGHT)
        # pygame.draw.rect(surface, color, rect)
        
    
    def get_collision(self, pos):
        """
        These four codes correspond to the different possible modes
        """
        if self.study_hover_rect.collidepoint(pos):
            return STUDY
        elif self.add_hover_rect.collidepoint(pos):
            return ADD_DRILL
        elif self.custom_hover_rect.collidepoint(pos):
            return CUSTOM
        elif self.help_hover_rect.collidepoint(pos):
            return HELP
        else:
            return TITLE_SCREEN
        

    def show_startup(self, surface):
        self.study_message.set_alpha(0)
        self.add_message.set_alpha(0)
        self.custom_message.set_alpha(0)
        self.help_message.set_alpha(0)


        alpha_counter = 0
        for x in range(255 * 6):
            if x % 6 == 0 and alpha_counter < 256:
                self.dragonfly_surf.set_alpha(alpha_counter)
                alpha_counter += 1

            pygame.draw.rect(surface, self.bg_color, self.bg_rect)
            surface.blit(self.dragonfly_surf, self.dragonfly_rect)
            pygame.display.update()

        study_counter = 0
        add_counter = 0
        custom_counter = 0
        help_counter = 0

        for x in range(255 * 8):
            if x % 2 == 0 and study_counter < 256:
                self.study_message.set_alpha(study_counter)
                study_counter += 1
            elif x % 2 == 0 and add_counter < 256:
                self.add_message.set_alpha(add_counter)
                add_counter += 1
            elif x % 2 == 0 and custom_counter < 256:
                self.custom_message.set_alpha(custom_counter)
                custom_counter += 1
            elif x % 2 == 0 and help_counter < 256:
                self.help_message.set_alpha(help_counter)
                help_counter += 1
                
                
                
                
                

            # bg
            pygame.draw.rect(surface, self.bg_color, self.bg_rect)

            # dragonfly
            surface.blit(self.dragonfly_surf, self.dragonfly_rect)

            surface.blit(self.study_message, self.study_message_rect)
            surface.blit(self.add_message, self.add_message_rect)
            surface.blit(self.custom_message, self.custom_message_rect)
            surface.blit(self.help_message, self.help_message_rect)
            pygame.display.update()


        
    
    