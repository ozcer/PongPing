import itertools
import logging

from src.const import *
from pygame.locals import *


class Paddle(pygame.sprite.Sprite):
    width = 50
    height = 200

    def __init__(self, game, pos, control=1):
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

        username = self.game.username1 if self.control_type == 1 else self.game.username2
        _surface = self.game.font.render(username, True, WHITE)
        _rect = _surface.get_rect()
        _rect.center = self.x, self.y
        self.game.surface.blit(_surface, _rect)

    def _handle_input(self):
        # single press
        for event in self.game.events:
            if event.type == KEYDOWN:
                pass

        # Constant down
        keys = pygame.key.get_pressed()
        if self.control_type == 1 == self.game.control_type:
            if keys[K_w]:
                self.move("up")
                self.game.client.send_msg(f'p0 {self.x} {self.y}')
            elif keys[K_s]:
                self.move("down")
                self.game.client.send_msg(f'p0 {self.x} {self.y}')
        elif self.control_type == 2 == self.game.control_type:
            if keys[K_UP]:
                self.move("up")
                self.game.client.send_msg(f'p1 {self.x} {self.y}')
            elif keys[K_DOWN]:
                self.move("down")
                self.game.client.send_msg(f'p1 {self.x} {self.y}')

    def move(self, direction):
        if direction == "up":
            self.dy = -self.speed
        elif direction == "down":
            self.dy = self.speed
