import unittest
import population
import genotype
import individual
import plot


class TestPlotter(unittest.TestCase):
    def test_scatter_plot(self):
        # create random population
        n = 30
        genotypes = [genotype.Genotype.get_random_genotype() for _ in range(n)]
        individuals = [individual.Individual(g) for g in genotypes]
        p = population.Population()
        p.set_individuals(individuals)
        plot.Plotter.scatter_plot(p)


if __name__ == '__main__':
    unittest.main()
