import unittest
import data_manager
import genotype
import individual
import population


class TestIndividual(unittest.TestCase):
    def test_calculate_tour_distance_and_cost(self):
        g = genotype.Genotype(data_manager.dm.city_ids)
        i = individual.Individual(genotype=g)
        self.assertEqual(i.tour_distance, 153809)
        self.assertEqual(i.tour_cost, 1921)

    def test_domination(self):
        g = genotype.Genotype(data_manager.dm.city_ids)
        i1 = individual.Individual(g)
        i2 = individual.Individual(g)

        i1.tour_distance = 500
        i2.tour_distance = 450

        i1.calculate_tour_cost = 40
        i2.calculate_tour_cost = 35

        self.assertTrue(i2.dominates(i1))
        self.assertFalse(i1.dominates(i2))

    def test_crowding_distace(self):
        p = population.Population()
        p.generate_individuals(20)

        pareto_front = p.get_non_dominated_individuals()
        max_dist = float(pareto_front[-1].tour_distance)
        min_dist = float(pareto_front[0].tour_distance)

        for i in range(len(pareto_front)):
            pareto_front[i].calculate_crowding_distance(i, pareto_front, max_dist, min_dist)

        for i in range(len(pareto_front)):
            self.assertTrue(pareto_front[i].crowding_distance > -1)

if __name__ == '__main__':
    unittest.main()
