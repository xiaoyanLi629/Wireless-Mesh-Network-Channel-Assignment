import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import math

import Gaussian_2d, NodeDistribution

class Link(object):
	def __init__(self, node1, node2, dis):
		# Note that node1 is the transmitter and node2 is the receiver
		self.node1 = node1
		self.node2 = node2
		# channel should be assigned between [1,12]
		self.channel = 0
		self.busy_idle_ratio = 0.9
		# link rank priority value, not order
		self.rank = 0
		self.distance = dis
		# score function for different frequencies of a link
		self.score = np.zeros(12)

		# used for conflict graph only
		self.out_neighbours = []
		self.in_neighbours = []


	def set_channel(self, SD, SS, SE):
		SD = self.normalize(SD)
		SS = self.normalize(SS)
		SE = self.normalize(SE)
		self.score = np.sum([SD, SS, SE], axis=0)
		self.channel = np.argmin(self.score) + 1

	def set_channel_base(self, SL):
		self.score = SL
		self.channel = np.argmin(self.score) + 1

	@classmethod	
	def normalize(self, v): 
		norm = np.linalg.norm(v) 
		if norm == 0: 
			return v 
		return v / norm
