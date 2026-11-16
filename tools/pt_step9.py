
import sys; sys.path.insert(0,"tools")
from ptlogin import *
ok=pt_login()
wid=sh("xdotool search --onlyvisible --name 'Cisco Packet Tracer'").stdout.split()[0]
sh(f"xdotool windowsize {wid} 1600 900 windowmove {wid} 0 0"); time.sleep(5)
print("MENU:",words("m1",20,(0,0,1600,80)),flush=True)
for nm in ["Extensions","Extension","Options","Help"]:
    pass
hit=click_text(r"Ext\w*",name="m2"); time.sleep(3)
print("clicked ext:",hit,flush=True)
print("DROPDOWN:",words("m3",20,(0,0,900,500)),flush=True)
