import pygame

from level import dir_vectors, TILE_W, TILE_H


class Player(pygame.sprite.DirtySprite):
    def __init__(self, frames, containers, pos=(0, 0)):
        pygame.sprite.DirtySprite.__init__(self, *containers)   
        self.x, self.y = pos
        self.moving_to = None  # non null = moving
        self.dir = 'S'
        self.standing_frames = {
            'S': frames[0],
            'N': frames[1],
            'W': frames[2],
            'E': pygame.transform.flip(frames[2], True, False)
            }
        self.moving_frames = {
            'S': frames[3],
            'N': frames[4],
            'W': frames[5],
            'E': pygame.transform.flip(frames[5], True, False)
            }
        self.image = self.standing_frames[self.dir]
        self.rect = pygame.Rect(pos[0] * TILE_W, pos[1] * TILE_H, TILE_W, TILE_H)
        self.animation_index = 0
    

    def move(self, direction):
        dx, dy = dir_vectors[direction]
        self.dir = direction
        self.moving_to = dx, dy
        self.animation_index = 0
        
    def update(self, fps):
        if self.moving_to:
            # move animation lasts half a second
            dx, dy = self.moving_to
            if self.animation_index < fps / 12:
                self.animation_index += 1
                self.image = self.standing_frames[self.dir]
            elif self.animation_index < fps * 2 / 12:
                self.animation_index += 1
                self.image = self.moving_frames[self.dir]
            elif self.animation_index < fps * 3 / 12:
                self.image = self.standing_frames[self.dir]
                self.animation_index += 1
            else:  # actually move at end of animation 
                dx, dy = self.moving_to
                self.x += dx
                self.y += dy
                self.animation_index = 0
                self.moving_to = None
            xx = self.x + dx * float(self.animation_index) / fps * 12 / 3
            yy = self.y + dy * float(self.animation_index) / fps * 12 / 3
            self.rect.x = int(xx * TILE_W)
            self.rect.y = int(yy * TILE_H)           
        
