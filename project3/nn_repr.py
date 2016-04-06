import json
from ann import Ann

nodes = [
    {
        'id': 'i0',
        'x': 1,
        'y': 0,
        'size': 1,
        'label': 'food_left',
        'type': 'input'
    },
    {
        'id': 'i1',
        'x': 2,
        'y': 0,
        'size': 1,
        'label': 'food_forward',
        'type': 'input'
    },
    {
        'id': 'i2',
        'x': 3,
        'y': 0,
        'size': 1,
        'label': 'food_right',
        'type': 'input'
    },
    {
        'id': 'i3',
        'x': 4,
        'y': 0,
        'size': 1,
        'label': 'poison_left',
        'type': 'input'
    },
    {
        'id': 'i4',
        'x': 5,
        'y': 0,
        'size': 1,
        'label': 'poison_forward',
        'type': 'input'
    },
    {
        'id': 'i5',
        'x': 6,
        'y': 0,
        'size': 1,
        'label': 'poison_right',
        'type': 'input'
    },
    {
        'id': 'i6',
        'x': 7,
        'y': 0,
        'size': 1,
        'label': 'bias',
        'type': 'bias'
    },
    {
        'id': 'o0',
        'x': 2,
        'y': 3,
        'size': 1,
        'label': 'motor_left',
        'type': 'output'
    },
    {
        'id': 'o1',
        'x': 4,
        'y': 3,
        'size': 1,
        'label': 'motor_forward',
        'type': 'output'
    },
    {
        'id': 'o2',
        'x': 6,
        'y': 3,
        'size': 1,
        'label': 'motor_right',
        'type': 'output'
    }
]

with open('best_individual.json') as best_agent_weights:
    weights = json.load(best_agent_weights)


num_inputs = 6
num_outputs = 3
a = Ann(num_inputs, num_outputs)
a.weights = weights

edges = []
i = 0

for output_index in range(num_outputs):
    for input_index in range(num_inputs + 1):
        idx = a.convert_2d_to_1d(input_index, output_index)
        weight = a.weights[idx]

        edges.append({
            'id': 'e{}'.format(i),
            'source': 'i{}'.format(input_index),
            'target': 'o{}'.format(output_index),
            'weight': weight
        })
        i += 1

data = {
    'nodes': nodes,
    'edges': edges
}

with open('best_individual_nn.json', 'w') as outfile:
    json.dump(data, outfile)

