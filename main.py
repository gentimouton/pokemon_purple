import pygame
from pygame.color import Color
from pygame.constants import RLEACCEL

from controls import InputController
from level import Level
from player import Player


SCREEN_W, SCREEN_H = 800, 600

def load_sprites():
    # front, back, left, run front, run back, run left
    chars_img = pygame.image.load('assets/character_sprites.png').convert()
    chars_img.set_colorkey(Color(255, 0, 255), RLEACCEL)
    chars_img = pygame.transform.scale2x(chars_img)
    spr_w, spr_h = 16 * 2, 16 * 2
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
        self.player = Player(self.allsprites[0], [self.sprites])
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        pygame.display.flip()
        
    def render(self):
        self.sprites.clear(self.screen, self.bg)
        self.sprites.update(self.fps)
        changed_rects = self.sprites.draw(self.screen)
        pygame.display.update(changed_rects)
        
    def move(self, direction):
        x, y = self.player.x, self.player.y
        if(self.level.is_walkable(x, y, direction) and not self.player.moving_to):
            self.player.move(direction)
    
    def run(self):
        while not self.game_over: 
            self.controller.process_inputs()
            self.render()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    Game().run()
    
