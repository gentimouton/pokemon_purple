import pygame
from pygame.constants import QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, \
    K_RIGHT, K_w, K_s, K_a, K_d, K_RETURN, K_KP_ENTER



BTN_UP = 'up'
BTN_DOWN = 'down'
BTN_LEFT = 'left'
BTN_RIGHT = 'right'
BTN_SUBMIT = 'submit'

_key_mapping = { # maps pygame keys to abstract buttons
    K_UP: BTN_UP, 
    K_w: BTN_UP,
    K_DOWN: BTN_DOWN, 
    K_s: BTN_DOWN,
    K_LEFT: BTN_LEFT, 
    K_a: BTN_LEFT,
    K_RIGHT: BTN_RIGHT, 
    K_d: BTN_RIGHT,
    K_RETURN: BTN_SUBMIT,
    K_KP_ENTER: BTN_SUBMIT
    }

class InputController():
    
    def __init__(self, game):
        self.game = game
        pygame.key.set_repeat(150, 30)

    def process_inputs(self):
        for event in pygame.event.get():  # inputs
            if event.type == QUIT:
                self.game.quit_game()
            if event.type == KEYDOWN:
                key = event.key
                if key == K_ESCAPE:
                    self.game.quit_game()
                elif key in _key_mapping.keys():
                    self.game.process_input(_key_mapping[key])        
