from numpy import *


class NeuralNetwork(object):
    def __init__(self):
        # Assign random weights to a 5 x 8 matrix,
        self.synaptic_weights = divide(random.randint(-1000, 1000, size=(5, 8)), 1000)

    # The Sigmoid function
    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))

    def learn(self, inputs):
        return self.__sigmoid(dot(inputs, self.synaptic_weights))
