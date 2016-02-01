import random
import math
import gfx
import object_collection


class Boid(object):
    DEFAULT_SPEED = 8
    BOID_NEIGHBOUR_DISTANCE_THRESHOLD = 150
    PREDATOR_NEIGHBOUR_DISTANCE_THRESHOLD = 150
    OBSTACLE_NEIGHBOUR_DISTANCE_THRESHOLD = 150
    SEPARATION_WEIGHT = 15
    SEPARATION_WEIGHT_MULTIPLIER = 1.0
    ALIGNMENT_WEIGHT = 1
    ALIGNMENT_WEIGHT_MULTIPLIER = 1.0
    COHESION_WEIGHT = .04
    COHESION_WEIGHT_MULTIPLIER = 1.0

    PREDATOR_SEPARATION_WEIGHT = 250
    PREDATOR_SEPARATION_WEIGHT_MULTIPLIER = 1.0
    OBSTACLE_SEPARATION_WEIGHT = 20
    OBSTACLE_AVOIDANCE_WEIGHT = 40
    OBSTACLE_SEPARATION_WEIGHT_MULTIPLIER = 1.0

    OBSTACLE_AVOIDANCE_ANGLE = 0.5 * math.pi

    id_counter = 1

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
    SIZE = 8
    LINE_THICKNESS = int(0.4 * SIZE)
    LINE_LENGTH = int(1.7 * SIZE)

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
        self.x = random.randint(0, gfx.Gfx.width)
        self.y = random.randint(0, gfx.Gfx.height)

    def set_random_velocity(self):
        angle = random.random() * 2 * math.pi
        self.dx = self.DEFAULT_SPEED * math.cos(angle)
        self.dy = self.DEFAULT_SPEED * math.sin(angle)

    def update(self):
        nearby_boids = self.get_nearby_boids()
        if len(nearby_boids) > 0:
            # calculate forces
            cohesion_x, cohesion_y = self.calculate_cohesion_force(nearby_boids)
            separation_x, separation_y = self.calculate_separation_force(nearby_boids)
            alignment_x, alignment_y = self.calculate_alignment_force(nearby_boids)

            # apply forces
            self.dx += self.COHESION_WEIGHT * self.COHESION_WEIGHT_MULTIPLIER * cohesion_x
            self.dy += self.COHESION_WEIGHT * self.COHESION_WEIGHT_MULTIPLIER * cohesion_y
            self.dx += self.SEPARATION_WEIGHT * self.SEPARATION_WEIGHT_MULTIPLIER * separation_x
            self.dy += self.SEPARATION_WEIGHT * self.SEPARATION_WEIGHT_MULTIPLIER * separation_y
            self.dx += self.ALIGNMENT_WEIGHT * self.ALIGNMENT_WEIGHT_MULTIPLIER * alignment_x
            self.dy += self.ALIGNMENT_WEIGHT * self.ALIGNMENT_WEIGHT_MULTIPLIER * alignment_y

        nearby_predators = self.get_nearby_predators(self)
        if len(nearby_predators) > 0:
            separation_x, separation_y = self.calculate_separation_force(nearby_predators)

            self.dx += self.PREDATOR_SEPARATION_WEIGHT * self.PREDATOR_SEPARATION_WEIGHT_MULTIPLIER * separation_x
            self.dy += self.PREDATOR_SEPARATION_WEIGHT * self.PREDATOR_SEPARATION_WEIGHT_MULTIPLIER * separation_y

        nearby_obstacles = self.get_nearby_obstacles(self)
        if len(nearby_obstacles) > 0:
            separation_x, separation_y = self.calculate_separation_force(nearby_obstacles)
            avoidance_x, avoidance_y = self.calculate_avoidance_force(nearby_obstacles)

            self.dx += self.OBSTACLE_SEPARATION_WEIGHT * self.OBSTACLE_SEPARATION_WEIGHT_MULTIPLIER * separation_x
            self.dy += self.OBSTACLE_SEPARATION_WEIGHT * self.OBSTACLE_SEPARATION_WEIGHT_MULTIPLIER * separation_y

            self.dx += self.OBSTACLE_AVOIDANCE_WEIGHT * self.OBSTACLE_SEPARATION_WEIGHT_MULTIPLIER * avoidance_x
            self.dy += self.OBSTACLE_AVOIDANCE_WEIGHT * self.OBSTACLE_SEPARATION_WEIGHT_MULTIPLIER * avoidance_y

        # normalize and damp the speed
        speed = math.sqrt(self.dx ** 2 + self.dy ** 2)
        speed_deviation = speed - self.DEFAULT_SPEED
        target_speed = speed - 0.7 * speed_deviation
        self.dx = target_speed * self.dx / speed
        self.dy = target_speed * self.dy / speed

        # move
        self.x += self.dx
        self.y += self.dy
        # wrap around
        self.x = self.x % gfx.Gfx.width
        self.y = self.y % gfx.Gfx.height

    def calculate_cohesion_force(self, neighbours):
        pos_x, pos_y = 0, 0
        for boid in neighbours:
            pos_x += boid.x
            pos_y += boid.y
        pos_x /= len(neighbours)
        pos_y /= len(neighbours)
        force_x, force_y = pos_x - self.x, pos_y - self.y
        return force_x, force_y

    def calculate_separation_force(self, neighbours):
        fx, fy = 0, 0
        for boid in neighbours:
            direction = math.atan2(boid.y - self.y, boid.x - self.x)
            distance = max(self.get_distance_to(boid) - self.SIZE, 1)
            force_scalar = 1 / (1 + distance)
            fx -= force_scalar * math.cos(direction)
            fy -= force_scalar * math.sin(direction)
        return fx, fy

    def calculate_avoidance_force(self, obstacles):
        fx, fy = 0, 0
        self_direction = self.get_direction()
        for obstacle in obstacles:
            direction = math.atan2(obstacle.y - self.y, obstacle.x - self.x)
            angle_diff = ((self_direction - direction + math.pi) % (2 * math.pi)) - math.pi
            if abs(angle_diff) < self.OBSTACLE_AVOIDANCE_ANGLE:
                distance = max(self.get_distance_to(obstacle) - self.SIZE, 1)
                force_scalar = 1 / (1 + distance)
                fx += force_scalar * math.cos(self_direction + 0.5 * math.pi * (1 if angle_diff > 0 else -1))
                fy += force_scalar * math.sin(self_direction + 0.5 * math.pi * (1 if angle_diff > 0 else -1))
        return fx, fy

    def calculate_alignment_force(self, neighbours):
        dx, dy = 0, 0
        for boid in neighbours:
            dx += boid.dx
            dy += boid.dy
        dx /= len(neighbours)
        dy /= len(neighbours)
        force_vector_length = math.sqrt(dx ** 2 + dy ** 2)
        force_x, force_y = dx / force_vector_length, dy / force_vector_length  # normalize
        return force_x, force_y

    def get_x(self):
        return int(self.x)

    def get_y(self):
        return int(self.y)

    def get_direction(self):
        return math.atan2(self.dy, self.dx)

    def get_distance_to(self, other_object):
        return math.sqrt((self.x - other_object.x) ** 2 + (self.y - other_object.y) ** 2)

    def __eq__(self, other_boid):
        return self.id == other_boid.id

    def draw(self, draw, screen):
        color_id = self.id % 8
        color = self.COLOR_MAP[color_id]
        draw.circle(screen, color, [self.get_x(), self.get_y()], self.SIZE)
        draw.line(
            screen,
            color,
            [self.get_x(), self.get_y()],
            [
                self.get_x() + self.LINE_LENGTH * math.cos(self.get_direction()),
                self.get_y() + self.LINE_LENGTH * math.sin(self.get_direction())
            ],
            self.LINE_THICKNESS
        )

    def get_nearby_boids(self):
        nearby_boids = []
        for other_boid in object_collection.ObjectCollection.all_boids:
            if self == other_boid:
                continue
            if self.get_distance_to(other_boid) < self.BOID_NEIGHBOUR_DISTANCE_THRESHOLD:
                nearby_boids.append(other_boid)
        return nearby_boids

    @staticmethod
    def get_nearby_predators(boid):
        nearby_predators = []
        for predator in object_collection.ObjectCollection.all_predators:
            if boid.get_distance_to(predator) < Boid.PREDATOR_NEIGHBOUR_DISTANCE_THRESHOLD:
                nearby_predators.append(predator)
        return nearby_predators

    @staticmethod
    def get_nearby_obstacles(boid):
        nearby_obstacles = []
        for obstacle in object_collection.ObjectCollection.all_obstacles:
            if boid.get_distance_to(obstacle) < Boid.OBSTACLE_NEIGHBOUR_DISTANCE_THRESHOLD:
                nearby_obstacles.append(obstacle)
        return nearby_obstacles


def change_multiplier(self, attr_name, factor):
    current_weight_multiplier = getattr(Boid, attr_name, 1.0)
    new_weight_multiplier = min(max(current_weight_multiplier * factor, 0), 10)
    setattr(Boid, attr_name, new_weight_multiplier)
    print "Boid", attr_name, new_weight_multiplier

gfx.Gfx.change_boid_weight_multiplier = change_multiplier


def reset_multipliers(self):
    Boid.OBSTACLE_SEPARATION_WEIGHT_MULTIPLIER = 1.0
    Boid.PREDATOR_SEPARATION_WEIGHT_MULTIPLIER = 1.0
    Boid.ALIGNMENT_WEIGHT_MULTIPLIER = 1.0
    Boid.COHESION_WEIGHT_MULTIPLIER = 1.0
    Boid.SEPARATION_WEIGHT_MULTIPLIER = 1.0
    print "Boid multipliers reset"

gfx.Gfx.reset_boid_weight_multipliers = reset_multipliers


def add_boids(self):
    num_boids = int(0.1 * len(object_collection.ObjectCollection.all_boids)) + 1
    for i in range(num_boids):
        object_collection.ObjectCollection.all_boids.append(Boid())
    print '#boids:', len(object_collection.ObjectCollection.all_boids)

gfx.Gfx.add_boids = add_boids


def remove_boids(self):
    num_boids = int(0.1 * len(object_collection.ObjectCollection.all_boids)) + 1
    for i in range(num_boids):
        if len(object_collection.ObjectCollection.all_boids) > 0:
            object_collection.ObjectCollection.all_boids.pop()
    print '#boids:', len(object_collection.ObjectCollection.all_boids)

gfx.Gfx.remove_boids = remove_boids
