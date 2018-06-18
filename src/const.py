import math
import os

import pygame

# Display
FPS = 60
CAPTION = "Pong Ping"
DISPLAY_WIDTH = int(640 * 1.2)
DISPLAY_HEIGHT = int(480 * 1.2)
START_WINDOW_POS = (100, 100)


# network
USERNAME = "ozcer the god"

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

MAX_BALL_SPEED = 10

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
