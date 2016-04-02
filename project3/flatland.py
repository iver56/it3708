import argparse
import agent
import grid
import gfx


class Flatland(object):
    def __init__(self, ann, grid_seed=1, num_time_steps=60, should_visualize=False):
        arg_parser = argparse.ArgumentParser()
        self.args, unknown_args = arg_parser.parse_known_args()
        self.agent = agent.Agent()
        self.grid = grid.Grid(seed=grid_seed)
        self.agent.set_grid(self.grid)
        self.gfx = gfx.Gfx() if should_visualize else None
        self.num_time_steps = num_time_steps
        self.ann = ann

        self.run()

    def run(self):
        for t in range(self.num_time_steps):
            if self.gfx:
                self.gfx.draw(self.grid, self.agent)
            sensor_data = self.agent.sense()
            motor_output = self.ann.activate(sensor_data)
            argmax = motor_output.index(max(motor_output))
            direction = (argmax - 1) * 90
            self.agent.move(direction)
