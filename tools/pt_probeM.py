
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
place("pc",450,520); place("pc",950,520)
dclick(450,520,4); note("M1 open pc0: "+str(devwins()))
click(604,129,2)
ids=[i for i,n in devwins()]
for i in ids: sh(f"xdotool key --window {i} Escape")
time.sleep(1.5); note("M2 after Escape: "+str(devwins()))
dclick(950,520,4); note("M3 dclick pc1: "+str(devwins()))
if not devwins():
    click(950,520,1); dclick(950,520,4); note("M4 retry: "+str(devwins()))
if not devwins():
    key("Escape"); click(800,650,1); dclick(950,520,4); note("M5 after deselect: "+str(devwins()))
note("M6 ws: "+" ".join(t[0] for t in ws_words("M_ws")))
