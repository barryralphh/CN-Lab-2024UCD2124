
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
place("pc",450,300); place("pc",450,520)
note("WS: "+" ".join(t[0] for t in ws_words("J_ws")))
base=dark(450,345,450,480); note(f"mean before {base}")
for cx in (255,295,335,375):
    click(120,795,2); click(cx,795,1)
    click(450,300,2); click(450,520,3)
    t=" ".join(x[0] for x in ws_words(f"J_after{cx}"))
    opened="Physical" in t and "Config" in t
    d=dark(450,345,450,480); note(f"cand {cx} mean {d} window_opened={opened} txt={t[:160]}")
    if opened: break
    if base>0 and d<base-0.01: note("CABLE DETECTED at "+str(cx)); break
