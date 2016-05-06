import unittest
import population
import plot


class TestPlotter(unittest.TestCase):
    def test_scatter_plot(self):
        p = population.Population(population_size=30, crossover_rate=0.5, mutation_rate=0.5)
        fronts = p.fast_non_dominated_sort()
        plot.Plotter.scatter_plot(
            fronts,
            title='Just a test plot. Nothing to see here.',
            output_filename='test.png'
        )


if __name__ == '__main__':
    unittest.main()
