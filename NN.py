from random import random
from ast import literal_eval
from math import e

def sigmoid(x):
   return 1/(1+e**-x)

class NeuralNet:
   def __init__(self, number_of_neurons_per_layer):
      self.global_i = 0
      self.f = open('error_data.csv', 'w')
      self.current_error = 0
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
               self.weights[i].append((random()*2)-1)
         #initialize biases for non-input layers
         self.biases.append([])
         if i != 0:
            for j in range(0,number_of_neurons_per_layer[i]):
               self.biases[i].append((random()*2)-1)

   def printo(self):
      for i in self.neurons[len(self.neurons)-1]:
         print "Output -> " + str(i)
            
   def print_net(self):
      for i in range(0,len(self.neurons)):
         print "Neurons Layer "+ str(i) + ": " + str(self.neurons[i])
      for i in range(0,len(self.weights)):
         print "Weights Layer "+ str(i) + ": " + str(self.weights[i])
      for i in range(0,len(self.biases)):
         print "Biases Layer "+ str(i) + ": " + str(self.biases[i])

   def run(self, inputs):
      self.set_input_neurons(inputs)
      for i in range(0,len(self.neurons)-1): 
         self.feed_forward(i)
      #print "Finished running the neuralnetwork."

   def set_input_neurons(self, inputs):
      if len(self.neurons[0]) != len(inputs):
         raise Exception("wrong number of inputs")
      for i in range(0,len(inputs)):
         self.neurons[0][i] = inputs[i]        

   def feed_forward(self, layer_index):
      weights_counter = 0
      for n in range(0,len(self.neurons[layer_index+1])):
         new_value = 0
         for o in self.neurons[layer_index]:
            new_value += o * self.weights[layer_index][weights_counter]
            weights_counter += 1
         new_value += self.biases[layer_index+1][n]
         self.neurons[layer_index+1][n] = sigmoid(new_value)

   def train(self, inputs, outputs, alpha, iterations, error):
      if len(inputs) != len(outputs):
         print "Must have the same number of inputs and outputs."
         return
      for i in inputs:
         if len(i) != len(self.neurons[0]):
            print "This network requires " + str(len(self.neurons[0])) + " inputs."
            return
      for o in outputs:
         if len(o) != len(self.neurons[len(self.neurons)-1]):
            print "This network requires " + str(len(self.neurons[len(self.neurons)-1])) + " outputs."
            return
      current_iteration    = 0
      self.current_error   = error + 1
      while True:
         if current_iteration >= iterations:
            print "finished training neural net"
            print "error: "+ str(self.current_error)
            print "max iteration reached."
            return
         if self.current_error <= error:
            print "finished training neural net"
            print "error: "+ str(self.current_error)
            print "current error less than target error."
            print "iterations: "+ str(current_iteration)
            return
         for q in range(0,len(inputs)):
            #Step 1: Run the neural network
            self.run(inputs[q])
            #self.print_net()
            #Step 2: Calculate delta-k for every output node k
            delta_ks = []
            for k in range(0,len(self.neurons[len(self.neurons)-1])):
               ko = self.neurons[len(self.neurons)-1][k]
               delta_ks.append(ko * (1 - ko) * (ko - outputs[q][k]))
            #Step 3: Calculate delta-j for every hidden node j
            delta_js = []
            for i in range(1,len(self.neurons)-1):
               delta_js.append([])
            delta_js.append(delta_ks)
            for i in range(len(delta_js)-2,-1,-1): 
               weight_counter = 0
               for j in range(0,len(self.neurons[1+i])):
                  jo = self.neurons[1+i][j]
                  summation = 0
                  for k in range(0,len(self.neurons[2+i])):
                     weightjk        = self.weights[i+1][weight_counter]
                     weight_counter += 1
                     summation      += delta_js[i+1][k] * weightjk
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
         self.calculate_error(inputs,outputs)
         current_iteration += 1

   def calculate_error(self, inputs, outputs):
      self.current_error = 0
      summ = 0
      for i in range(0,len(inputs)):
         self.run(inputs[i])
         for o in range(0,len(outputs[i])):
            summ += (self.neurons[len(self.neurons)-1][o] - outputs[i][o])**2
      self.current_error = 0.5 * summ
      self.f.write(str(self.current_error)+','+str(self.global_i)+'\n')
      self.global_i += 1

   def save_network(self,savefile):   
      f = open(savefile, 'w')
      s = "Neurons\n"+str(self.neurons)+"\nWeights\n"+str(self.weights)+"\nBiases\n"+str(self.biases)+"\n"
      f.write(s)

def load_network(savefile):
   network = NeuralNet([])
   f = open(savefile, 'r+')
   lines = f.readlines()
   network.neurons = literal_eval(lines[1])
   network.weights = literal_eval(lines[3])
   network.biases  = literal_eval(lines[5])
   f.close
   return network

"""
print "Creating a [2,2,3,1] neural network."
print "Training network with XOR gate examples."
print "alpha = 0.03, max iterations = 150000, error = 0.08"
a = NeuralNet([2,2,3,1])
a.train([[1,1],[0,0],[1,0],[0,1]], [[0],[0],[1],[1]], 0.03, 150000, 0.08)

print "[1,1]"
a.run([1,1])
a.printo()
print "[0,0]"
a.run([0,0])
a.printo()
print "[1,0]"
a.run([1,0])
a.printo()
print "[0,1]"
a.run([0,1])
a.printo()
"""





