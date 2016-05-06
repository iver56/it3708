import unittest
import genotype
import copy
import individual


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

    def test_crossover_no_double_elements(self):
        g_1 = genotype.Genotype.get_random_genotype()
        parent_1 = individual.Individual(g_1)

        g_2 = genotype.Genotype.get_random_genotype()
        parent_2 = individual.Individual(g_2)

        new_g = parent_1.genotype.crossover(parent_2.genotype)
        for i in range(len(new_g)):
            count = 0
            for j in range(len(new_g)):
                if j != i and new_g[j] == new_g[i]:
                    if new_g[j] is not None:
                        count += 1
            self.assertTrue(count == 0)

    def test_crossover_distinct_count(self):
        g_1 = genotype.Genotype.get_random_genotype()
        parent_1 = individual.Individual(g_1)

        g_2 = genotype.Genotype.get_random_genotype()
        parent_2 = individual.Individual(g_2)

        new_g = parent_1.genotype.crossover(parent_2.genotype)
        key_map = {}
        for i in range(len(new_g)):
            if new_g[i] not in key_map:
                key_map[new_g[i]] = 1
            else:
                key_map[new_g[i]] += 1

        for k,v in key_map.iteritems():
            self.assertTrue(v == 1)

if __name__ == '__main__':
    unittest.main()
