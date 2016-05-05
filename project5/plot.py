import matplotlib.pyplot as plt
from itertools import cycle


class Plotter(object):
    @staticmethod
    def scatter_plot(population):
        fronts = population.fast_non_dominated_sort()

        color_cycle = cycle('bgrcmyk').next
        marker_cycle = cycle('*oD8sh+Hdx').next

        for rank in fronts:
            individuals = sorted(fronts[rank], key=lambda i: i.tour_distance)
            distances = [ind.tour_distance for ind in individuals]
            costs = [ind.tour_cost for ind in individuals]

            color = color_cycle()
            marker = marker_cycle()

            plt.plot(distances, costs, c=color)
            plt.scatter(
                distances,
                costs,
                marker=marker,
                s=150,
                c=color,
                alpha=0.5
            )
        plt.show()
