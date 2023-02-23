from drill import Drill 
from const import * 
import datetime

class Scheduler:
    """
    This class will be called each time the "study" option is chosen from the main class.
    It needs to take in a deck file and then interpret and manipulate it properly
    """

    def __init__(self):
        self.drills = []

        # Once loaded, self.drills is partitioned into these two lists
        self.due_today = []
        self.due_later = []

    def load_drills(self, deck_file_name):
        """
        This is separate from the __init__ method so that users can alternate between the drill add and drill practice modes

        This method loads all drills and orders them. Logic for choosing the drills due today is contained in a separate method
        """
        self.drills = []
        with open (deck_file_name, 'a') as f:
            pass
        with open (deck_file_name, 'r') as f:
            self.drills = f.readlines()
        
        self.drills = [self.get_drill_from_deck_string(line) for line in self.drills]

        # Sort the drills in ascending order by timestamp. 
        # Drills earlier in the list are due sooner
        self.drills = sorted(self.drills, key = lambda x: x.due_date.timestamp())  

    def get_due_today(self):
        """
        This method takes self.drills and splits it into due today and not due today. The drills due later can be written to the log and the 
        rest will be appended at the end of the training sesssion. 
        """
        # Today's date
        tod = datetime.date.today()
        
        # End of the day expressed as a POSIX timestamp
        end_of_day = datetime.datetime(tod.year, tod.month, tod.day, 23, 59, 59).timestamp()

        cutoff = 0
        for drill in self.drills:
            if drill.due_date.timestamp() > end_of_day:
                break
            else: 
                cutoff += 1
        
        self.due_today = self.drills[:cutoff]
        self.due_later = self.drills[cutoff:]



    @staticmethod
    def get_drill_from_deck_string(deck_string):
        """
        Take a line from the deck file and turn it into a drill object
        """
        
        sections = deck_string.strip().split(":")
        sequence = sections[0].split(",")
        ease = float(sections[1])
        interval = int(sections[2])
        color = sections[3]
        # POSIX time stamp
        due_date = int(sections[4])
        due_date = datetime.datetime.fromtimestamp(due_date)
        if interval == 0:
            mode = NEW
        else:
            mode = REVIEW
        return Drill(sequence, mode, ease, interval, due_date, color)


