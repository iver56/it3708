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
        '--average',
        nargs='?',
        dest='average',
        help='Average the runs before plotting',
        const=True,
        required=False,
        default=False
    )
    arg_parser.add_argument(
        '--small-font',
        nargs='?',
        dest='small_font',
        help='Use a small font in the legend',
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
        '--answer-found',
        nargs='?',
        dest='answer_found',
        help='Show a line that represents when the answer was found',
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
            is_answer_found_sum = 0
            for log in logs:
                fitness_max_sum += log[x]['max_fitness']
                fitness_avg_sum += log[x]['avg_fitness']
                fitness_std_dev_sum += log[x]['fitness_std_dev']
                is_answer_found_sum += log[x]['is_answer_found']

            fitness_max_avg = float(fitness_max_sum) / len(logs)
            fitness_avg_avg = float(fitness_avg_sum) / len(logs)
            fitness_std_dev_avg = float(fitness_std_dev_sum) / len(logs)
            is_answer_found_avg = float(is_answer_found_sum) / len(logs)

            log_item = {
                'max_fitness': fitness_max_avg,
                'avg_fitness': fitness_avg_avg,
                'fitness_std_dev': fitness_std_dev_avg,
                'is_answer_found': is_answer_found_avg
            }
            average_log.append(log_item)
        logs = [average_log]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for log in logs:
        x = np.array(range(len(log)))
        max_fitness = np.array([log_item['max_fitness'] for log_item in log])
        avg_fitness = np.array([log_item['avg_fitness'] for log_item in log])
        fitness_std_dev = np.array([log_item['fitness_std_dev'] for log_item in log])
        is_answer_found = np.array([log_item['is_answer_found'] for log_item in log])

        fitness_max_plot, = plt.plot(x, max_fitness, label='fitness max')
        fitness_avg_plot, = plt.plot(x, avg_fitness, label='fitness avg')
        fitness_std_dev_plot, = plt.plot(x, fitness_std_dev, label='fitness std dev')
        handles = [fitness_max_plot, fitness_avg_plot, fitness_std_dev_plot]
        if args.answer_found:
            is_answer_found_plot, = plt.plot(x, is_answer_found, label='is answer found')
            handles.append(is_answer_found_plot)
        if args.legend:
            font_p = FontProperties()
            if args.small_font:
                font_p.set_size('small')
            plt.legend(handles=handles, prop=font_p, loc='best')

    ax.set_xlabel('# generations')

    if args.output is None:
        plt.show()
    else:
        plt.savefig(args.output, dpi=96)


if __name__ == "__main__":
    main()
