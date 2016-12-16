from scapy.all import *
import threading
import Queue
import time

'''
create a multi-threaded port scanner in Python which uses SYN Scanning
'''

# Unfortunately you have to complete module 3 before being able to complete this exercise
# You haven't covered anything related to SYN scanning, or scapy at this point

# Should be relatively easy to combine your 2.5 - FTP exercise with 3.8  SYN scanner

host = "scanme.nmap.org"
ports = [22,23,80,400, 200, 443]

# uses Vivek's skeleton code and replaces the "run" fcn w/ my SYN scanner code from 3.8
class WorkerThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            port = self.queue.get()
            resp = sr1(IP(dst=host)/TCP(dport=port,flags="S"), verbose=0, timeout=3)
            if(resp):
                if resp.haslayer(TCP):  
                    if resp[TCP].flags == 18:
                        print("port {} is open".format(port))
                else:
                    print("port {} is closed".format(port))

            else:
                print("port {} is closed".format(port))

            self.queue.task_done()
        return

queue = Queue.Queue()

for i in range(5):
    worker = WorkerThread(queue)
    worker.setDaemon(True)
    worker.start()

for port in ports:
    queue.put(port)

queue.join()

# http://stackoverflow.com/a/21964880
# Add a brief sleep to avoid a known thread bug
# Vivek handles this bug by printing within the run() command, but I think this is better
time.sleep(1)
print("\nDone.")
