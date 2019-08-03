from enum import Enum


class Location(Enum):
    DISCARD_PILE = 1
    BAG = 2


class GameMode(Enum):
    SELECTING_TILE = 1
    SELECTING_TARGET = 2
    AWAITING_CONFIRMATION = 3
    MOVING_TILES = 4
