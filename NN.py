from random import random
from math import e

def sigmoid(x):
   return 1/(1+e**-x)

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
         print "Neurons Layer "+ str(i) + ": " + str(self.neurons[i])
      for i in range(0,len(self.weights)):
         print "Weights Layer "+ str(i) + ": " + str(self.weights[i])
      for i in range(0,len(self.biases)):
         print "Biases Layer "+ str(i) + ": " + str(self.biases[i])

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
#         print "n was: "+ str(self.neurons[layer_index+1][n])
         new_value = 0
         #o is the output of every node in the current layer
         for o in self.neurons[layer_index]:
            new_value += o * self.weights[layer_index][weights_counter]
            weights_counter += 1
         new_value += self.biases[layer_index+1][n]
         self.neurons[layer_index+1][n] = sigmoid(new_value)
 #        print "now n is: " + str(self.neurons[layer_index+1][n])
#      print "layer " + str(layer_index) + " finished."


   def train(self, inputs, outputs, alpha, iterations, error):
      if len(inputs) != len(self.neurons[0]):
         print "This neuron requires "+ str(len(self.neurons[0])) + " inputs."
         return

      if len(outputs) != len(self.neurons[len(self.neurons)-1]):
         print "This neuron requires "+ str(len(self.neurons[len(self.neurons)-1])) + " outputs."
         return
      #Step 1: Run the neural network
      self.run(inputs)
      #Step 2: Calculate delta-k for every output node k
      delta_ks = []
      for k in range(0,len(self.neurons[len(self.neurons)-1])):
         ko = self.neurons[len(self.neurons)-1][k]
         delta_ks.append(ko * (1 - ko) * (ko - outputs[k]))
      #Step 3: Calculate delta-j for every hidden node j
      delta_js = []
      for i in range(1,len(self.neurons)-1):
         delta_js.append([])
         #delta-j for last hidden layer
      delta_js.append(delta_ks)
      for i in range(len(delta_js)-2,-1,-1): #i starts from highest index and goes to 0
         weight_counter = 0
         for j in range(0,len(self.neurons[1+i])):
            jo = self.neurons[1+i][j]
            summation = 0
            for k in range(0,len(self.neurons[2+i])):
               weightjk        = self.weights[i+1][weight_counter]
               weight_counter += 1
               summation      += delta_js[i+1][k] * weightjk
            print "i: "+ str(i)
            print "j: "+ str(j)
            print "length of delta_js: " + str(len(delta_js))
            delta_js[i].append(jo * (1 - jo) * summation) 
      #Step 4: Update the weights and biases
      for i in range(0,len(self.weights)):
         nshift         = 0
         weight_counter = 0
         output_counter = 0
         while (weight_counter < len(self.weights[i])):
            for j in range(0,len(delta_js[i])):
               delta_w = -1 * alpha * delta_js[i][j] * self.neurons[i][nshift]
               self.weights[i][weight_counter] += delta_w
               weight_counter += 1
            nshift += 1
      for i in range(1,len(self.neurons)):
         for b in range(0,len(self.biases[i])):
            delta_b = -1 * alpha * delta_js[i-1][b]
            self.biases[i][b] += delta_b
      #Step 5: Profit
      print "finished training neural net"

            
            
print "Making a 2,3,1 neural net." 
a = NeuralNet([2,3,1])
print "Training the net......"
a.train([1,1],[2], 0,0,0)




















