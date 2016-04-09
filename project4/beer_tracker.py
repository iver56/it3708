from world import Agent, World
import random


class BeerTracker(object):
    def __init__(self, nn, seed=1, num_time_steps=600, should_visualize=False):
        self.world = World()
        item_x, item_y, item_width = 0, self.world.HEIGHT, 1
        self.world.set_item(item_x, item_y, item_width)
        agent_x = 0
        self.agent = Agent(agent_x, self.world)
        self.agent.set_nn(nn)
        self.world.set_agent(self.agent)
        if should_visualize:
            import gfx
            self.gfx = gfx.Gfx()
        else:
            self.gfx = None
        self.num_time_steps = num_time_steps
        random.seed(seed)

    def run(self):
        for t in range(self.num_time_steps):
            # update
            self.agent.move_autonomously()
            self.world.move_item_down()
            self.agent.try_capture()

            if self.world.item.y >= self.world.HEIGHT:
                # spawn new item
                random_x = random.randint(0, self.world.WIDTH - 1)
                random_width = random.randint(1, 6)
                self.world.set_item(x=random_x, y=0, width=random_width)

            # draw
            if self.gfx:
                self.gfx.draw(self.world)


if __name__ == '__main__':
    import json
    import argparse
    import sys
    import os
    import gfx
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from rnn import Rnn

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

    nn = Rnn(num_input_nodes=5, num_hidden_nodes=2, num_output_nodes=2)
    nn.set_weights(weights)

    g = gfx.Gfx()
    g.fps = 8

    for i in range(args.num_scenarios):
        seed = i + ((997 * args.generation) if args.mode == 'dynamic' else 0)
        print 'seed', seed
        bt = BeerTracker(
            nn=nn,
            seed=seed,
            should_visualize=True
        )
        bt.gfx = g
        bt.run()
        print bt.world.agent.num_misses, 'miss(es)'
        print bt.world.agent.num_partial_captures, 'partial capture(s)'
        print bt.world.agent.num_small_captures, 'small capture(s)'
        print bt.world.agent.num_large_captures, 'large capture(s)'

