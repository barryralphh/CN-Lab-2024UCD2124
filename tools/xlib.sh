#!/bin/bash
# Real terminal screenshots: every command runs live inside an xterm window on a virtual display, and that window is captured.
export DISPLAY=:99
PROMPT="$(whoami)@$(hostname):~/CN-Lab\$"
xstart(){
  pgrep -x Xvfb >/dev/null && return
  Xvfb :99 -screen 0 1800x1300x24 >/dev/null 2>&1 &
  sleep 2
}
xrun(){
  xstart
  local base="$1" cmd="$2" s xp i id
  s=$(mktemp /tmp/xrun.XXXXXX)
  printf '%s\n' "$cmd" > "$s"
  printf '%s %s\n' "$PROMPT" "${cmd#sudo }" > "$s.p"
  cp "$s.p" "$base.txt"
  cat > "$s.w" <<EOF
#!/bin/bash
cat "$s.p"
( timeout 60 bash "$s" 2>&1 | head -55 | tee -a "$base.txt" )
touch "$s.done"
sleep 12
EOF
  xterm -geometry 150x62+0+0 -fa 'DejaVu Sans Mono' -fs 12 -bg '#1e1e1e' -fg '#e6e6e6' -e bash "$s.w" &
  xp=$!
  for i in $(seq 1 130); do [ -e "$s.done" ] && break; sleep 0.5; done
  sleep 1
  id=$(xdotool search --onlyvisible --class xterm | head -1)
  import -window "$id" "$base.raw.png"
  kill $xp 2>/dev/null; pkill -x xterm 2>/dev/null
  convert "$base.raw.png" -fuzz 3% -trim +repage -bordercolor '#1e1e1e' -border 14 "$base.png"
  rm -f "$base.raw.png" "$s" "$s.p" "$s.w" "$s.done"
}
