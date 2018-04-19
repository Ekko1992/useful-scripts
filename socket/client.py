import socket  
import os 
import time
import socket  
import cv2  
import numpy  

#capture = cv2.VideoCapture(0)  
#ret, frame = capture.read()
frame = cv2.imread('3.png')
t1 = time.time()
address=('127.0.0.1',8000) 
sock = socket.socket()
sock.connect(address)
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
#while ret: 
result, imgencode = cv2.imencode('1.png', frame, encode_param)
data = numpy.array(imgencode)
stringData = data.tostring()
print str(len(stringData)).ljust(16)
sock.send(str(len(stringData)).ljust(16)) 
sock.send(stringData)
t2 = time.time()
print t2-t1
#ret, frame = capture.read() 
#decimg=cv2.imdecode(data,1)
#cv2.imshow('CLIENT',decimg) 
#cv2.waitKey(10)
#sock.close()
#cv2.destroyAllWindows()