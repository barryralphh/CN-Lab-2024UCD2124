
import time, sys, os, glob
sys.path.insert(0,"tools")
from ptgui import *
U=os.environ["NETACAD_USER"]; P=os.environ["NETACAD_PASS"]
def clean(t): return t.replace(U,"<user>").replace(P,"***")
time.sleep(40)
click_text(r"No"); time.sleep(20)
sh("xdotool mousemove 792 360 click 1"); time.sleep(25)
for w in sh("xdotool search --name 'Additional Terms'").stdout.split():
    sh(f"xdotool windowmove {w} 4000 4000"); sh(f"xdotool windowunmap {w}")
time.sleep(4)
p=shot("login_a"); rows=ocr(p)
print("[a]"," ".join(x["text"] for x in rows)[:700],flush=True)
for x in rows:
    if float(x["conf"])>40: print(x["text"],x["left"],x["top"],x["width"],x["height"],flush=True)
sh("xdotool mousemove 800 450")
type_(U); key("Return"); time.sleep(8)
p=shot("login_b"); print("[b]",clean(text_of(p))[:500],flush=True)
sh("xdotool mousemove 800 450")
type_(P); key("Return"); time.sleep(30)
p=shot("login_c"); print("[c]",clean(text_of(p))[:700],flush=True)
for w in sh("xdotool search --onlyvisible --name .").stdout.split():
    print("win",sh(f"xdotool getwindowname {w}").stdout.strip(),flush=True)
for f in glob.glob("ptprobe/login_*.png"): os.remove(f)
