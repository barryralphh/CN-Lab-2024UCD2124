#!/bin/bash
PROMPT='pradumn@2024UCD2124:~$'
E="sudo ip netns exec"
export E
clean(){
  sudo pkill -x dnsmasq; sudo pkill -x dhclient; sudo pkill -x tcpdump; sudo pkill -f http.server
  for n in $(ip netns list | awk '{print $1}'); do sudo ip netns del "$n"; done
  sudo rm -rf /etc/netns
  true
}
init(){ EXP=$1; OUT=$EXP/out; mkdir -p "$OUT"; N=0; clean; }
cap(){
  N=$((N+1))
  xrun "$OUT/$(printf %02d $N)_$1" "$2"
}
mksw(){ sudo ip netns add $1; sudo ip -n $1 link add br0 type bridge; sudo ip -n $1 link set br0 up; sudo ip -n $1 link set lo up; }
mknode(){ sudo ip netns add $1; sudo ip -n $1 link set lo up; sudo mkdir -p /etc/netns/$1; sudo touch /etc/netns/$1/resolv.conf; }
attach(){ local n=$1 i=$2 s=$3 ip=$4 p="p-$1-$2"; sudo ip link add $i netns $n type veth peer name $p netns $s; sudo ip -n $n link set $i up; sudo ip -n $s link set $p master br0; sudo ip -n $s link set $p up; [ -n "$ip" ] && sudo ip -n $n addr add $ip dev $i; true; }
link(){ sudo ip link add $2 netns $1 type veth peer name $5 netns $4; sudo ip -n $1 link set $2 up; sudo ip -n $4 link set $5 up; sudo ip -n $1 addr add $3 dev $2; sudo ip -n $4 addr add $6 dev $5; }
topo_lan(){ mksw sw; for h in pc1 pc2 pc3; do mknode $h; done; attach pc1 eth0 sw 192.168.10.11/24; attach pc2 eth0 sw 192.168.10.12/24; attach pc3 eth0 sw 192.168.10.13/24; }
topo_routed(){ mksw sw1; mksw sw2; mknode pc1; mknode pc2; mknode r; attach pc1 eth0 sw1 10.0.1.2/24; attach r eth0 sw1 10.0.1.1/24; attach pc2 eth0 sw2 10.0.2.2/24; attach r eth1 sw2 10.0.2.1/24; sudo ip netns exec pc1 ip route add default via 10.0.1.1; sudo ip netns exec pc2 ip route add default via 10.0.2.1; sudo ip netns exec r sysctl -qw net.ipv4.ip_forward=0; }
capstart(){ sudo ip netns exec $1 tcpdump -U -i $2 -w /tmp/$3 >/dev/null 2>&1 & sleep 2; }
capstop(){ sleep 1; sudo pkill -x tcpdump; sleep 1; sudo cp /tmp/$1 "$OUT/$1"; sudo chmod 644 "$OUT/$1"; }
wsshot(){
  local pc="$PWD/$OUT/$1" png="$PWD/$OUT/WS_$3.png"
  xvfb-run -a -s "-screen 0 1400x850x24" bash -c "
    wireshark -r '$pc' ${2:+-Y '$2'} -o gui.update.enabled:FALSE >/dev/null 2>&1 &
    sleep 10
    w=\$(xdotool search --onlyvisible --class wireshark | head -1)
    [ -n \"\$w\" ] && xdotool windowmove \$w 0 0 windowsize \$w 1400 850
    sleep 3
    import -window root '$png'
    pkill wireshark" || true
}
dhcp_server(){
cat > /tmp/dnsmasq.conf <<EOF
port=0
interface=$2
bind-interfaces
dhcp-range=10.0.1.100,10.0.1.150,255.255.255.0,12h
dhcp-option=3,10.0.1.1
dhcp-option=6,8.8.8.8
dhcp-leasefile=/tmp/dnsmasq.leases
log-dhcp
log-facility=-
EOF
  sudo rm -f /tmp/dnsmasq.leases
  sudo ip netns exec $1 dnsmasq -k -C /tmp/dnsmasq.conf > "$OUT/dnsmasq.log" 2>&1 &
  sleep 2
}
source "$(dirname "${BASH_SOURCE[0]}")/xlib.sh"
