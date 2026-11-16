
set -x
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq xvfb xdotool imagemagick libopengl0 libgl1 libglx-mesa0 libegl1 libgles2 libglu1-mesa libxcb-xinerama0 libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-xkb1 libxkbcommon-x11-0 libxkbfile1 libnss3 libxss1 libasound2t64 libpulse0 libdbus-1-3 libfontconfig1 fonts-dejavu-core libxcomposite1 libxdamage1 libxrandr2 libxtst6 libxi6 dbus-x11 >/dev/null 2>&1 || true
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y ./pt.deb >/tmp/ptinst.log 2>&1 || (tail -20 /tmp/ptinst.log; true)
ls /opt/pt
