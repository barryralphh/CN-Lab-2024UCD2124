
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
click(52,795)
for x in (18,52,86,120,154,188):
    click(x,835); w=strip(f"B_sub_{x}"); note(f"B sub {x}: "+" ".join(t[0] for t in w))
click(18,835); w=strip("B_ends"); r=find(w,r"PC|Generic")
note("pc hits "+str(r))
if r: drag(r[0][1]+10,r[0][2]+5,500,400)
ww=ws_words("B_ws"); note("WS: "+" ".join(t[0] for t in ww))
