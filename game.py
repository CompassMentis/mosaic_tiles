import pygame

from players import Player
from tiles import Tiles
from locations import Locations, FactoryLocation, CentreLocation, PatternLocation
from buttons import Button
from enums import GameMode
from settings import Settings


class Game:
    def __init__(self, player_details, canvas):
        self.players = [Player(name, order, is_human) for (order, (name, is_human)) in enumerate(player_details)]
        self.tiles = Tiles()
        self.locations = Locations(self)
        self.active_tile = None
        self.active_target = None
        self.mode = GameMode.SELECTING_TILE
        self.canvas = canvas

        # TODO: Move fonts into Settings or separate fonts module?
        self.small_floor_tile_scores_font = pygame.font.SysFont('Arial', Settings.floor_tile_scores_font_size)
        self.large_floor_tile_scores_font = pygame.font.SysFont('Arial', int(Settings.floor_tile_scores_font_size * Settings.player_area_multiplier))
        self.button_font = self.large_floor_tile_scores_font

        x, y = Settings.player_area_location
        multiplier = Settings.player_area_multiplier
        x += Settings.pattern_area_width * multiplier
        x += 3 * Settings.tile_width * multiplier
        width = 3 * Settings.tile_width * multiplier
        y += (Settings.area_height - Settings.tile_height * 1.9) * multiplier
        height = Settings.tile_height * multiplier

        self.confirmation_button = Button(self, x, y, width, height, 'Continue', 'confirm')

    @property
    def number_of_players(self):
        return len(self.players)

    def draw_background(self):
        self.canvas.fill((0, 0, 0))

    def draw(self):
        self.draw_background()
        self.locations.draw()
        if self.mode == GameMode.AWAITING_CONFIRMATION:
            # TODO: Move this into separate function/method?
            pygame.draw.rect(
                self.canvas,
                Settings.active_grid_colour,
                self.confirmation_button.rect,
            )
            self.canvas.blit(self.confirmation_button.image, self.confirmation_button.rect)

        pygame.display.flip()

    @property
    def clicked_location(self):
        return self.locations.find(*pygame.mouse.get_pos())

    def select_source_tile(self, location):
        if isinstance(location, CentreLocation):
            return
        if isinstance(location, FactoryLocation):
            for i in self.locations.all:
                if type(i) == PatternLocation:
                    i.selected = False
                elif type(i) == FactoryLocation:
                    i.selected = (i.factory_id == location.factory_id and i.content.tile_type == location.content.tile_type)
        self.mode = GameMode.SELECTING_TARGET

    def select_target_row(self, location):
        print('select target row')
        for i in self.locations.all:
            if type(i) is not PatternLocation or i.player_id is not 0:
                continue
            i.selected = (i.row == location.row)
            if i.selected:
                print('selected')
        self.mode = GameMode.AWAITING_CONFIRMATION


    def process_mouse_click(self):
        location = self.clicked_location
        if location is None or not location.can_click:
            return

        if isinstance(location, FactoryLocation):
            self.select_source_tile(location)
            return

        if isinstance(location, PatternLocation):
            self.select_target_row(location)
            return
