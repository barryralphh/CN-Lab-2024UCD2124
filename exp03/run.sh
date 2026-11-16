#!/bin/bash
source tools/lib.sh; init exp03
topo_routed
cap ip_pc1 "$E pc1 ip -br addr; $E pc1 ip route"
cap ip_pc2 "$E pc2 ip -br addr; $E pc2 ip route"
cap router_interfaces "$E r ip -br addr; $E r sysctl net.ipv4.ip_forward"
cap ping_before_forwarding "$E pc1 ping -c 3 -W 1 10.0.2.2"
cap enable_forwarding "$E r sysctl -w net.ipv4.ip_forward=1"
cap ping_after_forwarding "$E pc1 ping -c 4 10.0.2.2"
cap traceroute "$E pc1 traceroute -n -I 10.0.2.2"
cap router_table "$E r ip route"
