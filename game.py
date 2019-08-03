import pygame

from players import Player
from tiles import Tiles
from locations import Locations, FactoryLocation, CentreLocation
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
        self.small_floor_tile_scores_font = pygame.font.SysFont('Arial', Settings.floor_tile_scores_font_size)
        self.large_floor_tile_scores_font = pygame.font.SysFont('Arial', int(Settings.floor_tile_scores_font_size * Settings.player_area_multiplier))

    @property
    def number_of_players(self):
        return len(self.players)

    def draw_background(self):
        self.canvas.fill((0, 0, 0))

    # def draw_floor_tile_scores(self):
    #     for player in self.players:
    #         for i, score in [-1, -1, -2, -2, -2, -3, -3]:
    #             x =

    def draw(self):
        self.draw_background()
        self.locations.draw()
        # self.draw_floor_tile_scores()
        pygame.display.flip()

    @property
    def clicked_location(self):
        return self.locations.find(*pygame.mouse.get_pos())

    def select_tile(self, location):
        if isinstance(location, CentreLocation):
            return
        if isinstance(location, FactoryLocation):
            for i in self.locations.all:
                if type(i) is not FactoryLocation:
                    continue
                i.selected = (i.factory_id == location.factory_id and i.content.tile_type == location.content.tile_type)
                    # i.selected = True
        # select all tiles of the selected type at this factory or centre

    def process_mouse_click(self):
        location = self.clicked_location
        if location is None or not location.can_click:
            return
        print('Location clicked')
        if self.mode == GameMode.SELECTING_TILE:
            self.select_tile(location)
            self.mode = GameMode.SELECTING_TARGET
        elif self.mode == GameMode.SELECTING_TARGET:
            if isinstance(location, FactoryLocation):
                self.select_tile(location)
