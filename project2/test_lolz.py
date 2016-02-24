import unittest
import lolz


class TestLolzProblem(unittest.TestCase):
    def test_fitness(self):
        size = 6
        g1 = lolz.LolzGenotype(size)
        g1.dna = [True, True, True, True, True, True]
        g2 = lolz.LolzGenotype(size)
        g2.dna = [False, False, False, False, False, False]

        p1 = lolz.LolzIndividual(g1)
        p2 = lolz.LolzIndividual(g2)

        fitness1, is_solution = lolz.LolzProblem.calculate_fitness(p1)
        fitness2, is_solution = lolz.LolzProblem.calculate_fitness(p2)
        self.assertEqual(fitness1, 1.0)
        self.assertLess(fitness2, 1.0)

    def test_phenotype(self):
        g1 = lolz.LolzGenotype(3)
        g1.dna = [False, False, True]
        individual = lolz.LolzIndividual(g1)
        self.assertEqual(individual.phenotype, [0, 0, 1])


if __name__ == '__main__':
    unittest.main()
