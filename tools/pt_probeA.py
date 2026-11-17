
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
click(18,795)
for x in (18,52,86,120,154,188):
    click(x,835); w=strip(f"A_sub_{x}"); note(f"A sub {x}: "+" ".join(t[0] for t in w))
click(18,835); w=strip("A_routers"); r=find(w,r"2911|1941|2901")
note("router hits "+str(r))
if r: drag(r[0][1]+10,r[0][2]+5,700,400)
ww=ws_words("A_ws"); note("WS: "+" ".join(t[0] for t in ww))
