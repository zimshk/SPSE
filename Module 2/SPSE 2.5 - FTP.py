#!/usr/local/bin/python3

from ftplib import FTP
import threading
import queue
import time

'''
- Create a list of FTP sites
- Create a WorkerThread and Queue which can login to these sites and list the root directory and exit
- Use 5 threads for this job and 10 FTP sites
'''

ftp_sites = ['ftp.opera.com','ftp.software.ibm.com','ftp.debian.org','ftp.ubuntu.com','ftp.cdc.gov','ftp.freebsd.org','bourbon.usc.edu','mirrors.kernel.org','gnu.mirror.iweb.com']

# uses Vivek's skeleton code and replaces the "run" fcn w/ ftp parts
# ftp code: https://docs.python.org/2/library/ftplib.html
class WorkerThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            site = self.queue.get()
            print("Attempting login for: {}".format(site))
            ftp = FTP(site)             # connect to host, default port
            ftp.login()                 # user anonymous, passwd anonymous@
            ftp.retrlines('LIST')       # list directory contents
            self.queue.task_done()
            print("\n\n")

queue = queue.Queue()

for i in range(5):
    worker = WorkerThread(queue)
    worker.setDaemon(True)
    worker.start()

for site in ftp_sites:
        queue.put(site)

queue.join()

print("\nDone.")
