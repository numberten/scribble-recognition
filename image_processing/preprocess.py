from random import randrange as rr
import Image
from os import listdir
from re import findall as findall


def generate_receptors(img, savefile, x):
   xrs   = []
   yrs   = []
   for i in range(0,x):
      xrs.append(new_x_receptor(img))
      yrs.append(new_y_receptor(img))
   save_receptors(xrs+yrs, savefile)

def tupify(x):
   t = tuple(int(i) for i in findall("[0-9]+", x))
   return (t[0:2],t[2:4])

def save_receptors(receptors, savefile):
   f = open(savefile, 'w')
   s = ""
   for i in receptors:
      s = s +str(i)+"\n"
   f.write(s)
   f.close

def read_receptors(savefile):
   receptors = []
   f = open(savefile, 'r+')
   lines = f.readlines()
   for i in lines:
      receptors.append(tupify(i))
   return receptors
   #save_receptors(receptors,savefile)

def apply_receptors_to_directory(receptor_path, img_dir):
   files = listdir(img_dir)   
   receptors = read_receptors(receptor_path)
   for i in files:
      img = Image.open(img_dir + i)

def new_x_receptor(img):
   (x,y) = img.size
   my_x  = rr(0,x)
   my_y1 = rr(0,y)
   my_y2 = rr(0,y)
   miny  = my_y1
   maxy  = my_y2
   if maxy < miny:
      miny = my_y2
      maxy = my_y1
   start = (my_x,miny)
   end   = (my_x,maxy)
   return (start,end)

def new_y_receptor(img):
   (x,y) = img.size
   my_y  = rr(0,y)
   my_x1 = rr(0,x)
   my_x2 = rr(0,x)
   minx  = my_x1
   maxx  = my_x2
   if maxx < minx:
      minx = my_x2
      maxx = my_x1
   start = (minx,my_y)
   end   = (maxx,my_y)
   return (start,end)

def activate_receptor(img, points):
   activated = False
   ((x1,y1),(x2,y2)) = points
   if x1 == x2:
      x_rec = True
   else:
      x_rec = False
   current_x = x1
   current_y = y1
   if x_rec:
      for i in range(y1,y2+1):
         if img.getpixel((current_x,i)) > 0:
            print "True at "+str((current_x,i))
            print str(img.getpixel((current_x,i)))
            return True
   else:
      for i in range(x1,x2+1):
         if img.getpixel((i,current_y)) > 0:
            print "True at "+str((i,current_y))
            print str(img.getpixel((i,current_y)))
            return True
   return False

img = Image.open('arial_a.png')
generate_receptors(img, 'receptors.txt',10)
#generate_receptors(img, 'receptors.txt', 100)
r = read_receptors('receptors.txt')
z = [activate_receptor(img, i) for i in r]
z = filter(lambda x:x==False, z)
print str(z)
         

#files = listdir(path)
#print str(files)
#for i in files:
#   mypaste(path+i, (100,100))

