#!/bin/bash
source tools/lib.sh; init exp06
mknode pc1; mknode r; mknode srv
link pc1 eth0 192.168.1.10/24 r eth0 192.168.1.1/24
link r eth1 203.0.113.2/24 srv eth0 203.0.113.10/24
sudo ip netns exec pc1 ip route add default via 192.168.1.1
sudo ip netns exec r sysctl -qw net.ipv4.ip_forward=1
sudo ip netns exec srv python3 -m http.server 80 --bind 203.0.113.10 > "$OUT/http.log" 2>&1 &
sleep 1
cap topology "for n in pc1 r srv; do echo \"== \$n\"; $E \$n ip -br -4 addr; $E \$n ip route; done"
cap ping_without_nat "$E srv timeout 5 tcpdump -ni eth0 -c 3 icmp & sleep 1; $E pc1 ping -c 2 -W 1 203.0.113.10; wait"
cap enable_nat "$E r iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o eth1 -j MASQUERADE && $E r iptables -t nat -L -n -v"
cap ping_with_nat "$E pc1 ping -c 4 203.0.113.10"
cap server_sees_public_ip "$E srv timeout 5 tcpdump -ni eth0 -c 4 icmp & sleep 1; $E pc1 ping -c 2 203.0.113.10; wait"
cap http_through_nat "$E pc1 curl -s -o /dev/null -w 'HTTP status: %{http_code}\n' http://203.0.113.10/"
cap web_server_log "cat $OUT/http.log"
cap nat_translation_table "$E r conntrack -L"
