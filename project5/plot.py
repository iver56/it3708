import matplotlib.pyplot as plt
from itertools import cycle
import os
import json


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
            individuals = sorted(fronts[rank], key=lambda i: i['tour_distance'])
            distances = [ind['tour_distance'] for ind in individuals]
            costs = [ind['tour_cost'] for ind in individuals]

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

if __name__ == '__main__':
    with open('log.json', 'r') as log_file:
        data = json.load(log_file)

    for generation, fronts in enumerate(data):
        print 'Plotting generation', generation
        Plotter.scatter_plot(
            fronts,
            title='Generation {}'.format(generation),
            output_filename='plot_{0:04d}.png'.format(generation)
        )
    print 'Done'
