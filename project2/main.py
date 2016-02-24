from population import Population
import argparse
import json


class Main(object):
    def __init__(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '--problem',
            dest='problem',
            type=str,
            choices=['onemax', 'lolz', 'ss'],
            required=False,
            default="onemax"
        )
        arg_parser.add_argument(
            '--adult-selection-method',
            dest='adult_selection_method',
            type=str,
            choices=['fgr', 'op', 'gm'],  # full generational replacement, over production or generational mixing
            required=False,
            default="gm"
        )
        arg_parser.add_argument(
            '--parent-selection-method',
            dest='parent_selection_method',
            type=str,
            choices=['fitness_proportionate', 'sigma_scaling', 'boltzmann_selection', 'tournament_selection'],
            required=False,
            default="fitness_proportionate"
        )
        arg_parser.add_argument(
            '--adult-pool-size',
            dest='adult_pool_size',
            help='Max number of adults in the adult pool',
            type=int,
            required=False,
            default=10
        )
        arg_parser.add_argument(
            '-p',
            '--population-size',
            dest='population_size',
            help='Number of genotypes in a population',
            type=int,
            required=False,
            default=20
        )
        arg_parser.add_argument(
            '-g',
            '--num-generations',
            dest='num_generations',
            help='Number of generations',
            type=int,
            required=False,
            default=20
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

        self.args, unknown_args = arg_parser.parse_known_args()

        if self.args.adult_pool_size < 1 or self.args.adult_pool_size > self.args.population_size:
            raise Exception('adult_pool_size must be a positive integer that is not greater than population_size')
        if self.args.crossover_rate < 0.0 or self.args.crossover_rate > 1.0:
            raise Exception('crossover_rate must be between 0.0 and 1.0')
        if self.args.mutation_rate < 0.0 or self.args.mutation_rate > 1.0:
            raise Exception('mutation_rate must be between 0.0 and 1.0')

        if self.args.problem == 'onemax':
            import one_max
            one_max.OneMaxProblem.parse_args()
            self.problem_class = one_max.OneMaxProblem
            self.genotype_class = one_max.OneMaxGenotype
            self.individual_class = one_max.OneMaxIndividual
        elif self.args.problem == 'lolz':
            import lolz
            lolz.LolzProblem.parse_args()
            self.problem_class = lolz.LolzProblem
            self.genotype_class = lolz.LolzGenotype
            self.individual_class = lolz.LolzIndividual
        elif self.args.problem == 'ss':  # surprising sequences
            import surprising_sequences
            surprising_sequences.SurprisingSequencesProblem.parse_args()
            self.problem_class = surprising_sequences.SurprisingSequencesProblem
            self.genotype_class = surprising_sequences.SurprisingSequencesGenotype
            self.individual_class = surprising_sequences.SurprisingSequencesIndividual

        logs = []
        for i in range(self.args.num_runs):
            population = self.run()
            logs.append(population.log)

        with open('logs.json', 'w') as log_file:
            json.dump(logs, log_file)

    def run(self):
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

        for generation in range(self.args.num_generations):
            print '---------'
            print 'generation', generation

            population.set_generation(generation)
            population.generate_phenotypes()
            population.evaluate_all()
            population.adult_selection_handler.select_adults()
            population.log_stats()
            population.parent_selection_handler.select_parents()
            population.reproduce()

        return population


if __name__ == '__main__':
    Main()
