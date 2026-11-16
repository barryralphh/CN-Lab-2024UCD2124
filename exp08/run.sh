#!/bin/bash
source tools/lib.sh; init exp08
topo_lan
cap arp_cache_before "$E pc1 ip neigh show; echo '(cache empty)'"
capstart sw br0 arp.pcap
cap ping_triggers_arp "$E pc1 ping -c 2 192.168.10.12"
capstop arp.pcap
PC=$OUT/arp.pcap
cap arp_cache_after "$E pc1 ip neigh show"
cap host_macs "for h in pc1 pc2; do echo -n \"\$h: \"; $E \$h cat /sys/class/net/eth0/address; done"
cap arp_packets "tshark -r $PC -Y arp"
cap arp_request_detail "tshark -r $PC -Y 'arp.opcode==1' -V -c 1 | head -45"
cap arp_reply_detail "tshark -r $PC -Y 'arp.opcode==2' -V -c 1 | head -45"
wsshot arp.pcap "arp" arp
