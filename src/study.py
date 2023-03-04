from game import Game
from const import * 
import pygame
import datetime
from scheduler import Scheduler


class Study(Game):

    def __init__(self):
        super().__init__()
        self.msg_color = self.config.study_neutral

        self.show_answer_text = self.config.study_button_font.render("Show Answer", False, (0, 0, 0))
        self.show_answer_rect = self.show_answer_text.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)), HEIGHT - 50))
        self.show_answer_button_color = (180, 180, 180)
        self.show_answer_button_rect = pygame.Rect(WIDTH + 140, HEIGHT - 60, 120, 25)

    def load_drills(self):
        # Initialize the scheduler
        self.scheduler = Scheduler()
        # Load the drills
        self.scheduler.load_drills(DRILLFILE)
        # Parse out the drills due today
        self.scheduler.get_due_today()
        # At this point, scheduler.due_today and due_later contain the drills in each respective category
        # print(self.scheduler.due_today)

    def show_bg(self, surface, flipped=False):
        super().show_bg(surface, flipped)

        self.study_msg = self.config.help_item.render("Study", False, self.msg_color)
        self.study_msg_rect = self.study_msg.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)), 50))
        surface.blit(self.study_msg, self.study_msg_rect)

        pygame.draw.rect(surface, self.show_answer_button_color, self.show_answer_button_rect)
        surface.blit(self.show_answer_text, self.show_answer_rect)