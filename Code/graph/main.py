import os
import sys
import argparse

import plot_avg_deg
import Mesh_network
import matplotlib.pyplot as plt
import Base
import utils

def parse_arguments(argv):
    # yapf: disable
    parser = argparse.ArgumentParser()
    # parser.add_argument("model",        default="E2ENCR", type=str.lower,  choices=MODEL, help="which model to use",)
    parser.add_argument("--min_node",   default=5, type=int, help="minimun number of nodes",)
    parser.add_argument("--max_node",   default=100, type=int, help="maximun number of nodes",)
    parser.add_argument("--height",     default=1000, type=int, help="height of the grid",)
    parser.add_argument("--width",      default=1000, type=int, help="width of the grid",)
    parser.add_argument("--comm_range",      default=250, type=int, help="communication range",)
    parser.add_argument("--inter_range",      default=250, type=int, help="interference range",)
    parser.add_argument("--path_loss",      default=250, type=int, help="path loss",)
    parser.add_argument("--gateway_prob",      default=0.05, type=int, help="path loss",)


    parser.add_argument("--fig_root",   default="./figs", type=str.lower, help="Folder path to store figures",)
    parser.add_argument("--plot_graph_analysis", action="store_true",    help="whether or not output is redirected",)
    parser.add_argument("--plot_steps", action="store_true",    help="whether or not output is redirected",)
    parser.add_argument("--plot_performance", action="store_true",    help="whether or not output is redirected",)
    parser.add_argument("--use_base", action="store_true",    help="whether or not output is redirected",)
    parser.add_argument("--use_sfs", action="store_true",    help="whether or not output is redirected",)
    parser.add_argument("--plot_special_n3", action="store_true",    help="whether or not output is redirected",)
    parser.add_argument("--plot_special_n4", action="store_true",    help="whether or not output is redirected",)
    # parser.add_argument("--is_disk_limited", action="store_true",    help="whether or not to limit chpkt saving",)
    # yapf: enable

    argv = parser.parse_args(argv)
    if argv.plot_special_n3 or argv.plot_special_n4:
        argv.plot_steps = True
        argv.plot_performance = True
    if not argv.use_base and not argv.use_sfs:
        argv.use_sfs = True
    utils.mkdir(argv.fig_root)
    return argv


def main(argv):
    if argv.plot_graph_analysis:
        print("Plotting graph analysis")
        plot_avg_deg.plot_avg_deg(argv)
    elif argv.plot_performance:
        if argv.use_base:
            print("Plotting performance using base method")
            Ns_base, fni_list_base, xlabel_base, ylabel_base, fig_name_base = Base.test_base_method(argv)

        if argv.use_sfs:
            print("Plotting performance using sfs method")
            Ns_sfs, fni_list_sfs, xlabel_sfs, ylabel_sfs, fig_name_sfs = Mesh_network.test_our_method(argv)

        if not argv.plot_special_n3 and not argv.plot_special_n4:
            fig, ax = plt.subplots()
            if argv.use_base:
                ax.plot(Ns_base, fni_list_base, "-", label='Base Method')
            if argv.use_sfs:
                ax.plot(Ns_sfs, fni_list_sfs, '-', label='SFS Method')
            ax.set_xlabel(xlabel_sfs)
            ax.set_ylabel(ylabel_sfs)
            # ax.set_yscale('log')
            lgd = ax.legend(loc='upper right')
            fig_path = os.path.join(argv.fig_root, f"total_{fig_name_sfs}")

            print(f'Saving to {fig_path}')
            plt.savefig(fig_path, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')

        print()

if __name__ == "__main__":
    # argv = parse_arguments("--plot_graph_analysis".split())
    # argv = parse_arguments("--plot_special_n3".split())
    # argv = parse_arguments("--plot_special_n4 --use_base".split())
    # argv = parse_arguments("--plot_performance --min_node 100 --max_node 100".split())
    argv = parse_arguments(sys.argv[1:])
    print(f"Parameters: {argv}\n")
    main(argv)