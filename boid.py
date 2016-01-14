from gfx import Gfx
import random
import math


class Boid(object):
    initial_speed = 8
    id_counter = 1

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
        self.dx = self.initial_speed * math.cos(angle)
        self.dy = self.initial_speed * math.sin(angle)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.x = self.x % Gfx.width
        self.y = self.y % Gfx.height

    def get_x(self):
        return int(self.x)

    def get_y(self):
        return int(self.y)

    def get_direction(self):
        return math.atan2(self.dy, self.dx)
