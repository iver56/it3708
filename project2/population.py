from genotype import Genotype
import random
import statistics


class Population(object):
    MAX_ADULT_POOL_SIZE = 4  # TODO: have a command line argument for this

    def __init__(self, genotypes, problem_class, individual_class, adult_selection_method='gm',
                 parent_selection_method='fp'):
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

        if parent_selection_method == 'fp':
            self.parent_selection_method = self.fitness_proportionate
        elif parent_selection_method == 'ts':
            self.parent_selection_method = self.tournament_selection
        elif parent_selection_method == 'ss':
            self.parent_selection_method = self.sigma_scaling
        elif parent_selection_method == 'bs':
            self.parent_selection_method = self.boltzmann_selection

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
        print 'fitness standard deviation', self.get_population_fitness_std_dev()

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
        self.parent_selection_method()

    def get_adults_fitness_sum(self):
        return sum([individual.fitness for individual in self.adults])

    def get_adults_fitness_std_dev(self):
        return statistics.pstdev([individual.fitness for individual in self.adults])

    def get_population_fitness_std_dev(self):
        return statistics.pstdev([individual.fitness for individual in self.individuals])

    def roulette_selection(self):
        r = random.random()

        # TODO: Could use binary search instead of linear search
        for adult in self.adults:
            if adult.cumulative_fitness > r:
                return adult

    def fitness_proportionate(self):
        adult_fitness_sum = self.get_adults_fitness_sum()

        cumulative_fitness_sum = 0
        for adult in self.adults:
            cumulative_fitness_sum += adult.fitness
            adult.cumulative_fitness = float(cumulative_fitness_sum) / adult_fitness_sum

        self.parents = []
        for i in range(self.population_size):
            parent = self.roulette_selection()
            self.parents.append(parent)

    def sigma_scaling(self):
        return self.fitness_proportionate()  # TODO: implement

    def boltzmann_selection(self):
        return self.fitness_proportionate()  # TODO: implement

    def tournament_selection(self):
        return self.fitness_proportionate()  # TODO: implement

    def reproduce(self):
        num_children = self.population_size

        self.genotypes = []

        for i in range(num_children):
            random_parent = random.choice(self.adults)
            new_genotype = random_parent.genotype.clone()
            new_genotype.mutate()
            self.genotypes.append(new_genotype)
