#!/local/usr/bin python
import time
import commands, os, re
import gc  
  
def process_info():  
    pid = os.getpid()  
    res = commands.getstatusoutput('ps aux|grep '+str(pid))[1].split('\n')[0]  
  
    p = re.compile(r'\s+')  
    l = p.split(res)  
    info = {'user':l[0],  
        'pid':l[1],  
        'cpu':l[2],  
        'mem':l[3],  
        'vsa':l[4],  
        'rss':l[5],  
        'start_time':l[6]}  
    return info 

def test():
	count = 0
	result =[]
	for i in range(0, 100000000):
		result.append(i)
	print("finished!")
	print process_info()

	print("free!")
	del result
	gc.collect()
	

	print("==============")
	time.sleep(10)
	gc.collect()
	print process_info()

	print("==============")
	time.sleep(10)
	gc.collect()
	print process_info()

	print("==============")
	time.sleep(10)
	gc.collect()
	print process_info()

	'''
	time.sleep(10)
	del result
	print process_info()

	gc.collect()
	print process_info()
	'''
test()
test()
