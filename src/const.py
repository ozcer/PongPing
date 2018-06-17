import math
import os

import pygame

# Display
FPS = 60
CAPTION = "Pong Ping"
DISPLAY_WIDTH = int(640 * 1.2)
DISPLAY_HEIGHT = int(480 * 1.2)
START_WINDOW_POS = (100, 100)

# logging
LOG_LEVEL = 0
EXIT_MESSAGE = "EXIT_MESSAGE"

# network
USERNAME = "tony2"

# string
HELP1 = 'W + S to move'
HELP2 = 'UP + DOWN to move'

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
D_GREY = (70, 70, 70)
L_GREY = (100, 100, 100)
RED = (255, 0, 0)
ORANGE = (244, 179, 66)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

PURPLE = (106, 27, 154)
L_PURPLE = (156, 77, 204)
D_PURPLE = (56, 0, 107)

OLIVE = (130, 119, 23)
D_OLIVE = (82, 76, 0)
MAROON = (180, 66, 70)

BLUE = (25, 118, 210)
L_BLUE = (99, 164, 255)
D_BLUE = (0, 75, 160)

PALETTE_L_GREY = (76, 84, 91)
PALETTE_D_GREEN = (123, 132, 80)
PALETTE_L_BLUE = (150, 200, 195)
PALETTE_D_BLUE = (105, 210, 231)
PALETTE_L_ORANGE = (243, 134, 48)
PALETTE_D_ORANGE = (250, 105, 0)

PLAYER_COLOR = D_OLIVE

# Group of all entities
ALL_SPRITES = "ALL"

GRAVITY = .55
TERMIANL_VELOCITY = 15

BLOCK_DIM = 75, 75


def _build_row(cls, game, start_pos, next_pos, amount, world=None, **kwargs):
    """
    given start position and next relative position
    build that many items and put them in given worlds
    :param cls: class to build
    :param start_pos: (int, int)
    :param next_pos: (int, int)
    :param amount: int
    :param world: str or None
    :return: None
    """
    for i in range(amount):
        pos = (start_pos[0] + i * next_pos[0],
               start_pos[1] + i * next_pos[1])
        instance = cls(game, pos=pos, **kwargs)
        game.add_entity(instance, world)

        # Return last position
        if i == amount - 1:
            return pos


def build_row(cls, game, start_pos, amount, left=False, world=None, **kwargs):
    next_x = cls.width if not left else -cls.width
    next_pos = (next_x, 0)
    last_pos = _build_row(cls, game, start_pos, next_pos, amount, world=world, **kwargs)
    return last_pos


def build_column(cls, game, start_pos, amount, up=False, world=None, **kwargs):
    next_y = cls.height if not up else -cls.height
    next_pos = (0, next_y)
    last_pos = _build_row(cls, game, start_pos, next_pos, amount, world=world, **kwargs)
    return last_pos


def build_array(cls, game, start_pos, dimensions, left=False, up=False, world=None, **kwargs):
    """
    build an array of objects
    :param cls: Type
    :param game: Game
    :param start_pos: (int, int)
    :param dimensions:  (int, int) width x height
    :param left: builds leftward
    :param up: builds upward
    :param world: str or None
    :return: (int, int) last position
    """
    for row in range(dimensions[1]):
        dy = row * cls.height
        if up:
            dy = -dy
        pos = start_pos[0], start_pos[1] + dy
        build_row(cls, game, pos, dimensions[0], left, world, **kwargs)
    return get_end_pos(cls, start_pos, dimensions, left=left, up=up)


def get_end_pos(cls, start_pos, dimensions, left=False, up=False):
    """
    calculate the end position if were to build an array of items
    :param cls: Type
    :param start_pos: (int, int)
    :param dimensions: (int, int)
    :param left: bool: default builds rightward
    :param up: bool: default builds downward
    :return: (int, int)
    """
    dx = (dimensions[0] - 1) * cls.width
    if left: dx = -dx
    dy = (dimensions[1] - 1) * cls.height
    if up: dy = -dy

    end_pos = start_pos[0] + dx, start_pos[1] + dy
    return end_pos


def find_closest(self, cls):
    """
    return the the closest instance of a class or None if not found
    :param cls: Type (a class)
    :return: Sprite or None
    """
    closest = None
    shortest_dist = None
    for sprite in self.game.entities[ALL_SPRITES]:
        if isinstance(sprite, cls):
            curr_dist = distance((self.x, self.y), (sprite.x, sprite.y))
            if shortest_dist is None or curr_dist < shortest_dist:
                closest = sprite
                shortest_dist = curr_dist
    return closest


def load_image_folder(path):
    cwd = os.path.dirname(__file__)
    relative_path = os.path.join(cwd, path)
    res = []
    try:
        for file in os.listdir(relative_path):
            _path = os.path.join(relative_path, file)
            res.append(pygame.image.load(_path).convert_alpha())
    except pygame.error as msg:
        raise type(msg)(str(msg) + " (try importing after initialization) ")
    return res


def solid_color(color):
    """
    Return a surface filled with given color
    :param color: (int, int, int)
    :return: Surface
    """
    surface = pygame.Surface((1, 1))
    surface.fill(color)
    return surface


def render_text_on_surface(text, surface, font, color=BLACK, top_padding=0, left_pading=0):
    """
    render text within boundary of surface's rect
    :param text: str
    :param surface: Surface
    :param font: Font
    :param paddings: {"left": int, "top":int}
    :return: None
    """
    rect = surface.get_rect()

    last_top = rect.top + top_padding
    for index, line in enumerate(text.split("\n")):
        text_surf = font.render(line, True, color)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (rect.left + left_pading, last_top)
        surface.blit(text_surf, text_rect)

        last_top += text_rect.h


def distance(p1, p2):
    """
    get distance between two points
    """
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def angle(p1, p2):
    """
    get angle between two points
    """
    x_dist = p2[0] - p1[0]
    y_dist = p2[1] - p1[1]
    return math.atan2(-y_dist, x_dist) % (2 * math.pi)


def sign(n):
    """
    get the sign of a number
    """
    return (n > 0) - (n < 0)


def within_range(v, start, end):
    return start <= v <= end
