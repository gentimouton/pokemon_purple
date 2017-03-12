import pygame


class EncounterMode():
    def __init__(self, screen):
        self.screen = screen
        self.screen.fill((255, 128, 128))
        pygame.display.flip()
        
    def do_action(self, action):
        """ Return the name of the mode to execute next.
        Return None if mode is unchanged.
        """ 
        print action
        return 'world'
    
    def reset(self):
        pass
    
    def tick(self, fps):
        self.screen.fill((255, 128, 128))
        pygame.display.flip()
        