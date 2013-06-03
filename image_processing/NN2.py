from random import random
from numpy import *
from ast import literal_eval
from math import e
from math import sqrt

def sigmoid(x):
   return 1/(1+e**-x)

#function [J grad] = nnCostFunction(nn_params, ...
#                                   input_layer_size, ...
#                                   hidden_layer_size, ...e
#                                   num_labels, ...
#                                   X, y, lambda)

def nnCostFunction(hidden_layers, X, y, reg, epilson):
#Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
 #                hidden_layer_size, (input_layer_size + 1));
   m = X.shape[0]
   if m != y.shape[0]:
      print "Must have the same number of training inputs as outputs"
      return 0
   input_layer_size = X.shape[1]
   output_layer_size = y.shape[1]
   thetas = []
   prevSize = input_layer_size
   for i in range(0,len(hidden_layers)):
      eint = sqrt(6)/sqrt(prevSize + hidden_layers[i])
      print "Eint: "+str(eint)
      temp = []
      for j in range(0,(hidden_layers[i] * (prevSize + 1))):
         temp.append(random.random() * 2 * eint - eint)
      thetas.append(array(temp))
      thetas[i].resize(hidden_layers[i],(prevSize + 1))
      prevSize = hidden_layers[i]
   eint = sqrt(6)/sqrt(prevSize + output_layer_size)
   print "Eint: "+str(eint)
   temp = []
   for j in range(0,output_layer_size * (prevSize + 1)):
      temp.append(random.random() * 2 * eint - eint)
   thetas.append(array(temp))
   thetas[len(thetas)-1].resize(output_layer_size,(prevSize + 1))

   print str(thetas)
   #Theta numbers working properly

#Xor gate testing, 4 reals
print "Making a [2,1] XOR gate"
X = array([[0,0],[1,0],[0,1],[1,1]])
y = array([[0], [1], [1], [0]])
nnCostFunction([2,1], X, y, 0, 0)
