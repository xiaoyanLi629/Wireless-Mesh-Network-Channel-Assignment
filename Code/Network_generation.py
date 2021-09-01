# CSE 812
# Generating mesh network graph

# 1000 nodes
# Generating locations first
# 13 channel available

import sys
import numpy as np
import random
import math
import pickle
from node_distance import node_distance_function
np.set_printoptions(threshold=sys.maxsize)
random.seed(30)

node_number = 1000
link_prob = 0.3
width = 500
length = 500
communication_range = 20
channel = 11

print('Running')


# mesh network matrix with 1000 rows and two columns
# The first column is node index
# the second is node x position
# The third is node y position

mesh_network = np.zeros((node_number, 3))

for node in range(node_number):
    mesh_network[node, 0] = node
    mesh_network[node, 1] = random.uniform(0, width)
    mesh_network[node, 2] = random.uniform(1, length)

# link mareix
# The first column is link index
# The second column is node 1
# The third colunmn is node 2
# The fourth column is distance between nodes
# The fifth column is link indicator

link_matrix = np.zeros((node_number*node_number, 5))

link = 0
for i in range(node_number):
    for j in range(node_number):
        link_matrix[link, 0] = link
        link_matrix[link, 1] = i
        link_matrix[link, 2] = j
        node_distance = math.sqrt((mesh_network[i, 1]-mesh_network[j, 1])**2 + (mesh_network[i, 2]-mesh_network[j, 2])**2)
        link_matrix[link, 3] = node_distance
        if node_distance <= 20:
            link_matrix[link, 4] = 1
        else:
            link_matrix[link, 4] = 0
        link = link + 1

# print(mesh_network.shape)
# print(mesh_network[0:10, :])
# print(link_matrix.shape)
# print(link_matrix[0:10, :])

# connected link matrix
# Record links of each node
# The first column is node index
# The second column is link number of the node
connected_link_matrix = np.zeros((node_number, 2))

for i in range(node_number):
    connected_link_matrix[i, 0] = i
    link_number = sum(link_matrix[i*1000:(i+1)*1000, 4])
    connected_link_matrix[i, 1] = link_number

# print(connected_link_matrix[0:10, :])

# link distance matrix
# The first column is one node of first link
# The second column is another node of first link
# The third column is one node of second link
# The fourth columnn is another node of second link
# The fifth column is distance between these two links

link_distance_matrix = np.zeros((int(sum(connected_link_matrix[:, 1])**2), 5))
link_num = int(sum(connected_link_matrix[:, 1]))

# existing link matrix extract existing links from link matrix
# link number * link number rows, total distance calcutaed (can be reduced)
# The first column is link index
# The second column is node 1
# The third colunmn is node 2
# The fourth column is distance between nodes
# The fifth column is link indicator

existing_link_matrix = link_matrix[link_matrix[:, 4]==1, :]

index = 0
for i in range(link_num):
    for j in range(link_num):
        link_distance_matrix[index, 0] = existing_link_matrix[i, 1]
        link_distance_matrix[index, 1] = existing_link_matrix[i, 2]
        link_distance_matrix[index, 2] = existing_link_matrix[j, 1]
        link_distance_matrix[index, 3] = existing_link_matrix[j, 2]

        dis_link1_node1_link2_node1 = node_distance_function(int(link_distance_matrix[index, 0]), int(link_distance_matrix[index, 2]), mesh_network)
        dis_link1_node1_link2_node2 = node_distance_function(int(link_distance_matrix[index, 0]), int(link_distance_matrix[index, 3]), mesh_network)
        dis_link1_node2_link2_node1 = node_distance_function(int(link_distance_matrix[index, 1]), int(link_distance_matrix[index, 2]), mesh_network)
        dis_link1_node2_link2_node2 = node_distance_function(int(link_distance_matrix[index, 1]), int(link_distance_matrix[index, 3]), mesh_network)
        min_dis = min(dis_link1_node1_link2_node1, dis_link1_node1_link2_node2, dis_link1_node2_link2_node1, dis_link1_node2_link2_node2)

        link_distance_matrix[index, 4] = min_dis
        index = index + 1
    if i%500 == 0:
        print("Link number: ", link_num, " | ", "link: ", i)

link_distance_matrix_reduced = link_distance_matrix[link_distance_matrix[:, 0] != link_distance_matrix[:, 1], :]
link_distance_matrix_reduced = link_distance_matrix_reduced[link_distance_matrix_reduced[:, 2] != link_distance_matrix_reduced[:, 3], :]
pickle_out = open("link_distance_matrix_reduced.pickle","wb")
pickle.dump(link_distance_matrix_reduced, pickle_out)
pickle_out.close()

pickle_in = open("link_distance_matrix_reduced.pickle","rb")
link_distance_matrix_reduced_read = pickle.load(pickle_in)
print(link_distance_matrix_reduced_read[0:100, :])
pickle_in.close()
