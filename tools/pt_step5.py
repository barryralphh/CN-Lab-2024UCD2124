
import time, sys, os
sys.path.insert(0,"tools")
from ptgui import *
time.sleep(40)
click_text(r"No"); time.sleep(20)
sh("xdotool mousemove 792 360 click 1"); time.sleep(25)
def wins():
    out=sh("xdotool search --onlyvisible --name .").stdout.split()
    res=[]
    for w in out:
        n=sh(f"xdotool getwindowname {w}").stdout.strip(); g=sh(f"xdotool getwindowgeometry {w}").stdout.replace("\n"," ")
        res.append((w,n,g))
    return res
for w in wins(): print(w,flush=True)
tos=sh("xdotool search --name 'Additional Terms'").stdout.split()
print("tos ids",tos,flush=True)
for w in tos:
    sh(f"xdotool windowminimize {w}")
time.sleep(5)
dump("s5_after_tos_min")
for w in wins(): print(w,flush=True)
