from gfx import Gfx
import random
import math


class Boid(object):
    SPEED = 8
    NEIGHBOUR_DISTANCE_THRESHOLD = 50
    SEPARATION_WEIGHT = 1
    ALIGNMENT_WEIGHT = 1
    COHESION_WEIGHT = 1

    id_counter = 1
    all_boids = None

    def __init__(self):
        self.id = Boid.id_counter
        Boid.id_counter += 1
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.set_random_position()
        self.set_random_velocity()

    def set_random_position(self):
        self.x = random.randint(0, Gfx.width)
        self.y = random.randint(0, Gfx.height)

    def set_random_velocity(self):
        angle = random.random() * 2 * math.pi
        self.dx = self.SPEED * math.cos(angle)
        self.dy = self.SPEED * math.sin(angle)

    def update(self):
        neighbours = self.get_nearby_boids(self)

        if len(neighbours) > 0:
            cohesion_x, cohesion_y = self.COHESION_WEIGHT * self.calculate_cohesion_force(neighbours)

            self.dx += cohesion_x
            self.dy += cohesion_y

            # normalize velocity
            velocity_vector_length = math.sqrt(self.dx ** 2 + self.dy ** 2)
            self.dx = self.SPEED * self.dx / velocity_vector_length
            self.dy = self.SPEED * self.dy / velocity_vector_length

        self.x += self.dx
        self.y += self.dy
        self.x = self.x % Gfx.width
        self.y = self.y % Gfx.height

    def calculate_cohesion_force(self, neighbours):
        pos_x, pos_y = 0, 0
        for boid in neighbours:
            pos_x += boid.x
            pos_y += boid.y
        pos_x /= len(neighbours)
        pos_y /= len(neighbours)
        force_x, force_y = pos_x - self.x, pos_y - self.y
        force_vector_length = math.sqrt(force_x ** 2 + force_y ** 2)
        force_x, force_y = force_x / force_vector_length, force_y / force_vector_length  # normalize
        return force_x, force_y

    def get_x(self):
        return int(self.x)

    def get_y(self):
        return int(self.y)

    def get_direction(self):
        return math.atan2(self.dy, self.dx)

    def get_distance_to(self, other_boid):
        return math.sqrt((self.x - other_boid.x) ** 2 + (self.y - other_boid.y) ** 2)

    def __eq__(self, other_boid):
        return self.id == other_boid.id

    @staticmethod
    def get_nearby_boids(boid):
        nearby_boids = []
        for other_boid in Boid.all_boids:
            if boid == other_boid:
                continue
            if boid.get_distance_to(other_boid) < Boid.NEIGHBOUR_DISTANCE_THRESHOLD:
                nearby_boids.append(other_boid)
        return nearby_boids
