from joblib.numpy_pickle_utils import xrange
from numpy import *


class NeuralNetwork(object):
    def __init__(self):
        # Generate random numbers
        # random.seed(1) 

        # Assign random weights to a 5 x 8 matrix,
        self.synaptic_weights = divide(random.randint(-1000, 1000, size=(5, 8)), 1000)

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


neural_network = NeuralNetwork()
# print(neural_network.synaptic_weights)

# The training set.
inputs = array([1, 3, 2, 0, 0])
# outputs = array([[1, 0, 1]]).T

# Train the neural network
# neural_network.train(inputs, outputs, 100000)

# Test the neural network with a test example.
print(neural_network.learn(inputs))
