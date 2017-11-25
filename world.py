import pygame
from pygame.color import Color
from pygame.constants import RLEACCEL

from character import Player, MonsterNPC, WanderingNPC, RockNPC, DIR_N, DIR_S, DIR_E, DIR_W
from controls import BTN_UP, BTN_DOWN, BTN_LEFT, BTN_RIGHT
from level import Level
from scene import Scene, SCN_ENCOUNTER
from settings import TILE_SIZE_PX


class WorldScene(Scene):
    def __init__(self, scene_manager):
        Scene.__init__(self, scene_manager)
        self.level = Level()
        self.bg = self.level.pre_render_map()
        self.allsprites = load_sprites()
        self.sprites = pygame.sprite.LayeredDirty()
        self.player = Player(self.level, self.allsprites[0], [self.sprites], (1, 1))
        monster = MonsterNPC(self.level, self.allsprites[4], [self.sprites], (1, 2))
        girl = WanderingNPC(self.level, self.allsprites[1], [self.sprites], (0, 0))
        rock = RockNPC(self.level, self.allsprites[3], [self.sprites], (3, 3))
        for char in [self.player, girl, rock, monster]:
            self.sprites.change_layer(char, 1)
        #self.resume()

    def resume(self):
        self._screen.fill((0, 0, 0))
        self._screen.blit(self.bg, (0, 0))
        pygame.display.flip()
        for char in self.sprites:
            char.dirty = 1
        
    def process_input(self, action):
        """ Return the name of the scene to execute next.
        Return None if scene is unchanged.
        """
        action_to_dir = {BTN_UP: DIR_N, BTN_DOWN: DIR_S, 
                         BTN_LEFT: DIR_W, BTN_RIGHT: DIR_E}
        if action not in action_to_dir.keys():
            return None

        direction = action_to_dir[action]
        trigger_encounter = self.player.try_moving_towards(direction)
        if trigger_encounter:
            return SCN_ENCOUNTER
        
    def tick(self, fps):
        self.sprites.clear(self._screen, self.bg)
        self.sprites.update(fps)
        changed_rects = self.sprites.draw(self._screen)
        pygame.display.update(changed_rects)
    
    
############################################################
####################   UTILS   #############################
############################################################

def load_sprites():
    # front, back, left, run front, run back, run left
    chars_img = pygame.image.load('assets/character_sprites.png').convert()
    chars_img.set_colorkey(Color(255, 0, 255), RLEACCEL)
    # chars_img = pygame.transform.scale2x(chars_img)
    spr_w, spr_h = TILE_SIZE_PX, TILE_SIZE_PX
    image_w, image_h = chars_img.get_size()
    sprites = []
    for spr_y in range(0, image_h // spr_h):
        line = []
        for spr_x in range(0, image_w // spr_w):
            rect = (spr_x * spr_w, spr_y * spr_h, spr_w, spr_h)
            line.append(chars_img.subsurface(rect))
        sprites.append(line)
    return sprites
