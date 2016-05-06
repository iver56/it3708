import unittest
import population


class TestPopulation(unittest.TestCase):
    def test_non_dominated_individuals(self):
        p = population.Population(population_size=30, crossover_rate=0.5, mutation_rate=0.5)

        fronts = p.fast_non_dominated_sort()
        self.assertGreaterEqual(len(fronts[1]), 1)

        num_individuals = 0
        for rank in fronts:
            num_individuals += len(fronts[rank])

        self.assertEqual(num_individuals, len(p.individuals))

    def test_calculate_all_crowding_distances(self):
        p = population.Population(
            population_size=30,
            crossover_rate=0.5,
            mutation_rate=0.5,
            individuals=None  # generated randomly in constructor
        )
        pareto_front = p.get_non_dominated_individuals()
        p.calculate_all_crowding_distances(pareto_front)

        for i in range(len(pareto_front)):
            self.assertTrue(pareto_front[i].crowding_distance > -1)


if __name__ == '__main__':
    unittest.main()
