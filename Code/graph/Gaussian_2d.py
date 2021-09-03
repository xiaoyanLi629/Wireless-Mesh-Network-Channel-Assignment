import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import math

class Gaussian_Distribution(object):
	def __init__(self, Num, Mean, Cov):
		self.Num = Num
		self.distribution = pd.DataFrame()
		# Mean is a (1,2) vector
		self.Mean = Mean
		# Cov is a (2,2) matrix
		self.Cov = Cov

	def get_pdf(self):
		x, y = np.random.multivariate_normal(self.Mean, self.Cov, self.Num).T
		#plt.plot(x, y, 'x')
		#plt.show()
		self.distribution['x_pos'] = x
		self.distribution['y_pos'] = y
		#print(self.distribution)
		return self.distribution