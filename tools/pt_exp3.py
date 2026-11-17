
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
R=(700,300); P0=(450,520); P1=(950,520)
place("router1941",*R); place("pc",*P0); place("pc",*P1)
cable(P0,R); cable(P1,R); time.sleep(10); shot("e3_topology")
cli(R,["enable","configure terminal","interface gigabitEthernet0/0","ip address 192.168.1.1 255.255.255.0","no shutdown","interface gigabitEthernet0/1","ip address 192.168.2.1 255.255.255.0","no shutdown","end","show ip interface brief","show ip route"],"e3_router"); close_all()
pc_ip(P0,"192.168.1.2","255.255.255.0","192.168.1.1","e3_pc0"); close_all()
pc_ip(P1,"192.168.2.2","255.255.255.0","192.168.2.1","e3_pc1"); close_all()
cmd(P0,["ipconfig","ping 192.168.2.2","tracert 192.168.2.2"],"e3_pc0"); close_all()
