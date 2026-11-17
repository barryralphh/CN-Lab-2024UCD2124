
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
click(18,795,2); w=strip_all("F_r"); r=find(w,r"1941")
for (X,Y) in ((450,300),(450,520)): drag(r[0][1]+10,r[0][2]+5,X,Y)
note("WS: "+" ".join(t[0] for t in ws_words("F_ws")))
base=dark(450,345,450,480); note(f"dark before {base}")
for cx in (215,255,295,335,375,415):
    click(120,795,2); click(cx,795,1)
    click(450,300,2); w=ws_words(f"F_menu{cx}"); note(f"F cand {cx} after click A: "+" ".join(t[0] for t in w)[:200])
    click(450,520,2)
    d=dark(450,345,450,480); note(f"F cand {cx} dark {d}")
    if d>0.5: break
