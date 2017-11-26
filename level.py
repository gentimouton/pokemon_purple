from configparser import ConfigParser

import pygame

from settings import BASE_RES
from utils import load_spritesheet_flat


DIR_N = 'N'
DIR_S = 'S'
DIR_E = 'E'
DIR_W = 'W'
dir_vectors = {DIR_N: (0, -1), DIR_S: (0, 1), DIR_E: (1, 0), DIR_W: (-1, 0)}

N_TILES = 16  # square levels of 16x16 tiles
tile_size = BASE_RES // N_TILES


def load_map(filename):
    # TODO: use JSON instead?
    tile_types = {}
    parser = ConfigParser()
    parser.read(filename)
    tiles = parser.get("level", "tiles").split("\n")
    for section in parser.sections():
        if len(section) == 1:  # single char = tile type
            tile_types[section] = dict(parser.items(section))
    return tiles, tile_types
        
        
class Level():
    def __init__(self):
        self.tiles, self.tile_types = load_map('assets/level.map')
        w, h = len(self.tiles[0]), len(self.tiles)
        self.w, self.h = w, h
        self.characters = {}
        self.occupancy = [[None for _ in range(h)] for _ in range(w)]  # map pos to char

        
    def pre_render_map(self):
        tileset = load_spritesheet_flat('assets/tileset.png')
        bg = pygame.Surface((self.w * tile_size, self.h * tile_size))
        for map_y, line in enumerate(self.tiles):
            for map_x, tile_type in enumerate(line):
                tileset_id = int(self.tile_types[tile_type]['tileset_id'])
                tile_img = tileset[tileset_id]
                bg.blit(tile_img, (map_x * tile_size, map_y * tile_size))
        return bg
    
    def get_terrain_penalty(self, pos):
        # return 1 if can't walk, 0 if full speed, 0.5 if half speed.
        x, y = pos
        tile_type = self.tiles[y][x]
        walkable = self.tile_types[tile_type]['walkable'] in ('true', 'True')
        if not walkable:
            penalty = 1 
        elif self.tile_types[tile_type]['name'] == 'grass': 
            penalty = 0.5  # 50% speed on grass
        else:
            penalty = 0
        return penalty
    
    
    def get_destination(self, cur_pos, direction):
        # return new position, delta to get there
        dx, dy = dir_vectors[direction]
        x, y = cur_pos
        newx, newy = x + dx, y + dy
        if newy < 0 or newy >= self.w or newx < 0 or newx >= self.h:
            return None, None
        else:
            return (newx, newy), (dx, dy)
        
    
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
        
