import random

import pygame

from level import dir_vectors, DIR_S, DIR_N, DIR_W, DIR_E
from settings import TILE_SIZE_PX


WACT_OUTCOME_STAY = 'stay'
WACT_OUTCOME_MOVE = 'move' 
WACT_OUTCOME_ENCOUNTER = 'encounter'

class Character(pygame.sprite.DirtySprite):
    pushable = False
    is_monster = False # encounters need 2 Characters: 1 player and 1 monster 
    is_player = False 
    base_move_speed = 1.0  # cells per second
    base_move_period = 5  # move every 4 seconds
    
    def __init__(self, level, frames, containers, pos=(0, 0)):
        # frames: 6 images (front, back, left, run front, run back, run left)
        # containers: list of sprite groups to join
        pygame.sprite.DirtySprite.__init__(self, *containers)
        self.x, self.y = pos
        self._moving_delta = None  # non null = moving
        self._moving_from = None
        self.is_moving = False
        self._inbound_speed = self._outbound_speed = self.base_move_speed 
        self.dir = DIR_S
        self.standing_frames = {
            DIR_S: [frames[0]],
            DIR_N: [frames[1]],
            DIR_W: [frames[2]],
            DIR_E: [pygame.transform.flip(frames[2], True, False)]
            }
        self.moving_frames = {
            DIR_S: [frames[3], pygame.transform.flip(frames[3], True, False)],
            DIR_N: [frames[4], pygame.transform.flip(frames[4], True, False)],
            DIR_W: [frames[5]],
            DIR_E: [pygame.transform.flip(frames[5], True, False)]
            }
        self.image = self.standing_frames[self.dir][0]
        self.rect = pygame.Rect(pos[0] * TILE_SIZE_PX, pos[1] * TILE_SIZE_PX, 
                                TILE_SIZE_PX, TILE_SIZE_PX)
        self._animation_index = 0
        self.level = level
        self.level.move_character_to(self, self.pos)
        self.dirty = 1
    
    
    def _get_pos(self):
        return self.x, self.y
    def _set_pos(self, pos):
        self.x, self.y = pos
    pos = property(_get_pos, _set_pos)
            
    
    def try_moving_towards(self, direction):
        """ Make the character move. 
        Return whether the move triggered an encounter.
        """
        if self.is_moving:
            return  # cant move if animation in progress
        self.dir = direction  # face the direction even if staying in place
        outcome, pos, delta, in_speed, out_speed = self.compute_movement(direction)
        if outcome in (WACT_OUTCOME_STAY, WACT_OUTCOME_MOVE):
            self.start_motion(pos, delta, in_speed, out_speed)
            self.level.move_character_to(self, pos)
        return 0

    def compute_movement(self, direction):
        """ Return outcome, future pos, and the delta and speed to get there
        possible outcomes: WACT_OUTCOME_STAY and such
        """
        level = self.level
        target_pos, delta = level.get_destination(self.pos, direction)
        
        if target_pos == None:  # I am trying to go out of bounds
            speed = self.base_move_speed
            return WACT_OUTCOME_STAY, self.pos, (0, 0), speed, speed
        
        destination_speed_penalty = level.get_terrain_penalty(target_pos)
        if destination_speed_penalty == 1:  # terrain is blocking me
            speed = self.base_move_speed
            return WACT_OUTCOME_STAY, self.pos, (0, 0), speed, speed
        
        target = self.level.get_occupancy(target_pos)
        if target == None:  # terrain not blocking and no NPC on the way
            # delta and target_pos are correct and stay unchanged
            out_speed = self.base_move_speed * (1 - destination_speed_penalty)
            local_speed_penalty = level.get_terrain_penalty(self.pos)
            in_speed = self.base_move_speed * (1 - local_speed_penalty)
            speed = self.base_move_speed
            return WACT_OUTCOME_MOVE, target_pos, delta, in_speed, out_speed
        
        # terrain not blocking, but monster on destination cell
        if target.is_monster:
            speed = self.base_move_speed
            return WACT_OUTCOME_ENCOUNTER, self.pos, (0, 0), speed, speed 

        # target not monster. Can it move?    
        npc_target_pos, npc_delta = level.get_destination(target_pos, direction)
        # NPCs and monsters cant push, or rock will go out of bounds.
        if (not self.is_player) or npc_target_pos == None:
            speed = self.base_move_speed
            return WACT_OUTCOME_STAY, self.pos, (0, 0), speed, speed

        npc_destination_penalty = level.get_terrain_penalty(npc_target_pos)
        third_npc = level.get_occupancy(npc_target_pos)
        # can push NPC
        if target.pushable and npc_destination_penalty != 1 and not third_npc:
            my_out_speed = self.base_move_speed * (1 - destination_speed_penalty)
            local_speed_penalty = level.get_terrain_penalty(self.pos)
            my_in_speed = self.base_move_speed * (1 - local_speed_penalty)
            npc_out_speed = target.base_move_speed * (1 - npc_destination_penalty)
            npc_in_speed = target.base_move_speed * (1 - destination_speed_penalty)
            in_speed = min(my_in_speed, npc_in_speed)
            out_speed = min(my_out_speed, npc_out_speed)
            target.start_motion(npc_target_pos, npc_delta, in_speed, out_speed)
            level.move_character_to(target, npc_target_pos)
            return WACT_OUTCOME_MOVE, target_pos, delta, in_speed, out_speed
        
        # NPC going out of bounds, or not pushable, or blocked by 3rd NPC
        speed = self.base_move_speed
        return WACT_OUTCOME_STAY, self.pos, (0, 0), speed, speed

    
    def start_motion(self, target_pos, delta, speed1, speed2):
        self._moving_from = self.pos
        self.pos = target_pos
        self._moving_delta = delta
        self._inbound_speed = speed1
        self._outbound_speed = speed2
        self.is_moving = True
        self._animation_index = 0
        
    
    def update(self, fps):
        # moving logic
        if self.is_moving:
            self.dirty = 1
            animation1_duration = int(fps / self._inbound_speed / 2)  # in frames
            animation2_duration = int(fps / self._outbound_speed / 2)  # in frames
            total_duration = animation1_duration + animation2_duration
            
            if self._animation_index >= total_duration:  # animation is over 
                self._animation_index = 0
                self._moving_delta = None
                self._moving_from = None
                self.is_moving = False
                return
            
            # animation is not over yet 
            self._animation_index += 1
            animation_index = self._animation_index
            # adapt character sprite
            if animation_index == 1:
                self.image = self.standing_frames[self.dir][0]
            elif animation_index == int(total_duration / 4):
                # alternate legs/arms when moving N or S
                if len(self.moving_frames[self.dir]) > 1:
                    self.image = self.moving_frames[self.dir][self.y % 2]
                else:
                    self.image = self.moving_frames[self.dir][0]
            elif animation_index == int(total_duration * 3 / 4):
                self.image = self.standing_frames[self.dir][0]
            
            # move character sprite 
            old_x, old_y = self._moving_from
            dx, dy = self._moving_delta
            if animation_index <= animation1_duration:
                progress = float(animation_index) / fps * self._inbound_speed
            else:
                offset1 = float(animation1_duration) / fps * self._inbound_speed
                offset2 = float(animation_index - animation1_duration) / fps * self._outbound_speed
                progress = offset1 + offset2
                
            xx = old_x + dx * progress
            yy = old_y + dy * progress
            self.rect.x = int(xx * TILE_SIZE_PX)
            self.rect.y = int(yy * TILE_SIZE_PX)
        


class RockNPC(Character):
    pushable = True
    is_monster = False
    is_player = False
    base_move_speed = 1  # cells per second
    def __init__(self, level, frames, containers, pos=(0, 0)):
        Character.__init__(self, level, frames, containers, pos)
        # hack to prevent rocks from alternating sprite when being pushed
        self.standing_frames[DIR_E] = self.standing_frames[DIR_W]
        self.moving_frames[DIR_S].pop()
        self.moving_frames[DIR_N].pop()
        
        
class WanderingNPC(Character): 
    def __init__(self, level, frames, containers, pos=(0, 0)):
        Character.__init__(self, level, frames, containers, pos)
        self.move_timer = random.random() * 4 # in seconds. Move when <= 0.
        
    def update(self, fps):
        Character.update(self, fps)
        if self.move_timer <= 0:
            direction = random.choice(list(dir_vectors.keys()))
            self.try_moving_towards(direction)
            self.move_timer = self.base_move_period
        else:
            self.move_timer -= 1.0 / fps
            

class MonsterNPC(WanderingNPC):
    pushable = False
    is_monster = True
    is_player = False
    base_move_period = 2.5  # move every 2.5 seconds

    def try_moving_towards(self, direction):
        """ Make the character move. 
        Return whether the move triggered an encounter.
        """
        if self.is_moving:
            return  # cant move if animation in progress
        self.dir = direction  # face the direction even if staying in place
        outcome, pos, delta, in_speed, out_speed = self.compute_movement(direction)
        if outcome in (WACT_OUTCOME_STAY, WACT_OUTCOME_MOVE):
            self.start_motion(pos, delta, in_speed, out_speed)
            self.level.move_character_to(self, pos)
            return 0
        elif outcome == WACT_OUTCOME_ENCOUNTER:
            return 1


class Player(Character):
    pushable = False
    is_monster = False 
    is_player = True
    base_move_speed = 5  # cells per second
    
    def try_moving_towards(self, direction):
        """ Make the character move. 
        Return whether the move triggered an encounter.
        """
        if self.is_moving:
            return  # cant move if animation in progress
        self.dir = direction  # face the direction even if staying in place
        outcome, pos, delta, in_speed, out_speed = self.compute_movement(direction)
        if outcome in (WACT_OUTCOME_STAY, WACT_OUTCOME_MOVE):
            self.start_motion(pos, delta, in_speed, out_speed)
            self.level.move_character_to(self, pos)
            return 0
        elif outcome == WACT_OUTCOME_ENCOUNTER:
            return 1
    