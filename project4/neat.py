import MultiNEAT as NEAT
import argparse
import statistics
import time
import pprint
import neat_net_wrapper
from beer_tracker import BeerTracker


try:
    import cv2
    import numpy as np
except:
    pass


class Neuroevolution(object):
    def __init__(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '-g',
            '--num-generations',
            dest='num_generations',
            type=int,
            required=False,
            default=100
        )
        arg_parser.add_argument(
            '-p',
            '--population_size',
            dest='population_size',
            type=int,
            required=False,
            default=50
        )
        arg_parser.add_argument(
            '-s',
            '--seed',
            dest='seed',
            type=int,
            required=False,
            default=1
        )
        arg_parser.add_argument(
            '-v',
            '--visualize',
            nargs='?',
            dest='visualize',
            help='Visualize the best neural network in each generation',
            const=True,
            required=False,
            default=False
        )
        arg_parser.add_argument(
            '--visualize-every',
            dest='visualize_every',
            type=int,
            required=False,
            default=1
        )
        arg_parser.add_argument(
            '--allow-clones',
            nargs='?',
            dest='allow_clones',
            help="""Allow clones or nearly identical genomes to exist simultaneously in the
                    population. This is useful for non-deterministic environments,
                    as the same individual will get more than one chance to prove himself, also
                    there will be more chances the same individual to mutate in different ways.
                    The drawback is greatly increased time for reproduction. If you want to
                    search quickly, yet less efficient, leave this to true.""",
            const=True,
            required=False,
            default=False
        )
        arg_parser.add_argument(
            '--add-neuron-prob',
            dest='add_neuron_probability',
            type=float,
            help='MutateAddNeuronProb: Probability for a baby to be mutated with the'
                 ' Add-Neuron mutation',
            required=False,
            default=0.03
        )
        arg_parser.add_argument(
            '--add-link-prob',
            dest='add_link_probability',
            type=float,
            help='MutateAddLinkProb: Probability for a baby to be mutated with the'
                 ' Add-Link mutation',
            required=False,
            default=0.03
        )
        arg_parser.add_argument(
            '--rem-link-prob',
            dest='remove_link_probability',
            type=float,
            help='MutateRemLinkProb: Probability for a baby to be mutated with the'
                 ' Remove-Link mutation',
            required=False,
            default=0.03
        )
        arg_parser.add_argument(
            '--rem-simple-neuron-prob',
            dest='remove_simple_neuron_probability',
            type=float,
            help='MutateRemSimpleNeuronProb: Probability for a baby that a simple neuron'
                 ' will be replaced with a link',
            required=False,
            default=0.03
        )
        arg_parser.add_argument(
            '--fs-neat',
            nargs='?',
            dest='fs_neat',
            help='Use FS-NEAT',
            const=True,
            required=False,
            default=False
        )
        self.args = arg_parser.parse_args()

        if self.args.visualize:
            import gfx
            self.beer_tracker_gfx = gfx.Gfx()
            self.beer_tracker_gfx.fps = 8

        self.run()

    def run(self):
        params = NEAT.Parameters()
        params.PopulationSize = self.args.population_size
        params.AllowClones = self.args.allow_clones
        params.MutateAddNeuronProb = self.args.add_neuron_probability
        params.MutateAddLinkProb = self.args.add_link_probability
        params.MutateRemLinkProb = self.args.remove_link_probability
        params.MutateRemSimpleNeuronProb = self.args.remove_simple_neuron_probability
        params.TimeConstantMutationMaxPower = 1.0
        params.MutateNeuronTimeConstantsProb = 0.2
        params.MutateNeuronBiasesProb = 0.03
        params.MinNeuronTimeConstant = 1.0
        params.MaxNeuronTimeConstant = 2.0
        params.MinNeuronBias = -1.0
        params.MaxNeuronBias = 1.0
        params.Elitism = 0.1  # fraction of population

        num_inputs = 5 + 1  # always add one extra input, see http://multineat.com/docs.html
        num_hidden_nodes = 2
        num_outputs = 2
        genome = NEAT.Genome(
            0,  # ID
            num_inputs,
            num_hidden_nodes,
            num_outputs,
            self.args.fs_neat,
            NEAT.ActivationFunction.UNSIGNED_SIGMOID,  # OutputActType
            NEAT.ActivationFunction.UNSIGNED_SIGMOID,  # HiddenActType
            0,  # SeedType
            params  # Parameters
        )
        pop = NEAT.Population(
            genome,
            params,
            True,  # whether the population should be randomized
            2.0,  # how much the population should be randomized,
            self.args.seed
        )

        for generation in range(1, self.args.num_generations + 1):
            print '--------------------------'
            generation_start_time = time.time()
            print('generation {}'.format(generation))
            # retrieve a list of all genomes in the population
            genotypes = NEAT.GetGenomeList(pop)

            genotype_fitness_values = []

            for genotype in genotypes:
                fitness = self.evaluate(genotype, generation)
                genotype_fitness_values.append(
                    (fitness, genotype)
                )
                genotype.SetFitness(fitness)

            genotype_fitness_values.sort()

            flat_fitness_list = [x[0] for x in genotype_fitness_values]
            max_fitness = flat_fitness_list[-1]
            min_fitness = flat_fitness_list[0]
            avg_fitness = statistics.mean(flat_fitness_list)
            fitness_std_dev = statistics.pstdev(flat_fitness_list)
            stats_item = {
                'generation': generation,
                'fitness_min': min_fitness,
                'fitness_max': max_fitness,
                'fitness_avg': avg_fitness,
                'fitness_std_dev': fitness_std_dev,
            }
            pprint.pprint(stats_item)

            if self.args.visualize and generation % self.args.visualize_every == 0:
                net = NEAT.NeuralNetwork()
                genotype_fitness_values[-1][1].BuildPhenotype(net)  # build phenotype from best genotype
                img = np.zeros((500, 500, 3), dtype=np.uint8)
                NEAT.DrawPhenotype(img, (0, 0, 500, 500), net)
                cv2.imshow("NN", img)
                cv2.waitKey(1)

                nn = neat_net_wrapper.NeatNetWrapper(net)

                seed = generation
                bt = BeerTracker(
                    nn=nn,
                    seed=seed
                )
                bt.gfx = self.beer_tracker_gfx
                bt.run()
                print bt.world.agent.num_small_misses, 'small miss(es)'
                print bt.world.agent.num_large_misses, 'large miss(es)'
                print bt.world.agent.num_partial_captures, 'partial capture(s)'
                print bt.world.agent.num_small_captures, 'small capture(s)'
                print bt.world.agent.num_large_captures, 'large capture(s)'

                net.Save('best_neat_net.txt')


            # advance to the next generation
            pop.Epoch()
            print("Generation execution time: %s seconds" % (time.time() - generation_start_time))

    def evaluate(self, genotype, generation):
        # this creates a neural network (phenotype) from the genome
        net = NEAT.NeuralNetwork()
        genotype.BuildPhenotype(net)

        nn = neat_net_wrapper.NeatNetWrapper(net)

        seed = generation  # assuming dynamic mode, 1 scenario per fitness evaluation

        beer_tracker = BeerTracker(
            nn=nn,
            seed=seed
        )
        beer_tracker.run()

        punishment = min(0.1 * generation, 10)

        fitness = (
            1 * beer_tracker.world.agent.num_small_captures +
            (-punishment) * beer_tracker.world.agent.num_partial_captures +
            (-punishment) * beer_tracker.world.agent.num_small_misses +
            (-punishment) * beer_tracker.world.agent.num_large_captures
        )

        return fitness


if __name__ == '__main__':
    Neuroevolution()
