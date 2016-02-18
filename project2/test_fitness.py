import unittest
from genotype import Genotype
from phenotype import Phenotype
import fitness


class TestFitness(unittest.TestCase):
    def test_one_max(self):
        g1 = Genotype(20)
        g1.dna[5] = 1
        g1.dna[8] = 1
        g2 = Genotype(20)

        p1 = Phenotype(g1)
        p2 = Phenotype(g2)

        fitness1 = fitness.OneMaxFitness.evaluate(p1)
        fitness2 = fitness.OneMaxFitness.evaluate(p2)
        self.assertGreater(fitness1, fitness2)

    def test_lolz(self):
        size = 6
        g1 = Genotype(size)
        g1.dna = [True, True, True, True, True, True]
        g2 = Genotype(size)
        g2.dna = [False, False, False, False, False, False]

        p1 = Phenotype(g1)
        p2 = Phenotype(g2)

        fitness1 = fitness.LolzFitness.evaluate(p1)
        fitness2 = fitness.LolzFitness.evaluate(p2)
        self.assertEqual(fitness1, 6)
        self.assertEqual(fitness2, 4)


if __name__ == '__main__':
    unittest.main()
