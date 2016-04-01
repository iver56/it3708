import math
from grid import Grid, Item
import pygame


class Direction:
    East = 0
    North = 90
    West = 180
    South = 270

    DIRECTIONS = {
        0: East,
        90: North,
        180: West,
        270: South
    }

    def __init__(self):
        pass

    @staticmethod
    def rotate(direction, rotation_amount):
        new_direction = (direction + rotation_amount) % 360
        return Direction.DIRECTIONS[new_direction]


class Agent(object):
    FOOD_REWARD = 5
    POISON_REWARD = -1

    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = Direction.East
        self.grid = None
        self.reward = 0

    def set_grid(self, grid):
        self.grid = grid

    def move(self, relative_direction):
        if relative_direction != 0:
            self.direction = Direction.rotate(self.direction, relative_direction)
        rad = math.radians(self.direction)
        self.x = (self.x + int(round(math.cos(rad)))) % Grid.WIDTH
        self.y = (self.y - int(round(math.sin(rad)))) % Grid.HEIGHT

        # consume any item at that position on the grid
        cell = self.grid.get_cell(self.x, self.y)
        if cell != Item.Nothing:
            if cell == Item.Food:
                self.reward += self.FOOD_REWARD
            elif cell == Item.Poison:
                self.reward += self.POISON_REWARD
            self.grid.clear_cell(self.x, self.y)

