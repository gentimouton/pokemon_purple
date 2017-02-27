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
        self._animation_index = 0
        self.level = level
        self.level.move_character_to(self, self.pos)
    
    
    def _get_pos(self):
        return self.x, self.y
    def _set_pos(self, pos):
        self.x, self.y = pos
    pos = property(_get_pos, _set_pos)
            
    
    def start_motion(self, target_pos, delta, speed1, speed2):
        self._moving_from = self.pos
        self.pos = target_pos
        self._moving_delta = delta
        self._move_speed = speed1
        self.is_moving = True
        self._animation_index = 0
        
    
    def compute_movement(self):
        pass
    
    def move_towards(self, direction):
        if self.is_moving:
            return # cant move if animation in progress
        
        self.dir = direction
        level = self.level
        
        target_pos, delta = level.get_destination(self.pos, direction)
        
        if target_pos == None: # going out of bounds
            delta = 0, 0
            target_pos = self.pos
            speed1 = speed2 = self.base_move_speed
        else:
            speed_penalty = level.get_terrain_penalty(target_pos)
            if speed_penalty == 1:  # terrain is blocking
                delta = 0, 0
                target_pos = self.pos
                speed1 = speed2 = self.base_move_speed
            else:
                npc = self.level.get_occupancy(target_pos)
                if npc == None: # regular move
                    # delta and target_pos are correct, stay unchanged
                    speed1 = speed2 = self.base_move_speed * (1 - speed_penalty)
                else: # terrain not blocking, but NPC on destination
                    npc_target_pos, npc_delta = level.get_destination(target_pos, direction)
                    if npc_target_pos == None: # NPC will go out of bounds
                        delta = 0, 0
                        target_pos = self.pos
                        speed1 = speed2 = self.base_move_speed
                    else:
                        npc_penalty = level.get_terrain_penalty(npc_target_pos)
                        third_npc = level.get_occupancy(npc_target_pos)
                        if npc.pushable and npc_penalty != 1 and not third_npc:  # can push
                            speed = self.base_move_speed * (1 - speed_penalty)
                            npc_speed = npc.base_move_speed * (1 - npc_penalty)
                            speed1 = speed2 = min(speed, npc_speed)
                            npc.start_motion(npc_target_pos, npc_delta, speed1, speed2)
                            level.move_character_to(npc, npc_target_pos)
                        else:
                            delta = 0, 0
                            target_pos = self.pos
                            speed1 = speed2 = self.base_move_speed

    
        self.start_motion(target_pos, delta, speed1, speed2)
        level.move_character_to(self, target_pos)

    
    def update(self, fps):
        # moving logic
        if self._moving_delta:
            dx, dy = self._moving_delta
            if self._animation_index >= int(fps / self._move_speed):  # animation is over
                self._animation_index = 0
                self._moving_delta = None
                self._moving_from = None
                self.is_moving = False
            else:  # animation is not over yet
                if self._animation_index == 0:
                    self.image = self.standing_frames[self.dir][0]
                elif self._animation_index == int(fps / self._move_speed / 4):
                    # alternate legs/arms when moving N or S
                    if len(self.moving_frames[self.dir]) > 1:
                        self.image = self.moving_frames[self.dir][self.y % 2]
                    else:
                        self.image = self.moving_frames[self.dir][0]
                elif self._animation_index == int(fps / self._move_speed * 3 / 4):
                    self.image = self.standing_frames[self.dir][0]
                self._animation_index += 1
                
                old_x, old_y = self._moving_from
                xx = old_x + dx * float(self._animation_index) / fps * self._move_speed
                yy = old_y + dy * float(self._animation_index) / fps * self._move_speed
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
        self.base_move_speed = 2  # cells per second
    

    
