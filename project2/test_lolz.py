import unittest
import lolz
from genotype import Genotype


class TestLolzProblem(unittest.TestCase):
    def test_fitness(self):
        size = 6
        g1 = Genotype(size)
        g1.dna = [True, True, True, True, True, True]
        g2 = Genotype(size)
        g2.dna = [False, False, False, False, False, False]

        p1 = lolz.LolzIndividual(g1)
        p2 = lolz.LolzIndividual(g2)

        fitness1 = lolz.LolzProblem.calculate_fitness(p1)
        fitness2 = lolz.LolzProblem.calculate_fitness(p2)
        self.assertEqual(fitness1, 6)
        self.assertEqual(fitness2, 4)

    def test_phenotype(self):
        g1 = Genotype(3)
        g1.dna = [False, False, True]
        individual = lolz.LolzIndividual(g1)
        self.assertEqual(individual.phenotype, [0, 0, 1])


if __name__ == '__main__':
    unittest.main()
