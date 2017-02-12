import pygame

from level import dir_vectors, TILE_W, TILE_H


class Player(pygame.sprite.Sprite):
    def __init__(self, frames, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)        
        self.x, self.y = pos
        self.dir = 'S'
        self.standing_frames = {
            'S': frames[0],
            'N': frames[1],
            'W': frames[2],
            'E': pygame.transform.flip(frames[2], True, False)
            }
        self.running_frames = {
            'S': frames[3],
            'N': frames[4],
            'W': frames[5],
            'E': pygame.transform.flip(frames[5], True, False)
            }
        self.image = self.standing_frames[self.dir]
        self.rect = pygame.Rect(pos[0] * TILE_W, pos[1] * TILE_H, TILE_W, TILE_H)
        
    def move(self, direction):
        dx, dy = dir_vectors[direction]
        self.image = self.standing_frames[direction]
        self.x += dx
        self.y += dy
        self.rect.x = self.x * TILE_W
        self.rect.y = self.y * TILE_H  
    
    def update(self):
        pass
    
