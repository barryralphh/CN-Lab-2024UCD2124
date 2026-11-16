
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
var out=[];
try{
 var lw=ipc.appWindow().getActiveWorkspace().getLogicalWorkspace();
 var n=lw.addDevice(8,'PC-PT',200,200);
 out.push('added '+n);
}catch(e){ out.push('ERR '+e); }
try{ ipc.systemFileManager().writeTextToFile('/tmp/t.txt', out.join('\\n')); }catch(e){}
"""
open("/tmp/exp.js","w").write(JS)
def ocr_inv(name,scale=3):
    p=shot(name); sh(f"convert {p} -negate -colorspace Gray -resize {scale*100}% /tmp/inv.png")
    t=sh("tesseract /tmp/inv.png - --psm 6 2>/dev/null").stdout; open(f"{OUT}/{name}.inv.txt","w").write(t); return t
imp=[x for x in words("n_btns",20,(400,800,900,860)) if x[0]=="Import"]
print("import hits",imp,flush=True)
sh(f"xdotool mousemove {imp[0][1]+20} {imp[0][2]+8} click 1"); time.sleep(3)
print("DLG:",ocr_inv("n_import_dlg")[:600],flush=True)
type_("/tmp/exp.js"); time.sleep(1); key("Return"); time.sleep(4)
print("AFTER IMPORT:",ocr_inv("n_after_import")[:600],flush=True)
sh("xdotool mousemove 1157 826 click 1"); time.sleep(8)
print("AFTER START:",ocr_inv("n_after_start")[:600],flush=True)
sh("cp /tmp/t.txt %s/t_out.txt" % OUT)
print(sh("cat /tmp/t.txt").stdout, flush=True)
