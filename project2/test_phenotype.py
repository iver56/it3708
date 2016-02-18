import unittest
from genotype import Genotype
from phenotype import Phenotype


class TestGenotype(unittest.TestCase):
    def test_mutation(self):
        g1 = Genotype(3)
        g1.dna = [False, False, True]
        p1 = Phenotype(g1)
        self.assertEqual(p1.data, [0, 0, 1])


if __name__ == '__main__':
    unittest.main()
