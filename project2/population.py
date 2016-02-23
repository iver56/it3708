import random
import statistics
import math
import argparse


class Population(object):
    def __init__(self, population_size, problem_class, genotype_class, individual_class, adult_selection_method, parent_selection_method,
                 adult_pool_size, initial_temperature=10.0, cooling_rate=1.0):

        self.genotypes = []
        for x in range(population_size):
            genotype = genotype_class.get_random_genotype(genotype_class.GENOTYPE_SIZE)
            self.genotypes.append(genotype)

        self.problem_class = problem_class
        self.individual_class = individual_class
        self.individuals = None
        self.adult_pool_size = adult_pool_size
        self.population_size = population_size
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.generation = 0
        self.adults = None
        self.parents = None
        self.log = []
        if adult_selection_method == 'gm':
            self.adult_selection_method = self.generational_mixing
        elif adult_selection_method == 'op':
            self.adult_selection_method = self.over_production
        else:
            self.adult_selection_method = self.full_generational_replacement

        if parent_selection_method == 'fitness_proportionate':
            self.parent_selection_method = self.fitness_proportionate
        elif parent_selection_method == 'sigma_scaling':
            self.parent_selection_method = self.sigma_scaling
        elif parent_selection_method == 'boltzmann_selection':
            self.parent_selection_method = self.boltzmann_selection
        elif parent_selection_method == 'tournament_selection':
            self.parent_selection_method = self.tournament_selection
            arg_parser = argparse.ArgumentParser()
            arg_parser.add_argument(
                '--tournament-selection-k',
                dest='tournament_selection_k',
                help='Number of contestants in tournament selection',
                type=int,
                required=False,
                default=2
            )
            arg_parser.add_argument(
                '--tournament-selection-epsilon',
                dest='tournament_selection_epsilon',
                help='probability of random choice in tournament selection',
                type=float,
                required=False,
                default=0.1
            )
            args, unknown_args = arg_parser.parse_known_args()

            if args.tournament_selection_k < 2:
                raise Exception('tournament_selection_k must be at least 2')
            elif args.tournament_selection_k > self.adult_pool_size:
                raise Exception('tournament_selection_k cannot be larger than adult_pool_size')
            if args.tournament_selection_epsilon < 0.0 or args.tournament_selection_epsilon > 1.0:
                raise Exception('tournament_selection_epsilon must be between 0.0 and 1.0')

            self.tournament_selection_k = args.tournament_selection_k
            self.tournament_selection_epsilon = args.tournament_selection_epsilon

    def generate_phenotypes(self):
        self.individuals = []
        for genotype in self.genotypes:
            phenotype = self.individual_class(genotype)
            self.individuals.append(phenotype)

    def evaluate_all(self):
        for phenotype in self.individuals:
            fitness = self.problem_class.calculate_fitness(phenotype)
            phenotype.set_fitness(fitness)

    def get_fittest_individual(self):
        """
        May raise an exception if the population is not evaluated
        :return:
        """
        max_fitness = self.adults[0].fitness
        fittest_individual = self.adults[0]
        for individual in self.adults:
            if individual.fitness > max_fitness:
                max_fitness = individual.fitness
                fittest_individual = individual
        return fittest_individual

    def log_stats(self):
        fittest_individual = self.get_fittest_individual()
        average_fitness = self.get_adults_fitness_avg()
        fitness_std_dev = self.get_adults_fitness_std_dev()
        print 'fittest phenotype:', fittest_individual
        print 'avg fitness =', average_fitness
        print 'fitness standard deviation =', fitness_std_dev
        log_item = {
            'max_fitness': fittest_individual.fitness,
            'avg_fitness': average_fitness,
            'fitness_std_dev': fitness_std_dev
        }
        self.log.append(log_item)

    def select_adults(self):
        self.adult_selection_method()
        for phenotype in self.adults:
            phenotype.genotype.increase_age()

    def generational_mixing(self):
        all_individuals = (self.adults if self.adults else []) + self.individuals
        sorted_individuals = sorted(all_individuals, key=lambda p: p.fitness, reverse=True)
        self.adults = sorted_individuals[0:self.adult_pool_size]

    def over_production(self):
        children = filter(lambda individual: individual.genotype.age == 0, self.individuals)
        sorted_phenotypes = sorted(children, key=lambda p: p.fitness, reverse=True)
        self.adults = sorted_phenotypes[0:self.adult_pool_size]

    def full_generational_replacement(self):
        self.adults = self.individuals

    def select_parents(self):
        self.parent_selection_method()

    def get_adults_fitness_sum(self):
        return sum([individual.fitness for individual in self.adults])

    def get_adults_fitness_avg(self):
        return float(self.get_adults_fitness_sum()) / len(self.adults)

    def get_adults_fitness_std_dev(self):
        return statistics.pstdev([individual.fitness for individual in self.adults])

    def roulette_wheel_selection(self):
        self.parents = []
        for i in range(self.population_size):
            parent = self.spin_roulette_wheel_once()
            self.parents.append(parent)

    def spin_roulette_wheel_once(self):
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

        self.roulette_wheel_selection()

    def sigma_scaling(self):
        fitness_avg = self.get_adults_fitness_avg()
        fitness_std_dev = self.get_adults_fitness_std_dev()

        if fitness_std_dev == 0:
            for adult in self.adults:
                adult.scaled_fitness = 1.0
        else:
            for adult in self.adults:
                adult.scaled_fitness = 1 + (adult.fitness - fitness_avg) / (2 * fitness_std_dev)

        scaled_fitness_sum = sum([individual.scaled_fitness for individual in self.adults])

        cumulative_fitness_sum = 0
        for adult in self.adults:
            cumulative_fitness_sum += adult.scaled_fitness
            adult.cumulative_fitness = float(cumulative_fitness_sum) / scaled_fitness_sum

        self.roulette_wheel_selection()

    def set_generation(self, generation):
        self.generation = generation

    def get_temperature(self):
        return self.initial_temperature / (1 + self.generation * self.cooling_rate)

    def boltzmann_selection(self):
        temperature = self.get_temperature()

        for adult in self.adults:
            adult.scaled_fitness = math.exp(adult.fitness / temperature)

        scaled_fitness_sum = sum([individual.scaled_fitness for individual in self.adults])

        cumulative_fitness_sum = 0
        for adult in self.adults:
            cumulative_fitness_sum += adult.scaled_fitness
            adult.cumulative_fitness = float(cumulative_fitness_sum) / scaled_fitness_sum

        self.roulette_wheel_selection()

    def tournament_selection(self):
        self.parents = []
        for i in range(self.population_size):
            parent = self.do_one_tournament()
            self.parents.append(parent)

    def do_one_tournament(self):
        contestants = random.sample(self.adults, self.tournament_selection_k)
        r = random.random()
        if r < self.tournament_selection_epsilon:
            return random.choice(contestants)
        else:
            sorted_contestants = sorted(contestants, key=lambda p: p.fitness, reverse=True)
            return sorted_contestants[0]

    def reproduce(self):
        num_children = self.population_size

        self.genotypes = []

        for i in range(num_children):
            random_parent = random.choice(self.adults)
            new_genotype = random_parent.genotype.clone()
            new_genotype.mutate()
            self.genotypes.append(new_genotype)
