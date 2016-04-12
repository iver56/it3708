from world import World, Agent, PullAgent, WallAgent
import random


class BeerTracker(object):
    def __init__(self, nn, seed=1, scenario='standard', num_time_steps=600):
        self.world = World()
        item_x, item_y, item_width = 0, self.world.HEIGHT + 1, 1  # initialize below world so that a new one is spawned
        self.world.set_item(item_x, item_y, item_width)
        agent_x = 0
        if scenario == 'pull':
            self.agent = PullAgent(agent_x, self.world)
        elif scenario == 'wall':
            self.agent = WallAgent(agent_x, self.world)
        else:
            self.agent = Agent(agent_x, self.world)
        self.agent.set_nn(nn)
        self.world.set_agent(self.agent)
        self.gfx = None
        self.num_time_steps = num_time_steps
        random.seed(seed)  # one could replace this with a prng instance, but it turned out that it became slow

    def run(self):
        for t in range(self.num_time_steps):
            # update
            self.agent.act()
            self.world.move_item_down()
            self.agent.try_capture()

            if self.world.item.y >= self.world.HEIGHT - 1:
                # spawn new item
                random_width = random.randint(1, 6)
                random_x = random.randint(0, self.world.WIDTH - random_width)
                self.world.set_item(x=random_x, y=0, width=random_width)

            # draw
            if self.gfx:
                self.gfx.draw(self.world)
