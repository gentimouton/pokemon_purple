import random

import pygame
from pygame.color import Color
from pygame.constants import RLEACCEL

from character import RockNPC, WanderingNPC, MonsterNPC, Player
from controls import InputController
from level import Level, TILE_W, TILE_H


SCREEN_W, SCREEN_H = 512, 512
FPS = 60

random.seed(1)

def load_sprites():
    # front, back, left, run front, run back, run left
    chars_img = pygame.image.load('assets/character_sprites.png').convert()
    chars_img.set_colorkey(Color(255, 0, 255), RLEACCEL)
    chars_img = pygame.transform.scale2x(chars_img)
    spr_w, spr_h = TILE_W, TILE_H
    image_w, image_h = chars_img.get_size()
    sprites = []
    for spr_y in range(0, image_h / spr_h):
        line = []
        for spr_x in range(0, image_w / spr_w):
            rect = (spr_x * spr_w, spr_y * spr_h, spr_w, spr_h)
            line.append(chars_img.subsurface(rect))
        sprites.append(line)
    return sprites


class Mode():
    def __init__(self, screen):
        self.screen = screen
        
    def render(self):
        pass
    
    def reset(self):
        pass
        
class EncounterMode(Mode):
    def __init__(self, screen):
        Mode.__init__(self, screen)
        self.screen.fill((255, 128, 128))
        pygame.display.flip()
        
    def do_action(self, action):
        """ Return the name of the mode to execute next.
        Return None if mode is unchanged.
        """ 
        print action
        return 'world'
    
    def render(self):
        self.screen.fill((255, 128, 128))
        pygame.display.flip()
        

class WorldMode(Mode):
    def __init__(self, screen):
        Mode.__init__(self, screen)
        self.level = Level()
        self.bg = self.level.pre_render_map()
        self.allsprites = load_sprites()
        self.sprites = pygame.sprite.LayeredDirty()
        self.player = Player(self.level, self.allsprites[0], [self.sprites], (1, 1))
        girl = WanderingNPC(self.level, self.allsprites[1], [self.sprites], (0, 0))
        rock = RockNPC(self.level, self.allsprites[3], [self.sprites], (1, 2))
        monster = MonsterNPC(self.level, self.allsprites[4], [self.sprites], (3, 3))
        for char in [self.player, girl, rock, monster]:
            self.sprites.change_layer(char, 1)
        self.reset()
        
    def reset(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        for char in self.sprites:
            char.dirty = 1
        pygame.display.flip()
        
    def do_action(self, action):
        """ Return the name of the mode to execute next.
        Return None if mode is unchanged.
        """
        action_to_dir = {'up': 'N', 'down': 'S', 'left': 'W', 'right': 'E'}
        direction = action_to_dir[action]
        trigger_encounter = self.player.try_moving_towards(direction)
        if trigger_encounter:
            return 'encounter'
    
    def render(self):
        self.sprites.clear(self.screen, self.bg)
        self.sprites.update(FPS)
        changed_rects = self.sprites.draw(self.screen)
        pygame.display.update(changed_rects)
    
    
class Game():
    
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
        next_mode = self.cur_mode.do_action(action)
        if next_mode:
            self.cur_mode = self.modes[next_mode]
            self.cur_mode.reset()
        
    def stop_game(self):
        self.game_over = True
        
    def run(self):
        while not self.game_over: 
            self.controller.process_inputs()
            self.cur_mode.render()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()
    
