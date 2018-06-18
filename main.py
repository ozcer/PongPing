import logging
import sys


from pygame.locals import *

from src.ball import Ball
from src.const import *
from src.paddle import Paddle
from client import Client


class Game:
    def __init__(self, id):
        # Initializing Pygame window
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption(CAPTION)
        self.surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), 0, 32)

        self.username1 = ''
        self.username2 = ''

        self.point1 = 0
        self.point2 = 0

        self.entities = pygame.sprite.Group()
        self.fps_clock = pygame.time.Clock()
        self.events = pygame.event.get()
        self.background_color = L_GREY
        self.font = pygame.font.SysFont('Comic Sans MS', 20)

        self.control_type = -1
        p1 = Paddle(self, (50, DISPLAY_HEIGHT/2))
        p2 = Paddle(self, (DISPLAY_WIDTH-50, DISPLAY_HEIGHT/2), control=2)
        b = Ball(self, (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2))
        self.add_entity(p1)
        self.add_entity(p2)
        self.add_entity(b)

        self.p1 = p1
        self.p2 = p2
        self.ball = b
        self.id = id

        self.client = Client(self, "25.8.62.7", 5000)
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

        self._draw_points()

        if self.control_type == 1:
            self._draw_instruction('left')
        elif self.control_type == 2:
            self._draw_instruction('right')

    def _draw_instruction(self, side):
        help_text = HELP1 if side == 'left' else HELP2
        _surface = self.font.render(help_text, True, L_BLUE)
        _rect = _surface.get_rect()
        _rect.centery = DISPLAY_HEIGHT / 2
        if side == 'left':
            _rect.centerx = DISPLAY_WIDTH * (1 / 4)
        elif side == 'right':
            _rect.centerx = DISPLAY_WIDTH * (3 / 4)

        self.surface.blit(_surface, _rect)

    def _draw_points(self):
        _surface = self.font.render(str(self.point1), True, BLACK)
        _rect = _surface.get_rect()
        _rect.topleft = 10, 10
        self.surface.blit(_surface, _rect)

        _surface2 = self.font.render(str(self.point2), True, BLACK)
        _rect2 = _surface2.get_rect()
        _rect2.topright = DISPLAY_WIDTH - 10, 10
        self.surface.blit(_surface2, _rect2)

    def add_entity(self, entity):
        logging.info(f"{entity} created")
        self.entities.add(entity)

    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game(0)