import matplotlib.pyplot as plt
from itertools import cycle
import os


class Plotter(object):
    @staticmethod
    def scatter_plot(fronts, title='', output_filename=None):
        color_cycle = cycle('bgrcmyk').next
        marker_cycle = cycle('*oD8sh+Hdx').next

        fig = plt.figure()
        ax = fig.add_subplot(111)
        if len(title) > 0:
            ax.set_title(title)

        for rank in fronts:
            individuals = sorted(fronts[rank], key=lambda i: i.tour_distance)
            distances = [ind.tour_distance for ind in individuals]
            costs = [ind.tour_cost for ind in individuals]

            color = color_cycle()
            marker = marker_cycle()

            ax.set_xlabel('Traveling distance')
            ax.set_ylabel('Traveling cost')

            ax.plot(distances, costs, c=color)
            ax.scatter(
                distances,
                costs,
                marker=marker,
                s=150,
                c=color,
                alpha=0.5
            )
        if output_filename is None:
            plt.show()
        else:
            plt.savefig(os.path.join('plots', output_filename), dpi=96)

        plt.close(fig)
