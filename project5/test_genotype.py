import unittest
import genotype


class TestGenotype(unittest.TestCase):
    def test_random_genotype(self):
        g = genotype.Genotype.get_random_genotype()
        self.assertEqual(len(g.city_ids), genotype.dm.get_num_cities())
        self.assertTrue(1 in g.city_ids)


if __name__ == '__main__':
    unittest.main()
