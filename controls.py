import pygame
from pygame.constants import QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, \
    K_RIGHT, K_w, K_s, K_a, K_d, K_RETURN


_key_mapping = { # maps pygame key to abstract controller action
    K_UP: 'up', 
    K_w: 'up',
    K_DOWN: 'down', 
    K_s: 'down',
    K_LEFT: 'left', 
    K_a: 'left',
    K_RIGHT: 'right', 
    K_d: 'right',
    K_RETURN: 'enter'
    }

class InputController():
    
    def __init__(self, game):
        self.game = game
        pygame.key.set_repeat(150, 30)

    def process_inputs(self):
        for event in pygame.event.get():  # inputs
            if event.type == QUIT:
                self.game.stop_game()
            if event.type == KEYDOWN:
                key = event.key
                if key == K_ESCAPE:
                    self.game.stop_game()
                elif key in _key_mapping.keys():
                    self.game.do_action(_key_mapping[key])        
