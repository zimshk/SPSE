#!/usr/local/bin/python

'''
Create a TCP SYN Scanner using Scapy
'''

# How to perform a SYN Scan is in the Scapy docs
# http://www.secdev.org/projects/scapy/doc/usage.html#syn-scans

# can run: nmap -sS against scanme.nmap.org -p22,80 to check your script
# https://nmap.org/book/osdetect-usage.html

# Good TCP Header diagram
# https://nmap.org/book/images/hdr/MJB-TCP-Header-800x564.png

from scapy.all import *

host = "scanme.nmap.org"
ports = [22,23,80,400]

def syn_scan(host, port):
	resp = sr1(IP(dst=host)/TCP(dport=port,flags="S"), verbose=0, timeout=3)
	if(resp):
		if resp.haslayer(TCP):	
			if resp[TCP].flags == 18:
				print("port {} is open".format(port))
		else:
			print("port {} is closed".format(port))

	else:
		print("port {} is closed".format(port))


for port in ports:
	syn_scan(host, port)