import math


class Ann(object):
    def __init__(self, num_inputs, num_outputs):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.num_edges = (num_inputs + 1) * num_outputs
        self.weights = [1.0] * self.num_edges
        self.bias_value = 1.0

    def convert_2d_to_1d(self, input_index, output_index):
        return input_index + output_index * self.num_inputs

    @staticmethod
    def output_activation_function(x):
        return math.tanh(x)

    def calculate_output_value(self, output_index, inputs):
        output_value = 0
        for input_index in range(self.num_inputs + 1):
            idx = self.convert_2d_to_1d(input_index, output_index)
            weight = self.weights[idx]
            input_value = inputs[input_index] if input_index < self.num_inputs else self.bias_value
            output_value += input_value * weight

        output_value = self.output_activation_function(output_value)
        return output_value

    def activate(self, inputs):
        output_values = []
        for output_index in range(self.num_outputs):
            output_value = self.calculate_output_value(output_index, inputs)
            output_values.append(output_value)
        return output_values

    def set_weights(self, weights):
        if len(weights) != self.num_edges:
            raise Exception('Wrong number of weights')

        self.weights = weights

    def __repr__(self):
        return 'ANN with {0} input(s), 1 bias and {1} output(s)'.format(self.num_inputs, self.num_outputs)
