import pygame

from settings import Settings


class Player:
    def __init__(self, name, order, is_human):
        self.name = name
        self.order = order
        self.is_human = is_human
        self.points = 0

    def show_score(self, game):
        # TODO - Refactor? Don't pass in canvas, maybe create local reference to game instead?
        # TODO - Refactor - a lot of code copied from locations.FloorLocation
        # TODO - Refactor - rename score to player_id?
        if self.order == 0:
            x, y = Settings.player_area_location
            multiplier = Settings.player_area_multiplier
            font = game.large_floor_tile_scores_font
        else:
            x, y = Settings.opponent_area_location
            y += (self.order - 1) * Settings.area_height
            multiplier = 1
            font = game.small_floor_tile_scores_font
        x += 9 * Settings.tile_width * multiplier
        y += (Settings.area_height - Settings.tile_height * 1.9) * multiplier

        width, height = Settings.tile_width, Settings.tile_height
        if self.order == 0:
            width *= Settings.player_area_multiplier
            height *= Settings.player_area_multiplier

        pygame.draw.rect(
            game.canvas,
            pygame.Color('white'),  # TODO: move to Settings?
            (x, y, width, height),
            Settings.grid_line_width
        )

        game.canvas.blit(
            font.render('{:2}'.format(self.points), True, Settings.floor_tile_scores_colour),
            (
                x + Settings.floor_tile_scores_spacing * multiplier,
                y + Settings.floor_tile_scores_spacing * multiplier
            )
        )
