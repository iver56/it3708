import unittest
from genotype import Genotype


class TestGenotype(unittest.TestCase):
    def test_mutation(self):
        g1 = Genotype(6)
        g1.bit_array = [0, 0, 0, 0, 0, 0]
        g1.mutate()
        self.assertNotEqual(g1.bit_array, [0, 0, 0, 0, 0, 0])

    def test_crossover(self):
        g1 = Genotype(6)
        g2 = Genotype(6)
        g1.bit_array = [0, 0, 0, 0, 0, 0]
        g2.bit_array = [1, 1, 1, 1, 1, 1]

        g1.crossover(g2)
        self.assertTrue(0 in g1.bit_array)
        self.assertTrue(1 in g1.bit_array)
        self.assertEqual(len(g1.bit_array), 6)


if __name__ == '__main__':
    unittest.main()
