#!/usr/bin/python
from scapy.all import *
import scapy_http.http

'''
Create a Packet sniffer with Scapy for HTTP protocol and print out the HTTP Headers and Data in the GET/POST
'''

# http://stackoverflow.com/a/35451261
# has some helpful info regarding scapy_http.http

# I would honestly recommend running this from the python REPL, it will have nice syntax formatting
# $ sudo scapy 
# >>> import scapy_http.http
# Then the 'sniff' line below
# Obviously replace enp0s3 with whatever your interface name is from 'ifconfig'


sniff(iface="enp0s3", prn=lambda x: x[0][3].show(), lfilter= lambda x: x.haslayer(scapy_http.http.HTTPResponse) or x.haslayer(scapy_http.http.HTTPRequest), s\
tore=0)