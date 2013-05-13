import Image

im = Image.open("../images/arial_characters.png")
#im = Image.open("images/Penguin03black.gif")

x = im.size[0]
y = im.size[1]

print x, y

#lots of values that aren't just 0 or 1
s = ''
for i in range(0,y):
   s = s + '\n'
   for j in range(0,x):
      z = im.getpixel((j,i))
      if z > 0:
         s = s + '#'
      else:
         s = s + ' '
      #print "("+str(j)+","+str(i)+") = " + str(im.getpixel((j,i)))
print s

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


#class Character:
   
#   def __init__(self, init):
      #init.

