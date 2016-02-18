import random


class Genotype(object):
    def __init__(self, size):
        if size < 2:
            raise Exception('Genotype size must be at least 2')
        self.size = size
        self.bit_array = [0] * size

    def mutate(self):
        i = random.randint(0, self.size - 1)
        self.bit_array[i] = 0 if self.bit_array[i] == 1 else 1

    def crossover(self, other_genotype):
        i = random.randint(1, self.size - 2)
        self.bit_array = self.bit_array[0:i] + other_genotype.bit_array[i:]
