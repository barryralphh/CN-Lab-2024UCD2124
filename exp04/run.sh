#!/bin/bash
source tools/lib.sh; init exp04
mksw sw; mknode pc1; mknode pc2; mknode r
attach r eth0 sw 10.0.1.1/24; attach pc1 eth0 sw ""; attach pc2 eth0 sw ""
cap before_dhcp_pc1 "$E pc1 ip addr show eth0"
dhcp_server r eth0
cap dhcp_server_config "cat /tmp/dnsmasq.conf"
cap dhclient_pc1 "$E pc1 dhclient -v -1 -pf /run/dhclient-pc1.pid -lf /var/lib/dhcp/dhclient-pc1.leases eth0"
cap dhclient_pc2 "$E pc2 dhclient -v -1 -pf /run/dhclient-pc2.pid -lf /var/lib/dhcp/dhclient-pc2.leases eth0"
cap after_dhcp_pc1 "$E pc1 ip addr show eth0; $E pc1 ip route"
cap after_dhcp_pc2 "$E pc2 ip addr show eth0; $E pc2 ip route"
cap server_leases "cat /tmp/dnsmasq.leases"
cap server_log "grep -i dhcp $OUT/dnsmasq.log | head -30"
P2=$(sudo ip netns exec pc2 ip -4 -br addr show eth0 | awk '{print $3}' | cut -d/ -f1)
cap ping_pc1_pc2 "$E pc1 ping -c 3 $P2"
