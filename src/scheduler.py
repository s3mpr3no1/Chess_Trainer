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

        self.hard_interval = 0
        self.good_interval = 0
        self.easy_interval = 0

        self.new_left = 0
        self.relearn_left = 0
        self.review_left = 0

    def load_new_drills(self):
        """
        Takes new drills from the new drill file and adds 20 of them to the new 
        """
        new_drills = []
        todays_new_drills = []
        with open(NEW_DRILLFILE, 'a') as f:
            pass
        with open(NEW_DRILLFILE, 'r') as f:
            new_drills = f.readlines()

        new_drills = [self.get_drill_from_deck_string(line) for line in new_drills]

        #At this point the due date is a datetime object

        if len(new_drills) > NEW_DRILLS_PER_DAY:
            todays_new_drills = new_drills[:NEW_DRILLS_PER_DAY]
            drills_to_rewrite = new_drills[NEW_DRILLS_PER_DAY:]
            with open(NEW_DRILLFILE, "w") as f:
                for d in drills_to_rewrite:
                    f.write(str(d))
        else:
            todays_new_drills = new_drills
            with open(NEW_DRILLFILE, "w") as f:
                pass

        for d in todays_new_drills:
            self.due_today.append(d)

        
        

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
        self.load_new_drills()

        self.update_counts()
        self.calc_intervals()


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
        
        self.update_counts()
        self.calc_intervals()

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

        self.update_counts()
        self.calc_intervals()

    def anki_again(self):
        if self.due_today[0].mode == NEW:
            self.due_today[0].mode = LEARN_RELEARN
            self.pop_to_end()
        elif self.due_today[0].mode == LEARN_RELEARN:
            self.due_today[0].relearn_step = 0
            self.pop_to_end()
        elif self.due_today[0].mode == REVIEW:
            # Turn the card back into a learn/relearn
            self.due_today[0].interval = 1
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
            self.due_today[0].due_date = datetime.datetime.fromtimestamp(int(datetime.datetime.now().timestamp()) + self.due_today[0].interval * DAY_SECONDS)
            self.pop_to_later()

    def anki_good(self):
        if self.due_today[0].mode == NEW:
            self.due_today[0].mode = LEARN_RELEARN
            self.due_today[0].relearn_step += 1
            self.pop_to_end()
        elif self.due_today[0].mode == LEARN_RELEARN:
            # If the card does not graduate
            if self.due_today[0].relearn_step < 1:
                self.due_today[0].relearn_step += 1
                self.pop_to_end()
            # If the card graduates
            else:
                self.due_today[0].mode = REVIEW
                self.due_today[0].relearn_step = 0
                self.due_today[0].interval = 1
                self.due_today[0].due_date = datetime.datetime.fromtimestamp(int(datetime.datetime.now().timestamp()) + self.due_today[0].interval * DAY_SECONDS)
                self.pop_to_later()
        elif self.due_today[0].mode == REVIEW:
            self.due_today[0].interval *= self.due_today[0].ease
            self.due_today[0].due_date = datetime.datetime.fromtimestamp(int(datetime.datetime.now().timestamp()) + self.due_today[0].interval * DAY_SECONDS)
            self.pop_to_later()

    def anki_easy(self):
        # print(self.due_today[1].color)
        if self.due_today[0].mode == NEW or self.due_today[0].mode == LEARN_RELEARN:
            self.due_today[0].mode = REVIEW
            self.due_today[0].ease *= 1.15
            self.due_today[0].interval *= self.due_today[0].ease
            self.due_today[0].due_date = datetime.datetime.fromtimestamp(int(datetime.datetime.now().timestamp()) + self.due_today[0].interval * DAY_SECONDS)
            self.pop_to_later()
            # print(self.due_today[0].color)
        elif self.due_today[0].mode == REVIEW:
            self.due_today[0].ease *= 1.15
            self.due_today[0].interval *= self.due_today[0].ease
            self.due_today[0].due_date = datetime.datetime.fromtimestamp(int(datetime.datetime.now().timestamp()) + self.due_today[0].interval * DAY_SECONDS)
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
        mode = int(sections[3])
        color = sections[4]
        # POSIX time stamp
        due_date = int(sections[5])
        due_date = datetime.datetime.fromtimestamp(due_date)
        # if interval == 1:
        #     mode = NEW
        # else:
        #     mode = REVIEW
        return Drill(sequence, mode, ease, interval, due_date, color)
    

    def write_to_file(self):
        if len(self.due_later) == len(self.due_today) == 0:
            return
        with open(DRILLFILE, 'w') as f:
            if len(self.due_later) > 0:
                for d in self.due_later:
                    f.write(str(d))
            
            if len(self.due_today) > 0:
                for d in self.due_today:
                    if d.mode != NEW:
                        f.write(str(d))
        with open(NEW_DRILLFILE, 'a') as f:
            if len(self.due_today) > 0:
                for d in self.due_today:
                    f.write(str(d))

    def calc_intervals(self):
        if len(self.due_today) == 0:
            return
        
        if self.due_today[0].mode == NEW:
            self.hard_interval = "1m"
            # print(self.int_to_duration(self.due_today[0].interval * (self.due_today[0].ease * 1.15)))
            self.easy_interval = self.int_to_duration(self.due_today[0].interval * (self.due_today[0].ease * 1.15))
            self.good_interval = "10m"
        elif self.due_today[0].mode == LEARN_RELEARN:
            # print("here")
            self.hard_interval = "1m"
            self.easy_interval = self.int_to_duration(self.due_today[0].interval * (self.due_today[0].ease * 1.15))
            self.good_interval = "10m" if self.due_today[0].relearn_step == 0 else "1d"
        elif self.due_today[0].mode == REVIEW:
            self.hard_interval = self.int_to_duration(self.due_today[0].interval * HARD_INTERVAL)
            self.easy_interval = self.int_to_duration(self.due_today[0].interval * (self.due_today[0].ease * 1.15))
            self.good_interval = self.int_to_duration(self.due_today[0].interval * self.due_today[0].ease)

        # print(self.good_interval)
        # print(self.easy_interval)

    def int_to_duration(self, days):
        duration = ""
        if days < 30:
            duration = duration + str(int(days)) + "d"
        elif 30 < days < 365:
            duration = duration + str(round(float(days / 30), 1)) + "mo"
        else:
            duration = duration + str(round(float(days / 365), 1)) + "y"
        return duration
    

    def update_counts(self):
        self.new_left = 0
        self.relearn_left = 0
        self.review_left = 0
        for d in self.due_today:
            if d.mode == NEW:
                self.new_left += 1
            elif d.mode == LEARN_RELEARN:
                self.relearn_left += 1
            elif d.mode == REVIEW:
                self.review_left += 1
        
    

