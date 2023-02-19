import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move
from title import Title

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()
        self.title = Title()

    def mainloop(self):

        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board
        title = self.title

        # Set title screen
        mode = TITLE_SCREEN
        
        while True: 
            if mode == TITLE_SCREEN:
                # show methods
                title.show_bg(screen)
                


                for event in pygame.event.get():
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mode = title.get_collision(event.pos)

                    # Quit the application
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.update()

            if mode == CUSTOM:
                # Show methods
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.show_hover(screen)

                if dragger.dragging: 
                    dragger.update_blit(screen)

                for event in pygame.event.get():

                    # Click event
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse(event.pos)

                        clicked_row = dragger.mouseY // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE

                        # If there is a piece in the clicked square
                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece

                            # valid color
                            if piece.color == game.next_player:
                                board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)
                                # show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)
                    
                    # Mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQSIZE
                        motion_col = event.pos[0] // SQSIZE

                        game.set_hover(motion_row, motion_col)

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            # Show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            game.show_hover(screen)
                            dragger.update_blit(screen)
                    
                    # Click release
                    elif event.type == pygame.MOUSEBUTTONUP:

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                            released_row = dragger.mouseY // SQSIZE
                            released_col = dragger.mouseX // SQSIZE

                            # create possible move
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            # if valid move
                            if board.valid_move(dragger.piece, move):
                                # normal capture
                                captured = board.squares[released_row][released_col].has_piece()


                                board.move(dragger.piece, move)

                                board.set_true_en_passant(dragger.piece)
                                # sounds
                                game.play_sound(captured)
                                # show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)

                                game.next_turn()


                        dragger.undrag_piece()

                    # key press
                    elif event.type == pygame.KEYDOWN:
                        # change the theme
                        if event.key == pygame.K_t:
                            game.change_theme()

                        if event.key == pygame.K_r or event.key == pygame.K_m:
                            game.reset()
                            game = self.game
                            dragger = self.game.dragger
                            board = self.game.board
                            if event.key == pygame.K_m:
                                mode = TITLE_SCREEN

                    
                    # Quit the application
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                
                
                
                pygame.display.update()



main = Main()
main.mainloop()

