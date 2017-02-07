import ConfigParser

import pygame
from pygame.constants import QUIT, KEYDOWN, K_ESCAPE


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
    
    
def render_map():
    TILE_WIDTH, TILE_HEIGHT = 16, 16
    cells, cell_types = load_map('assets/level.map')
    width = len(cells[0])
    height = len(cells)
    screen = pygame.display.set_mode((20 * TILE_WIDTH, 20 * TILE_HEIGHT))
    tileset = load_tileset("assets/tileset.png", TILE_WIDTH, TILE_HEIGHT)
    bg = pygame.Surface((width * TILE_WIDTH, height * TILE_HEIGHT))
    for map_y, line in enumerate(cells):
        for map_x, cell_type in enumerate(line):
            tile_x, tile_y = cell_types[cell_type]['tileset_pos'].split(',')
            tile_img = tileset[int(tile_x)][int(tile_y)]
            bg.blit(tile_img, (map_x * TILE_WIDTH, map_y * TILE_HEIGHT))
    return screen, bg


def init():
    pygame.init()
    clock = pygame.time.Clock()
    screen, bg = render_map()    
    return screen, bg, clock


def render(screen, bg):
    screen.fill((0, 0, 111))
    screen.blit(bg, (0, 0))
    pygame.display.update()


def process_inputs():
    game_over = False
    for event in pygame.event.get():  # inputs
        if event.type == QUIT:
            game_over = True
        if event.type == KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                game_over = True
    return game_over


if __name__ == "__main__":
    screen, bg, clock = init()
    game_over = False
    
    while not process_inputs():
        render(screen, bg)
        clock.tick(50)
