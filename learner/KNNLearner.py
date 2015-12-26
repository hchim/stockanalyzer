import numpy as np
import math

from utils.MaxHeap import MaxHeap
from learner.Learner import Learner

"""
K nearest neighbors learning algorithm.
"""
class KNNLearner(Learner):

    def __init__(self, k=3):
        self.k = k
        self.x = None
        self.y = None


    def train(self, datax, datay):
        if not self.x:
            self.x = datax
        else:
            self.x = np.vstack(self.x, datax)

        if not self.y:
            self.y = datay
        else:
            self.y = np.vstack(self.y, datay)


    def query(self, points):
        values = []
        for point in points:
            values.append(self.get_y(point))
        return np.array(values)


    def get_y(self, x):
        """
        Use KNN algorithm to find the y value of the point.

        Parameters
        ----------
        point: array
        :return:
        """
        heap = MaxHeap(self.k)

        for i in range(len(self.x)):
            distance = Learner.euclidean_distance(self.x[i], x)
            heap.add((distance, self.x[i], self.y[i]))

        values = heap.heapsort()
        values = [val[2] for val in values]
        return np.array(values).sum()/len(values)