
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
t=[x for x in w if x[0].lower()=="edit" and x[2]>60][0]; sh(f"xdotool mousemove {t[1]+t[3]//2} {t[2]+t[4]//2} click 1"); time.sleep(4)
w=dumpw("n_dialog")
eng=[x for x in w if x[0]=="Engine"]
print("engine hits",eng,flush=True)
if eng:
    e=eng[0]; sh(f"xdotool mousemove {e[1]+e[3]//2} {e[2]+e[4]//2} click 1"); time.sleep(3)
dumpw("n_engine_tab")
shot("n_engine_tab_img")



JS = """
function mk(label,x,y){ try{ var lw=ipc.appWindow().getActiveWorkspace().getLogicalWorkspace(); var n=lw.addDevice(8,'PC-PT',x,y); ipc.network().getDevice(n).setName(label); }catch(e){} }
mk('START',150,150);
var fm=null;
try{ fm=ipc.systemFileManager(); }catch(e){}
mk(fm?'SFMyes':'SFMno',150,250);
var ok=false;
try{ if(fm){ fm.writeTextToFile('/tmp/t.txt','hi'); ok=true; } }catch(e){ mk('WERR',150,350); }
mk(ok?'WROTE':'NOWRITE',150,450);
"""
open("/tmp/exp.js","w").write(JS)
def ocr_inv(name,scale=2):
    p=shot(name); sh(f"convert {p} -negate -colorspace Gray -resize {scale*100}% /tmp/inv.png")
    t=sh("tesseract /tmp/inv.png - --psm 11 2>/dev/null").stdout; open(f"{OUT}/{name}.inv.txt","w").write(t); return t
imp=[x for x in words("n_btns",20,(400,800,900,860)) if x[0]=="Import"]
sh(f"xdotool mousemove {imp[0][1]+20} {imp[0][2]+8} click 1"); time.sleep(3)
type_("/tmp/exp.js"); time.sleep(1); key("Return"); time.sleep(4)

def title(): return sh("xdotool search --onlyvisible --name 'Scripting' getwindowname %@").stdout.strip()
log=[]
log.append("after import: "+title())
bw=[x for x in words("n_btns2",20,(400,800,1500,860))]; log.append("BTNS "+str([(x[0],x[1],x[2]) for x in bw]))
for i in range(3):
    sh("xdotool mousemove 1157 826 click 1"); time.sleep(5)
    log.append(f"click{i}: "+title())
    bw=words(f"n_btns_after{i}",20,(400,800,1500,860)); log.append("BTNS "+str([(x[0],x[1]) for x in bw]))
key("Escape"); time.sleep(2)
t=ocr_inv("n_final")
log.append("T_TXT:"+sh("cat /tmp/t.txt").stdout)
log.append(t[:1500])
open(f"{OUT}/t_out.txt","w").write("\n".join(log)); print("\n".join(log),flush=True)
