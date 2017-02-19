import pygame

from level import dir_vectors, TILE_W, TILE_H

MOVE_DURATION = 1.0 / 4  # duration of move animation, in seconds

class Character(pygame.sprite.DirtySprite):
    def __init__(self, frames, containers, pos=(0, 0)):
        # frames: 6 images (front, back, left, run front, run back, run left)
        # containers: list of sprite groups to join
        pygame.sprite.DirtySprite.__init__(self, *containers)
        self.x, self.y = pos
        self.moving_to = None  # non null = moving
        self.dir = 'S'
        self.standing_frames = {
            'S': [frames[0]],
            'N': [frames[1]],
            'W': [frames[2]],
            'E': [pygame.transform.flip(frames[2], True, False)]
            }
        self.moving_frames = {
            'S': [frames[3], pygame.transform.flip(frames[3], True, False)],
            'N': [frames[4], pygame.transform.flip(frames[4], True, False)],
            'W': [frames[5]],
            'E': [pygame.transform.flip(frames[5], True, False)]
            }
        self.image = self.standing_frames[self.dir][0]
        self.rect = pygame.Rect(pos[0] * TILE_W, pos[1] * TILE_H, TILE_W, TILE_H)
        self.animation_index = 0
    

    def move(self, direction):
        dx, dy = dir_vectors[direction]
        self.dir = direction
        self.moving_to = dx, dy
        self.animation_index = 0
        
    def update(self, fps):
        if self.moving_to:
            dx, dy = self.moving_to
            if self.animation_index >= int(fps * MOVE_DURATION): # animation is over
                dx, dy = self.moving_to
                self.x += dx
                self.y += dy
                self.animation_index = 0
                self.moving_to = None
            else: # animation is not over yet
                if self.animation_index == 0:
                    self.image = self.standing_frames[self.dir][0]
                elif self.animation_index == int(fps * MOVE_DURATION / 3):
                    # alternate legs/arms when moving N or S
                    if len(self.moving_frames[self.dir]) > 1:
                        self.image = self.moving_frames[self.dir][self.y % 2]
                    else:
                        self.image = self.moving_frames[self.dir][0]
                elif self.animation_index == int(fps * MOVE_DURATION * 2 / 3):
                    self.image = self.standing_frames[self.dir][0]
                self.animation_index += 1
            
            xx = self.x + dx * float(self.animation_index) / fps / MOVE_DURATION
            yy = self.y + dy * float(self.animation_index) / fps / MOVE_DURATION
            self.rect.x = int(xx * TILE_W)
            self.rect.y = int(yy * TILE_H)
        
