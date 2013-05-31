import preprocess
from os import listdir
import sys
sys.path.append("..")
import NN

net         = NeuralNet([100,39])
receptors   = read_receptors('best100.txt')

arial       = listdir('../images/arial_characters')
arial       = arial.sort()
arial       = map(lambda x: '../images/arial_characters'+x,arial)
comic       = listdir('../images/comic_sans_characters')
comic       = comic.sort()
comic       = map(lambda x: '../images/comic_sans_characters'+x,comic)
courier     = listdir('../images/courier_characters')
courier     = courier.sort()
courier     = map(lambda x: '../images/courier_characters'+x,courier)
times       = listdir('../images/times_new_roman_characters')
times       = times.sort()
times       = map(lambda x: '../images/times_new_roman_characters'+x,times)
verdana     = listdir('../images/verdana_characters')
verdana     = verdana.sort()
verdana     = map(lambda x: '../images/verdana_characters'+x,verdana)

images      = []

classes     = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "!", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", ".", "q", "?", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
inputs   = []
outputs  = []

