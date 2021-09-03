import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import math
import copy

import Mesh_node

class Node_IR(object):
    def __init__(self, node1, node2, path_loss = 1):
        self.ir = math.sqrt(node1.pt * node1.gain * node2.gain * node1.height**2\
								 * node2.height**2 / node2.CS_th) * path_loss