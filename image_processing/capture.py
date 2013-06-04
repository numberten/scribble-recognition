import Image
from os import listdir



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

def firstCluster(img):
   x = img.size[0]
   y = img.size[1]
   myx = 0
   myy = 0
   i = 0
   while (myx != x and myy != y):
      point = (myx, myy)
      cluster = getCluster(point, img)
      if len(cluster) > 0:
         return cluster
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

def expandPos(x_expand, y_expand, pos):
   posx = pos[0]
   posy = pos[1]
   return (posx + x_expand, posy + y_expand)

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
         print displayImage(im)
         mnm = maxAndmins(cluster)
         print str(mnm)
         newImage = img.crop(mnm)
         print "new size: "+ str(newImage.size[0])
         print "new size2: "+ str(newImage.size[1])
         newImage.load()
         print "Displaying Image"
         print displayImage(newImage)
         print "Name of character:"
         name = raw_input()
         while name == 'grab':
            (t1, t2, t3, t4) = mnm
            print "How far on x-axis from left hand side?"
            dx = input()
            print "How far on y-axis from bottom?"
            dy = input()
            newpoint = expandPos(dx,dy,(t1,t4))
            newCluster = getCluster(newpoint, img)
            print "Cluster length: "+  str(len(newCluster))
            cluster += newCluster
            mnm = maxAndmins(cluster)
            newImage = img.crop(mnm)
            print "new size: "+ str(newImage.size[0])
            print "new size2: "+ str(newImage.size[1])
            newImage.load()
            print "Displaying Image Check"
            print displayImage(newImage)
            print "Name of character:"
            name = raw_input()
         name += '.png'
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

def mypaste(fileName, (nx,ny)):
   resize(fileName, (nx,ny))
   img_old = Image.open(fileName)
   cluster = firstCluster(img_old)
   (minx, miny, maxx, maxy) = maxAndmins(cluster) 
   lx = maxx - minx
   ly = maxy - miny
   dx = (nx-lx)/2
   print 'dx: '+str(dx)
   dy = (ny-ly)/2
   print 'dy: '+str(dy)
   cluster = map(lambda (x,y): (x+dx,y+dy), cluster)
   new = Image.new(img_old.mode, (nx,ny), 255)
   for c in cluster:
      new.putpixel(c, 10)
   new.save(fileName)
   


def mypaste2(imgName, (nx,ny)):
   img_old = resize2(imgName, (nx,ny))
   cluster = firstCluster(img_old)
   (minx, miny, maxx, maxy) = maxAndmins(cluster) 
   lx = maxx - minx
   ly = maxy - miny
   dx = (nx-lx)/2
   dy = (ny-ly)/2
   cluster = map(lambda (x,y): (x+dx,y+dy), cluster)
   new = Image.new(img_old.mode, (nx,ny), 255)
   for c in cluster:
      new.putpixel(c, 10)
   return new



def collectCharacters2(img):
   imgs = []
   x = img.size[0]
   y = img.size[1]
   myx = 0
   myy = 0
   i = 0
   points = []
   while (myx != x and myy != y):
      point = (myx, myy)
      cluster = getCluster(point, img)
      if len(cluster) > 0:
         points.append(point)
         mnm = maxAndmins(cluster)
         newImage = img.crop(mnm)
         newImage.load()

         newImage = mypaste2(newImage, (100,100))
         newImage = resize2(newImage, (25,25))
         #resize
         
        # print displayImage(newImage)
         print "Appending cluster.."
         imgs.append(newImage)
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
   return zip(points,imgs)
  
def resize(fileName, (nx,ny)):
   img = Image.open(fileName)
   (ix,iy) = img.size
   while (ix*2 <= nx and iy*2 <= ny):
      img = img.resize((ix*2,iy*2), Image.ANTIALIAS)
      #(ix,iy) = img.size
      ix = ix*2
      iy = iy*2
      print str((ix,iy))
   while (ix/2 >= nx and iy/2 >= ny):
      img = img.resize((ix/2,iy/2), Image.ANTIALIAS)
      (ix,iy) = img.size
   img.save(fileName)
   
   #img.thumbnail(newSize, Image.ANTIALIAS)
   #img.save(fileName)

def resize2(imgName, (nx,ny)):
   img = imgName
   (ix,iy) = img.size
   while (ix*2 <= nx and iy*2 <= ny):
      img = img.resize((ix*2,iy*2), Image.ANTIALIAS)
      #(ix,iy) = img.size
      ix = ix*2
      iy = iy*2
   while (ix/2 >= nx and iy/2 >= ny):
      img = img.resize((ix/2,iy/2), Image.ANTIALIAS)
      (ix,iy) = img.size
   return img


#collectCharacters(im)

#im = Image.open("arial_0.png")
"""
paths = ['../images/arial_characters/','../images/comic_sans_characters/','../images/times_new_roman_characters/','../images/verdana_characters/','../images/courier_characters/']
for path in paths:
   files = listdir(path)
#print str(files)
   for i in files:
      resize(path+i, (20,20))
#   mypaste(path+i, (100,100))
print 'All done!' 
"""

#resize('arial_a.png', (20,20))

#collectCharacters(im)

#resize("../images/arial_characters/arial_0.png", (100,100))

#path = '../images/arial_characters/'
#resize(path+'0.png', (100,100))
#img = Image.open('test2.png')
#img = Image.open('test2.png')
#mypaste(img, (100,100))
#print 'done!'
#print str(img.mode)
#a = Image.new(img.mode, (100,100), 255)
#a.save('test3.png')
#a = Image.open('test3.png')
#a.paste(img, (0,0))
#a.save('test3.png')
#a.save('test3.png')
#xs = listdir(path)
#for i in xs:
#   im = Image.open(path+i)
#   print i+': '+str(im.size)
   

