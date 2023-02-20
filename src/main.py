import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move
from title import Title
from help import Help
from add_drills import DrillAdder

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((TRUEWIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()
        self.title = Title()
        self.help = Help()
        self.drill_adder = DrillAdder()

    def mainloop(self):

        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board
        add_board = self.drill_adder.board
        add_dragger = self.drill_adder.dragger
        title = self.title
        help = self.help
        adder = self.drill_adder

        # Board flipping
        flipped = False

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

            elif mode == HELP:
                help.show_bg(screen)

                for event in pygame.event.get():

                    if event.type == pygame.KEYDOWN:
                        
                        if event.key == pygame.K_m:
                            mode = TITLE_SCREEN

                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.update()

            elif mode == ADD_DRILL:
                # Show methods
                adder.show_bg(screen, flipped)
                adder.show_last_move(screen, flipped)
                adder.show_moves(screen, flipped)
                adder.show_pieces(screen, flipped)
                adder.show_hover(screen)

                if add_dragger.dragging: 
                    add_dragger.update_blit(screen)

                for event in pygame.event.get():

                    # Click event
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        add_dragger.update_mouse(event.pos)
                        
                        if add_dragger.mouseX < WIDTH and add_dragger.mouseY < HEIGHT:
                            clicked_row = (add_dragger.mouseY // SQSIZE) if not flipped else (7 - (add_dragger.mouseY // SQSIZE))
                            clicked_col = (add_dragger.mouseX // SQSIZE) if not flipped else (7 - (add_dragger.mouseX // SQSIZE))

                            # If there is a piece in the clicked square
                            if add_board.squares[clicked_row][clicked_col].has_piece():
                                piece = add_board.squares[clicked_row][clicked_col].piece

                                # valid color
                                if piece.color == adder.next_player:
                                    add_board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                    add_dragger.save_initial(event.pos, flipped)
                                    add_dragger.drag_piece(piece)
                                    # show methods
                                    adder.show_bg(screen, flipped)
                                    adder.show_last_move(screen, flipped)
                                    adder.show_moves(screen, flipped)
                                    adder.show_pieces(screen, flipped)
                    
                    # Mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQSIZE
                        motion_col = event.pos[0] // SQSIZE

                        adder.set_hover(motion_row, motion_col)

                        if add_dragger.dragging:
                            add_dragger.update_mouse(event.pos)
                            # Show methods
                            adder.show_bg(screen, flipped)
                            adder.show_last_move(screen, flipped)
                            adder.show_moves(screen, flipped)
                            adder.show_pieces(screen, flipped)
                            adder.show_hover(screen)
                            add_dragger.update_blit(screen)
                    
                    # Click release
                    elif event.type == pygame.MOUSEBUTTONUP:

                        if add_dragger.dragging:
                            add_dragger.update_mouse(event.pos)

                            if add_dragger.mouseX < WIDTH and add_dragger.mouseY < HEIGHT:
                                released_row = (add_dragger.mouseY // SQSIZE) if not flipped else (7 - (add_dragger.mouseY // SQSIZE))
                                released_col = (add_dragger.mouseX // SQSIZE) if not flipped else (7 - (add_dragger.mouseX // SQSIZE))
                            else: 
                                released_row = add_dragger.initial_row
                                released_col = add_dragger.initial_col


                            # create possible move
                            initial = Square(add_dragger.initial_row, add_dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            # if valid move
                            if add_board.valid_move(add_dragger.piece, move):
                                # normal capture
                                captured = add_board.squares[released_row][released_col].has_piece()


                                add_board.move(add_dragger.piece, move)

                                add_board.set_true_en_passant(add_dragger.piece)
                                # sounds
                                adder.play_sound(captured)
                                # show methods
                                adder.show_bg(screen, flipped)
                                adder.show_last_move(screen, flipped)
                                adder.show_pieces(screen, flipped)

                                adder.next_turn()


                        add_dragger.undrag_piece()

                    # key press
                    elif event.type == pygame.KEYDOWN:
                        # change the theme
                        if event.key == pygame.K_t:
                            adder.change_theme()

                        # reset the board or reset and quit to menu
                        elif event.key == pygame.K_r or event.key == pygame.K_m:
                            adder.reset()
                            adder = self.drill_adder
                            add_dragger = self.drill_adder.dragger
                            add_board = self.drill_adder.board
                            if event.key == pygame.K_m:
                                mode = TITLE_SCREEN

                        # Flip the board
                        elif event.key == pygame.K_f:
                            flipped = False if flipped else True
                            # print(flipped)
                            


                    
                    # Quit the application
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                
                
                
                pygame.display.update()

            elif mode == CUSTOM:
                # Show methods
                game.show_bg(screen, flipped)
                game.show_last_move(screen, flipped)
                game.show_moves(screen, flipped)
                game.show_pieces(screen, flipped)
                game.show_hover(screen)

                if dragger.dragging: 
                    dragger.update_blit(screen)

                for event in pygame.event.get():

                    # Click event
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse(event.pos)
                        
                        if dragger.mouseX < WIDTH and dragger.mouseY < HEIGHT:
                            clicked_row = (dragger.mouseY // SQSIZE) if not flipped else (7 - (dragger.mouseY // SQSIZE))
                            clicked_col = (dragger.mouseX // SQSIZE) if not flipped else (7 - (dragger.mouseX // SQSIZE))

                            # If there is a piece in the clicked square
                            if board.squares[clicked_row][clicked_col].has_piece():
                                piece = board.squares[clicked_row][clicked_col].piece

                                # valid color
                                if piece.color == game.next_player:
                                    board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                    dragger.save_initial(event.pos, flipped)
                                    dragger.drag_piece(piece)
                                    # show methods
                                    game.show_bg(screen, flipped)
                                    game.show_last_move(screen, flipped)
                                    game.show_moves(screen, flipped)
                                    game.show_pieces(screen, flipped)
                    
                    # Mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQSIZE
                        motion_col = event.pos[0] // SQSIZE

                        game.set_hover(motion_row, motion_col)

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            # Show methods
                            game.show_bg(screen, flipped)
                            game.show_last_move(screen, flipped)
                            game.show_moves(screen, flipped)
                            game.show_pieces(screen, flipped)
                            game.show_hover(screen)
                            dragger.update_blit(screen)
                    
                    # Click release
                    elif event.type == pygame.MOUSEBUTTONUP:

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                            if dragger.mouseX < WIDTH and dragger.mouseY < HEIGHT:
                                released_row = (dragger.mouseY // SQSIZE) if not flipped else (7 - (dragger.mouseY // SQSIZE))
                                released_col = (dragger.mouseX // SQSIZE) if not flipped else (7 - (dragger.mouseX // SQSIZE))
                            else: 
                                released_row = dragger.initial_row
                                released_col = dragger.initial_col


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
                                game.show_bg(screen, flipped)
                                game.show_last_move(screen, flipped)
                                game.show_pieces(screen, flipped)

                                game.next_turn()


                        dragger.undrag_piece()

                    # key press
                    elif event.type == pygame.KEYDOWN:
                        # change the theme
                        if event.key == pygame.K_t:
                            game.change_theme()

                        # reset the board or reset and quit to menu
                        elif event.key == pygame.K_r or event.key == pygame.K_m:
                            game.reset()
                            game = self.game
                            dragger = self.game.dragger
                            board = self.game.board
                            if event.key == pygame.K_m:
                                mode = TITLE_SCREEN

                        # Flip the board
                        elif event.key == pygame.K_f:
                            flipped = False if flipped else True
                            # print(flipped)
                            


                    
                    # Quit the application
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                
                
                
                pygame.display.update()



main = Main()
main.mainloop()

