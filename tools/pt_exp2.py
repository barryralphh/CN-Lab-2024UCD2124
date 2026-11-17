
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
SW=(700,300); P=[(450,520),(700,520),(950,520)]
place("switch2960",*SW)
for p in P: place("pc",*p)
note("WS: "+" ".join(t[0] for t in ws_words("e2_ws")))
for p in P: cable(p,SW)
time.sleep(40); shot("e2_topology")
for i,(p,ip) in enumerate(zip(P,("192.168.1.2","192.168.1.3","192.168.1.4"))):
    pc_ip(p,ip,"255.255.255.0","",f"e2_pc{i}"); close_all(); note("wins now: "+str(devwins()))
cmd(P[0],["ipconfig","ping 192.168.1.3","ping 192.168.1.4","arp -a"],"e2_pc0"); close_all()
