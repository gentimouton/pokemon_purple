import ConfigParser

import pygame

TILE_W, TILE_H = 16, 16

dir_vectors = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}


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
    cell_types = {}
    parser = ConfigParser.ConfigParser()
    parser.read(filename)
    cells = parser.get("level", "cells").split("\n")
    for section in parser.sections():
        if len(section) == 1:  # single char = cell type
            cell_types[section] = dict(parser.items(section))
    return cells, cell_types
        
        
class Level():
    def __init__(self):
        cells, cell_types = load_map('assets/level.map')
        self.cells = cells
        self.cell_types = cell_types
        self.w, self.h = len(cells[0]), len(cells)
        
    def pre_render_map(self):
        tileset = load_tileset("assets/tileset.png", TILE_W, TILE_H)
        bg = pygame.Surface((self.w * TILE_W, self.h * TILE_H))
        for map_y, line in enumerate(self.cells):
            for map_x, cell_type in enumerate(line):
                tile_x, tile_y = self.cell_types[cell_type]['tileset_pos'].split(',')
                tile_img = tileset[int(tile_x)][int(tile_y)]
                bg.blit(tile_img, (map_x * TILE_W, map_y * TILE_H))
        return bg
    
    def is_walkable(self, x, y, direction):
        dx, dy = dir_vectors[direction]
        if y + dy < 0 or y + dy >= self.w or x + dx < 0 or x + dx >= self.h:
            return False # out of bounds
        cell_type = self.cells[y + dy][x + dx]        
        is_walkable = self.cell_types[cell_type]['walkable'] in ('true', 'True')
        return is_walkable
