from numpy import *


class NeuralNetwork(object):
    def __init__(self):
        # Assign random weights to a 5 x 8 matrix, between -1 and 1
        self.synaptic_weights = divide(random.randint(-1000, 1000, size=(5, 7)), 1000)

    # The Sigmoid function
    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))

    # Get output layer
    def learn(self, inputs):
        return self.__sigmoid(dot(inputs, self.synaptic_weights))
