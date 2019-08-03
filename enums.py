from enum import Enum


# class Pattern(Enum):
#     A = 1
#     B = 2
#     C = 3
#     D = 4
#     E = 5


class Location(Enum):
    DISCARD_PILE = 1
    BAG = 2


class GameMode(Enum):
    SELECTING_TILE = 1
    SELECTING_TARGET = 2
    AWAITING_CONFIRMATION = 3
    MOVING_TILES = 4
