
import sys, json, subprocess; sys.path.insert(0,"tools")
from ptlogin import *
sh("sudo apt-get install -y -qq xclip >/dev/null 2>&1")
def dumpw(name,minconf=20):
    w=words(name,minconf); json.dump(w,open(f"{OUT}/{name}.json","w")); print(name,len(w),flush=True); return w
def paste(text):
    subprocess.run(["xclip","-selection","clipboard"],input=text.encode()); time.sleep(0.5); sh("xdotool key ctrl+v"); time.sleep(1)
ok=pt_login(); print("login ok:",ok,flush=True)
wid=sh("xdotool search --onlyvisible --name 'Cisco Packet Tracer'").stdout.split()[0]
sh(f"xdotool windowsize {wid} 1600 900 windowmove {wid} 0 0"); time.sleep(6)

import json
res={}
for y in (795,835):
    for x in (18,52,86,120,154,188):
        sh(f"xdotool mousemove {x} {y} click 1"); time.sleep(1.5)
        w=words(f"p_{x}_{y}",15,(190,760,760,900))
        res[f"{x},{y}"]=" ".join(t[0] for t in w)
        print(x,y,res[f"{x},{y}"],flush=True)
open(f"{OUT}/t_out.txt","w").write(json.dumps(res))
