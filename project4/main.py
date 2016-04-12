import sys
import os
import argparse
import json
import ga
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from project2.population import Population
from beer_tracker import BeerTracker


class Main(object):
    def __init__(self):
        arg_parser = argparse.ArgumentParser()

        arg_parser.add_argument(
            '--scenario',
            dest='scenario',
            type=str,
            choices=['standard', 'pull', 'wall'],
            required=False,
            default="standard"
        )
        arg_parser.add_argument(
            '--mode',
            dest='mode',
            type=str,
            choices=['static', 'dynamic'],
            required=False,
            default="dynamic"
        )
        arg_parser.add_argument(
            '--num-scenarios',
            dest='num_scenarios',
            help='Number of scenarios per agent per generation',
            type=int,
            required=False,
            default=3
        )
        arg_parser.add_argument(
            '--adult-selection-method',
            dest='adult_selection_method',
            type=str,
            choices=['full_generational_replacement', 'over_production', 'generational_mixing'],
            required=False,
            default="over_production"
        )
        arg_parser.add_argument(
            '--parent-selection-method',
            dest='parent_selection_method',
            type=str,
            choices=['fitness_proportionate', 'sigma_scaling', 'boltzmann_selection', 'tournament_selection'],
            required=False,
            default="tournament_selection"
        )
        arg_parser.add_argument(
            '--adult-pool-size',
            dest='adult_pool_size',
            help='Max number of adults in the adult pool',
            type=int,
            required=False,
            default=50
        )
        arg_parser.add_argument(
            '-p',
            '--population-size',
            dest='population_size',
            help='Number of genotypes in a population',
            type=int,
            required=False,
            default=100
        )
        arg_parser.add_argument(
            '-g',
            '--num-generations',
            dest='num_generations',
            help='Number of generations',
            type=int,
            required=False,
            default=250
        )
        arg_parser.add_argument(
            '--num-runs',
            dest='num_runs',
            help='Number of runs',
            type=int,
            required=False,
            default=1
        )
        arg_parser.add_argument(
            '--crossover-rate',
            dest='crossover_rate',
            help='Probability of sexual reproduction (two parents) instead of asexual reproduction (one parent)',
            type=float,
            required=False,
            default=0.5
        )
        arg_parser.add_argument(
            '--mutation-rate',
            dest='mutation_rate',
            help='Probability of gene mutation in new genotypes',
            type=float,
            required=False,
            default=0.5
        )
        arg_parser.add_argument(
            '--silent',
            nargs='?',
            dest='silent',
            help='Add this flag for the program to be less verbose',
            const=True,
            required=False,
            default=False
        )
        arg_parser.add_argument(
            '--visualize-every',
            dest='visualize_every',
            type=int,
            required=False,
            default=-1
        )

        self.args = arg_parser.parse_args()

        if self.args.adult_pool_size < 1 or self.args.adult_pool_size > self.args.population_size:
            raise Exception('adult_pool_size must be a positive integer that is not greater than population_size')
        if self.args.crossover_rate < 0.0 or self.args.crossover_rate > 1.0:
            raise Exception('crossover_rate must be between 0.0 and 1.0')
        if self.args.mutation_rate < 0.0 or self.args.mutation_rate > 1.0:
            raise Exception('mutation_rate must be between 0.0 and 1.0')
        if self.args.num_scenarios < 1:
            raise Exception('num_scenarios must be at least 1')
        if self.args.adult_selection_method == 'generational_mixing' and self.args.mode == 'dynamic':
            raise Exception('Generational mixing and dynamic mode do not work well together')

        ga.BeerTrackerProblem.parse_args()
        self.problem_class = ga.BeerTrackerProblem
        self.problem_class.dynamic_mode = self.args.mode == 'dynamic'
        self.problem_class.num_scenarios = self.args.num_scenarios
        self.problem_class.scenario = self.args.scenario
        if self.args.scenario == 'pull':
            self.genotype_class = ga.BeerTrackerPullGenotype
        elif self.args.scenario == 'wall':
            self.genotype_class = ga.BeerTrackerWallGenotype
        else:
            self.genotype_class = ga.BeerTrackerGenotype
        self.individual_class = ga.BeerTrackerIndividual
        self.individual_class.genotype_class = self.genotype_class

        if self.args.visualize_every >= 1:
            import gfx
            self.beer_tracker_gfx = gfx.Gfx()
            self.beer_tracker_gfx.fps = 8

        logs = []
        for i in range(self.args.num_runs):
            population = self.run()
            logs.append(population.log)

        with open('logs.json', 'w') as log_file:
            json.dump(logs, log_file)

    def run(self):
        self.problem_class.pre_run_hook()

        population = Population(
            self.args.population_size,
            self.problem_class,
            self.genotype_class,
            self.individual_class,
            self.args.adult_selection_method,
            self.args.parent_selection_method,
            self.args.adult_pool_size,
            self.args.crossover_rate,
            self.args.mutation_rate
        )
        self.problem_class.population = population

        for generation in range(self.args.num_generations):
            start_time = time.time()
            if not self.args.silent:
                print '---------'
                print 'generation', generation

            population.set_generation(generation)
            population.generate_phenotypes()
            population.evaluate_all()
            population.adult_selection_handler.select_adults()
            population.log_stats(self.args.silent)
            population.parent_selection_handler.select_parents()
            population.reproduce()
            if not self.args.silent:
                print "execution time: %s seconds" % (time.time() - start_time)

            if self.args.visualize_every >= 1 and generation % self.args.visualize_every == 0:
                fittest_individual = population.get_fittest_individual()

                seed = generation
                bt = BeerTracker(
                    nn=fittest_individual.phenotype,
                    seed=seed,
                    scenario=self.args.scenario
                )
                bt.gfx = self.beer_tracker_gfx
                bt.run()
                print bt.world.agent.num_small_misses, 'small miss(es)'
                print bt.world.agent.num_large_misses, 'large miss(es)'
                print bt.world.agent.num_partial_captures, 'partial capture(s)'
                print bt.world.agent.num_small_captures, 'small capture(s)'
                print bt.world.agent.num_large_captures, 'large capture(s)'

        self.problem_class.post_run_hook(population)

        return population


if __name__ == '__main__':
    Main()
