from population import Population
import genotype
import phenotype
import fitness
import argparse


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
            '-p',
            '--population-size',
            dest='population_size',
            help='Number of genotypes in a population',
            type=int,
            required=False,
            default=50
        )
        arg_parser.add_argument(
            '-g',
            '--num-generations',
            dest='num_generations',
            help='Number of generations',
            type=int,
            required=False,
            default=50
        )

        self.args = arg_parser.parse_args()

        self.dna_size = None
        if self.args.problem == 'onemax':
            self.dna_size = 20
            self.fitness_class = fitness.OneMaxFitness
        elif self.args.problem == 'lolz':
            self.dna_size = 6
            self.fitness_class = fitness.LolzFitness
        elif self.args.problem == 'ss':
            self.fitness_class = fitness.SurprisingSequencesFitness
            # self.dna_size = ...  # TODO

        self.run()

    def run(self):
        population = Population.get_random_population(self.args.population_size, self.dna_size)

        for generation in range(self.args.num_generations):
            print 'generation', generation
            population.evaluate_all(self.fitness_class)
            fittest_phenotype = population.get_fittest_phenotype()
            average_fitness = population.get_average_fitness()
            print 'max fitness', fittest_phenotype.fitness
            print 'avg fitness', average_fitness
            print '---------'

            population.advance(method=None)  # TODO


if __name__ == '__main__':
    Main()
