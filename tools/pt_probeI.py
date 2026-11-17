
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
place("pc",700,400)
dclick(700,400,5)
w=words("I_win",15); note("I win: "+str([(t[0],t[1],t[2]) for t in w if t[2]<400])[:1500])
d=find(w,r"Desktop")
note("Desktop hits "+str(d))
if d: click(d[0][1]+10,d[0][2]+5,3)
w=words("I_desk",15); note("I desk: "+str([(t[0],t[1],t[2]) for t in w])[:1500])
cp=[t for t in w if t[0].lower().startswith("command")]
note("CP hits "+str(cp))
if cp: click(cp[0][1]+10,cp[0][2]-30,3)
note("I after CP: "+" ".join(t[0] for t in words("I_cp",15))[:800])
