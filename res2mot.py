#!/usr/local/bin/ python
#
#convert result from yolo pedestrain detector to mot format
#
#author: xiaohong zhao
#date: 2017.06.19
count = 1
resultdir = 'result.txt'
f = open(resultdir, 'r')
outputdir = '/home/zhao/work/person_detection_data/MOT/motchallenge-devkit/motchallenge/res/MOT17Det/DPM/data/MOT17-04.txt'
f1 = open(outputdir, 'w')
while(1):
	print count
	count += 1
	imagename = f.readline()
	
	if not imagename:
		break
	col1 = str(int(imagename.split('/')[1].split('.')[0]))
	col2 = f.readline()[:-1]
	baseline = col1 + ',-1,'
	
	num = int(col2)
	for i in range(0, num):
		row = f.readline()[:-1].split(' ')
		col3 = row[0]
		col4 = row[1]
		col5 = str(int(row[2]) - int(row[0]))
		col6 = str(int(row[3]) - int(row[1]))
		col7 = str(float(row[4])*100)
		col8 = '-1'
		col9 = '-1'
		col10 = '-1'
		line = baseline + col3 + ',' + col4 + ',' + col5 + ',' + col6 + ',' + \
			col7 + ',' +col8 + ',' + col9 + ',' +col10 + '\n'
		f1.write(line)
		f1.flush()
f.close()
f1.close()
	