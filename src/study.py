from game import Game
from const import * 
import pygame
import datetime
from scheduler import Scheduler


class Study(Game):

    def __init__(self):
        super().__init__()

       
        self.study_msg = self.config.help_item.render("Study", False, (255, 255, 255))
        self.study_msg_rect = self.study_msg.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)), 50))

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

        surface.blit(self.study_msg, self.study_msg_rect)