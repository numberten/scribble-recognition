from random import random
from math import e

def sigmoid(x):
   return 1/(1+e^-x)

class NeuralNet:
   def __init__(self, number_of_neurons_per_layer):
      self.neurons = []
      self.weights = []
      self.biases  = []
      for i in range(0,len(number_of_neurons_per_layer)):
         self.neurons.append([])
         #initialize neurons to 0.0
         for j in range(0,number_of_neurons_per_layer[i]):
            self.neurons[i].append(0.0)
         #initialize weights for non-output layers
         self.weights.append([])
         if i+1 != len(number_of_neurons_per_layer):
            for j in range(0,number_of_neurons_per_layer[i]*number_of_neurons_per_layer[i+1]):
               self.weights[i].append(random())
         #initialize biases for non-input layers
         self.biases.append([])
         if i != 0:
            for j in range(0,number_of_neurons_per_layer[i]):
               self.biases[i].append(random())
      #zip neurons and weights into net
      self.net = zip(self.neurons, self.weights)
            
   def print_net(self):
      for i in range(0,len(self.neurons)):
         print "Layer "+ str(i) + ": " + str(self.neurons[i])
      for i in range(0,len(self.weights)):
         print "Layer "+ str(i) + ": " + str(self.weights[i])
      for i in range(0,len(self.biases)):
         print "Layer "+ str(i) + ": " + str(self.biases[i])

   def run(self, inputs):
      self.set_input_neurons(inputs)
      #self.print_net()
      for i in range(0,len(self.neurons)-1): 
         self.feed_forward(i)
      print "Finished running the neuralnetwork."

   def set_input_neurons(self, inputs):
      if len(self.neurons[0]) != len(inputs):
         raise Exception("wrong number of inputs")
      for i in range(0,len(inputs)):
         self.neurons[0][i] = inputs[i]        

   def feed_forward(self, layer_index):
      #n is each neuron in the next layer
      weights_counter = 0
      for n in range(0,len(self.neurons[layer_index+1])):
         print "n was: "+ str(self.neurons[layer_index+1][n])
         new_value = 0
         #o is the output of every node in the current layer
         for o in self.neurons[layer_index]:
            new_value += o * self.weights[layer_index][weights_counter]
            weights_counter += 1
         self.neurons[layer_index+1][n] = new_value
         print "now n is: " + str(self.neurons[layer_index+1][n])
      print "layer " + str(layer_index) + " finished."
            
            
         






















