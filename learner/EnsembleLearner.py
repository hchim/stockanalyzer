import numpy as np
import math

from Learner import Learner
from LRLearner import LRLearner
from KNNLearner import KNNLearner

"""
EnsembleLearner learner. It use
"""
class EnsembleLearner(Learner):

    def __init__(self, learners):
        """
        Create an ensemble learner.

        Parameters
        ----------
        learners: map
            Learner names and arguments to create the learner. For example:
            {
                "LR":None,
                "KNN": {"k": 5}
            }
        """
        instances = []
        for name in learners.keys():
            learner = EnsembleLearner.create_learner(name, learners[name])
            if learner:
                instances.append(learner)

        self.learners = instances

    def train(self, datax, datay):
        for learner in self.learners:
            learner.train(datax, datay)


    def query(self, points):
        predict = None
        for learner in self.learners:
            temp = learner.query(points)
            if predict is None:
                predict = temp
            else:
                predict = predict + temp

        return predict/len(self.learners)

    @staticmethod
    def create_learner(name, args=None):
        """
        Create an instance of the learner .

        Parameters
        ----------
        name: string
            the name of the learner, could be "LR", "KNN"
        args: map
            the arguments of the learner

        Returns
        ---------
        learner: subclass of Learner or None
        """
        if name == "LR":
            return LRLearner()
        elif name == "KNN":
            return KNNLearner(args['k'])

        return None