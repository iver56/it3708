import sys
import os
from ann import Ann

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project2.individual import Individual
from project2.genotype import Genotype
from project2.problem import Problem


class FlatLandGenotype(Genotype):
    num_inputs = 6 + 1
    num_outputs = 3
    bits_per_weight = 8
    GENOTYPE_SIZE = num_inputs * num_outputs * bits_per_weight


class FlatLandProblem(Problem):
    @staticmethod
    def parse_args():
        pass

    @staticmethod
    def calculate_fitness(individual):
        print individual.phenotype
        return 1


class FlatLandIndividual(Individual):
    def calculate_phenotype(self):
        self.phenotype = Ann(FlatLandGenotype.num_inputs, FlatLandGenotype.num_outputs)
        for i in range(self.phenotype.num_edges):
            j = i * FlatLandGenotype.bits_per_weight
            weight = sum(self.genotype.dna[j:j + FlatLandGenotype.bits_per_weight])
            weight = 4 * float(weight) / FlatLandGenotype.bits_per_weight - 2
            self.phenotype.weights[i] = weight
