

class Phenotype(object):
    def __init__(self, genotype):
        self.genotype = genotype
        self.data = map(lambda x: 1 if x else 0, genotype.dna)
        self.fitness = None

    def set_fitness(self, fitness):
        self.fitness = fitness

    def __repr__(self):
        return str(self.data) + ', fitness = {}'.format(self.fitness)
