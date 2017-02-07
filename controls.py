import pygame
from pygame.constants import QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, \
    K_RIGHT


def process_inputs(game):
    game_over = False
    for event in pygame.event.get():  # inputs
        if event.type == QUIT:
            game_over = True
        if event.type == KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                game_over = True
            elif key == K_UP:
                game.move('N')
            elif key == K_DOWN:
                game.move('S')
            elif key == K_LEFT:
                game.move('W')
            elif key == K_RIGHT:
                game.move('E')
    return game_over
