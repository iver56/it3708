from genotype import Genotype
from phenotype import Phenotype
import random


class Population(object):
    NUM_PARENTS = 4

    def __init__(self, genotypes):
        self.genotypes = genotypes
        self.phenotypes = None
        self.population_size = len(genotypes)
        self.selected_parents = None

    @staticmethod
    def get_random_population(population_size, dna_size):
        genotypes = []
        for x in range(population_size):
            genotype = Genotype.get_random_genotype(dna_size)
            genotypes.append(genotype)
        return Population(genotypes)

    def generate_phenotypes(self):
        self.phenotypes = []
        for genotype in self.genotypes:
            phenotype = Phenotype(genotype)
            self.phenotypes.append(phenotype)

    def evaluate_all(self, fitness_class):
        for phenotype in self.phenotypes:
            fitness = fitness_class.evaluate(phenotype)
            phenotype.set_fitness(fitness)

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

    def get_age_stats(self):
        max_age = self.phenotypes[0].genotype.age
        age_sum = 0
        for phenotype in self.phenotypes:
            age_sum += phenotype.genotype.age
            if phenotype.genotype.age > max_age:
                max_age = phenotype.genotype.age
        avg_age = float(age_sum) / len(self.phenotypes)
        return avg_age, max_age

    def print_stats(self):
        fittest_phenotype = self.get_fittest_phenotype()
        average_fitness = self.get_average_fitness()
        avg_age, max_age = self.get_age_stats()
        print 'avg fitness', average_fitness
        print 'max fitness', fittest_phenotype.fitness
        print 'avg age', avg_age
        print 'max age', max_age

    def advance(self):
        self.select_parents()
        self.reproduce()

    def select_parents(self):
        sorted_phenotypes = sorted(self.phenotypes, key=lambda p: p.fitness, reverse=True)
        self.selected_parents = sorted_phenotypes[0:self.NUM_PARENTS]

    def reproduce(self):
        num_children = self.population_size - self.NUM_PARENTS

        self.genotypes = []
        for phenotype in self.selected_parents:
            phenotype.genotype.increase_age()
            self.genotypes.append(phenotype.genotype)

        for i in range(num_children):
            random_parent = random.choice(self.selected_parents)
            new_genotype = random_parent.genotype.clone()
            new_genotype.mutate()
            self.genotypes.append(new_genotype)
