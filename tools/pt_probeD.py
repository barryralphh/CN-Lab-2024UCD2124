
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
for cx in (18,52,154):
    click(cx,795,2); w=strip_all(f"D_{cx}"); note(f"D cat {cx}: "+str([(t[0],t[1],t[2]) for t in w]))
click(154,795,2); w=strip_all("D_sw"); r=find(w,r"2960")
note("2960 hits "+str(r))
if r: drag(r[0][1]+10,r[0][2]+5,700,300)
note("WS: "+" ".join(t[0] for t in ws_words("D_ws")))
