import Image

im = Image.open("../images/arial_characters.png")
#im = Image.open("images/Penguin03black.gif")


def displayImage(img):
   x = img.size[0]
   y = img.size[1]
   s = ''
   for i in range(0,y):
      s = s + '\n'
      for j in range(0,x):
         z = img.getpixel((j,i))
         if z > 0:
            s = s + '#'
         else:
            s = s + ' '
   return s

def isEmptyPixel((x,y), img, emptyval = 0):
   return img.getpixel((x,y)) == emptyval

def getNeighbors((x,y), cluster, img):
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
   neighbors = [item for item in neighbors if item not in cluster]
   return neighbors
      
def getActiveNeighbors(xy, cluster, img):
   return filter(lambda (x,y): not isEmptyPixel((x,y), img), getNeighbors(xy, cluster, img))

def getCluster(xy, img):
   cluster = []
   if (not isEmptyPixel(xy, img)):
      cluster.append(xy)
      cluster += getActiveNeighbors(cluster[0], cluster, img)
      i = 1
      while (i < len(cluster)):
         cluster += getActiveNeighbors(cluster[i], cluster, img)
         i += 1
   return cluster

def eraseCluster(cluster, img):
   for p in cluster:
      img.putpixel(p, 0)

def maxAndmins(cluster):
   max_x = cluster[0][0]
   min_x = cluster[0][0]
   max_y = cluster[0][1]
   min_y = cluster[0][1]
   for i in range(1,len(cluster)):
      if cluster[i][0] > max_x:
         max_x = cluster[i][0]
      if cluster[i][0] < min_x:
         min_x = cluster[i][0]
      if cluster[i][1] > max_y:
         max_y = cluster[i][1]
      if cluster[i][1] < min_y:
         min_y = cluster[i][1]
   return (min_x, min_y, max_x+1, max_y+1)

def collectCharacters(img):
   x = img.size[0]
   y = img.size[1]
   myx = 0
   myy = 0
   i = 0
   while (myx != x and myy != y):
      point = (myx, myy)
      cluster = getCluster(point, img)
      if len(cluster) > 0:
         mnm = maxAndmins(cluster)
         print str(mnm)
         newImage = img.crop(mnm)
         print "new size: "+ str(newImage.size[0])
         print "new size2: "+ str(newImage.size[1])
         newImage.load()
         print "Displaying Image"
         print displayImage(newImage)
         print "Name of character:"
         name = raw_input() + '.png'
            
         newImage.save(name)
         eraseCluster(cluster, img)
      if (myx < x-1):
         i += 1
         myx += 1
      elif (myy < y-1):
         i += 1
         myx = 0
         myy += 1
      else:
         if (myx == x-1 and myy == y-1):
            i += 1
            myx += 1
            myy += 1

print displayImage(im)

collectCharacters(im)
#class Character:
   
#   def __init__(self, init):
      #init.

