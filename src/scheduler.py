from drill import Drill 
from const import * 
import datetime

class Scheduler:
    """
    This class will be called each time the "study" option is chosen from the main class.
    It needs to take in a deck file and then interpret and manipulate it properly

    Functionality to add:

        - maintaining and updating a list of drills
    """

    def __init__(self, deck_file_name):
        drills = []
        with open (deck_file_name, 'a') as f:
            pass
        with open (deck_file_name, 'r') as f:
            drills = f.readlines()
        
        drills = [self.get_drill_from_deck_string(line) for line in drills]

    @staticmethod
    def get_drill_from_deck_string(deck_string):
        """
        Take a line from the deck file and turn it into a drill object
        """
        
        sections = deck_string.strip().split(":")
        sequence = sections[0].split(",")
        ease = float(sections[1])
        interval = int(sections[2])
        due_date = [int(x) for x in sections[3].split("-")]
        due_date = datetime.date(due_date[0], due_date[1], due_date[2])
        if interval == 0:
            mode = NEW
        else:
            mode = REVIEW
        return Drill(sequence, mode, ease, interval, due_date)


