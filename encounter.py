import pygame
from pygame.color import Color
from pygame.constants import RLEACCEL

PORTRAIT_W, PORTRAIT_H = 56, 56  # each image is 56 x 56px, and 2x zoom 
GRID_W, GRID_H = 32, 32  # 16 x 16 grid of 32px cells


# pygame inits
# pygame.display.init() # OK to init multiple times
# pygame.font.init()

class EncounterMode():
    def __init__(self, screen):
        self.screen = screen
        self.bg = self.make_bg()
        # load sprites
        self.front_sprites = self.load_sprites('assets/monsters_front.png',
                                               PORTRAIT_W, PORTRAIT_H, True)
        self.back_sprites = self.load_sprites('assets/player_back.png',
                                              GRID_W, GRID_H)
        self.sprites = pygame.sprite.LayeredDirty()
        
        # add monster and player sprites 
        monster_id = 5
        monster_img = self.front_sprites[monster_id]
        EncounterSprite(monster_img, [self.sprites], (11, 1))
        player_img = self.back_sprites[0]
        EncounterSprite(player_img, [self.sprites], (1, 5))
        for char in self.sprites:
            self.sprites.change_layer(char, 1)
        self.reset()
    
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
        font = pygame.font.SysFont("monospace", GRID_H)
        menu_item_area = (0, 0, 5 * GRID_W, GRID_H)
        surf = font.render('Scare', 1, (0, 0, 0))
        bg.blit(surf, (2 * GRID_W, 10 * GRID_H), menu_item_area)
        surf = font.render('Bait', 1, (0, 0, 0))
        bg.blit(surf, (10 * GRID_W, 10 * GRID_H), menu_item_area)
        return bg
    
    def load_sprites(self, filename, spr_w, spr_h, flip_h=False):
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
                img = pygame.transform.scale(img, (4 * GRID_W, 4 * GRID_H))
                sprites.append(img)
        return sprites
    
        
    def do_action(self, action):
        """ Return the name of the mode to execute next.
        Return None if mode is unchanged.
        """ 
        # TODO: move between menu choices
        return 'world'
    
    def reset(self):
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
    def __init__(self, image, containers, pos=(0, 0)):
        # containers: list of sprite groups to join
        pygame.sprite.DirtySprite.__init__(self, *containers)
        self.image = image
        self.rect = pygame.Rect(pos[0] * GRID_W, pos[1] * GRID_H, GRID_W, GRID_H)
        self.dirty = 1
    
    def update(self, fps):
        self.dirty = 1
        # pass
            
            
            
            
if __name__ == "__main__":
    from pygame.constants import QUIT, KEYDOWN, K_ESCAPE
    pygame.init()
    screen = pygame.display.set_mode((16 * GRID_W, 16 * GRID_H))
    fps = 10
    clock = pygame.time.Clock()
    em = EncounterMode(screen)
    game_over = False
    while not game_over:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                game_over = True
        em.tick(fps)
        clock.tick(fps)
                        
