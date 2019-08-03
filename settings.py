class Settings:
    screen_width = 1800
    screen_height = 950

    tile_width = 40
    tile_height = tile_width

    factories_centre = 360, 350
    factories_circle_radius = 250
    factory_circle_radius = 80

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
    floor_tile_scores_colour = 90, 90, 90