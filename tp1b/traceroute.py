from scapy.all import *
import time
import sys
t=0.0
promedio=0.0
target = sys.argv[1]
count = int(sys.argv[2])
ans,unans=traceroute([target])
packet = Ether()/IP(dst=target)/ICMP()
for i in range(count):
	ans,unans=srp(packet, filter='icmp', verbose=0)
	rx = ans[0][1]
	tx = ans[0][0]
	delta = rx.time-tx.sent_time
	print "Ping:", delta
	t+=delta
print "RTT:", (t/count)*1000
