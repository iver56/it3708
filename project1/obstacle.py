import gfx
import object_collection
import math


class Obstacle(object):
    SIZE = 8
    COLOR = 255, 255, 255

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, draw, screen):
        draw.circle(screen, self.COLOR, [self.x, self.y], self.SIZE)

    @staticmethod
    def obstacle_exists_at_position(x, y):
        for obstacle in object_collection.ObjectCollection.all_obstacles:
            if math.sqrt((x - obstacle.x) ** 2 + (y - obstacle.y) ** 2) < Obstacle.SIZE:
                return True
        return False


def add_obstacle(self, x, y):
    if not Obstacle.obstacle_exists_at_position(x, y):
        obstacle = Obstacle(x, y)
        object_collection.ObjectCollection.all_obstacles.append(obstacle)


gfx.Gfx.add_obstacle = add_obstacle


def remove_all_obstacles(self):
    object_collection.ObjectCollection.all_obstacles = []


gfx.Gfx.remove_all_obstacles = remove_all_obstacles
