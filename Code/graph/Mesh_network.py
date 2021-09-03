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
import main
import plot_graph

# hyper parameters
# links interference range list from 0 to 11
G = [2, 1.125, 0.75, 0.375, 0.125, 0, 0, 0, 0, 0, 0, 0]
F = [0, 0, 0.0009, 0.0175, 0.1295, 0.3521, 0.3521, 0.1295, 0.0175, 0.0009, 0, 0]
Minkowski = 2


def SFS_channel_assignment(Nodes, Links, C_Links, argv, fni_all=False):
	fni_list = []
	# caculate minimum hop count for each node by BFS
	for i in range(len(Nodes)):
		mhc = 1
		if Nodes[i].is_gateway == 1:
			Nodes[i].min_hop_count = mhc
			continue
		queue = []
		vis = []
		queue.append(i)
		vis.append(i)
		while queue:
			s = queue.pop(0)
			mhc += 1
			for j in Nodes[i].out_neighbours:
				if Nodes[j].is_gateway == 1:
					break
				if j in vis:
					continue
				queue.append(j)
				vis.append(j)
		Nodes[i].min_hop_count = mhc
	print('minimum hop count calculated')

	# calculate rank for each link
	for i in range(len(Links)):
		link_neighbours = len(Links[i].node1.out_neighbours) + len(Links[i].node2.in_neighbours)
		link_min_hop_count = min(Links[i].node1.min_hop_count, Links[i].node2.min_hop_count)
		link_distance = Links[i].distance
		Links[i].rank = link_neighbours * link_distance**2 * Links[i].node2.Rx_th / (link_min_hop_count * \
			Links[i].node1.pt * Links[i].node1.gain * Links[i].node2.gain)
	print('rank list generated')

	# create deep copy of links list and sort in descending order by rank
	def take_rank(elem):
		# elem is a link object
		return elem.rank

	des_links_list = Links
	des_links_list.sort(key=take_rank)

	if argv.plot_steps:
		link_ranks = [l.rank for l in Links]
		print(link_ranks)

	for it in range(len(des_links_list)):
		print(f"\r\t[{it+1}/{len(des_links_list)}]", end='')
		SD = np.zeros(12)
		SS = np.zeros(12)
		SE = np.zeros(12)

		node_s = des_links_list[it].node1
		node_t = des_links_list[it].node2
		D_st = node_distance.Dis.cal_dis(node_s, node_t)
		Prt = node_s.pt * node_s.gain * node_t.gain / D_st**2
		# calculate SD, SS, SE score function
		for omega in range(12):
			if it != 0:
				for j in range(it):
					if des_links_list[j].channel == 0:
						delta_omega = abs(omega - des_links_list[j].channel)
					else:
						delta_omega = abs(omega - des_links_list[j].channel + 1)
					node_p = des_links_list[j].node1
					node_q = des_links_list[j].node2
					D_pt = node_distance.Dis.cal_dis(node_p, node_t)
					D_sq = node_distance.Dis.cal_dis(node_s, node_q)
					# claculate how current link interferenced by other links
					if node_p.index in node_t.in_neighbours:
						Prti = node_p.pt * node_p.gain * node_t.gain / D_pt**2
						SD[omega] += Prti / Prt * G[delta_omega]

					# calculate how current link interferences other assigned links
					if node_q.index in node_s.out_neighbours:
						Prtj = node_s.pt * node_s.gain * node_q.gain / D_sq**2
						SS[omega] += pow(
						abs(Prtj / Prt - 1) * G[delta_omega],
						Minkowski)

				SS = [x**(1 / Minkowski) for x in SS]

			# calculate how current link interferences other unassigned links
			if it != len(des_links_list) - 1:
				for j in range(it + 1, len(des_links_list)):
					node_q = des_links_list[j].node2
					D_sq = node_distance.Dis.cal_dis(node_s, node_q)
					if node_q.index in node_s.out_neighbours:
						SE[omega] += node_q.gain / D_sq**2 * F[omega]

		# call set_channel function
		des_links_list[it].set_channel(SD, SS, SE)

		if argv.plot_steps:
			fig_path = os.path.join(argv.fig_root, f"n{len(Nodes)}", f"step_{it:04d}.png")
			plot_graph.plot_graph(Nodes, Links, fig_path=fig_path)
			print(f'Saving to {fig_path} ')

		if fni_all:
			fni = utils.cal_fni(C_Links, argv.inter_range)
			fni_list.append(fni)

	if len(fni_list) == 0:
		fni = utils.cal_fni(C_Links, argv.inter_range)
		fni_list.append(fni)
		print()

	return fni_list

def test_our_method(argv):
	Ns = list(range(argv.min_node, argv.max_node + 1))
	fni_list = []

	if argv.plot_special_n3 or argv.plot_special_n4:
		Ns = [0]
	elif argv.plot_steps and len(Ns) > 1:
		raise Exception("min_node and max_node should equal if you want to plot steps")

	for num in Ns:
		# generate graph
		# generate location matrix
		if argv.plot_special_n3:
			LM = pd.DataFrame([[20, 20], [20, 10], [10, 20]])
		elif argv.plot_special_n4:
			LM = pd.DataFrame([[20, 20], [20, 10], [10, 20], [10, 10]])
		else:
			t = NodeDistribution.location_matrix(argv.width, argv.height, num, 'Random')
			LM = t.generate()
		# LM = pd.DataFrame([[20, 20], [20, 10], [10, 20], [10, 10]])
		Nodes, Links = utils.gen_graph(LM, argv.gateway_prob, argv.path_loss)

		print(f"Processing {len(Nodes)} nodes")
		C_Links = utils.gen_conflict_graph(Links, argv.inter_range)
		print('link list generated')

		if len(Ns) == 1:
			fni_list = SFS_channel_assignment(Nodes, Links, C_Links, argv, fni_all=True)
		else:
			fni_list_local = SFS_channel_assignment(Nodes, Links, C_Links, argv)
			fni_list.append(fni_list_local[-1])
			
	xlabel = None
	ylabel = None
	fig_name = None
	if not argv.plot_special_n3 and not argv.plot_special_n4:
		fig, ax = plt.subplots()

		if len(Ns) == 1:
			Ns = list(range(1, len(Links) + 1))
			xlabel = 'Number of Links with channel assigned'
			ylabel = 'Frictional Network Interference'
			fig_name = "fni_nlink.png"
		else:
			xlabel = 'Number of Nodes'
			ylabel = 'Frictional Network Interference'
			fig_name = "fni_n.png"
		ax.plot(Ns, fni_list)

		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)
		# ax.set_yscale('log')
		fig_path = os.path.join(argv.fig_root, fig_name)

		print(f'Saving to {fig_path}')
		plt.savefig(fig_path, format='png', bbox_inches='tight')
		print()

	return Ns, fni_list, xlabel, ylabel, fig_name



if __name__ == '__main__':
	argv = main.parse_arguments([])
	test_our_method(argv)
