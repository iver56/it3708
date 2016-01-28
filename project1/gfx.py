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

    add_boids = None
    remove_boids = None
    add_predator = None
    remove_predator = None
    add_obstacle = None
    remove_all_obstacles = None
    change_boid_weight_multiplier = None
    change_predator_weight_multiplier = None

    INCREASE_WEIGHT_MULTIPLIER_FACTOR = 1.25
    DECREASE_WEIGHT_MULTIPLIER_FACTOR = 0.8

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
                if event.key == pygame.K_q and Gfx.add_boids:
                    self.add_boids()
                if event.key == pygame.K_a and Gfx.remove_boids:
                    self.remove_boids()
                if event.key == pygame.K_w and Gfx.add_predator:
                    self.add_predator()
                if event.key == pygame.K_s and Gfx.remove_predator:
                    self.remove_predator()

                if event.key == pygame.K_e and Gfx.change_boid_weight_multiplier:
                    self.change_boid_weight_multiplier('SEPARATION_WEIGHT_MULTIPLIER', self.INCREASE_WEIGHT_MULTIPLIER_FACTOR)
                if event.key == pygame.K_d and Gfx.change_boid_weight_multiplier:
                    self.change_boid_weight_multiplier('SEPARATION_WEIGHT_MULTIPLIER', self.DECREASE_WEIGHT_MULTIPLIER_FACTOR)
                if event.key == pygame.K_r and Gfx.change_boid_weight_multiplier:
                    self.change_boid_weight_multiplier('COHESION_WEIGHT_MULTIPLIER', self.INCREASE_WEIGHT_MULTIPLIER_FACTOR)
                if event.key == pygame.K_f and Gfx.change_boid_weight_multiplier:
                    self.change_boid_weight_multiplier('COHESION_WEIGHT_MULTIPLIER', self.DECREASE_WEIGHT_MULTIPLIER_FACTOR)
                if event.key == pygame.K_t and Gfx.change_boid_weight_multiplier:
                    self.change_boid_weight_multiplier('ALIGNMENT_WEIGHT_MULTIPLIER', self.INCREASE_WEIGHT_MULTIPLIER_FACTOR)
                if event.key == pygame.K_g and Gfx.change_boid_weight_multiplier:
                    self.change_boid_weight_multiplier('ALIGNMENT_WEIGHT_MULTIPLIER', self.DECREASE_WEIGHT_MULTIPLIER_FACTOR)
                if event.key == pygame.K_y and Gfx.change_boid_weight_multiplier:
                    self.change_boid_weight_multiplier('PREDATOR_SEPARATION_WEIGHT_MULTIPLIER', self.INCREASE_WEIGHT_MULTIPLIER_FACTOR)
                if event.key == pygame.K_h and Gfx.change_boid_weight_multiplier:
                    self.change_boid_weight_multiplier('PREDATOR_SEPARATION_WEIGHT_MULTIPLIER', self.DECREASE_WEIGHT_MULTIPLIER_FACTOR)
                if event.key == pygame.K_u and Gfx.change_boid_weight_multiplier:
                    self.change_boid_weight_multiplier('OBSTACLE_SEPARATION_WEIGHT_MULTIPLIER', self.INCREASE_WEIGHT_MULTIPLIER_FACTOR)
                if event.key == pygame.K_j and Gfx.change_boid_weight_multiplier:
                    self.change_boid_weight_multiplier('OBSTACLE_SEPARATION_WEIGHT_MULTIPLIER', self.DECREASE_WEIGHT_MULTIPLIER_FACTOR)

                if event.key == pygame.K_i and Gfx.change_boid_weight_multiplier:
                    self.change_predator_weight_multiplier('BOID_COHESION_WEIGHT_MULTIPLIER', self.INCREASE_WEIGHT_MULTIPLIER_FACTOR)
                if event.key == pygame.K_k and Gfx.change_boid_weight_multiplier:
                    self.change_predator_weight_multiplier('BOID_COHESION_WEIGHT_MULTIPLIER', self.DECREASE_WEIGHT_MULTIPLIER_FACTOR)
                if event.key == pygame.K_o and Gfx.change_boid_weight_multiplier:
                    self.change_predator_weight_multiplier('BOID_ALIGNMENT_WEIGHT_MULTIPLIER', self.INCREASE_WEIGHT_MULTIPLIER_FACTOR)
                if event.key == pygame.K_l and Gfx.change_boid_weight_multiplier:
                    self.change_predator_weight_multiplier('BOID_ALIGNMENT_WEIGHT_MULTIPLIER', self.DECREASE_WEIGHT_MULTIPLIER_FACTOR)

            if pygame.mouse.get_pressed()[0]:  # left click
                mouse_pos = pygame.mouse.get_pos()
                self.add_obstacle(*mouse_pos)
            if pygame.mouse.get_pressed()[2]:  # right click
                self.remove_all_obstacles()


        self.clock.tick(self.fps)

        self.screen.fill(self.BLACK)

        for obj in object_collection.ObjectCollection.all_boids:
            obj.draw(pygame.draw, self.screen)

        for obj in object_collection.ObjectCollection.all_predators:
            obj.draw(pygame.draw, self.screen)

        for obj in object_collection.ObjectCollection.all_obstacles:
            obj.draw(pygame.draw, self.screen)

        pygame.display.flip()
