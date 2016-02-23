import unittest
import one_max


class TestOneMaxProblem(unittest.TestCase):
    def test_fitness(self):
        size = 20
        one_max.OneMaxProblem.TARGET_BIT_PATTERN = [1] * size
        g1 = one_max.OneMaxGenotype(size)
        g1.dna[5] = 1
        g1.dna[8] = 1
        g2 = one_max.OneMaxGenotype(size)

        p1 = one_max.OneMaxIndividual(g1)
        p2 = one_max.OneMaxIndividual(g2)

        fitness1 = one_max.OneMaxProblem.calculate_fitness(p1)
        fitness2 = one_max.OneMaxProblem.calculate_fitness(p2)
        self.assertGreater(fitness1, fitness2)

    def test_phenotype(self):
        g1 = one_max.OneMaxGenotype(3)
        g1.dna = [False, False, True]
        individual = one_max.OneMaxIndividual(g1)
        self.assertEqual(individual.phenotype, [0, 0, 1])


if __name__ == '__main__':
    unittest.main()
