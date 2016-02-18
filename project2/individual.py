class Individual(object):
    def __init__(self, genotype):
        self.genotype = genotype
        self.phenotype = None
        self.fitness = None
        self.calculate_phenotype()

    def calculate_phenotype(self):
        # Example:
        # self.phenotype = map(lambda x: 1 if x else 0, self.genotype.dna)
        raise Exception('calculate_phenotype must be implemented by the subclass')

    def set_fitness(self, fitness):
        self.fitness = fitness

    def get_phenotype_repr(self):
        return str(self.phenotype)

    def __repr__(self):
        return self.get_phenotype_repr() + ', fitness = {}'.format(self.fitness)
