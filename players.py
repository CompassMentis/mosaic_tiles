from settings import Settings


class Player:
    def __init__(self, name, order, is_human):
        self.name = name
        self.order = order
        self.is_human = is_human

    @property
    def board_coordinate(self):
        return self.order * Settings.player_board_width + Settings.player_area_location[0], Settings.player_area_location[1]


        #     player_board_width = 150
        #     player_board_height = 150
        #     player_area_location = spacing, spacing