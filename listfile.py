#!/usr/local/bin/ python
'''
from os import listdir
from os.path import isfile, join
mypath = 'img1/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

result = open('person.list','w')
for file in onlyfiles:
	result.write(mypath + file + '\n')
result.close()
'''
import commands as cm
mypath = 'img1/'
result = open('person.list','w')
(status, info) = cm.getstatusoutput('ls img1')
info = info.split('\n')
for row in info:
	print row
	result.write(mypath + row + '\n')
#print(info)
