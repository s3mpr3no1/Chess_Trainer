import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square

class Game:

    def __init__(self):
        self.next_player = "white"
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    # Show methods 

    def show_bg(self, surface, flipped=False):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

                # row coordinates 
                if col == 0:
                    # color 
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    
                    # label
                    if not flipped:
                        lbl = self.config.font.render(str(ROWS-row), 1, color)
                    else: 
                        lbl = self.config.font.render(str(row + 1), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    # blit 
                    surface.blit(lbl, lbl_pos)
                # column coordinates
                if row == 7:
                    # color 
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # label 
                    lbl = self.config.font.render(Square.get_alphacol(col, flipped), 1, color)
                    
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    surface.blit(lbl, lbl_pos)

    def show_pieces(self, surface, flipped=False):
        
        for row in range(ROWS):
            for col in range(COLS):
                # Piece ? 
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    # All pieces except for dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        if not flipped:
                            img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        # flipped
                        else:
                            img_center = (7 - col) * SQSIZE + SQSIZE // 2, (7 - row) * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface, flipped=False):
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # Loop all valid moves
            for move in piece.moves:
                fr = move.final.row if not flipped else (7 - move.final.row)
                fc = move.final.col if not flipped else (7 - move.final.col)
                # color 
                color = theme.moves.light if (fr + fc) % 2 == 0 else theme.moves.dark
                # rect
                #rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                center = (fc * SQSIZE + (SQSIZE//2), fr * SQSIZE + (SQSIZE//2))
                # blit
                #pygame.draw.rect(surface, color, rect)
                if not self.board.squares[move.final.row][move.final.col].has_piece():
                    pygame.draw.circle(surface, color, center, 15.0)
                else:
                    pygame.draw.circle(surface, color, center, 50, 5)

    def show_last_move(self, surface, flipped=False):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial 
            final = self.board.last_move.final 
            for pos in [initial, final]:
                r = pos.row if not flipped else (7 - pos.row)
                c = pos.col if not flipped else (7 - pos.col)
                # color 
                color = theme.trace.light if (r + c) % 2 == 0 else theme.trace.dark
                # rect
                rect = (c * SQSIZE, r * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)


    # other methods
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        if row < 8 and col < 8:
            self.hovered_sqr = self.board.squares[row][col]
        else:
            return

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, capture=False):
        if capture:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()
