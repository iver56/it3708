import json
import argparse
from rnn import Rnn
from ga import BeerTrackerGenotype, BeerTrackerPullGenotype, BeerTrackerWallGenotype

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '--scenario',
        dest='scenario',
        type=str,
        choices=['standard', 'pull', 'wall'],
        required=False,
        default="standard"
    )
    args = arg_parser.parse_args()
    with open('best_individual.json') as best_agent_weights:
        weights = json.load(best_agent_weights)

    if args.scenario == 'pull':
        genotype_class = BeerTrackerPullGenotype
    elif args.scenario == 'wall':
        genotype_class = BeerTrackerWallGenotype
    else:
        genotype_class = BeerTrackerGenotype

    nn = Rnn(
        num_input_nodes=genotype_class.num_input_nodes,
        num_hidden_nodes=genotype_class.num_hidden_nodes,
        num_output_nodes=genotype_class.num_output_nodes
    )
    nn.set_weights(weights)

    activations = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [1, 1, 0, 0, 0],

        [0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
    ]

    for activation in activations:
        output = nn.activate(activation)
        output = map(lambda s: '{0:.10f}'.format(s), output)
        output = '[' + ', '.join(output) + ']  # move ' + ('left' if output[0] > output[1] else 'right')
        print activation, '->', output
