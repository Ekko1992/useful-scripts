import schedule
import threading
import os
import datetime
import time

def download():
	print "test"
	os.system("azcopy \
		--source https://vmaxx.blob.core.windows.net/office/the\ irvine\ company/the\ irvine\ spectrum/storage_backup/ \
		--destination /home/ekko/test --source-key MOQ77kfnjGVv6rBZB8wiHXfKWg/vmGbGfsvr7llxXjvvUrCx2bg+q1gfGkFghZojeAGmhDzTnyIRRR7Hk53OjA== \
		--include \"2017-12-26\", \"2017-12-27\" \
		--recursive")	


def run_threaded(job_func):
	job_thread = threading.Thread(target = job_func)
	job_thread.start()

if __name__ == '__main__':
	schedule.every().day.at("11:48").do(run_threaded, download)
	while True:
			print datetime.datetime.now()
			schedule.run_pending()
			time.sleep(5)
			
