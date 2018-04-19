import socket  
import cv2  
import numpy  
  
address=('127.0.0.1',8000) 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
s.bind(address)  
s.listen(True)  

def recvall(sock, count): 
    buf = b'' 
    while count: 
        newbuf = sock.recv(count) 
        if not newbuf: 
            return None 
        buf += newbuf 
        count -= len(newbuf)
    return buf

conn, addr = s.accept()

length = recvall(conn,16)
print length
stringData = recvall(conn, int(length)) 
data = numpy.fromstring(stringData, dtype='uint8') 
decimg=cv2.imdecode(data,1) 
cv2.imshow('SERVER',decimg) 
cv2.waitKey(0) 
s.close()
cv2.destroyAllWindows()




