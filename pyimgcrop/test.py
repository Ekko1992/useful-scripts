from PIL import Image, ImageDraw
import sys

im = Image.open("30800537.jpg")

draw = ImageDraw.Draw(im)
'''
draw.line((622, 568, 374, 589), fill=128)
draw.line((374, 589, 294, 869), fill=128)
draw.line((294, 869, 690, 866), fill=128)
draw.line((690, 866, 620, 570), fill=128)
draw.line((620, 570, 622, 568), fill=128)
'''
#f = open("awsbox5.txt")
f = open("azurebox5.txt")
data = f.readline().split(" ")
box_count = len(data)/4
for i in range(0, box_count):
	xy = [float(data[4*i]),float(data[4*i+1]),float(data[4*i+2]),float(data[4*i+3])]
	draw.rectangle(xy, fill=None, outline=255)
del draw



# write to stdout
#im.save("aws5.jpg")
im.save("azure5.jpg")
