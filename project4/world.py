class Item(object):
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width


class Agent(object):
    WIDTH = 5
    FIRING_THRESHOLD = 0

    def __init__(self, x, world):
        self.x = x
        self.world = world
        self.y = World.HEIGHT - 1
        self.nn = None
        self.num_small_captures = 0
        self.num_large_captures = 0
        self.num_partial_captures = 0
        self.num_small_misses = 0
        self.num_large_misses = 0

    def set_nn(self, nn):
        self.nn = nn

    def get_occupied_x_positions(self):
        return [(x % World.WIDTH) for x in range(self.x, self.x + self.WIDTH)]

    def sense(self):
        return tuple([(1 if self.world.is_shadowed(x) else 0) for x in self.get_occupied_x_positions()])

    def move(self, num_steps):
        if abs(num_steps) > 4:
            num_steps = 4 if num_steps > 0 else -4
        self.x = (self.x + num_steps) % World.WIDTH

    def act(self):
        sensor_data = self.sense()
        neural_output = self.nn.activate(sensor_data)
        max_neural_output = max(neural_output)
        if max_neural_output > self.FIRING_THRESHOLD:
            num_steps = int(round(5 * max_neural_output))
            argmax = neural_output.index(max_neural_output)
            if argmax == 0:
                # move left
                num_steps *= -1

            self.move(num_steps)

    def try_capture(self):
        if self.world.item.y == self.y:
            num_shadowed_cells = sum(self.sense())
            if num_shadowed_cells == self.WIDTH:
                # entire agent is shadowed, so the item is wider than or as wide as the agent
                self.num_large_captures += 1
            elif self.world.item.width == num_shadowed_cells:
                # not all of the agent's cells are shadowed, hence the item is smaller than the agent
                self.num_small_captures += 1
            elif 0 < num_shadowed_cells < self.world.item.width:
                # item partially shadows agent, so it is not fully captured
                self.num_partial_captures += 1
            elif num_shadowed_cells == 0 and self.world.item.width < self.WIDTH:
                # small item avoided
                self.num_small_misses += 1
            elif num_shadowed_cells == 0 and self.world.item.width >= self.WIDTH:
                # large item avoided
                self.num_large_misses += 1


class PullAgent(Agent):
    PULL_THRESHOLD = 0.5

    def __init__(self, x, world):
        super(PullAgent, self).__init__(x, world)
        self.num_good_pulls = 0
        self.num_bad_pulls = 0

    def act(self):
        sensor_data = self.sense()
        neural_output = self.nn.activate(sensor_data)
        max_neural_output = max(neural_output)

        if neural_output[2] > self.PULL_THRESHOLD:
            self.world.pull_item_down()

            num_shadowed_cells = sum(self.sense())
            if num_shadowed_cells == 0 and self.world.item.width >= self.WIDTH or self.world.item.width == num_shadowed_cells:
                self.num_good_pulls += 1
            else:
                self.num_bad_pulls += 1
        else:
            argmax = neural_output.index(max_neural_output)
            num_steps = int(round(5 * max_neural_output))

            if argmax == 0:
                # move left
                num_steps *= -1

            self.move(num_steps)


class WallAgent(Agent):
    def sense(self):
        sensor_data = [(1 if self.world.is_shadowed(x) else 0) for x in self.get_occupied_x_positions()]
        sensor_data.append(1 if self.x <= 0 else 0)
        sensor_data.append(1 if self.x >= (self.world.WIDTH - self.WIDTH) else 0)
        return tuple(sensor_data)

    def move(self, num_steps):
        if abs(num_steps) > 4:
            num_steps = 4 if num_steps > 0 else -4
        self.x += num_steps
        if self.x < 0:
            self.x = 0
        elif self.x > (self.world.WIDTH - self.WIDTH):
            self.x = self.world.WIDTH - self.WIDTH

    # TODO


class World(object):
    WIDTH = 30
    HEIGHT = 15

    def __init__(self):
        self.item = None
        self.agent = None

    def __repr__(self):
        s = 'World'
        if self.item:
            s += ' with item of width {2} at pos ({0}, {1})'.format(self.item.x, self.item.y, self.item.width)
        return s

    def set_item(self, x, y, width):
        self.item = Item(x, y, width)

    def set_agent(self, agent):
        self.agent = agent

    def move_item_down(self):
        self.item.y += 1

    def pull_item_down(self):
        self.item.y = self.agent.y - 1

    def is_shadowed(self, x):
        if x < self.item.x:
            return False
        elif x < self.item.x + self.item.width:
            return True
        return False
