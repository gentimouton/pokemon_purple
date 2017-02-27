import ConfigParser

import pygame


TILE_W, TILE_H = 16 * 2, 16 * 2  # 16x16 tiles and 2x zoom

dir_vectors = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}


def load_tileset():
    tileset_img = pygame.image.load('assets/tileset.png').convert()
    tileset_img = pygame.transform.scale2x(tileset_img)
    tile_w, tile_h = TILE_W, TILE_H
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
        self.cells, self.cell_types = load_map('assets/level.map')
        w, h = len(self.cells[0]), len(self.cells)
        self.w, self.h = w, h
        self.characters = {}
        self.occupancy = [[None for _ in range(h)] for _ in range(w)]  # map pos to char

        
    def pre_render_map(self):
        tileset = load_tileset()
        bg = pygame.Surface((self.w * TILE_W, self.h * TILE_H))
        for map_y, line in enumerate(self.cells):
            for map_x, cell_type in enumerate(line):
                tile_x, tile_y = self.cell_types[cell_type]['tileset_pos'].split(',')
                tile_img = tileset[int(tile_x)][int(tile_y)]
                bg.blit(tile_img, (map_x * TILE_W, map_y * TILE_H))
        return bg
    
    
    def get_destination(self, cur_pos, direction):
        # return how much faster/slower it is to walk to the destination cell.
        # < 1 means slower, > 1 is faster than normal.
        # return 0 if can't be walked to.
        dx, dy = dir_vectors[direction]
        x, y = cur_pos
        newx, newy = x + dx, y + dy
        if newy < 0 or newy >= self.w or newx < 0 or newx >= self.h:
            walkable = False  # out of bounds
        else:
            cell_type = self.cells[newy][newx]
            walkable = self.cell_types[cell_type]['walkable'] in ('true', 'True')
        
        if not walkable:
            speed_adjustment = 0 
        elif self.cell_types[cell_type]['name'] == 'grass': # half speed on grass
            speed_adjustment = 0.5
        else:
            speed_adjustment = 1
        return (newx, newy), speed_adjustment, (dx, dy)
    
    
    def get_occupancy(self, pos):
        x, y = pos
        target_char = self.occupancy[x][y]
        return target_char
    

    def move_character_to(self, char, pos):
        x, y = pos
        if char in self.characters.keys():
            oldx, oldy = self.characters[char]
            self.occupancy[oldx][oldy] = None
        self.occupancy[x][y] = char
        self.characters[char] = pos
        
