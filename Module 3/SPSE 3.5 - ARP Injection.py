#!/usr/bin/python
import socket
import struct
import binascii

'''
Send an ARP Request Packet using Raw Sockets, verify using Tcpdump or Wireshark
'''

# basically you're trying to create this: http://aftabsiddiqui.com/wp-content/uploads/2013/06/ARP-Packet.jpg

# written and tested on ubuntu sever 16.04 LTS because macOS doesn't have PF_PACKET
# keep this chart handy: https://docs.python.org/2/library/struct.html#format-characters

# command I used to test: sudo tcpdump -i enp0s3 -vv -XX -v arp
# replace enp0s3 with your device name, which can be found using ifconfig

def str_to_network_long(ip):
	'''
	1. pass in a dotted quad ip
	2. converts to network long
	3. converts from host format to network (the [0] is because pack creates a tuple)'''
	return socket.ntohl(struct.unpack("I",socket.inet_aton(ip))[0])

# magic numbers and names from: https://en.wikipedia.org/wiki/Address_Resolution_Protocol#Packet_structure
ether_type = 0x0806
arp_htype = 0x0001
arp_ptype = 0x0800
arp_hlen = 0x06
arp_plen = 0x04
arp_oper = 0x0001
sha = binascii.unhexlify('0800270a8f1b') # found using ifconfig
spa = str_to_network_long("0.0.0.0") 
tha = binascii.unhexlify('ffffffffffff') # arp broadcast
tpa = str_to_network_long("192.168.1.4") # ip address of host you want to resolve


rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))

rawSocket.bind(("enp0s3", socket.htons(0x0800)))

# ethernet header, revisit 3.4 code 
eth_header = struct.pack("!6s6sH", sha, tha, ether_type)

# arp packet
arp_packet = struct.pack("!HHBBH6sI6sI", arp_htype, arp_ptype, arp_hlen, arp_plen, arp_oper, sha, spa, tha, tpa)

packet = eth_header + arp_packet

rawSocket.send(packet)
rawSocket.close()

