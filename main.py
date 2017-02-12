import pygame

from controls import process_inputs
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
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((12 * TILE_W, 12 * TILE_H))
        self.level = Level()
        self.bg = self.level.pre_render_map()
        self.sprites = load_sprites('assets/character_sprites.png', TILE_W, TILE_H)
        self.player = Player(self.sprites[0])
        self.allsprites = pygame.sprite.Group((self.player))

        
    def render(self):
        self.screen.fill((0, 55, 111))
        self.screen.blit(self.bg, (0, 0))
        # self.player.update()
        self.allsprites.draw(self.screen)
        pygame.display.update()
    
    def move(self, direction):
        x, y = self.player.x, self.player.y
        if(self.level.is_walkable(x, y, direction)):
            self.player.move(direction)
    
    def run(self):
        while not process_inputs(self):
            self.render()
            self.clock.tick(50)


if __name__ == "__main__":
    Game().run()
    
