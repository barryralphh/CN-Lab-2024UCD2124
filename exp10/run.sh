#!/bin/bash
source tools/lib.sh; init exp10
mksw sw; for h in r pc1 pc2 pc3; do mknode $h; done
attach r eth0 sw 10.0.1.1/24; for h in pc1 pc2 pc3; do attach $h eth0 sw ""; done
dhcp_server r eth0
cap switch_mac_table_before "$E sw bridge fdb show br br0 | grep -v permanent || echo '(no dynamic entries learned yet)'"
capstart sw br0 dhcp.pcap
cap dhcp_pc1 "$E pc1 dhclient -v -1 -pf /run/dhclient-pc1.pid -lf /var/lib/dhcp/dhclient-pc1.leases eth0"
cap dhcp_pc2 "$E pc2 dhclient -v -1 -pf /run/dhclient-pc2.pid -lf /var/lib/dhcp/dhclient-pc2.leases eth0"
cap dhcp_pc3 "$E pc3 dhclient -v -1 -pf /run/dhclient-pc3.pid -lf /var/lib/dhcp/dhclient-pc3.leases eth0"
P2=$(sudo ip netns exec pc2 ip -4 -br addr show eth0 | awk '{print $3}' | cut -d/ -f1)
cap unicast_not_flooded_to_pc3 "$E pc3 timeout 5 tcpdump -ni eth0 icmp & sleep 1; $E pc1 ping -c 3 $P2; wait"
cap switch_mac_table_after "$E sw bridge fdb show br br0 | grep -v permanent"
cap host_macs_and_ports "for h in r pc1 pc2 pc3; do echo -n \"\$h: \"; $E \$h cat /sys/class/net/eth0/address; done; $E sw bridge link show"
capstop dhcp.pcap
PC=$OUT/dhcp.pcap
cap dhcp_packets "tshark -r $PC -Y dhcp"
cap dhcp_detail "tshark -r $PC -Y dhcp -V -c 2 | head -55"
wsshot dhcp.pcap "dhcp" dhcp_dora
