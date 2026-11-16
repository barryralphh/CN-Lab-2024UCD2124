
import sys; sys.path.insert(0,"tools")
from ptlogin import *
ok=pt_login(); print("login ok:",ok,flush=True)
wid=sh("xdotool search --onlyvisible --name 'Cisco Packet Tracer'").stdout.split()[0]
sh(f"xdotool windowsize {wid} 1600 900 windowmove {wid} 0 0"); time.sleep(6)
sh("xdotool mousemove 250 9 click 1"); time.sleep(3)
print("EXT:",words("e1",20,(150,0,700,400)),flush=True)
sh("xdotool key Escape"); time.sleep(1)
sh("xdotool mousemove 192 9 click 1"); time.sleep(3)
print("TOOLS:",words("e2",20,(100,0,700,400)),flush=True)
sh("xdotool key Escape")
