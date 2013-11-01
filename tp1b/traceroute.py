#! /usr/bin/python
from scapy.all import *

target = "www.google.com"
ans,unans = sr1(IP(dst=target, ttl=(1,25), id=RandShort())/ICMP())
for snd,rcv in ans:
	print snd.ttl, rcv.src

print ans.summary()


