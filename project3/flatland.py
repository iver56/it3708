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
    import argparse
    from ann import Ann

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '--mode',
        dest='mode',
        type=str,
        choices=['static', 'dynamic'],
        required=False,
        default="static"
    )
    arg_parser.add_argument(
        '--num-scenarios',
        dest='num_scenarios',
        help='Number of scenarios per agent per generation',
        type=int,
        required=False,
        default=1
    )
    arg_parser.add_argument(
        '-g',
        '--generation',
        dest='generation',
        help='If dynamic mode, this specifies which generation to pick board(s) from',
        type=int,
        required=False,
        default=0
    )

    args = arg_parser.parse_args()

    with open('best_individual.json') as best_agent_weights:
        weights = json.load(best_agent_weights)

    a = Ann(num_inputs=6, num_outputs=3)
    a.weights = weights

    g = gfx.Gfx()
    g.fps = 8

    for i in range(args.num_scenarios):
        grid_seed = i + (997 * args.generation if args.mode == 'dynamic' else 0)
        print 'grid_seed', i
        f = Flatland(
            ann=a,
            grid_seed=i,
            should_visualize=True
        )
        f.gfx = g
        f.run()
        print '{0} food items, {1} poison items'.format(f.agent.num_food_consumed, f.agent.num_poison_consumed)

