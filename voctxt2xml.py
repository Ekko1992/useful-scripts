#!/bin/python
#convert labeled txt dataset to xml
#Author: Xiaohong zhao
#Date: 2017.3.28

import os
import os.path
import re
from PIL import Image  

ori_dir = "./labels/"
new_dir = "./Annotations/"
jpg_dir = "./JPEGImages/"


def txt2xml(filename):
	name = filename.split(".")[0]
	
	ori_filename = ori_dir + name + ".txt"
	new_filename = new_dir + name + ".xml"
	jpg_filename = name + ".jpg"

	infile = open(ori_filename)
	outfile = open(new_filename,'w')
	
	outfile.write("<annotation>\n")
	outfile.write("\t<filename>"+ jpg_filename + "</filename>\n")
	jpg_filename = jpg_dir + name + ".jpg"
	
	img = Image.open(jpg_filename)  
	width = str(img.size[0])
	height = str(img.size[1])
	depth = "3"

	infile.readline()
	data = infile.readline().split()

	outfile.write("\t<size>\n")
	outfile.write("\t\t<width>" + width + "</width>\n")
	outfile.write("\t\t<height>" + height + "</height>\n")
	outfile.write("\t\t<depth>" + depth + "</depth>\n")
	outfile.write("\t</size>\n")

	outfile.write("\t<segmented>0</segmented>\n")


	outfile.write("\t<object>\n")

	outfile.write("\t\t<name>face</name>\n")
	outfile.write("\t\t<pose>Unspecified</pose>\n")
	outfile.write("\t\t<truncated>0</truncated>\n")
	outfile.write("\t\t<difficult>0</difficult>\n")
	
	outfile.write("\t\t<bndbox>\n")
	outfile.write("\t\t\t<xmin>" + data[0] + "</xmin>\n")
	outfile.write("\t\t\t<ymin>" + data[1] + "</ymin>\n")
	outfile.write("\t\t\t<xmax>" + data[2] + "</xmax>\n")
	outfile.write("\t\t\t<ymax>" + data[3] + "</ymax>\n")
	outfile.write("\t\t</bndbox>\n")
	
	outfile.write("\t</object>\n")
	outfile.write("</annotation>\n")
	
		
	infile.close()
	outfile.close()
	

for i in os.listdir(ori_dir):
	if os.path.isfile(os.path.join(ori_dir, i)):
		txt2xml(i)
#txt2xml("000001.txt")
				



