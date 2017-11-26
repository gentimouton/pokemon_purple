import pygame

# filename -> size of sprites (in pixels) in that file. Sprites must be square.
_spr_size_map = {
    'assets/monsters_front.png': 56,
    'assets/player_back.png': 32,
    'assets/icons.png': 8,
    'assets/tileset.png': 16,
    'assets/character_sprites.png': 16
    }

TRANSPARENT = (255, 0, 255)


def load_spritesheet_flat(filename, resize_to=None, flip_h=False):
    """
    Load sprites from file.
    :resize_to: desired output size in pixel of each sprite.
    :flip_h: true to flip the sprites horizontally.
    :return: Flat list of sprites.
    """
    sheet_img = pygame.image.load(filename).convert()
    sheet_img.set_colorkey(TRANSPARENT, pygame.RLEACCEL)
    sheet_w, sheet_h = sheet_img.get_size()
    spr_size = _spr_size_map[filename]
    sprites = []
    for spr_y in range(0, sheet_h // spr_size):
        for spr_x in range(0, sheet_w // spr_size):
            rect = (spr_x * spr_size, spr_y * spr_size, spr_size, spr_size)
            img = sheet_img.subsurface(rect)
            img = pygame.transform.flip(img, flip_h, False)
            if resize_to:
                img = pygame.transform.scale(img, (resize_to, resize_to))
            sprites.append(img)
    return sprites


def load_spritesheet_nested(filename, resize_to=None, flip_h=False):
    """
    Load sprites from file. Each row contains the sprites for *one* character.
    :resize_to: desired output size in pixel of each sprite.
    :flip_h: true to flip the sprites horizontally.
    :return: Nested list of sprites, eg [ [a1,a2], [b1,b2] ].
    """
    sheet_img = pygame.image.load(filename).convert()
    sheet_img.set_colorkey(TRANSPARENT, pygame.RLEACCEL)
    sheet_w, sheet_h = sheet_img.get_size()
    spr_size = _spr_size_map[filename]
    sprites = []
    for spr_y in range(0, sheet_h // spr_size):
        line = []
        for spr_x in range(0, sheet_w // spr_size):
            rect = (spr_x * spr_size, spr_y * spr_size, spr_size, spr_size)
            line.append(sheet_img.subsurface(rect))
        sprites.append(line)
    return sprites
    
    