import unittest
import population
import plot


class TestPlotter(unittest.TestCase):
    def test_scatter_plot(self):
        p = population.Population(population_size=30, crossover_rate=0.5, mutation_rate=0.5)
        plot.Plotter.scatter_plot(p)


if __name__ == '__main__':
    unittest.main()
