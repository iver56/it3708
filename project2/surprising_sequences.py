from individual import Individual
from genotype import Genotype
from problem import Problem
import argparse
import random


class SurprisingSequencesGenotype(Genotype):
    GENOTYPE_SIZE = 8
    ALPHABET = None
    ASCII_OFFSET = 65  # A

    @staticmethod
    def set_alphabet(alphabet_size):
        if alphabet_size < 2:
            raise Exception('Alphabet size must be at least 2')
        if alphabet_size > 26:
            raise Exception('Alphabet size must not exceed 26')
        SurprisingSequencesGenotype.ALPHABET = []
        for i in range(SurprisingSequencesGenotype.ASCII_OFFSET, SurprisingSequencesGenotype.ASCII_OFFSET + alphabet_size):
            SurprisingSequencesGenotype.ALPHABET.append(chr(i))

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

    @staticmethod
    def parse_args():
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '-s',
            '--genotype-size',
            dest='genotype_size',
            help='Number of items in a genotype',
            type=int,
            required=False,
            default=SurprisingSequencesGenotype.GENOTYPE_SIZE
        )
        arg_parser.add_argument(
            '--alphabet-size',
            dest='alphabet_size',
            help='Number of unique characters in the alphabet',
            type=int,
            required=False,
            default=3
        )
        arg_parser.add_argument(
            '--surprising-sequences-mode',
            dest='surprising_sequences_mode',
            help='In local mode only subsequences of distance = 0 are considered',
            choices=['global', 'local'],
            type=str,
            required=False,
            default=SurprisingSequencesProblem.MODE
        )
        args, unknown_args = arg_parser.parse_known_args()
        SurprisingSequencesGenotype.GENOTYPE_SIZE = args.genotype_size
        SurprisingSequencesGenotype.set_alphabet(args.alphabet_size)
        SurprisingSequencesProblem.MODE = args.surprising_sequences_mode

    @staticmethod
    def calculate_fitness(individual):
        num_repeating_patterns = 0
        patterns = set()

        max_subsequence_length = 2 if SurprisingSequencesProblem.MODE == 'local' else len(individual.genotype.dna)

        for i in range(len(individual.genotype.dna) - 1):
            for length in range(1, min(len(individual.genotype.dna) - i, max_subsequence_length)):
                a = individual.genotype.dna[i]
                b = individual.genotype.dna[i+length]
                pattern = (a, length, b)
                if pattern in patterns:
                    num_repeating_patterns += 1
                else:
                    patterns.add(pattern)

        return 1.0 / (1.0 + num_repeating_patterns)


class SurprisingSequencesIndividual(Individual):
    def calculate_phenotype(self):
        self.phenotype = map(lambda c: ord(c) - SurprisingSequencesGenotype.ASCII_OFFSET, self.genotype.dna)

    def get_phenotype_repr(self):
        return ', '.join(map(str, self.phenotype))
