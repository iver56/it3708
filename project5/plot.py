import matplotlib.pyplot as plt


class Plotter(object):
    @staticmethod
    def scatter_plot(population):
        non_dominated_invividuals = population.get_non_dominated_individuals()
        non_dominated_invividuals = sorted(non_dominated_invividuals, key=lambda i: i.tour_distance)
        non_dominated_individual_ids = set(i.id for i in non_dominated_invividuals)

        dominated_individuals = [i for i in population.individuals if i.id not in non_dominated_individual_ids]

        dominated_distances = [i.tour_distance for i in dominated_individuals]
        dominated_costs = [i.tour_cost for i in dominated_individuals]

        non_dominated_distances = [i.tour_distance for i in non_dominated_invividuals]
        non_dominated_costs = [i.tour_cost for i in non_dominated_invividuals]

        plt.scatter(
            dominated_distances,
            dominated_costs,
            marker='o',
            s=50,
            c=(.5, .5, .5),
            alpha=0.5
        )

        plt.plot(non_dominated_distances, non_dominated_costs, c='#ff0000')
        plt.scatter(
            non_dominated_distances,
            non_dominated_costs,
            marker='*',
            s=200,
            c='#ff0000',
            alpha=0.5
        )
        plt.show()
