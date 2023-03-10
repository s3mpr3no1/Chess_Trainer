from game import Game
from const import * 
import pygame
import datetime
from scheduler import Scheduler


class Study(Game):

    def __init__(self):
        super().__init__()
        self.show_anki_choices = False
        self.wrong_move = False

        self.msg_color = self.config.study_neutral

        self.show_answer_text = self.config.study_button_font.render("Show Answer", False, (0, 0, 0))
        self.show_answer_rect = self.show_answer_text.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)), HEIGHT - 50))
        self.show_answer_button_color = (220, 220, 220)
        self.show_answer_button_hover_color = (180, 180, 180)
        self.show_answer_button_rect = pygame.Rect(WIDTH + 140, HEIGHT - 60, 120, 25)

        self.anki_again_text = self.config.study_button_font.render("Again", False, (0, 0, 0))
        self.anki_hard_text = self.config.study_button_font.render("Hard", False, (0, 0, 0))
        self.anki_good_text = self.config.study_button_font.render("Good", False, (0, 0, 0))
        self.anki_easy_text = self.config.study_button_font.render("Easy", False, (0, 0, 0))

        self.anki_again_rect = self.anki_again_text.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)), 300))
        self.anki_hard_rect = self.anki_hard_text.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)), 400))
        self.anki_good_rect = self.anki_good_text.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)), 500))
        self.anki_easy_rect = self.anki_easy_text.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)), 600))

        self.anki_button_color = (220, 220, 220)
        # self.anki_button_hover_color = (150, 150, 150)
        self.anki_button_hover_color = self.config.theme_blue

        self.anki_again_button_rect = pygame.Rect(WIDTH + 140, 290, 120, 25)
        self.anki_hard_button_rect = pygame.Rect(WIDTH + 140, 390, 120, 25)
        self.anki_good_button_rect = pygame.Rect(WIDTH + 140, 490, 120, 25)
        self.anki_easy_button_rect = pygame.Rect(WIDTH + 140, 590, 120, 25)

        self.again_interval_text = self.config.study_button_font.render("1m", False, self.config.theme_blue)
        self.again_interval_rect = self.again_interval_text.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)) + 100, 300))

        self.undo_text = self.config.help_item.render("<", False, (255, 0, 0))
        self.undo_rect = self.undo_text.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)) - 150, 50))

        self.undo_button_color = self.config.theme_hover
        self.undo_button_rect = pygame.Rect((WIDTH + ((TRUEWIDTH - WIDTH) / 2)) - 175, 25, 50, 50)
        
        
    def load_drills(self):
        # Initialize the scheduler
        self.scheduler = Scheduler()
        # Load the drills
        self.scheduler.load_drills(DRILLFILE)
        # Parse out the drills due today
        self.scheduler.get_due_today()
        # At this point, scheduler.due_today and due_later contain the drills in each respective category
        # print(self.scheduler.due_today)
        #print(self.scheduler.due_today[0])

    def show_bg(self, surface, flipped=False):
        super().show_bg(surface, flipped)
        mouse_pos = pygame.mouse.get_pos()

        self.study_msg = self.config.help_item.render("Study", False, self.msg_color)
        self.study_msg_rect = self.study_msg.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)), 50))
        surface.blit(self.study_msg, self.study_msg_rect)

        show_color = self.show_answer_button_color if not self.show_answer_button_rect.collidepoint(mouse_pos) else self.anki_button_hover_color

        pygame.draw.rect(surface, show_color, self.show_answer_button_rect)
        surface.blit(self.show_answer_text, self.show_answer_rect)

        self.new_left_msg = self.config.study_button_font.render(str(self.scheduler.new_left), False, self.config.theme_blue)
        self.relearn_left_msg = self.config.study_button_font.render(str(self.scheduler.relearn_left), False, (255, 0, 0))
        self.review_left_msg = self.config.study_button_font.render(str(self.scheduler.review_left), False, (0, 255, 0))


        self.new_left_rect = self.new_left_msg.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)) - 100, HEIGHT - 100))
        self.relearn_left_rect = self.relearn_left_msg.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)), HEIGHT - 100))
        self.review_left_rect = self.review_left_msg.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)) + 100, HEIGHT - 100))

        surface.blit(self.new_left_msg, self.new_left_rect)
        surface.blit(self.relearn_left_msg, self.relearn_left_rect)
        surface.blit(self.review_left_msg, self.review_left_rect)

        

        # If we're in the endgame now
        
        if self.show_anki_choices:
            

            again_color = self.anki_button_color if not self.anki_again_button_rect.collidepoint(mouse_pos) else self.anki_button_hover_color
            hard_color = self.anki_button_color if not self.anki_hard_button_rect.collidepoint(mouse_pos) else self.anki_button_hover_color
            good_color = self.anki_button_color if not self.anki_good_button_rect.collidepoint(mouse_pos) else self.anki_button_hover_color
            easy_color = self.anki_button_color if not self.anki_easy_button_rect.collidepoint(mouse_pos) else self.anki_button_hover_color

            pygame.draw.rect(surface, again_color, self.anki_again_button_rect)
            pygame.draw.rect(surface, hard_color, self.anki_hard_button_rect)
            pygame.draw.rect(surface, good_color, self.anki_good_button_rect)
            pygame.draw.rect(surface, easy_color, self.anki_easy_button_rect)

            surface.blit(self.anki_again_text, self.anki_again_rect)
            surface.blit(self.anki_hard_text, self.anki_hard_rect)
            surface.blit(self.anki_good_text, self.anki_good_rect)
            surface.blit(self.anki_easy_text, self.anki_easy_rect)

            surface.blit(self.again_interval_text, self.again_interval_rect)

            self.hard_interval_text = self.config.study_button_font.render(self.scheduler.hard_interval, False, self.config.theme_blue)
            self.hard_interval_rect = self.hard_interval_text.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)) + 100, 400))

            self.easy_interval_text = self.config.study_button_font.render(self.scheduler.easy_interval, False, self.config.theme_blue)
            self.easy_interval_rect = self.easy_interval_text.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)) + 100, 600))

            self.good_interval_text = self.config.study_button_font.render(self.scheduler.good_interval, False, self.config.theme_blue)
            self.good_interval_rect = self.good_interval_text.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)) + 100, 500))

            surface.blit(self.hard_interval_text, self.hard_interval_rect)
            surface.blit(self.easy_interval_text, self.easy_interval_rect)
            surface.blit(self.good_interval_text, self.good_interval_rect)

        if self.wrong_move:
            if self.undo_button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(surface, self.config.theme_red, self.undo_button_rect, border_radius=10)
            surface.blit(self.undo_text, self.undo_rect)



            #again_interval_text = self.config.study_button_font.render(self.scheduler.due_today[0]., False, (225, 225, 225))