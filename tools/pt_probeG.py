
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
place("router1941",450,300); place("router1941",450,520)
note("WS: "+" ".join(t[0] for t in ws_words("G_ws")))
base=dark(450,345,450,480); note(f"mean before {base}")
for cx in (215,255,295,335,375,415):
    click(120,795,2); click(cx,795,1)
    click(450,300,2); note(f"cand {cx} after click A: "+" ".join(t[0] for t in ws_words(f"G_menu{cx}"))[:250])
    click(450,520,2)
    d=dark(450,345,450,480); note(f"cand {cx} mean {d}")
    if base>0 and d<base-0.02: note("CABLE DETECTED"); break
