#!/bin/bash
source tools/lib.sh; init exp05
for n in pc1 pc3 r1 r2 r3; do mknode $n; done
link pc1 eth0 10.1.1.10/24 r1 eth0 10.1.1.1/24
link r1 eth1 10.12.0.1/30 r2 eth0 10.12.0.2/30
link r2 eth1 10.23.0.1/30 r3 eth0 10.23.0.2/30
link r3 eth1 10.3.3.1/24 pc3 eth0 10.3.3.10/24
link r1 eth2 10.13.0.1/30 r3 eth2 10.13.0.2/30
for r in r1 r2 r3; do sudo ip netns exec $r sysctl -qw net.ipv4.ip_forward=1; done
sudo ip netns exec pc1 ip route add default via 10.1.1.1
sudo ip netns exec pc3 ip route add default via 10.3.3.1
cap routes_before_r1 "$E r1 ip route"
cap ping_fails_no_routes "$E pc1 ping -c 3 -W 1 10.3.3.10"
cap r1_static_route "$E r1 ip route add 10.3.3.0/24 via 10.12.0.2 && $E r1 ip route"
cap r2_static_routes "$E r2 ip route add 10.3.3.0/24 via 10.23.0.2 && $E r2 ip route add 10.1.1.0/24 via 10.12.0.1 && $E r2 ip route"
cap r3_static_route "$E r3 ip route add 10.1.1.0/24 via 10.23.0.1 && $E r3 ip route"
cap ping_works "$E pc1 ping -c 4 10.3.3.10"
cap traceroute_via_r2 "$E pc1 traceroute -n -I 10.3.3.10"
cap change_path "$E r1 ip route replace 10.3.3.0/24 via 10.13.0.2 && $E r3 ip route replace 10.1.1.0/24 via 10.13.0.1 && $E r1 ip route get 10.3.3.10"
cap traceroute_direct_r1_r3 "$E pc1 traceroute -n -I 10.3.3.10"
