
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()

place("router1941",*R1); place("router1941",*R2); place("pc",*L1)
cable(L1,R1); cable(R1,R2); cabling_wait("e6",30)
cli2(R1,["enable","terminal length 0","configure terminal","interface gigabitEthernet0/0","ip address 192.168.1.1 255.255.255.0","no shutdown","interface gigabitEthernet0/1","ip address 203.0.113.1 255.255.255.252","no shutdown","exit","ip route 0.0.0.0 0.0.0.0 203.0.113.2","end","show ip interface brief"],"e6_r1")
cli2(R2,["enable","terminal length 0","configure terminal","interface gigabitEthernet0/0","ip address 203.0.113.2 255.255.255.252","no shutdown","end","show ip interface brief"],"e6_r2")
pc_ip2(L1,"192.168.1.2","255.255.255.0","192.168.1.1","e6_pc")
cmd2(L1,["ping 203.0.113.2"],"e6_nonat")
cli2(R1,["configure terminal","access-list 1 permit 192.168.1.0 0.0.0.255","interface gigabitEthernet0/0","ip nat inside","interface gigabitEthernet0/1","ip nat outside","exit","ip nat inside source list 1 interface gigabitEthernet0/1 overload","end","show running-config | include nat"],"e6_nat")
cmd2(L1,["ping 203.0.113.2"],"e6_withnat")
cli2(R1,["show ip nat translations","show ip nat statistics"],"e6_trans")
