from random import random
from numpy import *
from ast import literal_eval
from math import e
from math import sqrt
from scipy import optimize

def sigmoid(x):
   return 1/(1+e**-x)

def msigmoid(x):
   v = vectorize(lambda z: 1/(1+e**-z))
   return v(x)

def sigmoidGradient(x):
   return msigmoid(x) * (1 - msigmoid(x)); 


#function [J grad] = nnCostFunction(nn_params, ...
#                                   input_layer_size, ...
#                                   hidden_layer_size, ...e
#                                   num_labels, ...
#                                   X, y, lambda)
def generate_weights(layers):
   input_layer_size = layers[0]
   output_layer_size = layers[len(layers)-1]
   hidden_layers = layers[1:len(layers)-1]
   thetas = []
   prevSize = input_layer_size
   for i in range(0,len(hidden_layers)):
      eint = sqrt(6)/sqrt(prevSize + hidden_layers[i])
      temp = []
      for j in range(0,(hidden_layers[i] * (prevSize + 1))):
         temp.append(random.random() * 2 * eint - eint)
      thetas.append(array(temp))
      thetas[i].resize(hidden_layers[i],(prevSize + 1))
      prevSize = hidden_layers[i]
   eint = sqrt(6)/sqrt(prevSize + output_layer_size)
   temp = []
   for j in range(0,output_layer_size * (prevSize + 1)):
      temp.append(random.random() * 2 * eint - eint)
   thetas.append(array(temp))
   thetas[len(thetas)-1].resize(output_layer_size,(prevSize + 1))
   return thetas

   #print str(thetas)
   #random epilson Theta numbers working properly

def runNet(nn_params, hidden_layers, X, y, reg):
   m = X.shape[0]
   if m != y.shape[0]:
      print "Must have the same number of training inputs as outputs"
      return 0
   input_layer_size = X.shape[1]
   output_layer_size = y.shape[1]

   #re-roll nn_params into individuals thetas
   thetas = []
   ii = 0
   prevSize = input_layer_size
   for i in range(0,len(hidden_layers)):
      thetas.append(nn_params[ii:ii + hidden_layers[i] * (prevSize + 1)])
      thetas[i].resize(hidden_layers[i],(prevSize + 1))
      ii = hidden_layers[i] * (prevSize + 1)
      prevSize = hidden_layers[i]
   thetas.append(nn_params[ii:ii + output_layer_size * (prevSize + 1)])
   thetas[len(thetas)-1].resize(output_layer_size,(prevSize + 1))



   #Set return values
   J = 0
   theta_grads = []
   for i in range(0,len(thetas)):
      theta_grads.append(zeros(thetas[i].shape))

   #Feed forward
   nX = append(ones((m,1)),X,axis=1)
   hidden_zs = []
   hidden_as = []

   prevNodes = nX
   for i in range(0,len(thetas)):
      hidden_zs.append(dot(prevNodes,thetas[i].transpose()))
      n = prevNodes.shape[0]
      hidden_as.append(msigmoid(hidden_zs[i]))
      if (i != len(thetas)-1):
         hidden_as[i] = append(ones((n,1)),hidden_as[i],axis=1)
      prevNodes = hidden_as[i]
   
   ol = hidden_as[len(hidden_as)-1]   

def nnCostFunction(nn_params, hidden_layers, X, y, reg):
   m = X.shape[0]
   if m != y.shape[0]:
      print "Must have the same number of training inputs as outputs"
      return 0
   input_layer_size = X.shape[1]
   output_layer_size = y.shape[1]

   #re-roll nn_params into individuals thetas
   thetas = []
   ii = 0
   prevSize = input_layer_size
   for i in range(0,len(hidden_layers)):
      thetas.append(nn_params[ii:ii + hidden_layers[i] * (prevSize + 1)])
      thetas[i].resize((prevSize + 1), hidden_layers[i])
      thetas[i] = thetas[i].transpose()
      ii = hidden_layers[i] * (prevSize + 1)
      prevSize = hidden_layers[i]
   thetas.append(nn_params[ii:ii + output_layer_size * (prevSize + 1)])
   thetas[len(thetas)-1].resize(output_layer_size,(prevSize + 1))
   thetas[len(thetas)-1].resize((prevSize + 1), output_layer_size)
   thetas[len(thetas)-1] = thetas[len(thetas)-1].transpose()



   #Set return values
   J = 0
   theta_grads = []
   for i in range(0,len(thetas)):
      theta_grads.append(zeros(thetas[i].shape))

   #Feed forward
   nX = append(ones((m,1)),X,axis=1)
   hidden_zs = []
   hidden_as = []

   prevNodes = nX
   for i in range(0,len(thetas)):
      hidden_zs.append(dot(prevNodes,thetas[i].transpose()))
      n = prevNodes.shape[0]
      hidden_as.append(msigmoid(hidden_zs[i]))
      if (i != len(thetas)-1):
         hidden_as[i] = append(ones((n,1)),hidden_as[i],axis=1)
      prevNodes = hidden_as[i]
   
   ol = hidden_as[len(hidden_as)-1]   
   J = (1.0/m) * sum(-y * log(ol) - (1 - y) * log(1 - ol))

   print "Theta1: \n"+str(thetas[0])
   print "Thetas2: \n"+str(thetas[1])

   print "Output Layer: "+str(ol)
   print "Unregularized J: "+str(J)

   #drop below to unregularize
   s = 0
   for t in thetas:
      s = s + sum(t[:,1:] * t[:,1:])
   J = J + ((reg*1.0)/(2*m)) * s
   print "Regularized J: "+str(J)

   #print str(J)
   #cost function J working properly

   #Backpropagation
   deltas = []
   deltas_big = []
   deltas.append(ol - y) #deltas for output layer
   for i in range(len(thetas)-1,0,-1): 
      deltas.insert(0,dot(deltas[0], thetas[i][:,1:]))
      deltas[0] = deltas[0] * sigmoidGradient(hidden_zs[i-1])

   deltas_big.append(dot(deltas[0].transpose(),nX))
   for i in range(1,len(thetas)):
      deltas_big.append(dot(deltas[i].transpose(), hidden_as[i-1]))

   for i in range(0,len(theta_grads)): 
      #theta_grads[i] = (1.0/m) * deltas_big[i] == unregularized
      theta_grads[i] = (1.0/m) * deltas_big[i] + ((reg*1.0)/m) * thetas[i]
      theta_grads[i][:,0] = theta_grads[i][:,0] - ((reg*1.0)/m) * thetas[i][:,0]

   return (J, theta_grads)

#   print str(theta_grads)

"""
%Backpropagation
delta_3 = ol - y;
delta_2 = delta_3 * Theta2(:,2:end);
delta_2 = delta_2 .* sigmoidGradient(phl);

big_delta_2 = delta_3' * hl;
big_delta_1 = delta_2' * nX;

Theta1_grad = (1/m) * big_delta_1 + (lambda/m) * Theta1;
Theta2_grad = (1/m) * big_delta_2 + (lambda/m) * Theta2;

Theta1_grad(:,1) = Theta1_grad(:,1) - (lambda/m)*Theta1(:,1);
Theta2_grad(:,1) = Theta2_grad(:,1) - (lambda/m)*Theta2(:,1);


%Feedforward
nX = [ones(m,1),X];
phl = nX * Theta1'; %should be size(25,5000)
hl = [ones(m,1),sigmoid(phl)]; %should be size (5000, 26)
ol = hl * Theta2'; %should be size(10,5000)
ol = sigmoid(ol);
y = eye(num_labels)(y,:); %turn each y (0-9) into a vector of 0's and 1's
J = (1/m) * sum(sum(-y .* log(ol) - (1 - y) .* log(1 - ol)));
%Regularization
J = J + (lambda/(2*m)) * (sum(sum(Theta1(:,2:end) .* Theta1(:,2:end))) + sum(sum(Theta2(:,2:end) .* Theta2(:,2:end))));
"""
def unroll(xs):
   acc = xs[0].ravel()
   for i in range(1,len(xs)):
      acc = append(acc, xs[i].ravel())
   return acc

def getJ(nnparams, *args):
   layers, X, y, reg = args
   answer = nnCostFunction(nnparams, layers, X, y, reg)[0]
   print "error: "+str(answer)
   return answer

def getGrad(nnparams, *args):
   layers, X, y, reg = args
   answer = nnCostFunction(nnparams, layers, X, y, reg)[1]
   return unroll(answer)

"""
#Xor gate testing, 4 reals
l = [2,2,2,1]
t = unroll(generate_weights(l))
print "Making a [2,2,1,1] XOR gate"
X = array([[0,0],[1,0],[0,1],[1,1]])
y = array([[0], [1], [1], [0]])
#nnCostFunction(t, [2,1], X, y, 1.0)
args = ([2,2],X,y,1.0)
#getJ(t, tup)
res1 = optimize.fmin_cg(getJ, t, fprime=getGrad, args=args, maxiter=150)
print 'res1 = ', res1
runNet(res1, [2,2], X, y, 1.0)
"""
