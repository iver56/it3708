

class Plotter(object):
    @staticmethod
    def scatter_plot(population):
        """
        Simple demo of a scatter plot.
        """
        import matplotlib.pyplot as plt

        distances = [i.calculate_tour_distance() for i in population.individuals]
        costs = [i.calculate_tour_cost() for i in population.individuals]

        # colors = np.random.rand(N)

        plt.scatter(distances, costs, alpha=0.5)
        plt.show()
