import pygame
from pygame.color import Color
from pygame.constants import RLEACCEL

from character import Character
from controls import InputController
from level import Level, TILE_W, TILE_H
from player import Player


SCREEN_W, SCREEN_H = 512, 512

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


class Game():
    
    def __init__(self):
        pygame.init()
        self.fps = 60
        self.game_over = False
        self.clock = pygame.time.Clock()
        self.controller = InputController(self)
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.level = Level()
        self.bg = self.level.pre_render_map()
        self.allsprites = load_sprites()
        self.sprites = pygame.sprite.RenderUpdates()
        self.player = Player(self.level, self.allsprites[0], [self.sprites])
        char = Character(self.level, self.allsprites[1], [self.sprites])
        self.characters = [char]
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        pygame.display.flip()
        
    def render(self):
        self.sprites.clear(self.screen, self.bg)
        self.sprites.update(self.fps)
        changed_rects = self.sprites.draw(self.screen)
        pygame.display.update(changed_rects)
    
    def do_action(self, action):
        action_to_direction = {'up': 'N', 'down': 'S', 'left': 'W', 'right': 'E'}
        direction = action_to_direction[action]
        self.player.try_moving_towards(direction)
    
    def stop_game(self):
        self.game_over = True
        
    def run(self):
        while not self.game_over: 
            self.controller.process_inputs()
            self.render()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    Game().run()
    
