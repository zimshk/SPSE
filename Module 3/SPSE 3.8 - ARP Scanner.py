#!/usr/local/bin/python

'''
Find out how to get the local subnet automatically
'''

from scapy.all import *
import socket

# http://stackoverflow.com/a/166589
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
# split on last '.', ignore final octet
local_subnet = s.getsockname()[0].rsplit('.',1)[0]
s.close()

# should be (1, 256) for the whole subnet, but that takes a long time
for i in range(1, 12):
    ip = "{}.{}".format(local_subnet,i)
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip, hwdst="ff:ff:ff:ff:ff:ff")
    arp_response = srp1(arp_request, timeout=1, verbose=0)
    if arp_response:
        print("IP: {} MAC: {}".format(arp_response.psrc, arp_response.hwsrc))
                
                                        
