import pygame

from players import Player
from tiles import Tiles
from locations import Locations, FactoryLocation, CentreLocation, PatternLocation, ButtonLocation, FloorLocation, WallLocation
from enums import GameMode, Location
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

    def show_scores(self):
        for player in self.players:
            player.show_score(self)

    def draw(self):
        self.draw_background()
        self.locations.draw()
        self.show_scores()
        pygame.display.flip()

    @property
    def selected_type(self):
        if not self.source:
            return None

        return self.source[0].content.tile_type

    @property
    def clicked_location(self):
        result = self.locations.find(*pygame.mouse.get_pos())
        if result is not None:
            return result

        return None

    def select_source_tile(self, location):
        self.source = []
        if type(location) == FactoryLocation:
            for i in self.locations.all:
                if type(i) == FactoryLocation:
                    if i.factory_id == location.factory_id and i.content.tile_type == location.content.tile_type:
                        self.source.append(i)
        elif type(location) == CentreLocation:
            for i in self.locations.all:
                if type(i) == CentreLocation and i.content:
                    if i.content.tile_type == location.content.tile_type:
                        self.source.append(i)
        self.mode = GameMode.SELECTING_TARGET

    def select_target_row(self, location):
        self.target = []
        for i in self.locations.all:
            if type(i) is not PatternLocation or i.player_id is not 0:
                continue
            if i.row == location.row:
                self.target.append(i)
        self.mode = GameMode.AWAITING_CONFIRMATION

    def sort_centre(self):
        centre_locations = self.locations.filter(location_type=CentreLocation)
        centre_pieces = [l.content for l in centre_locations if l.content is not None]
        centre_pieces.sort(key=lambda x: x.tile_type.colour)
        for location in centre_locations:
            location.content = None
        for i in range(len(centre_pieces)):
            centre_locations[i].content = centre_pieces[i]

    def move_pieces(self):
        self.target.sort(key=lambda x: -x.column)
        free_target = [t for t in self.target if not t.content]
        for i in range(min(len(free_target), len(self.source))):
            free_target[i].content = self.source[i].content
            self.source[i].content = None

        # TODO: Refactor - lots of duplication from code just above
        source = [s for s in self.source if s.content]
        free_target = [t for t in self.locations.all if isinstance(t, FloorLocation) and not t.content and t.player_id == 0]
        free_target.sort(key=lambda x: x.column)
        for i in range(min(len(free_target), len(source))):
            free_target[i].content = source[i].content
            source[i].content = None

        if type(self.source[0]) == FactoryLocation:
            centre_locations = self.locations.filter(location_type=CentreLocation, is_free=True, sort_by='cell_id')
            factory_locations = self.locations.filter(location_type=FactoryLocation, factory_id=self.source[0].factory_id)
            to_move_to_centre = [l for l in factory_locations if l.content]
            for i, location in enumerate(to_move_to_centre):
                centre_locations[i].content = location.content
                location.content = None
            if to_move_to_centre:
                self.sort_centre()

        # TODO: Move to separate function to reset mode?
        self.mode = GameMode.SELECTING_TILE
        self.source = []
        self.target = []

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

    def new_tiles(self):
        for location in self.locations.filter(location_type=FactoryLocation):
            if not location.content:
                location.content = self.tiles.random_tile()

    def points_for_range(self, h_range, v_range):
        result = 0
        for x in h_range:
            for y in v_range:
                if self.locations.filter(location_type=WallLocation, column=x, row=y)[0].content is None:
                    return result
                result += 1
        return result

    def points_for_wall_location(self, location):
        h_points = self.points_for_range(range(location.column - 1, -1, -1), [location.row]) + \
                   self.points_for_range(range(location.column + 1, 5), [location.row])
        if h_points:
            h_points += 1
        v_points = self.points_for_range([location.column], range(location.row - 1, -1, -1)) + \
                   self.points_for_range([location.column], range(location.row + 1, 5))
        if v_points:
            v_points += 1
        result = max(1, h_points + v_points)
        # print(location.column, location.row, h_points, v_points)
        return result

    def score(self):
        for player in self.players:
            pattern_locations = self.locations.filter(location_type=PatternLocation, player_id=player.order)
            wall_locations = self.locations.filter(location_type=WallLocation, player_id=player.order)
            for row in range(5):
                source_locations = [l for l in pattern_locations if l.row == row and l.content]
                if len(source_locations) != row + 1:
                    continue

                tile_type = source_locations[0].content.tile_type
                target_location = [l for l in wall_locations if l.row == row and l.tile_type == tile_type][0]
                player.points += self.points_for_wall_location(target_location)
                target_location.content = source_locations[0].content
                source_locations[0].content = None
                for location in source_locations[1:]:
                    location.content.location = Location.DISCARD_PILE
                    location.content = None

        for location in self.locations.filter(location_type=FloorLocation):
            if location.content:
                location.content.location = Location.DISCARD_PILE
                location.content = None

        self.new_tiles()
