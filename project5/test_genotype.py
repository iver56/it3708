import unittest
import genotype
import copy


class TestGenotype(unittest.TestCase):
    def test_random_genotype(self):
        g = genotype.Genotype.get_random_genotype()
        self.assertEqual(len(g.city_ids), genotype.dm.num_cities)
        self.assertTrue(1 in g.city_ids)

    def test_mutate(self):
        g = genotype.Genotype.get_random_genotype()
        first_city_list = copy.deepcopy(g.city_ids)
        g.mutate()
        self.assertNotEqual(first_city_list, g.city_ids)
        self.assertEqual(set(first_city_list), set(g.city_ids))

if __name__ == '__main__':
    unittest.main()
