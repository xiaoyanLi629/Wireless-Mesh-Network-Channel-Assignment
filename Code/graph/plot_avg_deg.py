import os
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import math
import copy

import main
import Gaussian_2d, NodeDistribution, Mesh_node, Mesh_link
import node_distance
import utils
# hyper parameters

marker = ['+', ',', '.', '1']
linestyles = ['-', '--', '-.', ':', (0, (3, 1, 1, 1))]  # ('densely dashdotted',    (0, (3, 1, 1, 1)))


def plot_avg_deg(argv):
    Ns = list(range(argv.min_node, argv.max_node + 1))
    avg_in = []
    avg_out = []
    num_edge = []
    conflict_avg_in = []
    conflict_avg_out = []
    conflict_num_edge = []
    for n in Ns:
        print(f'\t[{n}/ {argv.max_node}] Process {n} nodes')
        t = NodeDistribution.location_matrix(argv.width, argv.height, n, 'Random')
        LM = t.generate()
        # LM = pd.DataFrame([[20, 20],[20, 10], [10,20]])
        nodes, links = utils.gen_graph(LM, argv.gateway_prob, argv.path_loss)
        c_links = utils.gen_conflict_graph(links, argv.inter_range)

        avg_in.append(sum([len(n.in_neighbours) for n in nodes]) / len(nodes))
        avg_out.append(sum([len(n.out_neighbours) for n in nodes]) / len(nodes))
        num_edge.append(len(links))

        conflict_avg_in.append(sum([len(n.in_neighbours) for n in links]) / len(links))
        conflict_avg_out.append(sum([len(n.out_neighbours) for n in links]) / len(links))
        conflict_num_edge.append(len(c_links))

    assert avg_in == avg_out
    assert conflict_avg_in == conflict_avg_out
    fig, ax = plt.subplots()

    ax.plot(Ns, avg_in, linestyle=linestyles[0], label=f"Communication Graph")
    ax.plot(Ns, conflict_avg_in, linestyle=linestyles[0], label=f"Conflict Graph")

    ax.set_xlabel('Number of Nodes')
    ax.set_ylabel('Average degree')
    ax.set_yscale('log')
    lgd = ax.legend(loc='upper left')

    fig_path = os.path.join(argv.fig_root, 'ave_deg.png')
    print(f'Saving to {fig_path}')
    plt.savefig(fig_path, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')

    fig, ax = plt.subplots()

    ax.plot(Ns, num_edge, linestyle=linestyles[0], label=f"Communication Graph")
    ax.plot(Ns, conflict_num_edge, linestyle=linestyles[0], label=f"Conflict Graph")


    ax.set_xlabel('Number of Nodes')
    ax.set_ylabel('Number of Edges')
    ax.set_yscale('log')
    lgd = ax.legend(loc='upper left')

    fig_path = os.path.join(argv.fig_root, 'ave_edge.png')
    print(f'Saving to {fig_path}')
    plt.savefig(fig_path, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    print()


if __name__ == '__main__':
    argv = main.parse_arguments([])
    plot_avg_deg(argv)
