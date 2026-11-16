
import sys; sys.path.insert(0,"tools")
from ptlogin import *
import glob
ok=pt_login()
print("windows:",[sh(f"xdotool getwindowname {w}").stdout.strip() for w in sh("xdotool search --onlyvisible --name .").stdout.split()],flush=True)
print("MENUBAR:",words("m0",20,(0,0,1600,60)),flush=True)
print("TOOLBAR/ALL:",[w for w in words("m0b",40)][:80],flush=True)
