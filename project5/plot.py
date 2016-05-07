import matplotlib.pyplot as plt
from itertools import cycle
import os
from matplotlib.font_manager import FontProperties


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

        min_distance = min(
            min(
                ind['tour_distance'] for ind in fronts[rank]
            ) for rank in fronts if len(fronts[rank]) > 0
        )
        min_distance_line = ax.axvline(
            min_distance,
            color='g',
            linestyle='-.',
            label='Min distance = {}'.format(min_distance)
        )

        min_cost = min(
            min(
                ind['tour_cost'] for ind in fronts[rank]
            ) for rank in fronts if len(fronts[rank]) > 0
        )
        min_cost_line = ax.axhline(
            min_cost,
            color='g',
            linestyle='-.',
            label='Min cost = {}'.format(min_cost)
        )

        max_distance = max(
            max(
                ind['tour_distance'] for ind in fronts[rank]
            ) for rank in fronts if len(fronts[rank]) > 0
        )
        max_distance_line = ax.axvline(
            max_distance,
            color='r',
            linestyle='--',
            label='Max distance = {}'.format(max_distance)
        )

        max_cost = max(
            max(
                ind['tour_cost'] for ind in fronts[rank]
            ) for rank in fronts if len(fronts[rank]) > 0
        )
        max_cost_line = ax.axhline(
            max_cost,
            color='r',
            linestyle='--',
            label='Max cost = {}'.format(max_cost)
        )

        font_p = FontProperties()
        font_p.set_size('small')
        ax.legend(
            handles=[
                min_distance_line,
                min_cost_line,
                max_distance_line,
                max_cost_line
            ],
            loc='best',
            prop=font_p
        )

        if output_filename is None:
            plt.show()
        else:
            plt.savefig(os.path.join('plots', output_filename), dpi=96)

        plt.close(fig)


if __name__ == '__main__':
    import argparse
    import json

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        '--filename',
        dest='filename',
        type=str,
        required=False,
        default='log.json'
    )

    arg_parser.add_argument(
        '--plot-every',
        dest='plot_every',
        type=int,
        required=False,
        default=1
    )

    arg_parser.add_argument(
        '--pareto-front-comparison',
        dest='pareto_front_comparison',
        nargs='+',
        type=str,
        required=False,
        default=None
    )

    args = arg_parser.parse_args()

    if args.pareto_front_comparison is not None:
        pareto_fronts = {}
        for i, filename in enumerate(args.pareto_front_comparison):
            with open(filename, 'r') as log_file:
                data = json.load(log_file)
            last_generation_fronts = data[len(data) - 1]
            pareto_front = last_generation_fronts['1']
            pareto_fronts[i + 1] = pareto_front
        Plotter.scatter_plot(
            pareto_fronts,
            title='Pareto front comparison',
            output_filename='plot_pareto_front_comparison.png'
        )
    else:
        with open(args.filename, 'r') as log_file:
            data = json.load(log_file)

        for generation, fronts in enumerate(data):
            if generation % args.plot_every == 0 or generation == len(data) - 1:
                print 'Plotting generation', generation + 1
                Plotter.scatter_plot(
                    fronts,
                    title='Generation {}'.format(generation + 1),
                    output_filename='plot_{0:04d}.png'.format(generation + 1)
                )

    print 'Done'
