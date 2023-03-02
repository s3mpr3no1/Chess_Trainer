
class Square:

    ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = self.ALPHACOLS[col]

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col    

    def has_piece(self):
        return self.piece != None

    def isempty(self):
        return not self.has_piece()

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def isempty_or_enemy(self, color):
        return self.isempty() or self.has_enemy_piece(color)

    # You can call and use a static method without creating a Square object
    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True

    @staticmethod
    def get_alphacol(col, flipped):
        ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
        FLIPPED = {0: 'h', 1: 'g', 2: 'f', 3:'e', 4:'d', 5:'c', 6:'b', 7:'a'}
        return ALPHACOLS[col] if not flipped else FLIPPED[col]
    
    @staticmethod
    def get_col_from_alpha(alpha, flipped=False):
        ALPHACOLS = {'a': 0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        FLIPPED = {'a':7, 'b':6, 'c':5, 'd':4, 'e':3, 'f':2, 'g':1, 'h':0}
        return ALPHACOLS[alpha] if not flipped else FLIPPED[alpha]
