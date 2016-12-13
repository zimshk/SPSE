#!/usr/local/bin/python

'''
Create a DNS poisoning tool similar to Dnsspoof using scapy
'''

from scapy.all import *

# https://thepacketgeek.com/scapy-p-09-scapy-and-dns/
# https://gist.github.com/thepacketgeek/6928674
# https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml
# http://blog.catchpoint.com/2014/07/09/dissecting-dns-communications/
# http://www.zytrax.com/books/dns/ch8/