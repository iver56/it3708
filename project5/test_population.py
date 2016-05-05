import unittest
import population
import genotype
import individual


class TestPopulation(unittest.TestCase):
    def test_non_dominated_individuals(self):
        # create random population
        n = 30
        genotypes = [genotype.Genotype.get_random_genotype() for _ in range(n)]
        individuals = [individual.Individual(g) for g in genotypes]
        p = population.Population()
        p.set_individuals(individuals)

        fronts = p.fast_non_dominated_sort()
        self.assertGreaterEqual(len(fronts[1]), 1)

        num_individuals = 0
        for rank in fronts:
            num_individuals += len(fronts[rank])

        self.assertEqual(num_individuals, len(individuals))


if __name__ == '__main__':
    unittest.main()
