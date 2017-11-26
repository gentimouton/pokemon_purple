import random

import pygame

from controls import InputController
from encounter import EncounterScene
from lib import pview
from scene import SCN_WORLD, SCN_ENCOUNTER
from settings import BASE_RES, FPS
from world import WorldScene


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
        pview.set_mode((BASE_RES, BASE_RES))
        self.screen = pview.screen
        self.scenes = {SCN_WORLD: WorldScene(self),
                      SCN_ENCOUNTER: EncounterScene(self)
                      }
        self.cur_scene = self.scenes[SCN_WORLD]
        
    def process_input(self, action):
        # some scenes change via user actions.
        next_scene = self.cur_scene.process_input(action) 
        # TODO: scene management should happen in scene.py
        if next_scene:
            self.cur_scene.stop()
            self.cur_scene = self.scenes[next_scene]
            self.cur_scene.resume()
    
    def toggle_fullscreen(self):
        # pview.toggle_fullscreen()
        pass
        
        
    def quit_game(self):
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

