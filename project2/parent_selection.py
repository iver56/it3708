import argparse
import random
import math


class ParentSelection(object):
    def __init__(self, population, parent_selection_method):
        self.population = population
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
            elif args.tournament_selection_k > self.population.adult_pool_size:
                raise Exception('tournament_selection_k cannot be larger than the population\'s adult_pool_size')
            if args.tournament_selection_epsilon < 0.0 or args.tournament_selection_epsilon > 1.0:
                raise Exception('tournament_selection_epsilon must be between 0.0 and 1.0')

            self.tournament_selection_k = args.tournament_selection_k
            self.tournament_selection_epsilon = args.tournament_selection_epsilon

    def select_parents(self):
        self.parent_selection_method()

    def roulette_wheel_selection(self):
        self.population.parents = []
        for i in range(self.population.population_size):
            parent = self.spin_roulette_wheel_once()
            self.population.parents.append(parent)

    def spin_roulette_wheel_once(self):
        r = random.random()

        # TODO: Could use binary search instead of linear search
        for adult in self.population.adults:
            if adult.cumulative_fitness > r:
                return adult

    def fitness_proportionate(self):
        adult_fitness_sum = self.population.get_adults_fitness_sum()

        cumulative_fitness_sum = 0
        for adult in self.population.adults:
            cumulative_fitness_sum += adult.fitness
            adult.cumulative_fitness = float(cumulative_fitness_sum) / adult_fitness_sum

        self.roulette_wheel_selection()

    def sigma_scaling(self):
        fitness_avg = self.population.get_adults_fitness_avg()
        fitness_std_dev = self.population.get_adults_fitness_std_dev()

        if fitness_std_dev == 0:
            for adult in self.population.adults:
                adult.scaled_fitness = 1.0
        else:
            for adult in self.population.adults:
                adult.scaled_fitness = 1 + (adult.fitness - fitness_avg) / (2 * fitness_std_dev)

        scaled_fitness_sum = sum([individual.scaled_fitness for individual in self.population.adults])

        cumulative_fitness_sum = 0
        for adult in self.population.adults:
            cumulative_fitness_sum += adult.scaled_fitness
            adult.cumulative_fitness = float(cumulative_fitness_sum) / scaled_fitness_sum

        self.roulette_wheel_selection()

    def get_temperature(self):
        return self.population.initial_temperature / (1 + self.population.generation * self.population.cooling_rate)

    def boltzmann_selection(self):
        temperature = self.get_temperature()

        for adult in self.population.adults:
            adult.scaled_fitness = math.exp(adult.fitness / temperature)

        scaled_fitness_sum = sum([individual.scaled_fitness for individual in self.population.adults])

        cumulative_fitness_sum = 0
        for adult in self.population.adults:
            cumulative_fitness_sum += adult.scaled_fitness
            adult.cumulative_fitness = float(cumulative_fitness_sum) / scaled_fitness_sum

        self.roulette_wheel_selection()

    def tournament_selection(self):
        self.population.parents = []
        for i in range(self.population.population_size):
            parent = self.do_one_tournament()
            self.population.parents.append(parent)

    def do_one_tournament(self):
        contestants = random.sample(self.population.adults, self.tournament_selection_k)
        r = random.random()
        if r < self.tournament_selection_epsilon:
            return random.choice(contestants)
        else:
            sorted_contestants = sorted(contestants, key=lambda p: p.fitness, reverse=True)
            return sorted_contestants[0]
