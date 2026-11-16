#!/bin/bash
source tools/lib.sh; init exp07
topo_lan
sudo ip netns exec pc3 python3 -m http.server 8080 --bind 192.168.10.13 >/dev/null 2>&1 &
cap tshark_interfaces "tshark -D"
capstart sw br0 lan_capture.pcap
sudo ip netns exec pc1 ping -c 3 192.168.10.12 >/dev/null 2>&1
sudo ip netns exec pc2 ping -c 2 192.168.10.13 >/dev/null 2>&1
sudo ip netns exec pc1 curl -s -o /dev/null http://192.168.10.13:8080/ >/dev/null 2>&1
capstop lan_capture.pcap
PC=$OUT/lan_capture.pcap
cap capture_info "capinfos $PC | head -20"
cap packet_list "tshark -r $PC | head -40"
cap protocol_hierarchy "tshark -r $PC -q -z io,phs"
cap filter_icmp "tshark -r $PC -Y icmp"
cap filter_http_port "tshark -r $PC -Y 'tcp.port==8080' | head -20"
cap packet_detail_icmp "tshark -r $PC -Y icmp -V -c 1 | head -55"
wsshot lan_capture.pcap "" all_packets
wsshot lan_capture.pcap "icmp" filter_icmp
wsshot lan_capture.pcap "tcp.port==8080" filter_tcp
