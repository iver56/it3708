import unittest
from genotype import Genotype


class TestGenotype(unittest.TestCase):
    def test_mutation(self):
        g1 = Genotype(6)
        g1.dna = [False, False, False, False, False, False]
        g1.mutate()
        self.assertNotEqual(g1.dna, [False, False, False, False, False, False])

    def test_crossover(self):
        size = 6
        g1 = Genotype(size)
        g2 = Genotype(size)
        g1.dna = [False, False, False, False, False, False]
        g2.dna = [True, True, True, True, True, True]

        g1.crossover(g2)
        self.assertTrue(False in g1.dna)
        self.assertTrue(True in g1.dna)
        self.assertEqual(len(g1.dna), size)


if __name__ == '__main__':
    unittest.main()
