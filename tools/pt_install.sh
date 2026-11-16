
set -x
sudo apt-get install -y -qq xvfb xdotool imagemagick libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0 libnss3 libxss1 libasound2t64 >/dev/null 2>&1 || true
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y ./pt.deb >/tmp/ptinst.log 2>&1 || (tail -20 /tmp/ptinst.log; true)
dpkg -L packettracer 2>/dev/null | grep -Ei 'bin/|PacketTracer' | head -10
ls /opt/pt 2>/dev/null | head
