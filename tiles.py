from random import choice

import pygame

from enums import Location
from settings import Settings


class TileType:
    def __init__(self, colour):
        self.colour = colour
        self.image = pygame.image.load('images/tile_{}.png'.format(colour))
        self.small_image = pygame.transform.scale(self.image, (Settings.tile_width, Settings.tile_height))
        self.large_image = pygame.transform.scale(
            self.image,
            (
                int(Settings.tile_width * Settings.player_area_multiplier),
                int(Settings.tile_height * Settings.player_area_multiplier)
            )
        )
        self.small_transparent_image = self.small_image.convert()
        self.small_transparent_image.set_alpha(80)
        self.large_transparent_image = self.large_image.convert()
        self.large_transparent_image.set_alpha(80)

    def __str__(self):
        return '<TileType>(colour={})'.format(self.colour)


class Tile:
    def __init__(self, tile_type):
        self.tile_type = tile_type
        self.location = Location.BAG
        self.x = None
        self.y = None

    @property
    def background_image(self):
        return self.tile_type.small_transparent_image


class Tiles:
    def __init__(self):
        self.all = []
        self.load_tiles()

    def load_tiles(self):
        for _ in range(20):
            for tile_type in tile_types:
                self.all.append(Tile(tile_type))

    def tiles_at_location(self, location):
        return [tile for tile in self.all if tile.location == location]


    @property
    def tiles_in_bag(self):
        return self.tiles_at_location(Location.BAG)

    @property
    def tiles_in_discard_pile(self):
        return self.tiles_at_location(Location.DISCARD_PILE)

    def random_tile(self):
        if not self.tiles_in_bag:
            for tile in self.all:
                if tile.location == Location.DISCARD_PILE:
                    tile.location = Location.BAG

        if self.tiles_in_bag:
            tile = choice(self.tiles_in_bag)
            tile.location = Location.DISCARD_PILE
            return tile

        return None

# TODO: Clean this up - very messy - initialise & set_mode called twice
pygame.init()
pygame.display.set_mode((Settings.screen_width, Settings.screen_height))
tile_types = [
    TileType(colour) for colour in ('blue', 'yellow', 'red', 'black', 'white')
]
