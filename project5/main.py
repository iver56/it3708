import argparse
import time
import population
import plot
import individual
import random


class Main(object):
    def __init__(self):
        arg_parser = argparse.ArgumentParser()

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
            '--seed',
            dest='seed',
            help='PRNG seed',
            type=int,
            required=False,
            default=1337
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
            '--plot',
            nargs='?',
            dest='plot',
            help='Plot population for each generation. The plots are stored as png files',
            const=True,
            required=False,
            default=False
        )

        self.args, unknown_args = arg_parser.parse_known_args()

        random.seed(self.args.seed)

        start_time = time.time()
        self.population = None

        self.run()

        print "Execution time: {} seconds".format(time.time() - start_time)

    def run(self):
        self.population = population.Population(
            self.args.population_size,
            self.args.crossover_rate,
            self.args.mutation_rate
        )

        for generation in range(self.args.num_generations):
            print 'Generation {}'.format(generation)
            fronts = self.population.fast_non_dominated_sort()
            if self.args.plot:
                plot.Plotter.scatter_plot(
                    fronts,
                    title='Generation {}'.format(generation),
                    output_filename='plot_{0:04d}.png'.format(generation)
                )

            for rank in fronts:
                front = fronts[rank]
                if len(front) > 0:
                    population.Population.calculate_all_crowding_distances(front)

            offspring_genotypes = self.population.create_offspring()
            offspring_individuals = [
                individual.Individual(genotype_instance)
                for genotype_instance in offspring_genotypes
                ]
            combined_population_individuals = set(self.population.individuals).union(set(offspring_individuals))
            combined_population = population.Population(
                population_size=len(combined_population_individuals),
                crossover_rate=self.args.crossover_rate,
                mutation_rate=self.args.mutation_rate,
                individuals=list(combined_population_individuals)
            )

            new_individuals = set()
            fronts = combined_population.fast_non_dominated_sort()
            for rank in fronts:
                num_more_individuals_needed = self.args.population_size - len(new_individuals)
                if len(fronts[rank]) <= num_more_individuals_needed:
                    new_individuals = new_individuals.union(fronts[rank])
                else:
                    front = fronts[rank]
                    population.Population.calculate_all_crowding_distances(front)
                    front = sorted(front, key=lambda x: x.crowding_distance, reverse=True)[:num_more_individuals_needed]
                    new_individuals = new_individuals.union(front)
                    break
            self.population = population.Population(
                population_size=self.args.population_size,
                crossover_rate=self.args.crossover_rate,
                mutation_rate=self.args.mutation_rate,
                individuals=list(new_individuals)
            )


if __name__ == '__main__':
    Main()
