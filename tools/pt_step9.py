
import sys; sys.path.insert(0,"tools")
from ptlogin import *
ok=pt_login()
print("login ok:",ok,flush=True)
ws=sh("xdotool search --onlyvisible --name 'Cisco Packet Tracer'").stdout.split()
print("wins",[(w,sh(f"xdotool getwindowgeometry {w}").stdout.replace("\\n"," ")) for w in ws],flush=True)
if ok:
    wid=ws[0]
    sh(f"xdotool windowsize {wid} 1600 900 windowmove {wid} 0 0"); time.sleep(6)
    print("MENU:",words("m1",20,(0,0,1600,80)),flush=True)
    print("ALL:",words("m1b",50)[:60],flush=True)
