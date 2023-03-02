
from square import Square

class Move:

    def __init__(self, initial, final):
        # Initial and final are squares
        self.initial = initial
        self.final = final 

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
    
    def __str__(self):
        return str(self.initial.row) + str(self.initial.col) + "-" + str(self.final.row) + str(self.final.col)

    
    @staticmethod
    def move_from_string(move_string, flipped=False):
        """
        The move string here is of the form <piece letter><initial><final>
        example: Pe7e5

        TODO: add flipped? 
        """
        # Parse the move string
        # piece_name = move_string[0]
        initial = move_string[1:3]
        final = move_string[3:5]

        initial_row = (7 - int(initial[1]) + 1)
        initial_col = Square.get_col_from_alpha(initial[0], flipped)

        final_row = (7 - int(final[1]) + 1)
        final_col = Square.get_col_from_alpha(final[0], flipped)

        initial_square = Square(initial_row, initial_col)
        final_square = Square(final_row, final_col)

        return Move(initial_square, final_square)





        