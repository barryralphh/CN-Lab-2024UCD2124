
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()

R=R1; S=L1; P0=L0; P1=L2
place("router1941",*R); place("switch2960",*S); place("pc",*P0); place("pc",*P1)
cable(R,S); cable(P0,S); cable(P1,S); cabling_wait("e4",45)
cli2(R,["enable","terminal length 0","configure terminal","interface gigabitEthernet0/0","ip address 192.168.10.1 255.255.255.0","no shutdown","exit","ip dhcp excluded-address 192.168.10.1 192.168.10.10","ip dhcp pool LAN","network 192.168.10.0 255.255.255.0","default-router 192.168.10.1","dns-server 8.8.8.8","end","show ip dhcp pool","show ip interface brief"],"e4_r")
pc_dhcp(P0,"e4_pc0"); pc_dhcp(P1,"e4_pc1")
cli2(R,["show ip dhcp binding"],"e4_r2")
cmd2(P0,["ipconfig","ping 192.168.10.12"],"e4_pc0")
