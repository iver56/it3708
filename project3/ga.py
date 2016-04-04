import sys
import os
from ann import Ann
from flatland import Flatland
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project2.individual import Individual
from project2.genotype import Genotype
from project2.problem import Problem


class FlatLandGenotype(Genotype):
    num_inputs = 6
    num_outputs = 3
    bits_per_weight = 8
    GENOTYPE_SIZE = (num_inputs + 1) * num_outputs * bits_per_weight


class FlatLandProblem(Problem):
    population = None
    dynamic_grid = False
    num_scenarios = 1

    @staticmethod
    def calculate_fitness(individual):
        fitness_sum = 0
        for i in range(FlatLandProblem.num_scenarios):
            grid_seed = i + (997 * FlatLandProblem.population.generation if FlatLandProblem.dynamic_grid else 0)

            flatland_universe = Flatland(
                ann=individual.phenotype,
                grid_seed=grid_seed
            )
            flatland_universe.run()
            fitness_sum += 1 * flatland_universe.agent.num_food_consumed - 0.5 * flatland_universe.agent.num_poison_consumed

        fitness = fitness_sum / FlatLandProblem.num_scenarios
        is_solution = False

        return fitness, is_solution

    @staticmethod
    def post_run_hook(population):
        fittest_individual = population.get_fittest_individual()
        with open('best_individual.json', 'w') as individual_file:
            json.dump(fittest_individual.phenotype.weights, individual_file)


class FlatLandIndividual(Individual):
    def calculate_phenotype(self):
        self.phenotype = Ann(FlatLandGenotype.num_inputs, FlatLandGenotype.num_outputs)
        for i in range(self.phenotype.num_edges):
            j = i * FlatLandGenotype.bits_per_weight
            weight = sum(self.genotype.dna[j:j + FlatLandGenotype.bits_per_weight])
            weight = 4 * float(weight) / FlatLandGenotype.bits_per_weight - 2
            self.phenotype.weights[i] = weight
