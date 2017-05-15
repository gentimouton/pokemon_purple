import random

import pygame

from controls import InputController
from encounter import EncounterMode
from world import WorldMode


SCREEN_W, SCREEN_H = 16 * 32, 16 * 32  # 16x16 cells of 32px
FPS = 60

random.seed(1)

class Game():
    """ Manage modes. Tick and forward inputs to current mode.
    A Mode must have resume(), process_action(action), and tick(FPS).
    """
    def __init__(self):
        pygame.init()
        self.game_over = False
        self.clock = pygame.time.Clock()
        self.controller = InputController(self)
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.modes = {'world': WorldMode(self.screen),
                      'encounter': EncounterMode(self.screen)
                      }
        self.cur_mode = self.modes['world']
        
    def do_action(self, action):
        # some modes change via user actions.
        next_mode = self.cur_mode.process_action(action)
        if next_mode:
            self.cur_mode = self.modes[next_mode]
            self.cur_mode.resume()
        
    def stop_game(self):
        self.game_over = True
        
    def run(self):
        while not self.game_over: 
            self.controller.process_inputs()
            # some modes change via timers.
            next_mode = self.cur_mode.tick(FPS)
            if next_mode:
                self.cur_mode = self.modes[next_mode]
                self.cur_mode.resume()
            self.clock.tick(FPS)
            
if __name__ == "__main__":
    Game().run()
