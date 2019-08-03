# import pygame

# from enums import Pattern


class Settings:
    screen_width = 1800
    screen_height = 950

    tile_width = 40
    tile_height = tile_width

    factories_centre = 360, 350
    factories_circle_radius = 250
    factory_circle_radius = 80
    # factory_grid_size = pygame.Rect(5, 5, 0, 0)  # space for 5 x 5 tiles in centre
    # factory_centre_grid_columns = 5
    # factory_centre_grid_rows = factory_centre_grid_columns

    spacing = 10

    grid_colour = 128, 128, 128
    active_grid_colour = 255, 128, 128
    selected_grid_colour = 50, 255, 50
    grid_line_width = 2

    opponent_area_location = 1300, 50
    player_area_location = 400, 450
    player_area_multiplier = 1.8
    area_height = (5 + 2) * tile_height + spacing
    pattern_area_width = (5 + 0.2) * tile_width + spacing

    floor_tile_scores_font_size = 24
    floor_tile_scores_spacing = 8

    # player_board_width = 150
    # player_board_height = 150
    # player_area_location = spacing, spacing

    # @staticmethod
    # def tile_colour(pattern):
    #     return {
    #         Pattern.A: (0.886 * 255, 0.569 * 255, 0.569 * 255), # pygame.Color('red'),
    #         Pattern.B: (0.6 * 255, 0.867 * 255, 0.573 * 255), #  pygame.Color('green'),
    #         Pattern.C: (0.702 * 255, 0.58 * 255, 0.8 * 255), #  pygame.Color('purple'),
    #         Pattern.D: (0.396 * 255, 0.769 * 255, 255),  # pygame.Color('blue'),
    #         Pattern.E: (0.875 * 255, 0.898 * 255, 0.573 * 255) # pygame.Color('yellow')
    #     }[pattern]
