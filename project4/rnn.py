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
            'hidden_gains': num_hidden_nodes,
            'hidden_time_constants': num_hidden_nodes,
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
        self.edge_chunk_indexes['hidden_gains'] = i
        i += self.edge_chunks['hidden_gains']
        self.edge_chunk_indexes['hidden_time_constants'] = i
        i += self.edge_chunks['hidden_time_constants']

        self.num_edges = sum(self.edge_chunks.values())
        self.weights = None
        self.input_buffer = None
        self.hidden_state = [0.0] * self.num_hidden_nodes
        self.hidden_output = [0.0] * self.num_hidden_nodes
        self.output_state = [0.5] * self.num_output_nodes
        self.output_output = [0.0] * self.num_output_nodes

    def set_weights(self, weights):
        if len(weights) != self.num_edges:
            raise Exception('Wrong number of weights')

        self.weights = weights

    @staticmethod
    def sigmoid(x):
        # sigmoid
        return 0.5 + 0.5 * math.tanh(0.5 * x)

    def input_to_hidden_weight(self, input_index, hidden_index):
        return self.weights[
            self.edge_chunk_indexes['input_hidden'] + input_index * self.num_hidden_nodes + hidden_index
        ]

    def hidden_to_hidden_weight(self, hidden_index, other_hidden_index):
        return self.weights[
            self.edge_chunk_indexes['hidden_hidden'] + hidden_index * self.num_hidden_nodes + other_hidden_index
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

    def hidden_time_constant(self, hidden_index):
        return self.weights[
            self.edge_chunk_indexes['hidden_time_constants'] + hidden_index
            ]

    def hidden_gain(self, hidden_index):
        return self.weights[
            self.edge_chunk_indexes['hidden_gains'] + hidden_index
            ]

    def calculate_hidden_values(self):
        for hidden_index in range(self.num_hidden_nodes):
            s_i = 0.0

            # signal from input nodes
            for input_index in range(self.num_input_nodes):
                weight = self.input_to_hidden_weight(input_index, hidden_index)
                s_i += self.input_buffer[input_index] * weight

            # signal among hidden nodes
            for other_hidden_index in range(self.num_hidden_nodes):
                weight = self.hidden_to_hidden_weight(hidden_index, other_hidden_index)
                s_i += self.hidden_output[other_hidden_index] * weight

            theta_i = self.BIAS_VALUE * self.bias_to_hidden_weight(hidden_index)  # internal bias
            tau_i = self.hidden_time_constant(hidden_index)
            dy_i = (-self.hidden_state[hidden_index] + s_i + theta_i) / tau_i
            self.hidden_state[hidden_index] += dy_i

            g_i = self.hidden_gain(hidden_index)
            self.hidden_output[hidden_index] = self.sigmoid(g_i * self.hidden_state[hidden_index])

    def calculate_output_values(self):
        for output_index in range(self.num_output_nodes):
            value = 0
            for hidden_index in range(self.num_hidden_nodes):
                weight = self.hidden_to_output_weight(hidden_index, output_index)
                value += self.hidden_output[hidden_index] * weight  # TODO

            # TODO: CTRNNify (use output_state etc)

            self.output_output[output_index] = self.sigmoid(value)

    def activate(self, inputs):
        self.input_buffer = inputs
        self.calculate_hidden_values()
        self.calculate_output_values()
        return self.output_output

    def flush(self):
        self.input_buffer = None
        self.hidden_state = [0.0] * self.num_hidden_nodes
        self.hidden_output = [0.0] * self.num_hidden_nodes
        self.output_state = [0.0] * self.num_output_nodes
        self.output_output = [0.0] * self.num_output_nodes
