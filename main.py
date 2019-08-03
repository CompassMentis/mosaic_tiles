import pygame

from game import Game
from settings import Settings

pygame.init()

canvas = pygame.display.set_mode((Settings.screen_width, Settings.screen_height))

game = Game(
    player_details=(
        ('Issie', True),
        ('Hugo', True),
        ('Lucy', True),
        ('Coen', True)
    ),
    canvas=canvas
)

done = False
while not done:
    game.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.process_mouse_click()
