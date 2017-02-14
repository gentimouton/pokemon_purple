import pygame

from controls import InputController
from level import Level, TILE_W, TILE_H
from player import Player


def load_sprites(filename, spr_w, spr_h):
    # front, back, left, run front, run back, run left
    chars_img = pygame.image.load(filename).convert()
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
        self.fps = 50
        self.game_over = False
        self.clock = pygame.time.Clock()
        self.controller = InputController(self)
        self.screen = pygame.display.set_mode((24 * TILE_W, 24 * TILE_H))
        self.level = Level()
        self.bg = self.level.pre_render_map()
        self.allsprites = load_sprites('assets/character_sprites.png', TILE_W, TILE_H)
        self.sprites = pygame.sprite.RenderUpdates()
        self.player = Player(self.allsprites[0], [self.sprites])
        self.screen.fill((0, 55, 111))
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
    
