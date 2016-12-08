#!/usr/bin/python3
import socket
import struct
import binascii
import codecs

'''
Create a sniffer which uses a filter to only print details of an HTTP packet (TCP, Port 80)
'''

# written and tested on ubuntu sever 16.04 LTS because macOS doesn't have PF_PACKET
# I just used python3 -m http.server 80 (or python -m SimpleHTTPServer 80) to create a simple HTTP server to intercept

# I really tried to make the code compatible for both python 2 and 3, but the changes to bytes/unicode/strings got too annoying
# In the parse_http function I made a note of how to make the code compatible for python 2

# probably the most annoying exercise, if you were to fully complete all the fields
# I opted just to print out the interesting bits of data in the ethernet, IP, and TCP headers

# Most of this is adapted from Vivek's lab
# keep this chart handy: https://docs.python.org/2/library/struct.html#format-characters

# this site shows the work you would have to put in to fully parse each field: http://www.binarytides.com/python-packet-sniffer-code-linux/
# scroll down to the section that talks about AF_PACKET instead of AF_INET
# AF_INET works at Layer 3 instead of Layer 2 (skips the ethernet stuff)

# https://docs.python.org/3/library/socket.html
# is helpful for understanding the various socket.*to* conversion functions

rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))

def format_mac(mac):
    return ":".join(mac[i:i+2] for i in range(0,len(mac),2))

def parse_ether(pkt):
    ethernetHeader = pkt[0][:14]
    eth_hdr = struct.unpack("!6s6sH", ethernetHeader)
    dest_mac = binascii.hexlify(eth_hdr[0]).decode("utf-8")
    source_mac = binascii.hexlify(eth_hdr[1]).decode("utf-8")
    ether_type = socket.ntohs(eth_hdr[2])
    # uncomment to print out MAC information
#    print("Dest MAC: {}, Source MAC: {}, Ether type: {}".format(format_mac(dest_mac), format_mac(source_mac), ether_type))
    if ether_type == 8: # 0800 is IP
        return True

def parse_ip(pkt):

    ipHeader = pkt[0][14:34]
    ip_hdr = struct.unpack("!9sB2s4s4s", ipHeader)
    # for printing IP addresses
#    print("Source IP: {}, Dest IP: {}".format(socket.inet_ntoa(ip_hdr[3]), socket.inet_ntoa(ip_hdr[4])))
    if ip_hdr[1] == 6: # if TCP
        return True

def parse_tcp(pkt):

    tcpHeader = pkt[0][34:54]
    tcp_hdr = struct.unpack("!HH16s", tcpHeader)
    source_port = tcp_hdr[0]
    dest_port = tcp_hdr[1]
    # print port inpfo
#    print("TCP source port: {}".format(tcp_hdr[0]))
#    print("TCP dest port: {}".format(tcp_hdr[1]))
    if source_port == 80 or dest_port == 80: # if HTTP
        return True

def parse_http(pkt):
    # Python 2
#   print(unicode(pkt[0][54:], errors='ignore'))
    # Python 3
    print(codecs.decode(pkt[0][54:],encoding='utf-8', errors='ignore'))

while True:
    pkt = rawSocket.recvfrom(2048)
    # not a great wat to do this, but works well for incrementally printing out non-HTTP fields to satisfy the first exercise's requirements
    if parse_ether(pkt):
        if parse_ip(pkt):
            if parse_tcp(pkt):
                parse_http(pkt)



