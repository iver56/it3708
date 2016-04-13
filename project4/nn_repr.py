import json
from rnn import Rnn
import ga
import argparse

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
    genotype_class = ga.BeerTrackerPullGenotype
elif args.scenario == 'wall':
    genotype_class = ga.BeerTrackerWallGenotype
else:
    genotype_class = ga.BeerTrackerGenotype

nn = Rnn(
    num_input_nodes=genotype_class.num_input_nodes,
    num_hidden_nodes=genotype_class.num_hidden_nodes,
    num_output_nodes=genotype_class.num_output_nodes
)
nn.set_weights(weights)


nodes = []

# input nodes
for i in range(nn.num_input_nodes):
    x = float(i) / (nn.num_input_nodes - 1)
    node = {
        'id': 'i{}'.format(i),
        'x': -0.2 + 1.4 * x,
        'y': 1.5 * (x - 0.5) ** 2 - 0.5,
        'size': 1,
        'label': 'input{}'.format(i),
        'type': 'input'
    }
    nodes.append(node)

# bias node
node = {
    'id': 'b0',
    'x': 1.4,
    'y': 0.15,
    'size': 1,
    'label': 'bias',
    'type': 'bias'
}
nodes.append(node)

# hidden nodes
for i in range(nn.num_hidden_nodes):
    x = float(i) / (nn.num_hidden_nodes - 1)
    node = {
        'id': 'h{}'.format(i),
        'x': x,
        'y': 0.5,
        'size': 1,
        'label': 'hidden{}'.format(i),
        'type': 'hidden'
    }
    nodes.append(node)

# output nodes
for i in range(nn.num_output_nodes):
    x = float(i) / (nn.num_output_nodes - 1)
    node = {
        'id': 'o{}'.format(i),
        'x': x,
        'y': 1.0,
        'size': 1,
        'label': 'output{}'.format(i),
        'type': 'output'
    }
    nodes.append(node)

edges = []
i = 0

curvy_edge_type = 'curvedArrow'

for hidden_index in range(nn.num_hidden_nodes):
    # edges from input nodes to hidden nodes
    for input_index in range(nn.num_input_nodes):
        weight = nn.input_to_hidden_weight(input_index, hidden_index)
        if weight != 0.0:
            edges.append({
                'id': 'e{}'.format(i),
                'source': 'i{}'.format(input_index),
                'target': 'h{}'.format(hidden_index),
                'label': str(weight),
                'size': 1,
                'weight': weight
            })
            i += 1

    # edges among hidden nodes
    for other_hidden_index in range(nn.num_hidden_nodes):
        weight = nn.hidden_to_hidden_weight(hidden_index, other_hidden_index)
        if weight != 0.0:
            edges.append({
                'id': 'e{}'.format(i),
                'source': 'h{}'.format(hidden_index),
                'target': 'h{}'.format(other_hidden_index),
                'label': str(weight),
                'size': 1,
                'weight': weight,
                'type': curvy_edge_type
            })
            i += 1

    # edge from bias to hidden node
    weight = nn.bias_to_hidden_weight(hidden_index)
    if weight != 0.0:
        edges.append({
            'id': 'e{}'.format(i),
            'source': 'b0',
            'target': 'h{}'.format(hidden_index),
            'label': str(weight),
            'size': 1,
            'weight': weight
        })
        i += 1

for output_index in range(nn.num_output_nodes):
    for hidden_index in range(nn.num_hidden_nodes):
        weight = nn.hidden_to_output_weight(hidden_index, output_index)
        if weight != 0.0:
            edges.append({
                'id': 'e{}'.format(i),
                'source': 'h{}'.format(hidden_index),
                'target': 'o{}'.format(output_index),
                'label': str(weight),
                'size': 1,
                'weight': weight
            })
            i += 1

data = {
    'nodes': nodes,
    'edges': edges
}

with open('best_individual_nn.json', 'w') as outfile:
    json.dump(data, outfile)

