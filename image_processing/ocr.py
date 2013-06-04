import preprocess as pp
import Image
from os import listdir
import NN2
from numpy import * 
from scipy import optimize
from ast import literal_eval


classes     = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "!", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", ".", "q", "?", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

def get_nn_io():
   receptors   = pp.read_receptors('Abest100.txt')

   arial       = listdir('../images/arial_characters')
   arial.sort()
   arial       = map(lambda x: '../images/arial_characters/'+x,arial)
   """
   comic       = listdir('../images/comic_sans_characters')
   comic.sort()
   comic       = map(lambda x: '../images/comic_sans_characters/'+x,comic)
   courier     = listdir('../images/courier_characters')
   courier.sort()
   courier     = map(lambda x: '../images/courier_characters/'+x,courier)
   times       = listdir('../images/times_new_roman_characters')
   times.sort()
   times       = map(lambda x: '../images/times_new_roman_characters/'+x,times)
   verdana     = listdir('../images/verdana_characters')
   verdana.sort()
   verdana     = map(lambda x: '../images/verdana_characters/'+x,verdana)
   """

   images      = []

   inputs   = []
   outputs  = []

   #generate inputs|outputs
   for i in range(0,len(classes)):
      o = ([0] * i) + [1] + ([0] * (len(classes)-1-i))

      img = Image.open(arial[i])
      inputs.append([])
      outputs.append(o)
      for r in receptors:
         inputs[len(inputs)-1].append(pp.activate_receptor(img, r))
         inputs[len(inputs)-1] = map(lambda x: 0.5 if x == True else -0.5, inputs[len(inputs)-1])
      """
      img = Image.open(comic[i])
      inputs.append([])
      outputs.append(o)
      for r in receptors:
         inputs[len(inputs)-1].append(pp.activate_receptor(img, r))
         inputs[len(inputs)-1] = map(lambda x: 0.5 if x == True else -0.5, inputs[len(inputs)-1])

      img = Image.open(courier[i])
      inputs.append([])
      outputs.append(o)
      for r in receptors:
         inputs[len(inputs)-1].append(pp.activate_receptor(img, r))
         inputs[len(inputs)-1] = map(lambda x: 0.5 if x == True else -0.5, inputs[len(inputs)-1])

      img = Image.open(times[i])
      inputs.append([])
      outputs.append(o)
      for r in receptors:
         inputs[len(inputs)-1].append(pp.activate_receptor(img, r))
         inputs[len(inputs)-1] = map(lambda x: 0.5 if x == True else -0.5, inputs[len(inputs)-1])

      img = Image.open(verdana[i])
      inputs.append([])
      outputs.append(o)
      for r in receptors:
         inputs[len(inputs)-1].append(pp.activate_receptor(img, r))
         inputs[len(inputs)-1] = map(lambda x: 0.5 if x == True else -0.5, inputs[len(inputs)-1])
      """
   f = open('nnio.txt', 'w')
   s = "input\n"+str(inputs)+"\noutput\n"+str(outputs)+"\n"
   f.write(s)
   f.close

def read_nn_io():
   f = open('nnio.txt', 'r+')
   lines = f.readlines()
   i = literal_eval(lines[1])
   o = literal_eval(lines[3])
   f.close
   return (i,o)

def imax(xs):
   m = max(xs)
   return [i for i, j in enumerate(xs) if j == m]

def get_class_match(xs):
   return classes[imax(xs)[0]]


#net         = NN.NeuralNet([100,39])
#net.train(inputs, outputs, 0.8, 100000, 0.08)

#net.save_network('ocrNN.txt')
   
   

   #train(self, inputs, outputs, alpha, iterations, error):
   #a.train([[1,1],[0,0],[1,0],[0,1]], [[0],[0],[1],[1]], 0.03, 150000, 0.08)
   #activate_receptor(img, receptor):

data = pp.read_pixeldata()
(inputs, outputs) = read_nn_io()
inputs = array(inputs)
inputs = array(data)
outputs = array(outputs)
#OCR attempt
l = [625,39]
t = NN2.unroll(NN2.generate_weights(l))
print "Making a [625,39] OCR network"
X = inputs
y = outputs
args = ([], X, y, 0.0)
"""
print "T:"
print(type(t))
print(str(t))
print(t.shape)
print "X:"
print(type(X))
print(str(X))
print(X.shape)
print "y:"
print(type(y))
print(str(y))
print(y.shape)
"""
res1 = optimize.fmin_cg(NN2.getJ, t, fprime=NN2.getGrad, args=args, maxiter=1000)#, gtol=0.0000000005)
#print 'res1 = ', res1
out = NN2.runNet(res1, [], X, y)
s = str(get_class_match(out[0]))
for i in out[1:len(out)]:
   s = s + ", "+str(get_class_match(i))
print s
NN2.save_theta('625_39_ocr_theta.txt', res1)
print "Theta saved to 625_39_ocr_theta."






