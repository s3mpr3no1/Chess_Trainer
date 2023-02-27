import os

class Piece:

    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        
        # For the AI
        value_sign = 1 if color == "white" else -1
        self.value = value * value_sign
        # List of valid moves
        self.moves = []
        self.moved = False


        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect


    def set_texture(self, size=80):
        self.texture = os.path.join(f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')


    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []


class Pawn(Piece):

    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        self.en_passant = False
        super().__init__("Pawn", color, 1.0)

    def __str__(self):
        return "P"


class Knight(Piece):

    def __init__(self, color):
        super().__init__("Knight", color, 3.0)

    def __str__(self):
        return "N"


class Bishop(Piece):

    def __init__(self, color):
        super().__init__("Bishop", color, 3.0)

    def __str__(self):
        return "B"


class Rook(Piece):

    def __init__(self, color):
        super().__init__("Rook", color, 5.0)  

    def __str__(self):
        return "R"  

class Queen(Piece):

    def __init__(self, color):
        super().__init__("Queen", color, 9.0)

    def __str__(self):
        return "Q"

class King(Piece):

    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__("King", color, 10000)

    def __str__(self):
        return "K"