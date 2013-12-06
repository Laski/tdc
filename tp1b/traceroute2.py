from scapy.all import *
import math
import sys
from scapy.all import *
hostname = sys.argv[1]
T=0
R=0
C=0
D=0
m=1
h=0
for i in range(1, 28):
    pkt = IP(dst=hostname, ttl=i, id=RandShort()) / TCP(flags=0x2)
    # Send the packet and get a reply
    ans, unans = sr(pkt, verbose=0)
    for snd,rcv in ans:
        C = C+1
        time=(rcv.time - snd.time)
        T=(time+T)
        R=(T/C)
        d=time-R
        h=h+(d*d)
        D= math.sqrt(h/C)
        total = R+(m*D)
        trans= (time > total)
        print snd.ttl, rcv.src, isinstance(rcv.payload, TCP), time*1000, " ms // PROMEDIO: ", R*1000, "Transatlatico: ", trans
    