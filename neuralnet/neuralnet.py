# This file contains the neural network class that will be used to create the genome's phenotype.
import torch
import torch.nn as nn
import torch.nn.functional as F


class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_layers, output_size):
        super(NeuralNetwork, self).__init__()
        assert input_size == 8, "The first layer of the neural network must accept an input size of 8."
        # Initialize the neural network layers based on the input size
        self.layers = nn.ModuleList()
        previous_size = input_size
        for layer_size in hidden_layers:
            self.layers.append(nn.Linear(previous_size, layer_size))
            previous_size = layer_size
        self.layers.append(nn.Linear(previous_size, output_size))

    def forward(self, x):
        # Forward pass through the network layers
        for layer in self.layers[:-1]:
            x = F.relu(layer(x))
        # The last layer should use a softmax to ensure the output is a probability distribution
        x = self.layers[-1](x)
        return F.softmax(x, dim=-1)


# Adjust the genome to represent the correct input size, hidden layers, and output size.
# For example, if the sensor input has 8 features and the output requires 4 actions:
# input_size = 8
# hidden_layers = [16, 8]  # Two hidden layers with 16 and 8 neurons respectively
# output_size = 4
# neural_net = NeuralNetwork(input_size, hidden_layers, output_size)
