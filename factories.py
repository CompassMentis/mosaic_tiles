import math

import pygame

from settings import Settings


class Factory:
    def __init__(self, degrees, game, is_centre=False):
        self.degrees = degrees
        self.game = game
        self.is_centre = is_centre
        if self.is_centre:
            self.grid_size = Settings.factory_grid_size
            # self.grid_columns = Settings.factory_centre_grid_columns
            # self.grid_rows =
        else:
            self.grid_size = pygame.Rect(2, 2, 0, 0)

        self.slots = []
        for i in range(self.number_of_slots):
            x, y = self.tile_coordinates(i)
            location = game.locations.add(x, y)
            self.slots.append(location)
            location.content = self.game.tiles.random_tile()

    @property
    def number_of_slots(self):
        return self.grid_size[0] * self.grid_size[1]

    @property
    def degrees_in_radians(self):
        return math.radians(self.degrees)

    @property
    def centre_coordinates(self):
        x, y = Settings.factories_centre


        if not self.is_centre:
            x += Settings.factories_circle_radius * math.sin(self.degrees_in_radians)
            y += Settings.factories_circle_radius * math.cos(self.degrees_in_radians)
        return x, y

    def tile_coordinates(self, slot_number):
        x, y = self.centre_coordinates

        grid_width = self.grid_size[0] * Settings.tile_width + (self.grid_size[0] - 1) * Settings.spacing
        grid_height = self.grid_size[1] * Settings.tile_width + (self.grid_size[1] - 1) * Settings.spacing

        x -= int(grid_width / 2)
        y -= int(grid_height / 2)

        row, column = divmod(slot_number, self.grid_size[0])
        row, column = row - 1, column - 1

        x += column * Settings.tile_width + (column - 1) * Settings.spacing
        y += row * Settings.tile_height + (row - 1) * Settings.spacing

        # dx, dy = {
        #     0: (0, 0),
        #     1: (Settings.tile_width + Settings.spacing, 0),
        #     2: (0, Settings.tile_height + Settings.spacing),
        #     3: (Settings.tile_width + Settings.spacing, Settings.tile_height + Settings.spacing)
        # }[slot_number]
        #
        # return x + dx, y + dy
        return x, y

    def place_tile(self, tile):
        tile.location = self
        self.tiles.append(tile)
        i = len(self.tiles)


    def draw(self):
        pass
        # Calculate coordinate of centre_coordinates
        # Draw circle
        # Draw 4 tiles, in a grid
        # Better:
        #   when creating a factory, calculate centre_coordinates
        #   and when moving a tile to a factory, calculate location
        # To facilitate movement
            # current_location (x/y)
            # target_location (x/y)
            # steps_remaining
            # delta (x/y)
        # Pieces move in turn
            # Keep a to_move list
