import Image

im = Image.open("images/arial_characters.png")
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
