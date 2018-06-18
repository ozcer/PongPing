import itertools
import logging
import random

from src.const import *
from pygame.locals import *

from src.paddle import Paddle


class Ball(pygame.sprite.Sprite):
    width = 50
    height = 50

    def __init__(self, game, pos, control=0):
        super().__init__()
        self.game = game
        self.x, self.y = pos
        self.dx, self.dy = 0, 0
        self.image = pygame.Surface((Ball.width, Ball.height))
        self.image.fill(D_GREY)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y

    def update(self):
        self._handle_input()
        self.x += self.dx
        self.y += self.dy
        self.rect.center = self.x, self.y

        # rebound horizontally hitting paddle
        collidee = self.collide_with_paddle()
        if collidee:
            self.dx *= -1.5
            if abs(self.dx) > MAX_BALL_SPEED:
                self.dx = sign(self.dx) * MAX_BALL_SPEED
            self.dy += collidee.dy * 0.5

        # rebound vertically hitting floor or ceiling
        if self.rect.top < 0 or self.rect.bottom > DISPLAY_HEIGHT:
            self.dy *= -1
        # reset upon leaving horizontally
        if self.rect.right < 0:
            self.game.client.send_msg('win player2')
            self.reset()
        if self.rect.left > DISPLAY_WIDTH:
            self.game.client.send_msg('win player1')
            self.reset()

    def draw(self):
        self.game.surface.blit(self.image, self.rect)

    def _handle_input(self):
        # single press
        for event in self.game.events:
            if event.type == KEYDOWN:
                key = event.key
                if key == pygame.K_SPACE:
                    self.kick()

    def kick(self):
        rand_vel = (random.choice([-1, 1]) * random.randint(2, 4),
                    random.choice([-1, 1]) * random.randint(2, 4))
        print(rand_vel)
        self.game.client.send_msg(f'b {rand_vel[0]} {rand_vel[1]}')
        self.dx = rand_vel[0]
        self.dy = rand_vel[1]

    def reset(self):
        self.x = DISPLAY_WIDTH / 2
        self.y = DISPLAY_HEIGHT / 2
        self.dx = 0
        self.dy = 0

    def collide_with_paddle(self):
        for sprite in self.game.entities:
            if self.rect.colliderect(sprite.rect) and isinstance(sprite, Paddle):
                return sprite
