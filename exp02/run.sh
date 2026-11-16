#!/bin/bash
source tools/lib.sh; init exp02
topo_lan
cap ip_pc1 "$E pc1 ip addr show eth0"
cap ip_pc2 "$E pc2 ip addr show eth0"
cap ip_pc3 "$E pc3 ip addr show eth0"
cap switch_ports "$E sw bridge link show"
cap ping_pc1_pc2 "$E pc1 ping -c 4 192.168.10.12"
cap ping_pc1_pc3 "$E pc1 ping -c 4 192.168.10.13"
cap ping_pc3_pc2 "$E pc3 ping -c 4 192.168.10.12"
cap arp_table_pc1 "$E pc1 ip neigh show"
cap switch_mac_table "$E sw bridge fdb show br br0 | grep -v permanent"
