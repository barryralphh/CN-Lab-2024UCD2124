
import sys, json, subprocess; sys.path.insert(0,"tools")
from ptlogin import *
sh("sudo apt-get install -y -qq xclip >/dev/null 2>&1")
def dumpw(name,minconf=20):
    w=words(name,minconf); json.dump(w,open(f"{OUT}/{name}.json","w")); print(name,len(w),flush=True); return w
def paste(text):
    subprocess.run(["xclip","-selection","clipboard"],input=text.encode()); time.sleep(0.5); sh("xdotool key ctrl+v"); time.sleep(1)
ok=pt_login(); print("login ok:",ok,flush=True)
wid=sh("xdotool search --onlyvisible --name 'Cisco Packet Tracer'").stdout.split()[0]
sh(f"xdotool windowsize {wid} 1600 900 windowmove {wid} 0 0"); time.sleep(6)
sh("xdotool mousemove 250 9 click 1"); time.sleep(2)
sh("xdotool mousemove 268 113 click 1"); time.sleep(2)
w=words("n_sub",20,(200,60,1100,400))
t=[x for x in w if x[0].lower()=="new"][0]; sh(f"xdotool mousemove {t[1]+t[3]//2} {t[2]+t[4]//2} click 1"); time.sleep(4)
w=dumpw("n_dialog")
eng=[x for x in w if x[0]=="Engine"]
print("engine hits",eng,flush=True)
if eng:
    e=eng[0]; sh(f"xdotool mousemove {e[1]+e[3]//2} {e[2]+e[4]//2} click 1"); time.sleep(3)
dumpw("n_engine_tab")
shot("n_engine_tab_img")
sh("xdotool mousemove 800 450 click 1"); time.sleep(1)
sh("xdotool key ctrl+a"); paste("var lw=ipc.appWindow().getActiveWorkspace().getLogicalWorkspace();\nvar n=lw.addDevice(8,'PC-PT',200,200);\nipc.systemFileManager().writeTextToFile('/tmp/t.txt','hello '+n);\n")
shot("n_pasted")
dumpw("n_pasted_w")
