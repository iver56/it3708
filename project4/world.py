class Item(object):
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width


class Agent(object):
    DEFAULT_WIDTH = 5

    def __init__(self, x):
        self.x = x
        self.y = World.HEIGHT - 1
        self.width = Agent.DEFAULT_WIDTH

    def move(self, num_steps):
        self.x = (self.x + num_steps) % World.WIDTH

    def get_occupied_x_positions(self):
        return [(x % World.WIDTH) for x in range(self.x, self.x + self.width)]


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

    def set_agent(self, x):
        self.agent = Agent(x)

    def move_item_down(self):
        self.item.y += 1

    def is_shadowed(self, x):
        if x < self.item.x:
            return False
        elif x < self.item.x + self.item.width:
            return True
        return False
