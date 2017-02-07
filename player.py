import pygame

TILE_W, TILE_H = 16, 16

dir_vectors = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)        
        self.x, self.y = pos
        self.image = image
        self.rect = pygame.Rect(pos[0] * TILE_W, pos[1] * TILE_H, TILE_W, TILE_H)
        
    def move(self, direction):
        dx, dy = dir_vectors[direction]
        self.x += dx
        self.y += dy
        self.rect.x = self.x * TILE_W
        self.rect.y = self.y * TILE_H  
    
    def update(self):
        pass
    
