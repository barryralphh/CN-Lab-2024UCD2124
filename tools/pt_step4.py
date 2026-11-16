
import time, sys, os
sys.path.insert(0,"tools")
from ptgui import *
U=os.environ["NETACAD_USER"]; P=os.environ["NETACAD_PASS"]
time.sleep(40)
click_text(r"No"); time.sleep(20)
sh("xdotool mousemove 792 360 click 1"); time.sleep(25)
p=shot("s3"); rows=ocr(p)
for x in rows:
    if float(x["conf"])>20 and x["text"].strip(): print(x["text"],x["left"],x["top"],x["width"],x["height"])
sh("xdotool search --onlyvisible --name . getwindowname %@ > ptprobe/s4_windows.txt"); print(open("ptprobe/s4_windows.txt").read())
# try accept
for pat in [r"Accept\W*",r"Agree\W*",r"Continue\W*",r"OK\W*",r"Next\W*"]:
    if click_text(pat): break
time.sleep(20)
p=shot("s4_after_accept"); rows=ocr(p)
print("[s4]"," ".join(x["text"] for x in rows)[:800],flush=True)
open("ptprobe/s4_after_accept.txt","w").write(" ".join(x["text"] for x in rows))
