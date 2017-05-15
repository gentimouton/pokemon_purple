import pygame
from pygame.color import Color
from pygame.constants import RLEACCEL


PORTRAIT_W, PORTRAIT_H = 56, 56  # each image is 56 x 56px, and 2x zoom 
GRID_W, GRID_H = 32, 32  # 16 x 16 grid of 32px cells
ICON_W, ICON_H = 8, 8

# pygame inits
# pygame.display.init() # OK to init multiple times
# pygame.font.init()


class EncounterMode():
    def __init__(self, screen):
        self.screen = screen
        
        # load sprites
        self.front_sprites = self.load_sprites('assets/monsters_front.png',
                                               PORTRAIT_W, PORTRAIT_H, 4, 4, True)
        self.back_sprites = self.load_sprites('assets/player_back.png',
                                              GRID_W, GRID_H, 4, 4)
        self.icon_sprites = self.load_sprites('assets/icons.png', ICON_W, ICON_H, 1, 1)
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
        bg = pygame.Surface((16 * GRID_W, 16 * GRID_H))
        bg.fill((255, 255, 255))
        # debugging grid
        for x in range(1, 16):
            start = x * GRID_W, 0
            end = x * GRID_W, 16 * GRID_H
            pygame.draw.line(bg, (200, 200, 200), start, end)
        for y in range(1, 16):
            start = 0, y * GRID_H
            end = 16 * GRID_W, y * GRID_H
            pygame.draw.line(bg, (200, 200, 200), start, end)
        # top HUD
        start = (0, 1 * GRID_H)
        end = (16 * GRID_W, 1 * GRID_H)
        pygame.draw.line(bg, (0, 0, 0), start, end, 2)
        # bottom HUD
        start = (0, 9 * GRID_H)
        end = (16 * GRID_W, 9 * GRID_H)
        pygame.draw.line(bg, (0, 0, 0), start, end, 2) 
        # menu choices
        # TODO: render via game font instead
        font = pygame.font.SysFont("monospace", GRID_H)
        menu_item_area = (0, 0, 5 * GRID_W, GRID_H)
        surf = font.render(self.menus[0][0], 1, (0, 0, 0))
        bg.blit(surf, (2 * GRID_W, 10 * GRID_H), menu_item_area)
        surf = font.render(self.menus[0][1], 1, (0, 0, 0))
        bg.blit(surf, (10 * GRID_W, 10 * GRID_H), menu_item_area)
        return bg
    
    def load_sprites(self, filename, spr_w, spr_h, display_w, display_h, flip_h=False):
        """
        Return an array of sprites loaded from filename.
        (spr_w, spr_h) is the expected size of each sprite.
        flip_h=True to flip the sprites horizontally.
        """
        chars_img = pygame.image.load(filename).convert()
        chars_img.set_colorkey(Color(255, 0, 255), RLEACCEL)
        image_w, image_h = chars_img.get_size()
        sprites = []
        for spr_y in range(0, image_h / spr_h):
            for spr_x in range(0, image_w / spr_w):
                rect = (spr_x * spr_w, spr_y * spr_h, spr_w, spr_h)
                img = chars_img.subsurface(rect)
                img = pygame.transform.flip(img, flip_h, False)
                size = (display_w * GRID_W, display_h * GRID_H)
                img = pygame.transform.scale(img, size)
                sprites.append(img)
        return sprites
    
        
    def process_action(self, action):
        """ action = 'up', 'down', 'right', or 'left'. 
        Return the name of the mode to execute next.
        Return None if mode is unchanged.
        """ 
        y, x = self.cur_menu
        if action == 'enter':
            choice = self.menus[y][x]
            if choice == 'Scare':
                return 'world'
        
        if action == 'up':
            y = (y - 1) % len(self.menus)
        elif action == 'down':
            y = (y + 1) % len(self.menus)
        elif action == 'left':
            x = (x - 1) % len(self.menus[0])
        elif action == 'right':
            x = (x + 1) % len(self.menus[0])
        self.cur_menu = y, x
        pos = (1 + x * 8, 10 + y * 2)
        self.cursor_spr.pos = pos
        return None
    
    def resume(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        pygame.display.flip()
        for char in self.sprites:
            char.dirty = 1
    
    def tick(self, fps):
        self.sprites.clear(self.screen, self.bg)
        self.sprites.update(fps)
        changed_rects = self.sprites.draw(self.screen)
        pygame.display.update(changed_rects)
                 


class EncounterSprite(pygame.sprite.DirtySprite):
    
    def _get_pos(self):
        return self.x, self.y
    def _set_pos(self, pos):
        x, y = pos
        self.x, self.y = x, y
        self.dirty = 1
        self.rect = pygame.Rect(x * GRID_W, y * GRID_H, GRID_W, GRID_H)
    pos = property(_get_pos, _set_pos)
    
    def __init__(self, image, containers, pos=(0, 0)):
        # containers: list of sprite groups to join
        pygame.sprite.DirtySprite.__init__(self, *containers)
        self.image = image
        self.pos = pos
    
    def update(self, fps):
        pass
            
            
    
if __name__ == "__main__":
    from pygame.constants import QUIT, KEYDOWN, K_ESCAPE, \
    K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RETURN, K_w, K_s, K_a, K_d, K_KP_ENTER
    
    pygame.init()
    
    _key_map = { K_UP: 'up', K_DOWN: 'down', K_LEFT: 'left', K_RIGHT: 'right',
                 K_w: 'up', K_s: 'down', K_a: 'left', K_d: 'right',
                 K_RETURN: 'enter', K_KP_ENTER: 'enter'}

    screen = pygame.display.set_mode((16 * GRID_W, 16 * GRID_H))
    fps = 60
    clock = pygame.time.Clock()
    em = EncounterMode(screen)
    game_over = False
    while not game_over:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                game_over = True
            elif (e.type == KEYDOWN and e.key in _key_map.keys()):
                if em.process_action(_key_map[e.key]) == 'world':
                    game_over = True
        em.tick(fps)
        clock.tick(fps)
                        
