from joblib.numpy_pickle_utils import xrange
from numpy import *


class NeuralNetwork(object):
    def __init__(self):
        # Generate random numbers
        # random.seed(1) 
  
        # Assign random weights to a 5 x 8 matrix,
        self.synaptic_weights = divide(random.randint(1, 1000, size=(5, 8)), 1000)
  
    # The Sigmoid function
    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))

    # The derivative of the Sigmoid function.
    # This is the gradient of the Sigmoid curve.
    def __sigmoid_derivative(self, x):
        return x * (1 - x)

    # Train the neural network and adjust the weights each time.
    def train(self, inputs, outputs, training_iterations):
        for iteration in xrange(training_iterations):
            # Pass the training set through the network.
            output = self.learn(inputs)
  
            # Calculate the error
            error = outputs - output
  
            # Adjust the weights by a factor
            factor = dot(inputs.T, error * self.__sigmoid_derivative(output))
            self.synaptic_weights += factor
  
        # The neural network thinks.
  
    def learn(self, inputs):
        return self.__sigmoid(dot(inputs, self.synaptic_weights))
