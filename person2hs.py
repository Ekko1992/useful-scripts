#!/bin/python
#convert person data to head-shoulder data
#Author: Xiaohong zhao
#Date: 2017.3.23


import os
import os.path
import re
ori_dir = "./Annotations/"
new_dir = "./Annotations_new/"

def convert2hs(filename):
	ori_filename = ori_dir + filename
	new_filename = new_dir + filename
	infile = open(ori_filename)
	outfile = open(new_filename,'w')
	
	x_min = 0
	x_max = 0
	y_min = 0
	y_max = 0
	#i = 1
	
	while(1):
		line = file.readline(infile)
		
		if not line:
			break
		#search for person tag
		if "xmin" in line:
			x_min_s = re.findall(r'\d+', line)[0]
			x_min = int(x_min_s)
			
			line1 = file.readline(infile)
			line2 = file.readline(infile)
			line3 = file.readline(infile)
			
			y_min_s = re.findall(r'\d+', line1)[0]
			y_min =int(y_min_s)
			
			x_max_s = re.findall(r'\d+', line2)[0]
			x_max = int(x_max_s)
			
			y_max_s = re.findall(r'\d+' , line3)[0]
			y_max = int(y_max_s)
			
			length = int((x_max - x_min)*0.1)
			width = int((y_max - y_min)*0.25)
			
			#replace 
			line = line.replace(x_min_s, str(x_min + length))
			line2 = line2.replace(x_max_s, str(x_max - length))
			line3 = line3.replace(y_max_s, str(y_min + width))			
			
			outfile.write(line)
			outfile.write(line1)
			outfile.write(line2)
			outfile.write(line3)
								  
		else:
			outfile.write(line)
		#i = i + 1
		
		
	infile.close()
	outfile.close()
	

for i in os.listdir(ori_dir):
	if os.path.isfile(os.path.join(ori_dir, i)):
		convert2hs(i)
#convert2hs("000001.xml")
				



