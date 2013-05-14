import Image

im = Image.open("../images/arial_characters.png")
#im = Image.open("images/Penguin03black.gif")

x = im.size[0]
y = im.size[1]

def displayImage(img):
   s = ''
   for i in range(0,y):
      s = s + '\n'
      for j in range(0,x):
         z = im.getpixel((j,i))
         if z > 0:
            s = s + '#'
         else:
            s = s + ' '
   return s

def isEmptyPixel((x,y), img, emptyval = 0):
   return img.getpixel((x,y)) == emptyval

def getNeighbors((x,y), img):
   neighbors = []
   if (x > 0):
      neighbors.append((x-1,y))
   if (x < img.size[0]-1):
      neighbors.append((x+1,y))
   if (y > 0):
      neighbors.append((x,y-1))
   if (y < img.size[1]-1):
      neighbors.append((x,y+1))
   if (x > 0 and y > 0):
      neighbors.append((x-1,y-1))
   if (x > 0 and y < img.size[1]-1):
      neighbors.append((x-1,y+1))
   if (x < img.size[0]-1 and y > 0):
      neighbors.append((x+1,y-1))
   if (x < img.size[0]-1 and y < img.size[1]-1):
      neighbors.append((x+1,y+1))
      
def getActiveNeighbors(xy, img):
   return filter(lambda (x,y): not isEmptyPixel((x,y), img), getNeighbors(xy, img))

def getCluster(xy, img):
   cluster = []
   if (not isEmptyPixel(xy, img)):
      cluster.append(xy)
      cluster += getActiveNeighbors(cluster[0], img)
      i = 1
      while (i < len(cluster)):
         cluster += getActiveNeighbors(cluster[i], img)
         i += 1
   return cluster

def eraseCluster(cluster, img):
   for p in cluster:
      img.putpixel(p, 0)


#class Character:
   
#   def __init__(self, init):
      #init.

