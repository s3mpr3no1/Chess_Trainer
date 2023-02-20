from game import Game
from const import * 


class DrillAdder(Game):

    def __init__(self):
        super().__init__()

        self.add_msg = self.config.help_item.render("Add Drills", False, (0, 0, 0))
        self.add_msg_rect = self.add_msg.get_rect(center = ((WIDTH + ((TRUEWIDTH - WIDTH) / 2)), 50))

    def show_bg(self, surface, flipped=False):
        super().show_bg(surface, flipped)

        surface.blit(self.add_msg, self.add_msg_rect)

    def show_entered_moves(self, surface):
        """
        This method should blit played moves one by one onto the side of the screen
        """
        # number of display rows
        move_counter = 1

        for move_index in range(len(self.board.moves)):
            move_surf = self.config.help_item.render(self.board.moves[move_index], False, (0,0,0))
            column = 1 if move_index % 2 == 0 else 2.5
            move_rect = move_surf.get_rect(midleft = ((WIDTH + 100 * column), (100 + 50 * move_counter)))
            surface.blit(move_surf, move_rect)
            if move_index % 2 == 1:
                move_counter += 1

    



        