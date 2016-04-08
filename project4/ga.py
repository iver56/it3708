import sys
import os
from beer_tracker import BeerTracker
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project3.ann import Ann
from project2.individual import Individual
from project2.genotype import Genotype
from project2.problem import Problem


class BeerTrackerGenotype(Genotype):
    num_inputs = 5
    num_outputs = 2
    bits_per_weight = 8
    GENOTYPE_SIZE = (num_inputs + 1) * num_outputs * bits_per_weight


class BeerTrackerProblem(Problem):
    population = None
    dynamic_mode = False
    num_scenarios = 1

    @staticmethod
    def calculate_fitness(individual):
        fitness_sum = 0
        for i in range(BeerTrackerProblem.num_scenarios):
            grid_seed = i + (997 * BeerTrackerProblem.population.generation if BeerTrackerProblem.dynamic_mode else 0)

            beer_tracker = BeerTracker(
                nn=individual.phenotype,
                seed=grid_seed
            )
            beer_tracker.run()
            fitness = (
                1 * beer_tracker.world.agent.num_small_captures +
                (-0.2) * beer_tracker.world.agent.num_partial_captures +
                (-0.5) * beer_tracker.world.agent.num_misses +
                0 * beer_tracker.world.agent.num_large_captures
            )
            fitness = max(0, fitness)
            fitness_sum += fitness

        fitness = fitness_sum / BeerTrackerProblem.num_scenarios
        is_solution = False

        return fitness, is_solution

    @staticmethod
    def post_run_hook(population):
        fittest_individual = population.get_fittest_individual()
        with open('best_individual.json', 'w') as individual_file:
            json.dump(fittest_individual.phenotype.weights, individual_file)


class BeerTrackerIndividual(Individual):
    def calculate_phenotype(self):
        self.phenotype = Ann(BeerTrackerGenotype.num_inputs, BeerTrackerGenotype.num_outputs)
        for i in range(self.phenotype.num_edges):
            j = i * BeerTrackerGenotype.bits_per_weight
            weight = sum(self.genotype.dna[j:j + BeerTrackerGenotype.bits_per_weight])
            weight = 4 * float(weight) / BeerTrackerGenotype.bits_per_weight - 2
            self.phenotype.weights[i] = weight
