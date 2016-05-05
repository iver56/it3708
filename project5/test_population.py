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

        non_dominated_individuals = p.get_non_dominated_individuals()
        self.assertGreaterEqual(len(non_dominated_individuals), 1)
        self.assertLessEqual(len(non_dominated_individuals), len(individuals))


if __name__ == '__main__':
    unittest.main()
