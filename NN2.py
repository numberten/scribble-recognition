from random import random
from numpy import *
from ast import literal_eval
from math import e
from math import sqrt
from scipy import optimize

def sigmoid(x):
   return 1/(1+e**-x)

def msigmoid(x):
   v = vectorize(lambda z: 1/(1+e**-helper(z)))
   return v(x)

def helper(x):
   #print str(x)
   if x < -700:
      return -700
   return x

def sigmoidGradient(x):
   return msigmoid(x) * (1 - msigmoid(x));

def safe_ln(x, minval=0.0000000001):
    return log(x.clip(min=minval))

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

   #random epilson Theta numbers working properly

def runNet(nn_params, hidden_layers, X, y):
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
      thetas[i].resize(hidden_layers[i], (prevSize + 1))
      #thetas[i].resize((prevSize+1), hidden_layers[i])
      #thetas[i] = thetas[i].transpose()
      ii = hidden_layers[i] * (prevSize + 1)
      prevSize = hidden_layers[i]
   thetas.append(nn_params[ii:ii + output_layer_size * (prevSize + 1)])
   thetas[len(thetas)-1].resize(output_layer_size, (prevSize + 1))
   #thetas[len(thetas)-1].resize((prevSize + 1), output_layer_size)
   #thetas[len(thetas)-1] = thetas[len(thetas)-1].transpose()



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
   #print "Running network...\n"+str(ol)
   return ol

def nnCostFunction(nn_params, hidden_layers, X, y, reg):
   #print "NN_params:\n"+str(nn_params)
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
      thetas[i].resize(hidden_layers[i], (prevSize + 1))
      #thetas[i].resize((prevSize + 1), hidden_layers[i])
      #thetas[i] = thetas[i].transpose()
      ii = hidden_layers[i] * (prevSize + 1)
      prevSize = hidden_layers[i]
   thetas.append(nn_params[ii:ii + output_layer_size * (prevSize + 1)])
   thetas[len(thetas)-1].resize(output_layer_size,(prevSize + 1))
   #thetas[len(thetas)-1].resize((prevSize + 1), output_layer_size)
   #thetas[len(thetas)-1] = thetas[len(thetas)-1].transpose()



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
   J = (1.0/m) * sum(-y * safe_ln(ol) - (1 - y) * safe_ln(1 - ol))

   #print "Theta1: \n"+str(thetas[0])
   #print "Thetas2: \n"+str(thetas[1])

   #print "Output Layer: "+str(ol)
   #print "Unregularized J: "+str(J)



   #drop below to unregularize
   s = 0
   for t in thetas:
      s = s + sum(t[:,1:] * t[:,1:])
   J = J + ((reg*1.0)/(2*m)) * s
   #print "Regularized J: "+str(J)

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

   #print "ThetaGrads:\n"+str(unroll(theta_grads))
   return (J, theta_grads)


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

def save_theta(filename, theta):
   st = "["+str(theta[0])
   for i in theta[1:len(theta)]:
      st = st + ","+str(i)
   st = st+"]"
      
   f = open(filename, 'w')
   s = "theta\n"+st+"\n"
   f.write(s)
   f.close


def load_theta(filename):
   f = open(filename, 'r+')
   lines = f.readlines()
   theta = literal_eval(lines[1])
   return theta


"""
#Xor gate testing, 4 reals
l = [2,2,1]
t = unroll(generate_weights(l))
print "Making a [2,2,1] XOR gate"
X = array([[0,0],[1,0],[0,1],[1,1]])
y = array([[0], [1], [1], [0]])
# Xor lambda should be ~ < 0.00001
args = ([2], X, y, 0.00001)

res1 = optimize.fmin_cg(getJ, t, fprime=getGrad, args=args, maxiter=500)#, gtol=0.0000000005)
#print 'res1 = ', res1
print "Output: \n"+str(runNet(res1, [2], X, y))
"""
