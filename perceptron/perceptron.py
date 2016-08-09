import numpy as np
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self, size, initial=None):
        self.size = size
        if not initial:
            self.weights = np.random.random(size + 1)
    def train(self, vector, pclass):
        """pclass is either +1 or -1"""
        extended = np.append(vector, [1])
        if (self.classify(vector) >= 0):
            pass
        else:
            self.weights+=extended
    def classify(self, vector):
        extended = np.append(vector, [1])
        dot = np.dot(self.weights, extended)
        if (dot >= 0):
            return 1
        else:
            return 0



class Visualizer:
    pass
