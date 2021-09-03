import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import math
import random

import Gaussian_2d

# Get a matrix of (n,2) containing n nodes
class location_matrix(object):
    def __init__(self, width, height, Num=100, method='Gaussian_2d', seed=0):
        self.Num = Num
        self.width = width
        self.height = height
        self.distribution = pd.DataFrame()
        self.method = method

        random.seed(seed)

    def generate(self):
        if self.method == 'Gaussian_2d':
            t = Gaussian_2d.Gaussian_Distribution(self.Num, [0,0], [[1,0],[0,1]])
            lm = t.get_pdf()
            return lm
        elif self.method == 'Random':
            X = [random.random() for _ in range(self.Num)]
            Y = [random.random() for _ in range(self.Num)]
            loc = pd.DataFrame()
            loc['x'] = X
            loc['y'] = Y
            loc['x'] *= self.width
            loc['y'] *= self.height
            return loc