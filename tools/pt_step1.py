
import time, sys
sys.path.insert(0,"tools")
from ptgui import *
time.sleep(40)
dump("s1_startup")
click_text(r"No"); time.sleep(20)
dump("s2_after_multiuser")
sh("xdotool search --onlyvisible --name . getwindowname %@ > ptprobe/s2_windows.txt")
