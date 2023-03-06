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
        
        # This tracks which drill in self.due_today is active
        self.drill_index = 0

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


    def board_matches_drill(self, board):
        for i in range(len(board.moves)):
            if board.moves[i] != self.due_today[0].sequence[i]:
                return False
        return True

    def pop_to_end(self):
        """
        Moves the first element of the due today list to the end
        """
        if len(self.due_today) <= 1:
            return
        # print("Here")
        temp = self.due_today[0]
        self.due_today = self.due_today[1:]
        self.due_today.append(temp)

    def pop_to_later(self):
        """
        Moves the first drill in due today to due later
        """
        if len(self.due_today) == 1:
            temp = self.due_today[0]
            self.due_today = []
            self.due_later.append(temp)
        elif len(self.due_today) == 0:
            return
        else: 
            temp = self.due_today[0]
            self.due_today = self.due_today[1:]
            self.due_later.append(temp)

    def anki_again(self):
        if self.due_today[0].mode == NEW:
            self.due_today[0].mode = LEARN_RELEARN
            self.pop_to_end()
        elif self.due_today[0].mode == LEARN_RELEARN:
            self.due_today[0].relearn_step = 0
            self.pop_to_end()
        elif self.due_today[0].mode == REVIEW:
            # Turn the card back into a learn/relearn
            self.due_today[0].interval = 0
            self.due_today[0].ease *= 0.8
            self.due_today[0].relearn_step = 0
            self.due_today[0].mode = LEARN_RELEARN
            self.pop_to_end()
        # self.due_today[0].mode = LEARN_RELEARN

        # Move the drill to the end
        #self.pop_to_end()

    def anki_hard(self):
        if self.due_today[0].mode == NEW:
            self.due_today[0].mode = LEARN_RELEARN
            self.pop_to_end()
        elif self.due_today[0].mode == LEARN_RELEARN:
            self.pop_to_end()
        elif self.due_today[0].mode == REVIEW:
            self.due_today[0].ease *= 0.85
            self.due_today[0].interval = int(self.due_today[0].interval * HARD_INTERVAL)
            self.due_today[0].due_date = int(datetime.datetime.now().timestamp()) + self.due_today[0].interval * DAY_SECONDS
            self.pop_to_later()

    def anki_good(self):
        if self.due_today[0].mode == NEW:
            self.due_today[0].mode = LEARN_RELEARN
            self.due_today[0].relearn_step += 1
            self.pop_to_end()
        elif self.due_today[0].mode == LEARN_RELEARN:
            # If the card does not graduate
            if self.due_today[0].relearn_step < 2:
                self.due_today[0].relearn_step += 1
                self.pop_to_end()
            # If the card graduates
            else:
                self.due_today[0].mode = REVIEW
                self.due_today[0].relearn_step = 0
                self.due_today[0].interval = 1
                self.due_today[0].due_date = int(datetime.datetime.now().timestamp()) + self.due_today[0].interval * DAY_SECONDS
                self.pop_to_later()
        elif self.due_today[0].mode == REVIEW:
            self.due_today[0].interval *= self.due_today[0].ease
            self.due_today[0].due_date = int(datetime.datetime.now().timestamp()) + self.due_today[0].interval * DAY_SECONDS
            self.pop_to_later()

    def anki_easy(self):
        # print(self.due_today[1].color)
        if self.due_today[0].mode == NEW or self.due_today[0].mode == LEARN_RELEARN:
            self.due_today[0].mode = REVIEW
            self.due_today[0].ease *= 1.15
            self.due_today[0].interval *= self.due_today[0].ease
            self.due_today[0].due_date = int(datetime.datetime.now().timestamp()) + self.due_today[0].interval * DAY_SECONDS
            self.pop_to_later()
            # print(self.due_today[0].color)
        elif self.due_today[0].mode == REVIEW:
            self.due_today[0].ease *= 1.15
            self.due_today[0].interval *= self.due_today[0].ease
            self.due_today[0].due_date = int(datetime.datetime.now().timestamp()) + self.due_today[0].interval * DAY_SECONDS
            self.pop_to_later()




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


