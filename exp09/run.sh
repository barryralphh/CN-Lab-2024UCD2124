#!/bin/bash
source tools/lib.sh; init exp09
topo_routed
sudo ip netns exec r sysctl -qw net.ipv4.ip_forward=1
capstart r eth0 icmp.pcap
cap ping_echo "$E pc1 ping -c 3 10.0.2.2"
cap ping_ttl_expired "$E pc1 ping -c 1 -t 1 10.0.2.2"
cap ping_big_packet "$E pc1 ping -c 2 -s 1000 10.0.2.2"
cap ping_unreachable_net "$E pc1 ping -c 1 -W 1 10.0.9.9"
capstop icmp.pcap
PC=$OUT/icmp.pcap
cap icmp_summary "tshark -r $PC -Y icmp -T fields -e frame.number -e ip.src -e ip.dst -e icmp.type -e icmp.code -E header=y"
cap echo_request_detail "tshark -r $PC -Y 'icmp.type==8' -V -c 1 | head -50"
cap ttl_exceeded_detail "tshark -r $PC -Y 'icmp.type==11' -V -c 1 | head -50"
cap net_unreachable_detail "tshark -r $PC -Y 'icmp.type==3' -V -c 1 | head -50"
wsshot icmp.pcap "icmp" icmp_all
wsshot icmp.pcap "icmp.type==11 || icmp.type==3" icmp_errors
