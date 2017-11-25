import pygame
from pygame.color import Color
from pygame.constants import RLEACCEL

from controls import BTN_SUBMIT, BTN_UP, BTN_DOWN, BTN_LEFT, BTN_RIGHT
from scene import Scene, SCN_WORLD


GRID_SIZE_PX = 16  # in pixels. 
N_GRID_CELLS = 16  # grid of 16x16 cells  


class EncounterScene(Scene):
    def __init__(self, scene_manager):
        Scene.__init__(self, scene_manager)
        
        # load sprites
        self.front_sprites = load_sprites('assets/monsters_front.png', 4, True)
        self.back_sprites = load_sprites('assets/player_back.png', 4)
        self.icon_sprites = load_sprites('assets/icons.png', 1)
        self.sprites = pygame.sprite.LayeredDirty()
        
        # build menu struct
        self.menus = [ ['Scare', 'Bait'] ]
        self.cur_menu = (0, 0)
        
        # make bg
        self.bg = self.make_bg()
        
        # add monster and player sprites 
        monster_id = 5
        monster_img = self.front_sprites[monster_id]
        EncounterSprite(monster_img, [self.sprites], (11, 1))
        player_img = self.back_sprites[0]
        EncounterSprite(player_img, [self.sprites], (1, 5))
        # add menu selector arrow
        arrow_img = self.icon_sprites[0]
        coords = (1, 10)
        self.cursor_spr = EncounterSprite(arrow_img, [self.sprites], coords)
        
        # needed?
        for char in self.sprites:
            self.sprites.change_layer(char, 1)
        
        
        # self.resume()
    
    def make_bg(self):
        """ Build all background elements. Return image.
        """
        bg = pygame.Surface((N_GRID_CELLS * GRID_SIZE_PX, N_GRID_CELLS * GRID_SIZE_PX))
        bg.fill((255, 255, 255))
        # debugging grid
        for x in range(1, N_GRID_CELLS):
            start = x * GRID_SIZE_PX, 0
            end = x * GRID_SIZE_PX, N_GRID_CELLS * GRID_SIZE_PX
            pygame.draw.line(bg, (200, 200, 200), start, end)
        for y in range(1, N_GRID_CELLS):
            start = 0, y * GRID_SIZE_PX
            end = N_GRID_CELLS * GRID_SIZE_PX, y * GRID_SIZE_PX
            pygame.draw.line(bg, (200, 200, 200), start, end)
        # top HUD
        start = (0, 1 * GRID_SIZE_PX)
        end = (N_GRID_CELLS * GRID_SIZE_PX, 1 * GRID_SIZE_PX)
        pygame.draw.line(bg, (0, 0, 0), start, end, 2)
        # bottom HUD
        start = (0, 9 * GRID_SIZE_PX)
        end = (N_GRID_CELLS * GRID_SIZE_PX, 9 * GRID_SIZE_PX)
        pygame.draw.line(bg, (0, 0, 0), start, end, 2) 
        # menu choices
        # TODO: render via game font instead
        font = pygame.font.SysFont("monospace", GRID_SIZE_PX)
        menu_item_area = (0, 0, 5 * GRID_SIZE_PX, GRID_SIZE_PX)
        surf = font.render(self.menus[0][0], 1, (0, 0, 0))
        bg.blit(surf, (2 * GRID_SIZE_PX, 10 * GRID_SIZE_PX), menu_item_area)
        surf = font.render(self.menus[0][1], 1, (0, 0, 0))
        bg.blit(surf, (10 * GRID_SIZE_PX, 10 * GRID_SIZE_PX), menu_item_area)
        return bg
    
        
    def process_input(self, action):
        """ Return the name of the mode to execute next.
        Return None if mode is unchanged.
        """ 
        y, x = self.cur_menu
        if action == BTN_SUBMIT:
            choice = self.menus[y][x]
            if choice == 'Scare':
                return SCN_WORLD
        
        if action == BTN_UP:
            y = (y - 1) % len(self.menus)
        elif action == BTN_DOWN:
            y = (y + 1) % len(self.menus)
        elif action == BTN_LEFT:
            x = (x - 1) % len(self.menus[0])
        elif action == BTN_RIGHT:
            x = (x + 1) % len(self.menus[0])
        self.cur_menu = y, x
        pos = (1 + x * 8, 10 + y * 2)
        self.cursor_spr.pos = pos
        return None
    
    def resume(self):
        self._screen.fill((0, 0, 0))
        self._screen.blit(self.bg, (0, 0))
        pygame.display.flip()
        for char in self.sprites:
            char.dirty = 1
    
    def tick(self, fps):
        self.sprites.clear(self._screen, self.bg)
        self.sprites.update(fps)
        changed_rects = self.sprites.draw(self._screen)
        pygame.display.update(changed_rects)
                 


class EncounterSprite(pygame.sprite.DirtySprite):
    
    def _get_pos(self):
        return self.x, self.y
    def _set_pos(self, pos):
        x, y = pos
        self.x, self.y = x, y
        self.dirty = 1
        self.rect = pygame.Rect(x * GRID_SIZE_PX, y * GRID_SIZE_PX, GRID_SIZE_PX, GRID_SIZE_PX)
    pos = property(_get_pos, _set_pos)
    
    def __init__(self, image, containers, pos=(0, 0)):
        # containers: list of sprite groups to join
        pygame.sprite.DirtySprite.__init__(self, *containers)
        self.image = image
        self.pos = pos
    
    def update(self, fps):
        pass
            
            
 
############################################################
####################   UTILS   #############################
############################################################

# filename -> size of sprites (in pixels) in that file. Sprites must be square.
spr_size_map = {'assets/monsters_front.png': 56,
            'assets/player_back.png': 32,
            'assets/icons.png': 8
            }

def load_sprites(filename, display_size, flip_h=False):
    """
    Return an array of sprites loaded from filename.
    display_size: number of tiles the sprite takes on the screen (scaling).
    flip_h=True to flip the sprites horizontally.
    """
    chars_img = pygame.image.load(filename).convert()
    chars_img.set_colorkey(Color(255, 0, 255), RLEACCEL)
    image_w, image_h = chars_img.get_size()
    spr_size = spr_size_map[filename]
    sprites = []
    for spr_y in range(0, image_h // spr_size):
        for spr_x in range(0, image_w // spr_size):
            rect = (spr_x * spr_size, spr_y * spr_size, spr_size, spr_size)
            img = chars_img.subsurface(rect)
            img = pygame.transform.flip(img, flip_h, False)
            size = (display_size * GRID_SIZE_PX, display_size * GRID_SIZE_PX)
            img = pygame.transform.scale(img, size)
            sprites.append(img)
    return sprites
   
   
if __name__ == "__main__":
    from pygame.constants import QUIT, KEYDOWN, K_ESCAPE, \
    K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RETURN, K_w, K_s, K_a, K_d, K_KP_ENTER
    
    pygame.init()
    
    _key_map = { K_UP: BTN_UP, K_DOWN: BTN_DOWN, K_LEFT: BTN_LEFT,
                K_RIGHT: BTN_RIGHT, K_w: BTN_UP, K_s: BTN_DOWN, K_a: BTN_LEFT,
                K_d: BTN_RIGHT, K_RETURN: BTN_SUBMIT, K_KP_ENTER: BTN_SUBMIT }

    screen_res = N_GRID_CELLS * GRID_SIZE_PX
    screen = pygame.display.set_mode((screen_res, screen_res))
    fps = 60
    clock = pygame.time.Clock()
    em = EncounterScene(screen)
    game_over = False
    while not game_over:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                game_over = True
            elif (e.type == KEYDOWN and e.key in _key_map.keys()):
                if em.process_input(_key_map[e.key]) == SCN_WORLD:
                    game_over = True
        em.tick(fps)
        clock.tick(fps)
                        
