#A simple script meant to demonstrate the results of a 625_39 backpropagation trained neuralnetwork for OCR.

import NN2
import Image
import numpy as np
import sys
sys.path.append("image_processing/")
import capture as cap

def imax(xs):
   m = max(xs)
   return [i for i, j in enumerate(xs) if j == m]

def get_class_match(xs):
   classes     = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "!", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", ".", "q", "?", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
   return classes[imax(xs)[0]]

theta = np.array(NN2.load_theta('625_39_ocr_theta.txt'))

img_path = sys.argv[1]
bimg = Image.open(img_path)
tup = cap.collectCharacters2(bimg)
tup.sort(key=lambda tup: tup[0][0])
imgs = [y[1] for y in tup]
s = ""
for img in imgs:
#   print str(img)
   X = np.array(list(img.getdata()))
#   print str(X.shape)
   s = s + get_class_match(NN2.runNet(theta,[625,39],X)[0])

print s
#img = Image.open('images/times_new_roman_characters/times_s.png')
#X = np.array(list(img.getdata()))
#print get_class_match(NN2.runNet(theta,[625,39],X)[0])

