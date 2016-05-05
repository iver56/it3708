import unittest
import data_manager
import genotype
import individual


class TestIndividual(unittest.TestCase):
    def test_calculate_tour_distance_and_cost(self):
        g = genotype.Genotype(data_manager.dm.city_ids)
        i = individual.Individual(genotype=g)
        self.assertEqual(i.calculate_tour_distance(), 153809)
        self.assertEqual(i.calculate_tour_cost(), 1921)

    def test_domination(self):
        i1 = individual.Individual(None)
        i2 = individual.Individual(None)

        i1.calculate_tour_distance = lambda: 500
        i2.calculate_tour_distance = lambda: 450

        i1.calculate_tour_cost = lambda: 40
        i2.calculate_tour_cost = lambda: 35

        self.assertTrue(i2.dominates(i1))
        self.assertFalse(i1.dominates(i2))

if __name__ == '__main__':
    unittest.main()
