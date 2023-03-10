from game import Game
from const import * 
import pygame
import datetime


class DrillAdder(Game):

    def __init__(self):
        super().__init__()

        self.color = "white"

        self.add_msg = self.config.help_item.render("Color:", False, self.config.theme_blue)
        self.add_msg_rect = self.add_msg.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)), 50))

        self.color_center = (TRUEWIDTH - 50, 50)
        self.color_color = self.config.theme_blue
        self.color_rect = pygame.Rect(TRUEWIDTH - 60, 40, 20, 20)

        self.button_color = self.config.theme_hover
        self.button_rect = pygame.Rect(WIDTH + 50, HEIGHT - 150, 300, 100)
        self.big_button_rect = (WIDTH + 40, HEIGHT - 160, 320, 120)
        # self.big_button = self.button_rect.inflate(10, 10)
        
        self.save_msg = self.config.help_item.render("Save", False, self.config.theme_blue)
        self.save_msg_rect = self.save_msg.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) // 2)), 700))

        # self.save_msg_hover = self.config.help_item_hover.render("Save", False, self.config.theme_blue)
        # self.save_msg_hover_rect = self.save_msg_hover.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) // 2)), 700))

        self.indicator_color = (209, 0, 126)

        

    def show_bg(self, surface, flipped=False):
        super().show_bg(surface, flipped)

        surface.blit(self.add_msg, self.add_msg_rect)
        mouse_pos = pygame.mouse.get_pos()
        

        # if self.save_msg_rect.collidepoint(mouse_pos):
        #     surface.blit(self.save_msg_hover, self.save_msg_hover_rect)
        # else:
        #     surface.blit(self.save_msg, self.save_msg_rect)

        if self.button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.button_color, self.button_rect, border_radius=20)

        surface.blit(self.save_msg, self.save_msg_rect)
        
        width = 5 if self.color == "black" else 0
        pygame.draw.circle(surface, self.color_color, self.color_center, 30, width)

        

    def show_entered_moves(self, surface):
        """
        This method should blit played moves one by one onto the side of the screen
        """
        # number of display rows
        move_counter = 1

        for move_index in range(len(self.board.moves)):
            if move_index % 2 == 0:
                num_surf = self.config.move_font.render(str(move_counter) + ".", False, (255, 255, 255))
                num_rect = num_surf.get_rect(midleft = (WIDTH + 20, (100 + 30 * move_counter)))
                surface.blit(num_surf, num_rect)
            move_surf = self.config.move_font.render(self.board.moves[move_index], False, (255, 255, 255))
            if move_index % 2 == 0: # white
                # if move_index == len(self.board.moves) - 1: # most recent move
                #     indicator_rect = (WIDTH + 90, 90 + 30 * move_counter, 100, 20)
                #     pygame.draw.rect(surface, self.indicator_color, indicator_rect, border_radius=2)
                move_rect = move_surf.get_rect(midleft = ((WIDTH + 100 * 1), (100 + 30 * move_counter)))
            else: # black
                # if move_index == len(self.board.moves) - 1: # most recent move
                #     indicator_rect = (WIDTH + 100 * 2.5 - 10, 90 + 30 * move_counter, 100, 20)
                #     pygame.draw.rect(surface, self.indicator_color, indicator_rect, border_radius=2)
                move_rect = move_surf.get_rect(midleft = ((WIDTH + 100 * 2.5), (100 + 30 * move_counter)))
            
            surface.blit(move_surf, move_rect)
            if move_index % 2 == 1:
                move_counter += 1
    
    def save_to_deck(self):
        """
        Save the current drill contained in self.board.moves to the log file
        """
        # Drill contents
        drill_contents = ""
        print(len(self.board.moves))
        print(self.color)
        if (len(self.board.moves) % 2 == 0 and self.color == "white") or (len(self.board.moves) % 2 == 1 and self.color == "black"):
            self.board.moves = self.board.moves[:-1]

        for move in self.board.moves:
            drill_contents += move
            drill_contents += ","
        drill_contents = drill_contents[:-1]
        ease = str(2.5)
        interval = str(1)
        mode = str(NEW)
        # POSIX time stamp
        due_date = str(int(datetime.datetime.now().timestamp()))

        log_entry = drill_contents + ":" + ease + ":" + interval + ":" + mode + ":" + self.color + ":" + due_date + "\n"
        
        with open(NEW_DRILLFILE, 'a') as f:
            f.write(log_entry)

    def switch_color(self):
        self.color = "white" if self.color == "black" else "black"



        


    



        