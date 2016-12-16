from scapy.all import *

# Super easy, just review the scapy docs and pop in DNS()
# http://www.secdev.org/projects/scapy/doc/usage.html#fuzzing

# can test with: sudo tcpdump -i enp0s3 udp port 53

sr(IP(dst="192.168.1.1")/UDP()/fuzz(DNS()),loop=1)


