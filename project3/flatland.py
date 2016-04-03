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

    def run(self):
        for t in range(self.num_time_steps):
            if self.gfx:
                self.gfx.draw(self.grid, self.agent)
            self.agent.move_autonomously()


if __name__ == '__main__':
    # run best agent
    import json
    from ann import Ann

    with open('best_individual.json') as best_agent_weights:
        weights = json.load(best_agent_weights)

    a = Ann(num_inputs=6, num_outputs=3)
    a.weights = weights

    g = gfx.Gfx()
    g.fps = 10

    for i in range(10) + range(10000000, 10000010):
        print 'grid_seed', i
        f = Flatland(
            ann=a,
            grid_seed=i,
            should_visualize=True
        )
        f.gfx = g
        f.run()

