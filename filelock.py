#!/usr/local/bin python
import time
import fcntl

f = open('test.txt','a')
fcntl.flock(f.fileno(), fcntl.LOCK_EX)
for i in range(0,10):
	print i
	time.sleep(1)
f.close()

