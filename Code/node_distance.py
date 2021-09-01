# import numpy as np
import math

def node_distance_function(node1, node2, position_matrix):
    dis = math.sqrt((position_matrix[node1, 1]-position_matrix[node2, 1])**2 + (position_matrix[node1, 2]-position_matrix[node2, 2])**2)
    return dis