import datetime

class Drill:

    def __init__(self, sequence, mode, ease, interval, due_date, color="white"):
        """
        Due date is a datetime.date object
        """
        # List of the moves to complete
        self.sequence = sequence
        self.mode = mode
        self.ease = ease
        self.interval = interval
        self.due_date = due_date
        self.color = color




    

    