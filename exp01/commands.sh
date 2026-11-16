#!/bin/bash
source tools/xlib.sh
mkdir -p exp01/out
i=0
while IFS= read -r c; do
  [ -z "$c" ] && continue
  i=$((i+1)); n=$(printf %02d $i); w=$(echo "$c" | awk '{print $1}')
  xrun "exp01/out/${n}_${w}" "$c" < /dev/null
done <<'EOF'
hostname
ip addr show
ifconfig
ip route
route -n
ping -c 4 8.8.8.8
traceroute -m 8 8.8.8.8
tracepath -m 8 8.8.8.8
nslookup google.com
dig google.com +short
host google.com
netstat -tuln
ss -tuln
arp -a
ip neigh
ip -s link show eth0
cat /etc/resolv.conf
curl -I https://example.com
wget --spider https://example.com
nmap -sT -p 22,80,443 localhost
EOF
