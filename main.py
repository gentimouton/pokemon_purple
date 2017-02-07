import ConfigParser

import pygame

from controls import process_inputs
from player import Player


TILE_W, TILE_H = 16, 16

def load_sprites(filename, spr_w, spr_h):
    # front, back, left, run front, run back, run left
    chars_img = pygame.image.load(filename).convert()
    image_w, image_h = chars_img.get_size()
    sprites = []
    for spr_x in range(0, image_w / spr_w):
        line = []
        for spr_y in range(0, image_h / spr_h):
            rect = (spr_x * spr_w, spr_y * spr_h, spr_w, spr_h)
            line.append(chars_img.subsurface(rect))
        sprites.append(line)
    return sprites

def load_tileset(filename, tile_w, tile_h):
    tileset_img = pygame.image.load(filename).convert()
    image_w, image_h = tileset_img.get_size()
    tileset = []
    for tile_x in range(0, image_w / tile_w):
        line = []
        for tile_y in range(0, image_h / tile_h):
            rect = (tile_x * tile_w, tile_y * tile_h, tile_w, tile_h)
            line.append(tileset_img.subsurface(rect))
        tileset.append(line)
    return tileset


def load_map(filename):
    key = {}
    parser = ConfigParser.ConfigParser()
    parser.read(filename)
    cells = parser.get("level", "cells").split("\n")
    for section in parser.sections():
        if len(section) == 1:
            desc = dict(parser.items(section))
            key[section] = desc
    return cells, key
    
    
def pre_render_map():
    cells, cell_types = load_map('assets/level.map')
    width, height = len(cells[0]), len(cells)
    tileset = load_tileset("assets/tileset.png", TILE_W, TILE_H)
    bg = pygame.Surface((width * TILE_W, height * TILE_H))
    for map_y, line in enumerate(cells):
        for map_x, cell_type in enumerate(line):
            tile_x, tile_y = cell_types[cell_type]['tileset_pos'].split(',')
            tile_img = tileset[int(tile_x)][int(tile_y)]
            bg.blit(tile_img, (map_x * TILE_W, map_y * TILE_H))
    return bg


class Game():
    
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((12 * TILE_W, 12 * TILE_H))
        self.bg = pre_render_map()
        self.sprites = load_sprites('assets/character_sprites.png', TILE_W, TILE_H)
        self.player = Player(self.sprites[0][0])
        self.allsprites = pygame.sprite.Group((self.player))

        
    def render(self):
        self.screen.fill((0, 0, 111))
        self.screen.blit(self.bg, (0, 0))
        # self.player.update()
        self.allsprites.draw(self.screen)
        pygame.display.update()
    
    def move(self, direction):
        self.player.move(direction)
    
    def run(self):
        while not process_inputs(self):  # TODO: make this a queue of events
            # and process events one by one in this loop
            self.render()
            self.clock.tick(50)


if __name__ == "__main__":
    Game().run()
    
