import random

import pygame

from controls import InputController
from encounter import EncounterScene
from scene import SCN_WORLD, SCN_ENCOUNTER
from world import WorldScene


SCREEN_W, SCREEN_H = 16 * 32, 16 * 32  # 16x16 cells of 32px
FPS = 60

random.seed(1)

class Game():
    """ Manage scenes. Tick and forward inputs to current mode.
    A Mode must have resume(), process_input(action), and tick(FPS).
    """
    def __init__(self):
        pygame.init()
        self.game_over = False
        self.clock = pygame.time.Clock()
        self.controller = InputController(self)
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.scenes = {SCN_WORLD: WorldScene(self.screen),
                      SCN_ENCOUNTER: EncounterScene(self.screen)
                      }
        self.cur_scene = self.scenes[SCN_WORLD]
        
    def process_input(self, action):
        # some scenes change via user actions.
        next_scene = self.cur_scene.process_input(action)
        if next_scene:
            self.cur_scene.stop()
            self.cur_scene = self.scenes[next_scene]
            self.cur_scene.resume()
        
    def stop_game(self):
        self.game_over = True
        
    def run(self):
        while not self.game_over: 
            self.controller.process_inputs()
            # some scenes change via timers or NPC actions.
            next_scene = self.cur_scene.tick(FPS)
            if next_scene:
                self.cur_scene = self.scenes[next_scene]
                self.cur_scene.resume()
            self.clock.tick(FPS)
            
if __name__ == "__main__":
    Game().run()
