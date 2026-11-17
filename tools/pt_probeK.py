
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
place("router1941",700,400)
dclick(700,400,5)
click(595,129,3)
note("K cli tab: "+" ".join(t[0] for t in words("K_cli",15))[:600])
click(800,450,1); key("Return"); time.sleep(3); type_("enable"); key("Return"); time.sleep(1); type_("show ip interface brief"); key("Return"); time.sleep(3)
note("K after cmds: "+" ".join(t[0] for t in words("K_cmds",15))[:900])
wins=sh("for w in $(xdotool search --onlyvisible --name .); do echo $w $(xdotool getwindowname $w); done").stdout
note("K wins: "+wins.replace("\n"," ; "))
