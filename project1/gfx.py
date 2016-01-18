import sys
import pygame
import object_collection


pygame.display.init()


class Gfx(object):
    """
    This class takes care of drawing the state of the search to a window using pygame
    """
    size = width, height = 960, 540

    WHITE = 255, 255, 255
    BLACK = 0, 0, 0

    add_predator = None
    remove_predator = None

    def __init__(self, fps=30.0):
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()  # used for limiting the fps, so one can see each step
        self.fps = fps

    def draw(self):
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
                if event.key == pygame.K_w and Gfx.add_predator:
                    self.add_predator()
                if event.key == pygame.K_s and Gfx.remove_predator:
                    self.remove_predator()

        self.clock.tick(self.fps)

        self.screen.fill(self.BLACK)

        for obj in object_collection.ObjectCollection.all_boids:
            obj.draw(pygame.draw, self.screen)

        for obj in object_collection.ObjectCollection.all_predators:
            obj.draw(pygame.draw, self.screen)

        pygame.display.flip()
