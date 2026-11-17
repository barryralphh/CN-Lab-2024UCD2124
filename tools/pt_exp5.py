
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()

place("router1941",*R0); place("router1941",*R1); place("router1941",*R2); place("pc",*L0); place("pc",*L2)
cable(L0,R0); cable(R0,R1); cable(R1,R2); cable(R2,L2); cabling_wait("e5",30)
def rc(pos,tag,cmds): cli2(pos,["enable","terminal length 0","configure terminal"]+cmds+["end","show ip interface brief"],tag)
rc(R0,"e5_r1",["interface gigabitEthernet0/0","ip address 192.168.1.1 255.255.255.0","no shutdown","interface gigabitEthernet0/1","ip address 10.0.12.1 255.255.255.252","no shutdown"])
rc(R1,"e5_r2",["interface gigabitEthernet0/0","ip address 10.0.12.2 255.255.255.252","no shutdown","interface gigabitEthernet0/1","ip address 10.0.23.1 255.255.255.252","no shutdown"])
rc(R2,"e5_r3",["interface gigabitEthernet0/0","ip address 10.0.23.2 255.255.255.252","no shutdown","interface gigabitEthernet0/1","ip address 192.168.3.1 255.255.255.0","no shutdown"])
pc_ip2(L0,"192.168.1.2","255.255.255.0","192.168.1.1","e5_pc0"); pc_ip2(L2,"192.168.3.2","255.255.255.0","192.168.3.1","e5_pc1")
cmd2(L0,["ping 192.168.3.2"],"e5_before")
cli2(R0,["show ip route"],"e5_r1_before")
cli2(R0,["configure terminal","ip route 192.168.3.0 255.255.255.0 10.0.12.2","ip route 10.0.23.0 255.255.255.252 10.0.12.2","end","show ip route"],"e5_r1_static")
cli2(R1,["configure terminal","ip route 192.168.1.0 255.255.255.0 10.0.12.1","ip route 192.168.3.0 255.255.255.0 10.0.23.2","end","show ip route"],"e5_r2_static")
cli2(R2,["configure terminal","ip route 192.168.1.0 255.255.255.0 10.0.23.1","ip route 10.0.12.0 255.255.255.252 10.0.23.1","end","show ip route"],"e5_r3_static")
cmd2(L0,["ping 192.168.3.2","tracert 192.168.3.2"],"e5_after")
