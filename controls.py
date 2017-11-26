import pygame


BTN_UP = 'up'
BTN_DOWN = 'down'
BTN_LEFT = 'left'
BTN_RIGHT = 'right'
BTN_SUBMIT = 'submit'

_key_mapping = { # maps pygame keys to abstract buttons
    pygame.K_UP: BTN_UP, 
    pygame.K_w: BTN_UP,
    pygame.K_DOWN: BTN_DOWN, 
    pygame.K_s: BTN_DOWN,
    pygame.K_LEFT: BTN_LEFT, 
    pygame.K_a: BTN_LEFT,
    pygame.K_RIGHT: BTN_RIGHT, 
    pygame.K_d: BTN_RIGHT,
    pygame.K_RETURN: BTN_SUBMIT,
    pygame.K_KP_ENTER: BTN_SUBMIT
    }

class InputController():
    
    def __init__(self, game):
        self.game = game
        pygame.key.set_repeat(150, 30)

    def process_inputs(self):
        for event in pygame.event.get():  # inputs
            if event.type == pygame.QUIT:
                self.game.quit_game()
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_ESCAPE:
                    self.game.quit_game()
                elif key == pygame.K_F11: 
                    self.game.toggle_fullscreen()
                elif key in _key_mapping.keys():
                    self.game.process_input(_key_mapping[key])
                # TODO: if prev frame keydowns was [up],
                # and cur frame keydowns is [up,left]
                # then send BTN_LEFT, and stop sending BTN_UP
                # if [up,down], send nothing, etc.