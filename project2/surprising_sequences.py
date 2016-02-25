from individual import Individual
from genotype import Genotype
from problem import Problem
import argparse
import random


class SurprisingSequencesGenotype(Genotype):
    GENOTYPE_SIZE = 8
    ALPHABET = None

    @staticmethod
    def set_alphabet_by_size(alphabet_size):
        if alphabet_size < 2:
            raise Exception('Alphabet size must be at least 2')
        SurprisingSequencesGenotype.ALPHABET = range(alphabet_size)

    @staticmethod
    def get_random_genotype(dna_size):
        genotype = SurprisingSequencesGenotype(dna_size)
        for i in range(dna_size):
            genotype.dna[i] = random.choice(SurprisingSequencesGenotype.ALPHABET)
        return genotype

    def mutate(self):
        i = random.randint(0, self.size - 1)
        self.dna[i] = random.choice(self.ALPHABET)


class SurprisingSequencesProblem(Problem):
    MODE = 'global'
    FIND_LONGEST_SEQUENCE = False
    LONGEST_SEQUENCE = None
    IS_SATISFIED = True

    @staticmethod
    def parse_args():
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '--genotype-size',
            dest='genotype_size',
            help='(minimum) number of items in a genotype. AKA L',
            type=int,
            required=False,
            default=SurprisingSequencesGenotype.GENOTYPE_SIZE
        )
        arg_parser.add_argument(
            '--alphabet-size',
            dest='alphabet_size',
            help='Number of unique "characters" in the alphabet. AKA S',
            type=int,
            required=False,
            default=3
        )
        arg_parser.add_argument(
            '--surprising-sequences-mode',
            dest='mode',
            help='In local mode only subsequences of distance = 0 are considered',
            choices=['global', 'local'],
            type=str,
            required=False,
            default=SurprisingSequencesProblem.MODE
        )
        arg_parser.add_argument(
            '--surprising-sequences-find-longest',
            dest='find_longest_sequence',
            help='Keep increasing the genotype size for the sake of finding the longest possible sequence with the'
                 ' given alphabet size',
            nargs='?',
            const=True,
            required=False,
            default=False
        )
        args, unknown_args = arg_parser.parse_known_args()
        SurprisingSequencesGenotype.GENOTYPE_SIZE = args.genotype_size
        SurprisingSequencesGenotype.set_alphabet_by_size(args.alphabet_size)
        SurprisingSequencesProblem.MODE = args.mode
        SurprisingSequencesProblem.FIND_LONGEST_SEQUENCE = args.find_longest_sequence

    @staticmethod
    def calculate_fitness(individual):
        num_repeating_patterns = 0
        patterns = set()

        max_subsequence_length = 2 if SurprisingSequencesProblem.MODE == 'local' else len(individual.genotype.dna)

        for i in range(len(individual.genotype.dna) - 1):
            for length in range(1, min(len(individual.genotype.dna) - i, max_subsequence_length)):
                a = individual.genotype.dna[i]
                b = individual.genotype.dna[i + length]
                pattern = (a, length, b)
                if pattern in patterns:
                    num_repeating_patterns += 1
                else:
                    patterns.add(pattern)

        is_solution = num_repeating_patterns == 0
        return 1.0 / (1.0 + num_repeating_patterns), is_solution

    @staticmethod
    def pre_run_hook():
        if SurprisingSequencesProblem.FIND_LONGEST_SEQUENCE and SurprisingSequencesProblem.IS_SATISFIED:
            SurprisingSequencesGenotype.GENOTYPE_SIZE += 1
        print 'Trying to find a surprising sequence of length', SurprisingSequencesGenotype.GENOTYPE_SIZE

    @staticmethod
    def post_run_hook(population):
        if population.solution is None:
            if SurprisingSequencesProblem.LONGEST_SEQUENCE is None:
                SurprisingSequencesProblem.IS_SATISFIED = True
            else:
                SurprisingSequencesProblem.IS_SATISFIED = False
        else:
            SurprisingSequencesProblem.IS_SATISFIED = True
            SurprisingSequencesProblem.LONGEST_SEQUENCE = population.solution
        if SurprisingSequencesProblem.FIND_LONGEST_SEQUENCE:
            print 'Longest sequence found so far:'
            print SurprisingSequencesProblem.LONGEST_SEQUENCE.get_phenotype_repr(), '(length: {})'.format(
                len(SurprisingSequencesProblem.LONGEST_SEQUENCE.phenotype)
            )


class SurprisingSequencesIndividual(Individual):
    def calculate_phenotype(self):
        self.phenotype = self.genotype.dna

    def get_phenotype_repr(self):
        return ', '.join(map(str, self.phenotype))
