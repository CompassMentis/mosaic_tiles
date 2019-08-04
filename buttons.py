import pygame

from settings import Settings

class Button:
    def __init__(self, game, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(Settings.active_grid_colour)
        self.can_click = True

        spacing = Settings.floor_tile_scores_spacing * Settings.player_area_multiplier
        self.image.blit(
            game.button_font.render(text, True, pygame.Color('white')), #  Settings.floor_tile_scores_colour),
            (spacing, spacing)
        )

        pygame.draw.rect(
            self.image,
            pygame.Color('white'),
            (0, 0, self.rect.width, self.rect.height),
            Settings.grid_line_width
        )
