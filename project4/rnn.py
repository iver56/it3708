import math


class Rnn(object):
    BIAS_VALUE = 1.0

    def __init__(self, num_input_nodes, num_hidden_nodes, num_output_nodes):
        self.num_input_nodes = num_input_nodes
        self.num_hidden_nodes = num_hidden_nodes
        self.num_output_nodes = num_output_nodes

        self.edge_chunks = {
            'input_hidden': num_input_nodes * num_hidden_nodes,
            'hidden_hidden': num_hidden_nodes * num_hidden_nodes,
            'bias_hidden': num_hidden_nodes,
            'hidden_output': num_hidden_nodes * num_output_nodes,
            'bias_output': num_output_nodes,
            'output_output': num_output_nodes * num_output_nodes
        }
        i = 0
        self.edge_chunk_indexes = {'input_hidden': i}
        i += self.edge_chunks['input_hidden']
        self.edge_chunk_indexes['hidden_hidden'] = i
        i += self.edge_chunks['hidden_hidden']
        self.edge_chunk_indexes['bias_hidden'] = i
        i += self.edge_chunks['bias_hidden']
        self.edge_chunk_indexes['hidden_output'] = i
        i += self.edge_chunks['hidden_output']
        self.edge_chunk_indexes['bias_output'] = i
        i += self.edge_chunks['bias_output']
        self.edge_chunk_indexes['output_output'] = i

        self.num_edges = sum(self.edge_chunks.values())
        self.weights = None
        self.input_buffer = [0.0] * self.num_input_nodes
        self.hidden_buffer = [0.0] * self.num_hidden_nodes
        self.output_buffer = [0.0] * self.num_output_nodes

    def set_weights(self, weights):
        if len(weights) != self.num_edges:
            raise Exception('Wrong number of weights')

        self.weights = weights

    @staticmethod
    def activation_function(x):
        # sigmoid
        return 0.5 + 0.5 * math.tanh(0.5 * x)

    def input_to_hidden_weight(self, input_index, hidden_index):
        return self.weights[
            self.edge_chunk_indexes['input_hidden'] + input_index * self.num_hidden_nodes + hidden_index
        ]

    def bias_to_hidden_weight(self, hidden_index):
        return self.weights[
            self.edge_chunk_indexes['bias_hidden'] + hidden_index
        ]

    def hidden_to_output_weight(self, hidden_index, output_index):
        return self.weights[
            self.edge_chunk_indexes['hidden_output'] + hidden_index * self.num_output_nodes + output_index
            ]

    def bias_to_output_weight(self, hidden_index):
        return self.weights[
            self.edge_chunk_indexes['bias_output'] + hidden_index
            ]

    def calculate_hidden_values(self):
        for hidden_index in range(self.num_hidden_nodes):
            value = 0
            for input_index in range(self.num_input_nodes):
                weight = self.input_to_hidden_weight(input_index, hidden_index)
                value += self.input_buffer[input_index] * weight
            value += self.BIAS_VALUE * self.bias_to_hidden_weight(hidden_index)

            # TODO: also consider inter-hidden values

            self.hidden_buffer[hidden_index] = self.activation_function(value)

    def calculate_output_values(self):
        for output_index in range(self.num_output_nodes):
            value = 0
            for hidden_index in range(self.num_hidden_nodes):
                weight = self.hidden_to_output_weight(hidden_index, output_index)
                value += self.hidden_buffer[hidden_index] * weight
            value += self.BIAS_VALUE * self.bias_to_output_weight(output_index)

            # TODO: also consider inter-output values

            self.output_buffer[output_index] = self.activation_function(value)

    def activate(self, inputs):
        self.input_buffer = inputs
        self.calculate_hidden_values()
        self.calculate_output_values()
        return self.output_buffer

    def flush(self):
        self.input_buffer = [0.0] * self.num_input_nodes
        self.hidden_buffer = [0.0] * self.num_hidden_nodes
        self.output_buffer = [0.0] * self.num_output_nodes
