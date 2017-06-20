#!/bin/python
import cv2
import os
import os.path
rootdir = "./"

def cut_video(filename):
	resdir = 'image_' + filename[:5]
	os.mkdir(resdir)
	vc = cv2.VideoCapture(filename) #read video file  
	c=1  
  
	if vc.isOpened(): #check if file is open
		rval , frame = vc.read()  
	else:  
		rval = False  
  
	timeF = 500  #frame rate 
	
  
	while rval: #read frames in loop  
		rval, frame = vc.read()  
		if(c%timeF == 0): #save img every timeF frames  
			cv2.imwrite(resdir + '/' +str(c) + '.jpg',frame) #save as img
		c = c + 1  
		cv2.waitKey(1) 
  
	vc.release()  
	

for i in os.listdir(rootdir):
	if os.path.isfile(os.path.join(rootdir, i)) and i[-4:] == ".mp4":
		cut_video(i)

				

