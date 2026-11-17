
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
place("router1941",700,400)
dclick(700,400,5)
w=words("H_win",15); note("H win: "+str([(t[0],t[1],t[2]) for t in w if t[2]<400])[:1500])
cli=find(w,r"CLI")
note("CLI hits "+str(cli))
if cli: click(cli[0][1]+10,cli[0][2]+5,3)
note("H after CLI: "+" ".join(t[0] for t in words("H_cli",15))[:800])
