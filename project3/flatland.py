import agent
import grid
import gfx


class Flatland(object):
    def __init__(self, ann, grid_seed=1, num_time_steps=60, should_visualize=False):
        self.agent = agent.Agent()
        self.grid = grid.Grid(seed=grid_seed)
        self.agent.set_ann(ann)
        self.agent.set_grid(self.grid)
        self.gfx = gfx.Gfx() if should_visualize else None
        self.num_time_steps = num_time_steps

        self.run()

    def run(self):
        for t in range(self.num_time_steps):
            if self.gfx:
                self.gfx.draw(self.grid, self.agent)
            self.agent.move_autonomously()
