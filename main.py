import logging
import sys
import time
import itertools


from pygame.locals import *

from src.ball import Ball
from src.const import *
from src.paddle import Paddle
from client import Client


class Game:
    logging.basicConfig(level=LOG_LEVEL,
                        datefmt='%m/%d/%Y %I:%M:%S%p',
                        format='%(asctime)s %(message)s')

    def __init__(self, id):
        # Initializing Pygame window
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()

        pygame.display.set_caption(CAPTION)
        self.surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), 0, 32)

        self.entities = pygame.sprite.Group()
        self.fps_clock = pygame.time.Clock()
        self.events = pygame.event.get()
        self.background_color = D_GREY

        p1 = Paddle(self, (50, DISPLAY_HEIGHT/2))
        p2 = Paddle(self, (DISPLAY_WIDTH-50, DISPLAY_HEIGHT/2), control=1)
        b = Ball(self, (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2))
        self.add_entity(p1)
        self.add_entity(p2)
        self.add_entity(b)

        self.p1 = p1
        self.p2 = p2
        self.ball = b
        self.id = id

        self.client = Client(self, "localhost", 8008)

        self.run()

    def run(self):
        while True:
            self.surface.fill(self.background_color)

            self.events = pygame.event.get()

            self.update_all_sprites()
            self.draw_all_sprites()

            for event in self.events:
                if event.type == pygame.locals.QUIT:
                    self.quit()

                if event.type == KEYDOWN:
                    key = event.key
                    if key == pygame.K_ESCAPE:
                        self.quit()

            pygame.display.update()
            self.fps_clock.tick(FPS)

    def update_all_sprites(self):
        for sprite in self.entities:
            sprite.update()

    def draw_all_sprites(self):
        for sprite in self.entities:
            sprite.draw()

    def add_entity(self, entity):
        logging.info(f"{entity} created")
        self.entities.add(entity)

    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game(0)