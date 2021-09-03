import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import math

import Mesh_node

class Dis(object):
	def __init__(self):
		self.dis

	@classmethod
	def cal_dis(self, node1, node2):
		self.dis = math.sqrt((node1.x_pos-node2.x_pos)**2+(node1.y_pos-node2.y_pos)**2)
		return self.dis

	@classmethod
	def cal_dis_link(self, link1, link2):
		l1_s = link1.node1
		l1_e = link1.node2
		l2_s = link2.node1
		l2_e = link2.node2

		l1_pos = [l1_e.x_pos - l1_s.x_pos, l1_e.y_pos - l1_s.y_pos]
		l2_pos = [l2_e.x_pos - l2_s.x_pos, l2_e.y_pos - l2_s.y_pos]

		self.dis = math.sqrt((l1_pos[0] - l2_pos[0])**2 +
							(l1_pos[1] - l2_pos[1])**2)
		return self.dis
