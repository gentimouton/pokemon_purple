import pygame


SCN_WORLD = 'world scene'
SCN_ENCOUNTER = 'encounter scene'

class Scene():
    def __init__(self, scene_manager):
        self._scene_manager = scene_manager
        self._screen = pygame.display.get_surface()
    def stop(self):
        pass
    def reset(self, params):
        pass
    def process_input(self):
        pass
    def tick(self):
        pass
    def render(self):
        pass