from const import *
from square import Square
from piece import *
from move import Move
import copy
from sound import Sound
import os

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")
        self.moves = []

    def reset(self):
        self.__init__()

    
        

    def move(self, piece, move, testing = False, captured=False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.col].isempty()

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        self.moves.append(str(piece) + Square.get_alphacol(initial.col, False) + str(7 - (initial.row - 1)) + Square.get_alphacol(final.col, False) + str(7 - (final.row - 1)))

        """
        if not testing:
            if not captured:
                # Regular move
                if not self.giving_check(piece, move):
                    self.moves.append(str(piece) + Square.get_alphacol(initial.col, False) + Square.get_alphacol(final.col, False) + str(7 - (final.row - 1)))
                # Giving a check
                else: 
                    self.moves.append(str(piece) + Square.get_alphacol(initial.col, False) + Square.get_alphacol(final.col, False) + str(7 - (final.row - 1)) + "#")
                
            else:
                # Regular capture
                if not isinstance(piece, Pawn):
                    if not self.giving_check(piece, move):
                        self.moves.append(str(piece) + Square.get_alphacol(initial.col, False) + "x" + Square.get_alphacol(final.col, False) + str(7 - (final.row - 1)))
                    # Regular capture with check
                    else:
                        self.moves.append(str(piece) + Square.get_alphacol(initial.col, False) + "x" + Square.get_alphacol(final.col, False) + str(7 - (final.row - 1)) + "#")
                # Pawn capture
                else:
                    if not self.giving_check(piece, move):
                        self.moves.append(Square.get_alphacol(initial.col, False) + "x" + Square.get_alphacol(final.col, False) + str(7 - (final.row - 1)))
                    # pawn capture with check
                    else: 
                        self.moves.append(Square.get_alphacol(initial.col, False) + "x" + Square.get_alphacol(final.col, False) + str(7 - (final.row - 1)) + "#")
        """
        if isinstance(piece, Pawn):
            diff = final.col - initial.col 
            # en passant capture
            if diff != 0 and en_passant_empty:
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(os.path.join('assets/sounds/capture.mp3'))
                    sound.play()

            

            else:
                # promotion
                self.check_promotion(piece, final)

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col 
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1]) # we added this in the kingmoves method
                if diff < 0 and not testing:
                    self.moves = self.moves[:-2] 
                    self.moves.append("O-O-O")
                elif diff > 0 and not testing:
                    self.moves = self.moves[:-2] 
                    self.moves.append("O-O")

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move
        # if not testing: print(self.moves)

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2 # did the king move two squares? (if so we castled)
    
    def set_true_en_passant(self, piece):

        if not isinstance(piece, Pawn):
            return
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False     

        piece.en_passant = True

    def giving_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)
        temp_board.calc_moves(temp_piece, move.final.row, move.final.col, bool=False)
        for m in temp_piece.moves:
            if isinstance(m.final.piece, King):
                return True
        return False



    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)
        
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False

    def calc_moves(self, piece, row, col, bool=True):
        '''
            Calculate all the possible moves for a specific piece on a specific square
        '''

        def pawn_moves():
            # Steps
            steps = 1 if piece.moved else 2

            # vertical moves 
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # create initial and final move squares
                        # Then create a new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(initial, final)

                        # check potential enemy checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else: 
                            piece.add_move(move)
                    # We are blocked
                    else: 
                        break
                # Not in range
                else:
                    break
            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else: 
                            piece.add_move(move)

            # en passant moves
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            # left en passant
            if Square.in_range(col -1) and row == r:
                if self.squares[row][col-1].has_enemy_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial = Square(row, col)
                            final = Square(fr, col-1, p)
                            move = Move(initial, final)
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else: 
                                piece.add_move(move)

            # right en passant
            if Square.in_range(col +1) and row == r:
                if self.squares[row][col+1].has_enemy_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial = Square(row, col)
                            final = Square(fr, col+1, p)
                            move = Move(initial, final)
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else: 
                                piece.add_move(move)




        def knight_moves():
            # Maximum 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                # Check if the move is on the board
                if Square.in_range(possible_move_row, possible_move_col):
                    # Next we check if the square is empty
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares for new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece) 
                        # Move 
                        move = Move(initial, final)
                        # append new valid move
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            # else:
                            #     break
                        else: 
                            piece.add_move(move)

            
        def straightline_moves(incrs):
            #print("Straightline Move")
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create squares for possible new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # Create the possible new move
                        move = Move(initial, final)


                        # empty = continue looping
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # append new move
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else: 
                                piece.add_move(move)

                        # Has enemy piece
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # append new move
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else: 
                                piece.add_move(move)
                            break

                        # has team piece 
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break


                        

                    # Not in range
                    else:
                        break

                    # increment the increments
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr    

        def king_moves():
            adjs = [(row-1, col), (row-1, col+1), (row, col+1), (row+1, col+1), (row+1, col), (row+1, col-1), (row, col-1), (row-1, col-1)]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            # else: break
                        else: 
                            piece.add_move(move)

            # castling moves
            if not piece.moved:
                # queenside castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # check for empty squares 
                            if self.squares[row][c].has_piece():
                                break # castling not possible
                            if c == 3:
                                # adds the left rook to the king
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)
                                
                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                

                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        left_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else: 
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK)
                # kingside castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # check for empty squares 
                            if self.squares[row][c].has_piece():
                                break # castling not possible
                            if c == 6:
                                # adds the right rook to the king
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)
                                
                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        right_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else: 
                                    right_rook.add_move(moveR)
                                    piece.add_move(moveK)
                                

        if isinstance(piece, Pawn): pawn_moves()
        
        elif isinstance(piece, Knight): knight_moves()
        
        elif isinstance(piece, Bishop): 
            straightline_moves([(-1, 1), (-1, -1), (1, 1), (1, -1)])

        elif isinstance(piece, Rook): 
            straightline_moves([(-1, 0), (0, 1), (1, 0), (0, -1)])

        elif isinstance(piece, Queen): 
            straightline_moves([(-1, 1), (-1, -1), (1, 1), (1, -1), (-1, 0), (0, 1), (1, 0), (0, -1)])

        elif isinstance(piece, King): 
            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)

        # pawns
        for col in range(COLS): 
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queens
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # King
        self.squares[row_other][4] = Square(row_other, 4, King(color))
