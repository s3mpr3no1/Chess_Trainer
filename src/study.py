from game import Game
from const import * 
import pygame
import datetime


class Study(Game):

    def __init__(self):
        super().__init__()

    def show_bg(self, surface, flipped=False):
        super().show_bg(surface, flipped)