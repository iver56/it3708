import math


class Rnn(object):
    BIAS_VALUE = 1.0

    def __init__(self, num_inputs, num_hidden_nodes, num_outputs):
        self.num_inputs = num_inputs
        self.num_hidden_nodes = num_hidden_nodes
        self.num_outputs = num_outputs
        self.num_edges = (num_inputs + 1) * num_outputs
        # self.weights_input_to_hidden = [1.0] * (self.num_inputs * self.num_hidden_nodes)
        # TODO

    @staticmethod
    def activation_function(x):
        # sigmoid
        return 0.5 + 0.5 * math.tanh(0.5 * x)

    def activate(self, inputs):
        # TODO
        pass
