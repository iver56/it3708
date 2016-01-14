import sys
import pygame
import math

pygame.display.init()


class Gfx(object):
    """
    This class takes care of drawing the state of the search to a window using pygame
    """
    size = width, height = 960, 540

    BOID_SIZE = 8
    LINE_THICKNESS = 3
    LINE_LENGTH = 14

    COLOR_MAP = {
        0: (255, 236, 130),  # yellow
        1: (47, 160, 19),  # green
        2: (109, 142, 224),  # blue
        3: (255, 130, 234),  # pink
        4: (132, 19, 160),  # purple
        5: (224, 191, 109),  # bronze
        6: (89, 255, 208),  # teal
        7: (255, 79, 108)  # red
    }
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0

    def __init__(self, fps=30.0):
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()  # used for limiting the fps, so one can see each step
        self.fps = fps

    def draw_boid(self, boid):
        color_id = boid.id % 8
        color = self.COLOR_MAP[color_id]
        pygame.draw.circle(self.screen, color, [boid.get_x(), boid.get_y()], self.BOID_SIZE)
        pygame.draw.line(
                self.screen,
                color,
                [boid.get_x(), boid.get_y()],
                [
                    boid.get_x() + self.LINE_LENGTH * math.cos(boid.get_direction()),
                    boid.get_y() + self.LINE_LENGTH * math.sin(boid.get_direction())
                ],
                self.LINE_THICKNESS
        )

    def draw(self, boids):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.fps /= 2  # halve the fps
                if event.key == pygame.K_UP:
                    self.fps *= 2  # double the fps
                    if self.fps > 256.0:
                        self.fps = 256.0

        self.clock.tick(self.fps)

        self.screen.fill(self.BLACK)

        for boid in boids:
            self.draw_boid(boid)

        pygame.display.flip()
