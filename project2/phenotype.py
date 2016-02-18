

class Phenotype(object):
    def __init__(self, genotype):
        self.data = map(lambda x: 1 if x else 0, genotype.dna)
        self.fitness = None

    def set_fitness(self, fitness):
        self.fitness = fitness
