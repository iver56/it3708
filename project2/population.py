from genotype import Genotype
import random


class Population(object):
    MAX_ADULT_POOL_SIZE = 4

    def __init__(self, genotypes, problem_class, individual_class, adult_selection_method='gm'):
        self.genotypes = genotypes
        self.problem_class = problem_class
        self.individual_class = individual_class
        self.individuals = None
        self.population_size = len(genotypes)
        self.adults = None
        self.parents = None
        if adult_selection_method == 'gm':
            self.adult_selection_method = self.generational_mixing
        elif adult_selection_method == 'op':
            self.adult_selection_method = self.over_production
        else:
            self.adult_selection_method = self.full_generational_replacement

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

    def print_stats(self):
        fittest_phenotype = self.get_fittest_phenotype()
        average_fitness = self.get_average_fitness()
        print 'fittest phenotype', fittest_phenotype
        print 'avg fitness', average_fitness

    def advance(self):
        self.select_adults()
        self.select_parents()
        self.reproduce()

    def select_adults(self):
        self.adult_selection_method()
        for phenotype in self.adults:
            phenotype.genotype.increase_age()

    def generational_mixing(self):
        all_individuals = (self.adults if self.adults else []) + self.individuals
        sorted_individuals = sorted(all_individuals, key=lambda p: p.fitness, reverse=True)
        self.adults = sorted_individuals[0:self.MAX_ADULT_POOL_SIZE]

    def over_production(self):
        children = filter(lambda individual: individual.genotype.age == 0, self.individuals)
        sorted_phenotypes = sorted(children, key=lambda p: p.fitness, reverse=True)
        self.adults = sorted_phenotypes[0:self.MAX_ADULT_POOL_SIZE]

    def full_generational_replacement(self):
        self.adults = self.individuals

    def select_parents(self):
        self.parents = self.adults

    def reproduce(self):
        num_children = self.population_size

        self.genotypes = []

        for i in range(num_children):
            random_parent = random.choice(self.adults)
            new_genotype = random_parent.genotype.clone()
            new_genotype.mutate()
            self.genotypes.append(new_genotype)
