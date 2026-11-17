
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
A=(250,300); B=(1250,300); C=(250,620)
place("pc",*A); place("pc",*B); place("pc",*C)
note("O ws: "+" ".join(t[0] for t in ws_words("O_ws")))
dclick(*A,4); note("O1 open A: "+str(devwins()))
dclick(*B,4); note("O2 open B w/o closing A: "+str(devwins()))
dclick(*C,4); note("O3 open C: "+str(devwins()))
for i,n in devwins(): sh(f"xdotool key --window {i} Escape")
time.sleep(1.5); note("O4 after Escape all: "+str(devwins()))
dclick(*A,4); note("O5 reopen A: "+str(devwins()))
mainid=sh("xdotool search --onlyvisible --name 'Cisco Packet Tracer'").stdout.split()[0]
sh(f"xdotool windowfocus {mainid}"); time.sleep(1)
dclick(*B,4); note("O6 B after windowfocus main: "+str(devwins()))
click(800,4,1); key("Escape"); time.sleep(1)
dclick(*C,4); note("O7 C after menu click+Esc: "+str(devwins()))
