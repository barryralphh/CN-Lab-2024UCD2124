
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()

R=R1; P0=L0; P1=L2
place("router1941",*R); place("pc",*P0); place("pc",*P1)
cable(P0,R); cable(P1,R); cabling_wait("e3",30)
cli2(R,["enable","terminal length 0","configure terminal","interface gigabitEthernet0/0","ip address 192.168.1.1 255.255.255.0","no shutdown","interface gigabitEthernet0/1","ip address 192.168.2.1 255.255.255.0","no shutdown","end","show ip interface brief","show ip route"],"e3_r")
pc_ip2(P0,"192.168.1.2","255.255.255.0","192.168.1.1","e3_pc0")
pc_ip2(P1,"192.168.2.2","255.255.255.0","192.168.2.1","e3_pc1")
cmd2(P0,["ipconfig","ping 192.168.2.2","tracert 192.168.2.2"],"e3_pc0")
