import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move
from title import Title
from help import Help
from add_drills import DrillAdder
from study import Study
import time

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((TRUEWIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()
        self.title = Title()
        self.help = Help()
        self.drill_adder = DrillAdder()
        self.study = Study()

        # When this is false, the board will freeze
        self.moveable = True

        # Finishing a drill automatically
        self.show_answer = False

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
        study = self.study
        study_board = self.study.board
        study_dragger = self.study.dragger

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
                        if mode == STUDY:
                            study.load_drills()

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
                adder.show_entered_moves(screen)

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
                                    adder.show_entered_moves(screen)
                        # Mouse in in the menu portion of the screen
                        else:
                            if adder.save_msg_rect.collidepoint(event.pos):
                                adder.save_to_deck()
                                # reset the screen
                                adder.reset()
                                adder = self.drill_adder
                                add_dragger = self.drill_adder.dragger
                                add_board = self.drill_adder.board
                            elif adder.color_rect.collidepoint(event.pos):
                                adder.switch_color()
                    
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
                            adder.show_entered_moves(screen)
                    
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


                                add_board.move(add_dragger.piece, move, captured=captured)

                                add_board.set_true_en_passant(add_dragger.piece)
                                # sounds
                                adder.play_sound(captured)
                                # show methods
                                adder.show_bg(screen, flipped)
                                adder.show_last_move(screen, flipped)
                                adder.show_pieces(screen, flipped)
                                adder.show_entered_moves(screen)

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

            elif mode == STUDY:
                if len(study.scheduler.due_today) == 0:
                    help.show_bg(screen)

                    for event in pygame.event.get():

                        if event.type == pygame.KEYDOWN:
                            
                            if event.key == pygame.K_m:
                                mode = TITLE_SCREEN

                        elif event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                    pygame.display.update()
                    continue
                
                flipped = True if study.scheduler.due_today[0].color == "black" else False

                # if someone hits the show answer button
                if self.show_answer:
                    # counter will be to delay the program ....
                    counter = 0
                    while self.show_answer:
                        if counter > SHOW_ANSWER_DELAY:
                            # If there is no need for another move
                            if len(study_board.moves) == len(study.scheduler.due_today[0].sequence):
                                self.show_answer = False
                                self.moveable = False
                                study.show_anki_choices = True
                                break

                            # Play and add the next move
                            # Get the next move string from the drill
                            next_move_string = study.scheduler.due_today[0].sequence[len(study_board.moves)]
                            # print(next_move_string)
                            # Get the next move
                            next_move = Move.move_from_string(next_move_string)
                            # print(next_move)
                            # Get the next piece
                            next_piece = study_board.squares[next_move.initial.row][next_move.initial.col].piece

                            # Check next captured status
                            next_captured = study_board.squares[next_move.final.row][next_move.final.col].has_piece()

                            # Make the move
                            study_board.move(next_piece, next_move, captured=next_captured)

                            study_board.set_true_en_passant(next_piece)
                            # sounds
                            study.play_sound(next_captured)
                            # show methods
                            study.show_bg(screen, flipped)
                            study.show_last_move(screen, flipped)
                            study.show_pieces(screen, flipped)
                            # study.show_entered_moves(screen)
                            study.next_turn()


                            counter = 0
                            
                        else:
                            study.show_bg(screen, flipped)
                            study.show_last_move(screen, flipped)
                            study.show_pieces(screen, flipped)
                            counter += 1
                        pygame.display.update()
                
                # If it's the first move of a black drill
                if (len(study_board.moves) == 0) and flipped:
                    # Get the next move string from the drill
                    next_move_string = study.scheduler.due_today[0].sequence[len(study_board.moves)]
                    # print(next_move_string)
                    # Get the next move
                    next_move = Move.move_from_string(next_move_string)
                    # print(next_move)
                    # Get the next piece
                    next_piece = study_board.squares[next_move.initial.row][next_move.initial.col].piece

                    # Check next captured status
                    next_captured = study_board.squares[next_move.final.row][next_move.final.col].has_piece()

                    # Make the move
                    study_board.move(next_piece, next_move, captured=next_captured)

                    study_board.set_true_en_passant(next_piece)
                    # sounds
                    study.play_sound(next_captured)
                    # show methods
                    study.show_bg(screen, flipped)
                    study.show_last_move(screen, flipped)
                    study.show_pieces(screen, flipped)
                    # study.show_entered_moves(screen)
                    study.next_turn()

                # Show methods
                study.show_bg(screen, flipped)
                study.show_last_move(screen, flipped)
                study.show_moves(screen, flipped)
                study.show_pieces(screen, flipped)
                study.show_hover(screen)
                # study.show_entered_moves(screen)

                if study_dragger.dragging: 
                    study_dragger.update_blit(screen)

                for event in pygame.event.get():

                    # Click event
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.moveable:
                            study_dragger.update_mouse(event.pos)
                            
                            if study_dragger.mouseX < WIDTH and study_dragger.mouseY < HEIGHT:
                                clicked_row = (study_dragger.mouseY // SQSIZE) if not flipped else (7 - (study_dragger.mouseY // SQSIZE))
                                clicked_col = (study_dragger.mouseX // SQSIZE) if not flipped else (7 - (study_dragger.mouseX // SQSIZE))

                                # If there is a piece in the clicked square
                                if study_board.squares[clicked_row][clicked_col].has_piece():
                                    piece = study_board.squares[clicked_row][clicked_col].piece

                                    # valid color
                                    if piece.color == study.next_player:
                                        study_board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                        study_dragger.save_initial(event.pos, flipped)
                                        study_dragger.drag_piece(piece)
                                        # show methods
                                        study.show_bg(screen, flipped)
                                        study.show_last_move(screen, flipped)
                                        study.show_moves(screen, flipped)
                                        study.show_pieces(screen, flipped)
                                        # study.show_entered_moves(screen)
                            # Mouse in in the menu portion of the screen

                            # The show answer button has been selected
                            elif study.show_answer_button_rect.collidepoint(event.pos):
                                self.show_answer = True
                        
                    
                    # Mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        if self.moveable:
                            motion_row = event.pos[1] // SQSIZE
                            motion_col = event.pos[0] // SQSIZE

                            study.set_hover(motion_row, motion_col)

                            if study_dragger.dragging:
                                study_dragger.update_mouse(event.pos)
                                # Show methods
                                study.show_bg(screen, flipped)
                                study.show_last_move(screen, flipped)
                                study.show_moves(screen, flipped)
                                study.show_pieces(screen, flipped)
                                study.show_hover(screen)
                                study_dragger.update_blit(screen)
                                # adder.show_entered_moves(screen)
                    
                    # Click release
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if self.moveable:
                            if study_dragger.dragging:
                                study_dragger.update_mouse(event.pos)

                                if study_dragger.mouseX < WIDTH and study_dragger.mouseY < HEIGHT:
                                    released_row = (study_dragger.mouseY // SQSIZE) if not flipped else (7 - (study_dragger.mouseY // SQSIZE))
                                    released_col = (study_dragger.mouseX // SQSIZE) if not flipped else (7 - (study_dragger.mouseX // SQSIZE))
                                else: 
                                    released_row = study_dragger.initial_row
                                    released_col = study_dragger.initial_col


                                # create possible move
                                initial = Square(study_dragger.initial_row, study_dragger.initial_col)
                                final = Square(released_row, released_col)
                                move = Move(initial, final)

                                # if valid move
                                if study_board.valid_move(study_dragger.piece, move):
                                    # normal capture
                                    captured = study_board.squares[released_row][released_col].has_piece()


                                    study_board.move(study_dragger.piece, move, captured=captured)
                                    

                                    study_board.set_true_en_passant(study_dragger.piece)
                                    # sounds
                                    study.play_sound(captured)
                                    # show methods
                                    study.show_bg(screen, flipped)
                                    study.show_last_move(screen, flipped)
                                    study.show_pieces(screen, flipped)
                                    # study.show_entered_moves(screen)

                                    study.next_turn()

                                    # If there is no need for another move
                                    if len(study_board.moves) == len(study.scheduler.due_today[0].sequence):
                                        study.msg_color = study.config.study_right
                                        self.moveable = False
                                        study.show_anki_choices = True

                                    # In the other case, we need to play the next move in the drill
                                    # If the move made matches the drill sequence
                                    elif study.scheduler.board_matches_drill(study_board):
                                        # study_dragger.undrag_piece()

                                        # Get the next move string from the drill
                                        next_move_string = study.scheduler.due_today[0].sequence[len(study_board.moves)]
                                        # print(next_move_string)
                                        # Get the next move
                                        next_move = Move.move_from_string(next_move_string)
                                        # print(next_move)
                                        # Get the next piece
                                        next_piece = study_board.squares[next_move.initial.row][next_move.initial.col].piece

                                        # Check next captured status
                                        next_captured = study_board.squares[next_move.final.row][next_move.final.col].has_piece()

                                        # Make the move
                                        study_board.move(next_piece, next_move, captured=next_captured)

                                        study_board.set_true_en_passant(next_piece)
                                        # sounds
                                        study.play_sound(next_captured)
                                        # show methods
                                        study.show_bg(screen, flipped)
                                        study.show_last_move(screen, flipped)
                                        study.show_pieces(screen, flipped)
                                        # study.show_entered_moves(screen)

                                    # The wrong move was entered
                                    elif not study.scheduler.board_matches_drill(study_board):
                                        study.msg_color = study.config.study_wrong
                                        self.moveable = False
                                        study.show_anki_choices = True

                                    study.next_turn()
                                


                            study_dragger.undrag_piece()

                        # At this point, we're in the end state. Anki buttons are now live
                        # event.pos is the place the button release occurs
                        else: 
                            if study.anki_again_button_rect.collidepoint(event.pos):
                                study.scheduler.anki_again()
                                study_board.reset()
                                self.moveable = True
                            elif study.anki_hard_button_rect.collidepoint(event.pos):
                                study.scheduler.anki_hard()
                                study_board.reset()
                                self.moveable = True
                            elif study.anki_good_button_rect.collidepoint(event.pos):
                                study.scheduler.anki_good()
                                study_board.reset()
                                self.moveable = True
                            elif study.anki_easy_button_rect.collidepoint(event.pos):
                                study.scheduler.anki_easy()
                                study_board.reset()
                                self.moveable = True
                            

                    # key press
                    elif event.type == pygame.KEYDOWN:
                        # change the theme
                        if event.key == pygame.K_t:
                            study.change_theme()

                        # reset the board or reset and quit to menu
                        elif event.key == pygame.K_r or event.key == pygame.K_m:
                            study.reset()
                            study = self.study
                            study_dragger = self.study.dragger
                            study_board = self.study.board
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
                # if not self.moveable: study.show_anki_choices = True

            # # No drills to complete
            # elif mode == STUDY and len(study.scheduler.due_today) != 0:
            #     print("Done")
            #     mode = HELP

main = Main()
main.mainloop()

