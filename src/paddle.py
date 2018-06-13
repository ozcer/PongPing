import itertools
import logging

from src.const import *
from pygame.locals import *


class Paddle(pygame.sprite.Sprite):
    width = 50
    height = 200

    def __init__(self, game, pos, control=0):
        super().__init__()
        self.game = game
        self.x, self.y = pos
        self.dx, self.dy = 0, 0
        self.control_type = control

        self.image = pygame.Surface((Paddle.width, Paddle.height))
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y

        self.speed = 5

    def update(self):
        self._handle_input()
        self.x += self.dx
        self.y += self.dy
        if self.rect.center != (self.x, self.y):
            self.game.client.send_msg(f'p{self.control_type} {self.x} {self.y}')

        self.rect.center = self.x, self.y
        self.dy = 0

        if self.rect.top < 0:
            self.rect.top = 0
            self.y = self.rect.centery

        if self.rect.bottom > DISPLAY_HEIGHT:
            self.rect.bottom = DISPLAY_HEIGHT
            self.y = self.rect.centery

    def draw(self):
        self.game.surface.blit(self.image, self.rect)

    def _handle_input(self):
        # single press
        for event in self.game.events:
            if event.type == KEYDOWN:
                pass

        # Constant down
        keys = pygame.key.get_pressed()
        if self.control_type == 0:
            if keys[K_w]:
                self.move("up")
            elif keys[K_s]:
                self.move("down")
        elif self.control_type == 1:
            if keys[K_UP]:
                self.move("up")
            elif keys[K_DOWN]:
                self.move("down")

    def move(self, direction):
        if direction == "up":
            self.dy = -self.speed
        elif direction == "down":
            self.dy = self.speed
