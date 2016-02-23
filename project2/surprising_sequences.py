from individual import Individual
from genotype import Genotype
from problem import Problem
import argparse
import random


class SurprisingSequencesGenotype(Genotype):
    GENOTYPE_SIZE = 8
    ALPHABET = None

    @staticmethod
    def set_alphabet(alphabet_size):
        if alphabet_size < 2:
            raise Exception('Alphabet size must be at least 2')
        if alphabet_size > 26:
            raise Exception('Alphabet size cannot exceed 26')
        SurprisingSequencesGenotype.ALPHABET = []
        ascii_offset = 65  # A
        for i in range(ascii_offset, ascii_offset + alphabet_size):
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
        args, unknown_args = arg_parser.parse_known_args()
        SurprisingSequencesGenotype.GENOTYPE_SIZE = args.genotype_size
        SurprisingSequencesGenotype.set_alphabet(args.alphabet_size)

    @staticmethod
    def calculate_fitness(individual):
        num_repeating_patterns = 0
        patterns = set()

        for i in range(len(individual.genotype.dna)):
            for length in range(1, len(individual.genotype.dna) - i):
                a = individual.genotype.dna[i]
                b = individual.genotype.dna[i+length]
                pattern = (a, length, b)
                print pattern
                if pattern in patterns:
                    num_repeating_patterns += 1
                else:
                    patterns.add(pattern)

        return 1.0 / (1.0 + num_repeating_patterns)


class SurprisingSequencesIndividual(Individual):
    def calculate_phenotype(self):
        self.phenotype = self.genotype.dna

    def get_phenotype_repr(self):
        return ''.join(self.phenotype)
