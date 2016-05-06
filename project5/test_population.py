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
            individuals=None  # individuals are generated randomly in population constructor
        )
        fronts = p.fast_non_dominated_sort()
        pareto_front = list(fronts[1])
        population.Population.calculate_all_crowding_distances(pareto_front)

        for i in range(len(pareto_front)):
            self.assertGreaterEqual(pareto_front[i].crowding_distance, 0)


if __name__ == '__main__':
    unittest.main()
