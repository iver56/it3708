from genotype import Genotype
from phenotype import Phenotype


class Population(object):
    def __init__(self, genotypes):
        self.genotypes = genotypes
        self.phenotypes = None

    def evaluate_all(self, fitness_class):
        self.phenotypes = []
        for genotype in self.genotypes:
            phenotype = Phenotype(genotype)
            fitness = fitness_class.evaluate(phenotype)
            phenotype.set_fitness(fitness)
            self.phenotypes.append(phenotype)

    def get_fittest_phenotype(self):
        """
        May raise an exception if the population is not evaluated
        :return:
        """
        max_fitness = self.phenotypes[0].fitness
        fittest_phenotype = self.phenotypes[0]
        for phenotype in self.phenotypes:
            if phenotype.fitness > max_fitness:
                max_fitness = phenotype.fitness
                fittest_phenotype = phenotype
        return fittest_phenotype

    def get_average_fitness(self):
        """
        May raise an exception if the population is not evaluated
        :return:
        """
        fitness_sum = 0
        for phenotype in self.phenotypes:
            fitness_sum += phenotype.fitness
        return float(fitness_sum) / len(self.phenotypes)

    def advance(self, method):
        pass  # TODO


    @staticmethod
    def get_random_population(population_size, dna_size):
        genotypes = []
        for x in range(population_size):
            genotype = Genotype.get_random_genotype(dna_size)
            genotypes.append(genotype)
        return Population(genotypes)
