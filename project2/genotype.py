import random


class Genotype(object):
    def __init__(self, size):
        if size < 2:
            raise Exception('Genotype size must be at least 2')
        self.size = size
        self.dna = [False] * size

    def mutate(self):
        i = random.randint(0, self.size - 1)
        self.dna[i] = False if self.dna[i] == 1 else True

    def crossover(self, other_genotype):
        i = random.randint(1, self.size - 2)
        self.dna = self.dna[0:i] + other_genotype.dna[i:]
