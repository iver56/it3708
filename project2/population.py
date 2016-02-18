from genotype import Genotype
from individual import Individual
import random


class Population(object):
    NUM_PARENTS = 4

    def __init__(self, genotypes, problem_class, individual_class):
        self.genotypes = genotypes
        self.problem_class = problem_class
        self.individual_class = individual_class
        self.individuals = None
        self.population_size = len(genotypes)
        self.selected_parents = None

    @staticmethod
    def get_random_population(population_size, problem_class, individual_class):
        genotypes = []
        for x in range(population_size):
            genotype = Genotype.get_random_genotype(problem_class.GENOTYPE_SIZE)
            genotypes.append(genotype)
        return Population(genotypes, problem_class, individual_class)

    def generate_phenotypes(self):
        self.individuals = []
        for genotype in self.genotypes:
            phenotype = self.individual_class(genotype)
            self.individuals.append(phenotype)

    def evaluate_all(self):
        for phenotype in self.individuals:
            fitness = self.problem_class.calculate_fitness(phenotype)
            phenotype.set_fitness(fitness)

    def get_fittest_phenotype(self):
        """
        May raise an exception if the population is not evaluated
        :return:
        """
        max_fitness = self.individuals[0].fitness
        fittest_phenotype = self.individuals[0]
        for phenotype in self.individuals:
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
        for phenotype in self.individuals:
            fitness_sum += phenotype.fitness
        return float(fitness_sum) / len(self.individuals)

    def get_age_stats(self):
        max_age = self.individuals[0].genotype.age
        age_sum = 0
        for phenotype in self.individuals:
            age_sum += phenotype.genotype.age
            if phenotype.genotype.age > max_age:
                max_age = phenotype.genotype.age
        avg_age = float(age_sum) / len(self.individuals)
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
        sorted_phenotypes = sorted(self.individuals, key=lambda p: p.fitness, reverse=True)
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
