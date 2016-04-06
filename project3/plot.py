import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--input",
        default="logs.json",
        help="Input json file"
    )
    arg_parser.add_argument(
        '--output',
        dest='output',
        help='Output image file (PNG). If specified, interactive window won\t appear.',
        required=False,
        default=None
    )
    args = arg_parser.parse_args()

    with open(args.input) as logs_file:
        logs = json.load(logs_file)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for log in logs:
        x = np.array(range(len(log)))
        max_fitness = np.array([log_item['max_fitness'] for log_item in log])
        avg_fitness = np.array([log_item['avg_fitness'] for log_item in log])
        fitness_std_dev = np.array([log_item['fitness_std_dev'] for log_item in log])

        fitness_max_plot, = plt.plot(x, max_fitness, label='fitness max')
        fitness_avg_plot, = plt.plot(x, avg_fitness, label='fitness avg')
        fitness_std_dev_plot, = plt.plot(x, fitness_std_dev, label='fitness std dev')
        handles = [fitness_max_plot, fitness_avg_plot, fitness_std_dev_plot]

        font_p = FontProperties()
        #font_p.set_size('small')
        plt.legend(handles=handles, prop=font_p, loc='best')

    ax.set_xlabel('# generations')

    if args.output is None:
        plt.show()
    else:
        plt.savefig(args.output, dpi=96)


if __name__ == "__main__":
    main()
