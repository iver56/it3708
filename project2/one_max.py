from individual import Individual
from problem import Problem


class OneMaxProblem(Problem):
    GENOTYPE_SIZE = 20

    @staticmethod
    def calculate_fitness(individual):
        return sum(individual.phenotype)


class OneMaxIndividual(Individual):
    def calculate_phenotype(self):
        self.phenotype = map(lambda x: 1 if x else 0, self.genotype.dna)
