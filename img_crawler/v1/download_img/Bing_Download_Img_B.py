#!/usr/bin/env python3
# coding=utf-8
import os, sys, urllib.request, re, threading, posixpath, urllib.parse, argparse, atexit, random, socket, time

##############################################################
# download images from BING (part B)
# download images again which are failed in part A
##############################################################

adult_filter = True #Do not disable adult filter by default
pool_sema = threading.BoundedSemaphore(value = 20) #max number of download threads
bingcount = 17 # default number download  images
socket.setdefaulttimeout(20)

in_progress = []
def download(url):
	pool_sema.acquire()
	path = urllib.parse.urlsplit(url).path
	filename = posixpath.basename(path)
	while os.path.exists(output_dir + '/' + filename):
		filename = str(random.randint(0,100)) + filename
	in_progress.append(filename)
	try:
		urllib.request.urlretrieve(url, output_dir + '/' + filename)
		in_progress.remove(filename)
	except:
		print("FAIL " + filename)
	pool_sema.release()

def removeNotFinished():
	for filename in in_progress:
		try:
			os.remove(output_dir + '/' + filename)
		except FileNotFoundError:
			pass

if __name__ == "__main__":
	num_page = 900 #deault num download bing images 
	atexit.register(removeNotFinished)
	parser = argparse.ArgumentParser(description = 'Bing image bulk downloader')
	parser.add_argument('keyword', help = 'Keyword to search')
	parser.add_argument('default_path', help = 'output path')
	parser.add_argument('-o', '--output', help = 'Output directory', required = False)
	parser.add_argument('-p', '--page', help = 'Number of download pages', type = int, required = False)
	parser.add_argument('--filter', help = 'Enable adult filter', action = 'store_true', required = False)
	parser.add_argument('--no-filter', help=  'Disable adult filter', action = 'store_true', required = False)
	args = parser.parse_args()
	keyword = args.keyword
	keyword2 = keyword
	keyword = keyword.strip()
	keyword_dir = keyword.replace(' ', '_')
	keyword_dir = keyword_dir.replace('\'', '')
	path_save = args.default_path
	output_dir = path_save+'/download_img/'+keyword_dir #default output_dir
	if args.output:
		output_dir = args.output
	if args.page:
		num_page = args.page
	if adult_filter:
		adlt = ''
	else:
		adlt = 'off'
	if args.no_filter:
		adlt = 'off'
	elif args.filter:
		adlt = ''
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	current = num_page
	last = ''
	url_list=['abc']
	url_path=path_save+'/download_img/'+keyword_dir+'.txt'
	file1=open(url_path,'r') # url link
	for line in file1.readlines():
		line=line.strip()
		url_list.append(line)
	file1.close()
	file2=open(url_path,'a')
	while True:
		socket.setdefaulttimeout(20)
		time.sleep(1)
		response = urllib.request.urlopen('https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(keyword) + '&async=content&first=' + str(current) + '&adlt=' + adlt)
		html = response.read().decode('utf8')
		response.close()
		links = re.findall('imgurl:&quot;(.*?)&quot;',html)
		bingcount = len(links)
		if bingcount<1:
			bingcount = 17
		try:
			if links[-1] == last:
				print("******links are empty ; break;************")
				break
			last = links[-1]

			print('-------------------------------------------------------------')
			print(current)
			current += bingcount #number of bing page
			for link in links:
				num = url_list.count(link)    
				if num > 0:
					continue #only download missed urls during phase A
				url_list.append(link)
				file2.write(link)
				file2.write('\n')
				t = threading.Thread(target = download,args = (link,))
				t.start()
		except IndexError:
			print("No search results")
			sys.exit()
		time.sleep(0.2)
	file2.close()
