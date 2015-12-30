import numpy as np
import math
import heapq

from utils.MaxHeap import MaxHeap
from Learner import Learner

"""
K nearest neighbors learning algorithm.
"""
class KNNLearner(Learner):

    def __init__(self, k=3):
        self.k = k
        self.x = None
        self.y = None


    def train(self, datax, datay):
        self.x = datax
        self.y = datay


    def query(self, points):
        values = []
        for point in points:
            values.append(self.get_y(point))
        return np.array(values)


    def get_y(self, point):
        """
        Use KNN algorithm to find the y value of the point.

        Parameters
        ----------
        point: array

        Returns
        ----------
        y: float
        """
        heap = MaxHeap(self.k)

        for i in range(len(self.x)):
            distance = Learner.euclidean_distance(self.x[i], point)
            heap.add((distance, i, self.x[i], self.y[i])) # if the first value in the tuple is equal, heapq use the second value to compare

        values = heap.heapsort()
        values = [val[3] for val in values]
        return np.array(values).sum()/len(values)