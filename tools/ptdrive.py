
import sys, os, json, time, subprocess
sys.path.insert(0,"tools")
os.environ["PTOUT"]=os.environ.get("PTOUT","pt_out/"+os.path.basename(sys.argv[0]).replace(".py",""))
from ptlogin import *
def start():
    ok=pt_login(); print("login ok:",ok,flush=True)
    wid=sh("xdotool search --onlyvisible --name 'Cisco Packet Tracer'").stdout.split()[0]
    sh(f"xdotool windowsize {wid} 1600 900 windowmove {wid} 0 0"); time.sleep(6)
def click(x,y,wait=1.5): sh(f"xdotool mousemove {x} {y} click 1"); time.sleep(wait)
def dclick(x,y,wait=3): sh(f"xdotool mousemove {x} {y} click --repeat 2 --delay 120 1"); time.sleep(wait)
def drag(x1,y1,x2,y2):
    sh(f"xdotool mousemove {x1} {y1} mousedown 1"); time.sleep(0.4)
    for i in range(1,11):
        sh(f"xdotool mousemove {x1+(x2-x1)*i//10} {y1+(y2-y1)*i//10}"); time.sleep(0.08)
    sh("xdotool mouseup 1"); time.sleep(1.5)
def strip(name,minconf=15): return words(name,minconf,(190,760,760,900))
def find(ws,pat):
    import re
    return [w for w in ws if re.fullmatch(pat,w[0],re.I)]
def ws_words(name,minconf=20): return words(name,minconf,(150,110,1450,740))
def note(s):
    print(s,flush=True); open(f"{OUT}/notes.txt","a").write(s+"\n")

def dark(x1,y1,x2,y2,n=60):
    from PIL import Image
    p=shot("dark_tmp"); im=Image.open(p).convert("L"); c=0
    for i in range(n+1):
        x=x1+(x2-x1)*i//n; y=y1+(y2-y1)*i//n
        if im.getpixel((x,y))<200: c+=1
    return c/(n+1)
def strip_all(name,minconf=10): return words(name,minconf,(190,770,760,860))
