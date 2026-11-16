
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
sh("xdotool key ctrl+a"); sh("xdotool key BackSpace")
JS = """
var out=[];
try{
 var lw=ipc.appWindow().getActiveWorkspace().getLogicalWorkspace();
 var n=lw.addDevice(8,'PC-PT',200,200);
 out.push('added '+n);
 var d=ipc.network().getDevice(n);
 out.push('model '+d.getModel()+' type '+d.getType());
}catch(e){ out.push('ERR '+e); }
try{ ipc.systemFileManager().writeTextToFile('/tmp/t.txt', out.join('\\n')); }catch(e){ out.push('WERR '+e); }
dprint(out.join('\\n'));
"""
paste(JS)
shot("n_pasted_img"); dumpw("n_pasted_w")
sh("xdotool mousemove 1157 826 click 1"); time.sleep(8)
shot("n_started_img"); dumpw("n_started_w")
sh("cp /tmp/t.txt %s/t_out.txt" % OUT)
print(sh("cat /tmp/t.txt").stdout, flush=True)
