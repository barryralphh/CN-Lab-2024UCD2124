
import sys; sys.path.insert(0,"tools")
from ptlogin import *
ok=pt_login(); print("login ok:",ok,flush=True)
wid=sh("xdotool search --onlyvisible --name 'Cisco Packet Tracer'").stdout.split()[0]
sh(f"xdotool windowsize {wid} 1600 900 windowmove {wid} 0 0"); time.sleep(6)
def open_scripting():
    sh("xdotool mousemove 250 9 click 1"); time.sleep(2)
    sh("xdotool mousemove 268 113 click 1"); time.sleep(2)
open_scripting()
w=words("m_sub",20,(200,60,1100,400)); print("SUBMENU:",w,flush=True)
tgt=[x for x in w if x[0].lower()=="new"]
if tgt:
    t=tgt[0]; sh(f"xdotool mousemove {t[1]+t[3]//2} {t[2]+t[4]//2} click 1"); time.sleep(4)
dump("m_new_dialog"); print("NEWDLG:",words("m_new_w",20),flush=True)
sh("xdotool key Escape"); time.sleep(1)
open_scripting()
tgt=[x for x in words("m_sub2",20,(200,60,1100,400)) if x[0].lower()=="configure"]
if tgt:
    t=tgt[0]; sh(f"xdotool mousemove {t[1]+t[3]//2} {t[2]+t[4]//2} click 1"); time.sleep(4)
dump("m_cfg_dialog"); print("CFGDLG:",words("m_cfg_w",20),flush=True)
