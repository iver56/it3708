from population import Population
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
            '-a',
            '--adult-selection-method',
            dest='adult_selection_method',
            type=str,
            choices=['fgr', 'op', 'gm'],
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

        self.args, unknown_args = arg_parser.parse_known_args()

        if self.args.problem == 'onemax':
            import one_max
            one_max.OneMaxProblem.parse_args()
            self.problem_class = one_max.OneMaxProblem
            self.individual_class = one_max.OneMaxIndividual
        elif self.args.problem == 'lolz':
            import lolz
            lolz.LolzProblem.parse_args()
            self.problem_class = lolz.LolzProblem
            self.individual_class = lolz.LolzIndividual
        elif self.args.problem == 'ss':  # surprising sequences
            pass  # TODO

        self.run()

    def run(self):
        population = Population.get_random_population(
            self.args.population_size,
            self.problem_class,
            self.individual_class
        )

        for generation in range(self.args.num_generations):
            print '---------'
            print 'generation', generation

            population.generate_phenotypes()

            population.evaluate_all()

            population.print_stats()

            # Advance to the next generation
            population.advance()


if __name__ == '__main__':
    Main()
