import argparse
import json
import numpy as np
import matplotlib.pyplot as plt


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--input",
        default="logs.json",
        help="Input json file"
    )
    arg_parser.add_argument(
        '--average',
        nargs='?',
        dest='average',
        help='Average the runs before plotting',
        const=True,
        required=False,
        default=False
    )
    arg_parser.add_argument(
        '--legend',
        nargs='?',
        dest='legend',
        help='Show legend',
        const=True,
        required=False,
        default=False
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

    if args.average:
        average_log = []
        for x in range(len(logs[0])):
            fitness_max_sum = 0
            fitness_avg_sum = 0
            fitness_std_dev_sum = 0
            for log in logs:
                fitness_max_sum += log[x]['max_fitness']
                fitness_avg_sum += log[x]['avg_fitness']
                fitness_std_dev_sum += log[x]['fitness_std_dev']

            fitness_max_avg = float(fitness_max_sum) / len(logs)
            fitness_avg_avg = float(fitness_avg_sum) / len(logs)
            fitness_std_dev_avg = float(fitness_std_dev_sum) / len(logs)

            log_item = {
                'max_fitness': fitness_max_avg,
                'avg_fitness': fitness_avg_avg,
                'fitness_std_dev': fitness_std_dev_avg
            }
            average_log.append(log_item)
        logs = [average_log]

    for log in logs:
        x = np.array(range(len(log)))
        max_fitness = np.array([log_item['max_fitness'] for log_item in log])
        avg_fitness = np.array([log_item['avg_fitness'] for log_item in log])
        fitness_std_dev = np.array([log_item['fitness_std_dev'] for log_item in log])

        fitness_max_plot, = plt.plot(x, max_fitness, label='fitness max')
        fitness_avg_plot, = plt.plot(x, avg_fitness, label='fitness avg')
        fitness_std_dev_plot, = plt.plot(x, fitness_std_dev, label='fitness std dev')
        if args.legend:
            plt.legend(handles=[fitness_max_plot, fitness_avg_plot, fitness_std_dev_plot])

    if args.output is None:
        plt.show()
    else:
        plt.savefig(args.output, dpi=96)


if __name__ == "__main__":
    main()
