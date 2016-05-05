import unittest
import data_manager
import genotype
import individual


class TestIndividual(unittest.TestCase):
    def test_calculate_tour_distance(self):
        g = genotype.Genotype(data_manager.dm.city_ids)
        i = individual.Individual(genotype=g)
        self.assertEqual(i.calculate_tour_distance(), 153809)


if __name__ == '__main__':
    unittest.main()
