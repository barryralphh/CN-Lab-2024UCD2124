
import time, sys, os
sys.path.insert(0,"tools")
from ptgui import *
U=os.environ["NETACAD_USER"]; P=os.environ["NETACAD_PASS"]
time.sleep(40)
click_text(r"No"); time.sleep(20)
shot("s2_login_window")
sh("xdotool mousemove 792 360 click 1"); time.sleep(25)
dump("s3_after_login_click")
sh("xdotool search --onlyvisible --name . getwindowname %@ > ptprobe/s3_windows.txt")
print(open("ptprobe/s3_windows.txt").read(),flush=True)
