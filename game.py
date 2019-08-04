import pygame

from players import Player
from tiles import Tiles
from locations import Locations, FactoryLocation, CentreLocation, PatternLocation, ButtonLocation
from enums import GameMode
from settings import Settings
from utils import within_rect


class Game:
    def __init__(self, player_details, canvas):
        self.players = [Player(name, order, is_human) for (order, (name, is_human)) in enumerate(player_details)]
        self.tiles = Tiles()
        self.locations = Locations(self)
        self.active_tile = None
        self.active_target = None
        self.mode = GameMode.SELECTING_TILE
        self.canvas = canvas
        self.source = []
        self.target = []

        # TODO: Move fonts into Settings or separate fonts module?
        self.small_floor_tile_scores_font = pygame.font.SysFont('Arial', Settings.floor_tile_scores_font_size)
        self.large_floor_tile_scores_font = pygame.font.SysFont('Arial', int(Settings.floor_tile_scores_font_size * Settings.player_area_multiplier))
        self.button_font = self.large_floor_tile_scores_font

        # TODO: Move this in with the ButtonLocation?
        x, y = Settings.player_area_location
        multiplier = Settings.player_area_multiplier
        x += Settings.pattern_area_width * multiplier
        x += 2 * Settings.tile_width * multiplier
        width = 3 * Settings.tile_width * multiplier
        y += (Settings.area_height - Settings.tile_height * 1.9) * multiplier
        height = Settings.tile_height * multiplier

        self.locations.all.append(ButtonLocation(self, x, y, width, height, 'Continue', 'confirm'))

    @property
    def selected(self):
        return self.source + self.target

    @property
    def number_of_players(self):
        return len(self.players)

    def draw_background(self):
        self.canvas.fill((0, 0, 0))

    def draw(self):
        self.draw_background()
        self.locations.draw()
        pygame.display.flip()

    @property
    def clicked_location(self):
        result = self.locations.find(*pygame.mouse.get_pos())
        if result is not None:
            return result

        return None

    def select_source_tile(self, location):
        self.source = []
        if isinstance(location, FactoryLocation):
            for i in self.locations.all:
                if type(i) == FactoryLocation:
                    if i.factory_id == location.factory_id and i.content.tile_type == location.content.tile_type:
                        self.source.append(i)
        self.mode = GameMode.SELECTING_TARGET

    def select_target_row(self, location):
        print('select target row')
        self.target = []
        for i in self.locations.all:
            if type(i) is not PatternLocation or i.player_id is not 0:
                continue
            if i.row == location.row:
                self.target.append(i)
        self.mode = GameMode.AWAITING_CONFIRMATION

    def get_movement_details(self):
        source = []
        target = []

        for i in self.locations.all:
            if i.selected:
                if isinstance(i, FactoryLocation):
                    source.append(i)
                elif isinstance(i, PatternLocation):
                    target.append(i)
        return source, target

    def move_pieces(self):
        source, target = self.get_movement_details()
        print(source)
        print(target)

    def confirm_movement(self):
        self.move_pieces()

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

        if isinstance(location, ButtonLocation) and location.action == 'confirm':
            self.move_pieces()
