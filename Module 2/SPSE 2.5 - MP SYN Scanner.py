from scapy.all import *
from multiprocessing import Pool

'''
Program the TCP SYN scanner using multiprocessing
'''

# Unfortunately you have to complete module 3 before being able to complete this exercise
# You haven't covered anything related to SYN scanning, or scapy at this point

# There are a TON of different ways too accomplish this exercise
# The Python docs a handful of different options
# https://docs.python.org/2/library/multiprocessing.html#the-process-class
# Pool takes only two new lines of code :)

host = "scanme.nmap.org"
ports = [22,23,80,400, 200, 443]

def worker(port):
    resp = sr1(IP(dst=host)/TCP(dport=port,flags="S"), verbose=0, timeout=3)
    if(resp):
        if resp.haslayer(TCP):  
            if resp[TCP].flags == 18:
                print("port {} is open".format(port))
        else:
            print("port {} is closed".format(port))

    else:
        print("port {} is closed".format(port))

    return

p = Pool(3)
p.map(worker, ports)





