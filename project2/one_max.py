from individual import Individual
from genotype import Genotype
from problem import Problem
import argparse
from my_random import random


class OneMaxGenotype(Genotype):
    GENOTYPE_SIZE = 20


class OneMaxProblem(Problem):
    TARGET_BIT_PATTERN = None

    @staticmethod
    def parse_args():
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '--genotype-size',
            dest='genotype_size',
            help='Number of bits in a genotype',
            type=int,
            required=False,
            default=OneMaxGenotype.GENOTYPE_SIZE
        )
        arg_parser.add_argument(
            '--target-bit-pattern',
            dest='target_bit_pattern',
            help='This can be set to random in case one does not want the target bit pattern to be all ones',
            choices=['all_ones', 'random'],
            type=str,
            required=False,
            default='all_ones'
        )
        args, unknown_args = arg_parser.parse_known_args()
        OneMaxGenotype.GENOTYPE_SIZE = args.genotype_size
        if args.target_bit_pattern == 'all_ones':
            OneMaxProblem.TARGET_BIT_PATTERN = [1] * OneMaxGenotype.GENOTYPE_SIZE
        elif args.target_bit_pattern == 'random':
            OneMaxProblem.TARGET_BIT_PATTERN = []
            for i in range(OneMaxGenotype.GENOTYPE_SIZE):
                OneMaxProblem.TARGET_BIT_PATTERN.append(1 if random.random() > 0.5 else 0)
            print 'Chosen random target bit pattern:'
            print OneMaxProblem.TARGET_BIT_PATTERN

    @staticmethod
    def calculate_fitness(individual):
        num_correct_bits = sum([
                       1 if individual.phenotype[i] == OneMaxProblem.TARGET_BIT_PATTERN[i] else 0
                       for i in range(OneMaxGenotype.GENOTYPE_SIZE)
                       ])
        half = OneMaxGenotype.GENOTYPE_SIZE * 0.5
        portion_above_avg = max(num_correct_bits - half, 0) / half
        num_wrong_bits = OneMaxGenotype.GENOTYPE_SIZE - num_correct_bits
        error_based_fitness = 1.0 / (1.0 + num_wrong_bits)
        is_solution = num_wrong_bits == 0
        return 0.5 * portion_above_avg + 0.5 * error_based_fitness, is_solution


class OneMaxIndividual(Individual):
    def calculate_phenotype(self):
        self.phenotype = map(lambda x: 1 if x else 0, self.genotype.dna)
