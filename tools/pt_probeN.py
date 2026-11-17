
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
place("router1941",700,400)
dclick(700,400,5); click(595,129,3); click(800,450,1); key("Return"); time.sleep(2)
type_("no"); key("Return"); time.sleep(8); key("Return"); time.sleep(2)
type_("enable"); key("Return"); time.sleep(1); type_("show version"); key("Return"); time.sleep(3)
note("N0 cli: "+" ".join(t[0] for t in words("N_cli",15,(460,170,1100,760)))[-300:])
def alive(): return [w for w in devwins()]
note("N1 open: "+str(alive()))
for name,cmd in [("esc_window","xdotool key --window {i} Escape"),("ctrl_w","xdotool key --window {i} ctrl+w"),("alt_f4","xdotool key --window {i} alt+F4"),("unmap","xdotool windowunmap {i}"),("close","xdotool windowclose {i}")]:
    ids=[i for i,n in alive()]
    if not ids: break
    for i in ids: sh(cmd.format(i=i))
    time.sleep(2); note(f"N {name}: {alive()}")
dclick(700,400,4); note("N reopen: "+str(alive()))
