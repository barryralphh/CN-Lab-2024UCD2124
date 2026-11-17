
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()

S=R1; P=[L0,L1,L2]
place("switch2960",*S)
for p in P: place("pc",*p)
for p in P: cable(p,S)
cabling_wait("e2")
for i,(p,ip) in enumerate(zip(P,("192.168.1.2","192.168.1.3","192.168.1.4"))): pc_ip2(p,ip,"255.255.255.0","",f"e2_pc{i}")
cmd2(P[0],["ipconfig","ping 192.168.1.3","ping 192.168.1.4","arp -a"],"e2_pc0")
cmd2(P[1],["ping 192.168.1.2"],"e2_pc1")
cli2(S,["enable","show mac address-table","show interfaces status"],"e2_sw")
