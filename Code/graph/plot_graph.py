import os
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import math
import copy

import Gaussian_2d, NodeDistribution, Mesh_node, Mesh_link
import node_distance
import utils
# hyper parameters
Num = 100
width = 1000
height = 1000

marker = ['+', ',', '.', '1']
color = ['gainsboro', 'lightcoral', 'maroon', 'bisque', 'tan', 'yellow', 'khaki', 'olive', 'chartreuse', 'forestgreen', 'turquoise', 'deepskyblue', 'lightslategray', 'navy']
linestyles = ['-', '--', '-.', ':', (0, (3, 1, 1, 1))]  # ('densely dashdotted',    (0, (3, 1, 1, 1)))


def plot_graph(nodes, links, fig_path=None):
    x = [n.x_pos for n in nodes]
    y = [n.y_pos for n in nodes]

    lines = dict()
    fig, ax = plt.subplots()
    for l in links:
        xs = [l.node1.x_pos, l.node2.x_pos]
        ys = [l.node1.y_pos, l.node2.y_pos]

        line = ax.plot(xs, ys, color=color[l.channel], alpha=0.5)
        lines[l.channel] = line

    labels = [f"channel {channel}" if channel > 0 else "unassigned" for channel in sorted(lines.keys())]
    lines = [line[0] for _, line in sorted(lines.items(), key=lambda x: x[0])]
    ax.scatter(x, y, marker='.')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    lgd = ax.legend(lines, labels, loc='upper left', bbox_to_anchor=(1, 1), frameon=False)
    if fig_path is None:
        plt.show()
    else:
        utils.mkdir(os.path.dirname(fig_path))
        plt.savefig(fig_path, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')


def main():
    t = NodeDistribution.location_matrix(width, height, Num, 'Random')
    LM = t.generate()
    LM = pd.DataFrame([[20, 20],[20, 10], [10,20], [10, 10]])
    nodes, links = utils.gen_graph(LM)
    plot_graph(nodes, links)

    print()


if __name__ == '__main__':
    main()
