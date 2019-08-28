import math

import pygame

from tiles import tile_types
from settings import Settings
from enums import GameMode
from utils import within_rect


# TODO: Refactor - make database with .filter(player_id=None, location_type=None, is_empty=None, etc)
class Location:
    def __init__(self, game, x, y, width=Settings.tile_width, height=Settings.tile_height):
        self.rect = pygame.Rect(x, y, width, height)
        self.content = None
        self.game = game

    def __str__(self):
        return('<Location>(tile={})'.format('<none>' if not self.content else self.content.tile_type.colour))

    @property
    def active(self):
        return False

    @property
    def selected(self):
        return self in self.game.selected

    @property
    def can_click(self):
        return False

    @property
    def is_visible(self):
        return True

    @property
    def image(self):
        return self.content.tile_type.small_image

    @property
    def border_colour(self):
        if self.active:
            return Settings.active_grid_colour

        if self.selected:
            return Settings.selected_grid_colour

        return Settings.grid_colour

    def draw_extra(self):
        pass

    def draw(self):
        if self.content:
            self.game.canvas.blit(self.image, self.rect)
        self.draw_extra()

        pygame.draw.rect(
            self.game.canvas,
            self.border_colour,
            self.rect,
            Settings.grid_line_width
        )


class FactoryLocation(Location):
    cells_per_row = 2
    rows_per_factory = 2

    def __init__(self, game, degrees, factory_id, cell_id):
        self.degrees = degrees
        self.factory_id = factory_id
        self.cell_id = cell_id
        x, y = self.coordinates
        super().__init__(game, x, y)

    @property
    def angle_in_radians(self):
        return math.radians(self.degrees)

    @property
    def factory_centre_coordinates(self):
        x = Settings.factories_circle_radius * math.sin(self.angle_in_radians) + Settings.factories_centre[0]
        y = Settings.factories_circle_radius * math.cos(self.angle_in_radians) + Settings.factories_centre[1]
        return x, y

    @property
    def coordinates(self):
        x, y = self.factory_centre_coordinates

        grid_width = self.cells_per_row * Settings.tile_width + (self.cells_per_row - 1) * Settings.spacing
        grid_height = self.rows_per_factory * Settings.tile_width + (self.rows_per_factory - 1) * Settings.spacing

        x -= int(grid_width / 2)
        y -= int(grid_height / 2)

        row, column = divmod(self.cell_id, self.cells_per_row)
        row, column = row - 1, column - 1

        x += column * Settings.tile_width + (column - 1) * Settings.spacing
        y += row * Settings.tile_height + (row - 1) * Settings.spacing

        return x, y

    @property
    def active(self):
        return self.can_click and self.game.mode is GameMode.SELECTING_TILE

    @property
    def can_click(self):
        if self.selected:
            return False

        return self.game.mode in [
            GameMode.SELECTING_TILE, GameMode.SELECTING_TARGET, GameMode.AWAITING_CONFIRMATION
        ] and self.content


class CentreLocation(FactoryLocation):
    cells_per_row = 5
    rows_per_factory = 5

    def __init__(self, game, cell_id):
        self.cell_id = cell_id
        x, y = self.coordinates
        Location.__init__(self, game, x, y)

    @property
    def factory_centre_coordinates(self):
        return Settings.factories_centre


class PatternLocation(Location):
    def __init__(self, game, player_id, row, column):
        self.player_id = player_id
        self.row = row
        self.column = column
        # TODO: Derive pattern from enum value - and move this to WallLocation??
        self.tile_type = tile_types[(self.column - self.row) % 5]

        x, y = self.coordinates()

        width, height = Settings.tile_width, Settings.tile_height
        if player_id == 0:
            width *= Settings.player_area_multiplier
            height *= Settings.player_area_multiplier
        super().__init__(game, x, y, width, height)

    def coordinates(self):
        if self.player_id == 0:
            x, y = Settings.player_area_location
            multiplier = Settings.player_area_multiplier
        else:
            x, y = Settings.opponent_area_location
            y += (self.player_id - 1) * Settings.area_height
            multiplier = 1
        x += ((4 - self.row) + self.column) * Settings.tile_width * multiplier
        y += self.row * Settings.tile_height * multiplier
        return x, y

    @property
    def active(self):
        return self.can_click and self.game.mode is GameMode.SELECTING_TARGET

    @property
    def can_click(self):
        if self.selected:
            return False

        if not(self.player_id == 0 and self.game.mode in [GameMode.SELECTING_TARGET, GameMode.AWAITING_CONFIRMATION]):
            return False

        if self.content:
            return False

        source_tile_type = self.game.selected_type
        if source_tile_type is None:
            return True

        row_tile_type = self.game.locations.tile_type_for_patternlocation_player_row(0, self.row)

        return row_tile_type in [None, source_tile_type]

    @property
    def image(self):
        # TODO: Refactor - test for human player instead of using player_id == 0
        if self.player_id == 0:
            return self.content.tile_type.large_image

        return self.content.tile_type.small_image


class WallLocation(PatternLocation):
    def coordinates(self):
        if self.player_id == 0:
            x, y = Settings.player_area_location
            multiplier = Settings.player_area_multiplier
        else:
            x, y = Settings.opponent_area_location
            y += (self.player_id - 1) * Settings.area_height
            multiplier = 1
        x += Settings.pattern_area_width * multiplier
        x += self.column * Settings.tile_width * multiplier
        y += self.row * Settings.tile_height * multiplier
        return x, y

    @property
    def background_image(self):
        if self.player_id == 0:
            return self.tile_type.large_transparent_image
        return self.tile_type.small_transparent_image

    @property
    def active(self):
        return False

    @property
    def can_click(self):
        return False

    def draw_extra(self):
        self.game.canvas.blit(self.background_image, self.rect)


class FloorLocation(Location):
    def __init__(self, game, player_id, column, score):
        self.player_id = player_id
        self.column = column
        self.score = score

        x, y = self.coordinates()

        width, height = Settings.tile_width, Settings.tile_height
        if player_id == 0:
            width *= Settings.player_area_multiplier
            height *= Settings.player_area_multiplier
        super().__init__(game, x, y, width, height)

    # TODO: Too much copied in this module - refactor some out
    def coordinates(self):
        if self.player_id == 0:
            x, y = Settings.player_area_location
            multiplier = Settings.player_area_multiplier
        else:
            x, y = Settings.opponent_area_location
            y += (self.player_id - 1) * Settings.area_height
            multiplier = 1
        x += self.column * Settings.tile_width * multiplier
        y += (Settings.area_height - Settings.tile_height * 1.9) * multiplier
        return x, y

    # TODO: Refactor - duplicate of PatternLocation
    @property
    def image(self):
        # TODO: Refactor - test for human player instead of using player_id == 0
        if self.player_id == 0:
            return self.content.tile_type.large_image

        return self.content.tile_type.small_image

    def draw_extra(self):
        if self.player_id == 0:
            multiplier = Settings.player_area_multiplier
            font = self.game.large_floor_tile_scores_font
        else:
            multiplier = 1
            font = self.game.small_floor_tile_scores_font
        self.game.canvas.blit(
            font.render(str(self.score), True, Settings.floor_tile_scores_colour),
            (
                self.rect.x + Settings.floor_tile_scores_spacing * multiplier,
                self.rect.y + Settings.floor_tile_scores_spacing * multiplier
            )
        )

class ButtonLocation(Location):
    def __init__(self, game, x, y, width, height, text, action):
        super().__init__(game, x, y, width, height)

        self._image = pygame.Surface(self.rect.size)
        self._image.fill(Settings.active_grid_colour)
        self.action = action

        spacing = Settings.floor_tile_scores_spacing * Settings.player_area_multiplier
        self._image.blit(
            game.button_font.render(text, True, pygame.Color('white')),
            (spacing, spacing)
        )

        pygame.draw.rect(
            self._image,
            pygame.Color('white'),
            (0, 0, self.rect.width, self.rect.height),
            Settings.grid_line_width
        )

    @property
    def image(self):
        return self._image

    @property
    def can_click(self):
        return self.game.mode is GameMode.AWAITING_CONFIRMATION

    @property
    def is_visible(self):
        return self.can_click

    def draw(self):
        pygame.draw.rect(
            self.game.canvas,
            Settings.active_grid_colour,
            self.rect,
        )
        self.game.canvas.blit(self.image, self.rect)


class Locations:
    def __init__(self, game):
        self.all = []
        self.game = game
        self.generate_factory_locations()
        self.generate_centre_location()
        self.generate_pattern_locations()
        self.generate_wall_locations()
        self.generate_floor_locations()

    @property
    def centre_locations(self):
        return [l for l in self.all if isinstance(l, CentreLocation)]

    def free_centre_locations(self):
        result = [l for l in self.all if isinstance(l, CentreLocation) and l.content is None]
        result.sort(key=lambda x: x.cell_id)
        return result

    @property
    def factory_locations(self):
        return [l for l in self.all if type(l) == FactoryLocation]

    @property
    def floor_locations(self):
        return [l for l in self.all if type(l) == FloorLocation]

    def factory_locations_for_id(self, factory_id):
        return [l for l in self.all if type(l) == FactoryLocation and l.factory_id == factory_id]

    def pattern_locations_for_player_id(self, player_id):
        return [l for l in self.all if type(l) == PatternLocation and l.player_id == player_id]

    def wall_locations_for_player_id(self, player_id):
        return [l for l in self.all if type(l) == WallLocation and l.player_id == player_id]

    def tile_type_for_patternlocation_player_row(self, player_id, row):
        locations = self.pattern_locations_for_player_id(player_id)
        row_locations = [l for l in locations if l.row == row]
        for l in row_locations:
            if l.content:
                return l.content.tile_type
        return None

    def generate_factory_locations(self):
        number_of_factories = {
            2: 5,
            3: 7,
            4: 9
        }[self.game.number_of_players]
        for factory_id in range(number_of_factories):
            for cell_id in range(4):
                location = FactoryLocation(self.game, factory_id * 360/number_of_factories, factory_id, cell_id)
                self.all.append(location)
                location.content = self.game.tiles.random_tile()

    def generate_centre_location(self):
        for cell_id in range(CentreLocation.rows_per_factory * CentreLocation.cells_per_row):
            self.all.append(CentreLocation(self.game, cell_id))

    def generate_pattern_locations(self):
        for player_id in range(self.game.number_of_players):
            for row in range(5):
                for column in range(row + 1):
                    self.all.append(PatternLocation(self.game, player_id, row, column))

    def generate_wall_locations(self):
        for player_id in range(self.game.number_of_players):
            for row in range(5):
                for column in range(5):
                    self.all.append(WallLocation(self.game, player_id, row, column))

    def generate_floor_locations(self):
        for player_id in range(self.game.number_of_players):
            for column, score in enumerate([-1, -1, -2, -2, -2, -3, -3]):
                self.all.append(FloorLocation(self.game, player_id, column, score))

    def find(self, x, y):
        for location in self.all:
            if not location.can_click:
                continue
            # TODO: Probably proper method of rect to check this
            if within_rect(x, y, location.rect):
                return location
        return None

    def draw(self):
        for location in self.all:
            if location.is_visible:
                location.draw()
