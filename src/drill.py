import datetime

class Drill:

    def __init__(self, sequence, mode, ease, interval, due_date, color="white", relearn_step=0):
        """
        Due date is a datetime.date object

        Interval of 0 indicates the drill is in the relearn mode
        """
        # List of the moves to complete
        self.sequence = sequence
        self.mode = mode
        self.ease = ease
        self.interval = interval
        self.due_date = due_date
        self.color = color
        self.relearn_step = relearn_step




    

    