import random


class Genotype(object):
    def __init__(self, dna_size):
        if dna_size < 2:
            raise Exception('Genotype size must be at least 2')
        self.size = dna_size
        self.dna = [False] * dna_size

    def mutate(self):
        i = random.randint(0, self.size - 1)
        self.dna[i] = False if self.dna[i] == 1 else True

    def crossover(self, other_genotype):
        i = random.randint(1, self.size - 2)
        self.dna = self.dna[0:i] + other_genotype.dna[i:]

    @staticmethod
    def get_random_genotype(dna_size):
        genotype = Genotype(dna_size)
        for i in range(dna_size):
            genotype.dna[i] = True if random.random() > 0.5 else False
        return genotype
