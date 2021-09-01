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
import matplotlib.pyplot as plt

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

plt.scatter(mesh_network[:, 1], mesh_network[:, 2], s=5, alpha=0.5)
plt.title('Mesh Networks Nodes Locations')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('Mesh Networks Nodes Locations.jpg', dpi = 600)
np.savetxt('Nodes locations.csv', mesh_network, delimiter=",")