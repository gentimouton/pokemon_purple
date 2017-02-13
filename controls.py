import pygame
from pygame.constants import QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, \
    K_RIGHT, K_w, K_s, K_a, K_d


class InputController():
    
    def __init__(self, game):
        self.game = game
        pygame.key.set_repeat(100, 25)

    def process_inputs(self):
        for event in pygame.event.get():  # inputs
            if event.type == QUIT:
                self.game.game_over = True
            if event.type == KEYDOWN:
                key = event.key
                if key == K_ESCAPE:
                    self.game.game_over = True
                elif key in (K_UP, K_w):
                    self.game.move('N')
                elif key in (K_DOWN, K_s):
                    self.game.move('S')
                elif key in (K_LEFT, K_a):
                    self.game.move('W')
                elif key in (K_RIGHT, K_d):
                    self.game.move('E')
        
