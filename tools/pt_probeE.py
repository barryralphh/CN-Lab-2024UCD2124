
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
click(52,795,2)
cands=[215,255,295,335,375]
for i,cx in enumerate(cands):
    click(52,795,1); drag(cx,795,350+i*180,300+(i%2)*200)
    note(f"E cand {cx}: WS "+" ".join(t[0] for t in ws_words(f"E_ws{i}")))
