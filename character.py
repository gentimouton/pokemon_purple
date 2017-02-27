import random

import pygame

from level import dir_vectors, TILE_W, TILE_H


class Character(pygame.sprite.DirtySprite):
    def __init__(self, level, frames, containers, pos=(0, 0)):
        # frames: 6 images (front, back, left, run front, run back, run left)
        # containers: list of sprite groups to join
        pygame.sprite.DirtySprite.__init__(self, *containers)
        self.pushable = False
        self.x, self.y = pos
        self._moving_delta = None  # non null = moving
        self._moving_from = None
        self.is_moving = False
        self.base_move_speed = 1.0  # cells per second
        self._move_speed = self.base_move_speed 
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
        self.level = level
        self.level.move_character_to(self, self.pos)
    
    def _get_pos(self):
        return self.x, self.y
    def _set_pos(self, pos):
        self.x, self.y = pos
    pos = property(_get_pos, _set_pos)
            
    
    def start_motion(self, target_pos, delta, speed):
        self._moving_delta = delta
        self._move_speed = speed
        self._moving_from = self.x, self.y
        self.is_moving = True
        self.pos = target_pos
        self.animation_index = 0
        
        
    def move_towards(self, direction):
        if self._moving_delta:
            return
        
        self.dir = direction
        level = self.level
        target_pos, speed_adjustment, delta = level.get_destination(self.pos, direction)
        speed = self.base_move_speed * speed_adjustment
        npc = self.level.get_occupancy(target_pos)
        
        if speed_adjustment == 0:  # terrain is blocking
            delta = 0, 0
            target_pos = self.pos
            speed = self.base_move_speed
        elif npc:  # terrain not blocking, but NPC on destination
            npc_target_pos, npc_speed_adj, npc_delta = level.get_destination(target_pos, direction)
            third_npc = level.get_occupancy(npc_target_pos)
            if npc.pushable and npc_speed_adj and not third_npc:  # NPC can be pushed
                speed = min(speed, npc.base_move_speed * npc_speed_adj)
                npc.start_motion(npc_target_pos, npc_delta, speed)
                level.move_character_to(npc, npc_target_pos)
            else:
                delta = 0, 0
                target_pos = self.pos
    
        self.start_motion(target_pos, delta, speed)
        level.move_character_to(self, target_pos)

    
    def update(self, fps):
        # moving logic
        if self._moving_delta:
            dx, dy = self._moving_delta
            if self.animation_index >= int(fps / self._move_speed):  # animation is over
                self.animation_index = 0
                self._moving_delta = None
                self._moving_from = None
                self.is_moving = False
            else:  # animation is not over yet
                if self.animation_index == 0:
                    self.image = self.standing_frames[self.dir][0]
                elif self.animation_index == int(fps / self._move_speed / 4):
                    # alternate legs/arms when moving N or S
                    if len(self.moving_frames[self.dir]) > 1:
                        self.image = self.moving_frames[self.dir][self.y % 2]
                    else:
                        self.image = self.moving_frames[self.dir][0]
                elif self.animation_index == int(fps / self._move_speed * 3 / 4):
                    self.image = self.standing_frames[self.dir][0]
                self.animation_index += 1
                
                old_x, old_y = self._moving_from
                xx = old_x + dx * float(self.animation_index) / fps * self._move_speed
                yy = old_y + dy * float(self.animation_index) / fps * self._move_speed
                self.rect.x = int(xx * TILE_W)
                self.rect.y = int(yy * TILE_H)
            


class WanderingNPC(Character):
    def __init__(self, level, frames, containers, pos=(0, 0)):
        Character.__init__(self, level, frames, containers, pos)
        self.move_timer = 0
        
    def update(self, fps):
        Character.update(self, fps)
        if self.move_timer == 0:
            direction = random.choice(dir_vectors.keys())
            self.move_towards(direction)
            self.move_timer = fps * 4  # try moving every 4 seconds
        else:
            self.move_timer -= 1
            

class RockNPC(Character):
    def __init__(self, level, frames, containers, pos=(0, 0)):
        Character.__init__(self, level, frames, containers, pos)
        self.pushable = True
        self.base_move_speed = 2 # cells per second
    

    
