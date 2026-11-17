
import sys, os, json, time, subprocess
sys.path.insert(0,"tools")
os.environ["PTOUT"]=os.environ.get("PTOUT","pt_out/"+os.path.basename(sys.argv[0]).replace(".py",""))
from ptlogin import *
def start():
    ok=pt_login(); print("login ok:",ok,flush=True)
    wid=sh("xdotool search --onlyvisible --name 'Cisco Packet Tracer'").stdout.split()[0]
    sh(f"xdotool windowsize {wid} 1600 900 windowmove {wid} 0 0"); time.sleep(6)
def click(x,y,wait=1.5): sh(f"xdotool mousemove {x} {y} click 1"); time.sleep(wait)
def dclick(x,y,wait=3): sh(f"xdotool mousemove {x} {y} click --repeat 2 --delay 120 1"); time.sleep(wait)
def drag(x1,y1,x2,y2):
    sh(f"xdotool mousemove {x1} {y1} mousedown 1"); time.sleep(0.4)
    for i in range(1,11):
        sh(f"xdotool mousemove {x1+(x2-x1)*i//10} {y1+(y2-y1)*i//10}"); time.sleep(0.08)
    sh("xdotool mouseup 1"); time.sleep(1.5)
def strip(name,minconf=15): return words(name,minconf,(190,760,760,900))
def find(ws,pat):
    import re
    return [w for w in ws if re.fullmatch(pat,w[0],re.I)]
def ws_words(name,minconf=20): return words(name,minconf,(150,110,1450,740))
def note(s):
    print(s,flush=True); open(f"{OUT}/notes.txt","a").write(s+"\n")

def dark(x1,y1,x2,y2,n=60):
    from PIL import Image
    p=shot("dark_tmp"); im=Image.open(p).convert("L"); c=0
    for i in range(n+1):
        x=x1+(x2-x1)*i//n; y=y1+(y2-y1)*i//n
        if im.getpixel((x,y))<200: c+=1
    return c/(n+1)
def strip_all(name,minconf=10): return words(name,minconf,(190,770,760,860))

def dark(x1,y1,x2,y2,n=0):
    p=shot("dark_tmp"); x=min(x1,x2); w=abs(x2-x1)+3; y=min(y1,y2); h=abs(y2-y1)+3
    r=sh(f"convert {p} -colorspace Gray -crop {w}x{h}+{x-1}+{y-1} +repage -format %[fx:mean] info:")
    try: return float(r.stdout.strip())
    except: return -1
def place(kind,X,Y):
    # kind: router1941, switch2960, pc, laptop, server
    if kind=="router1941": click(18,795,2); drag(425,812,X,Y)
    elif kind=="switch2960": click(154,795,2); drag(424,812,X,Y)
    elif kind=="pc": click(52,795,2); drag(255,795,X,Y)
    elif kind=="laptop": click(52,795,2); drag(295,795,X,Y)
    elif kind=="server": click(52,795,2); drag(335,795,X,Y)

def wins():
    out=sh("for w in $(xdotool search --onlyvisible --name .); do echo $w:$(xdotool getwindowname $w); done").stdout.strip().splitlines()
    return [tuple(l.split(":",1)) for l in out]
def devwins(): return [w for w in wins() if w[1] not in ("Cisco Packet Tracer",) and not w[1].startswith("Scripting")]
def cable(a,b):
    click(120,795,1); click(255,795,1); click(a[0],a[1],1.5); click(b[0],b[1],2.5)
def close_all():
    for i,n in devwins():
        sh(f"xdotool key --window {i} Escape"); time.sleep(0.5)
    left=devwins()
    if left: note("still open after Escape: "+str(left))
    for i,n in devwins():
        sh(f"xdotool windowunmap {i}")
    time.sleep(1)
def setf(x,y,text):
    click(x,y,0.5); key("ctrl+a"); type_(text); time.sleep(0.5)
def pc_ip(pos,ip,mask,gw,tag):
    dclick(pos[0],pos[1],4); click(604,129,2); click(505,250,3)
    click(717,245,1); setf(790,275,ip); setf(790,303,mask)
    if gw: setf(790,331,gw)
    click(1000,250,1); time.sleep(1); shot(f"{tag}_ipconfig")
    note(f"{tag}: "+" ".join(t[0] for t in words(f"{tag}_ipw",15,(460,170,1100,520)))[:200])
def cmd(pos,cmds,tag):
    dclick(pos[0],pos[1],4); click(604,129,2)
    click(905,255,3)
    for c in cmds:
        type_(c); key("Return"); time.sleep(4 if c.startswith("ping") or c.startswith("tracert") else 1.5)
    shot(f"{tag}_cmd"); note(f"{tag} cmd: "+" ".join(t[0] for t in words(f"{tag}_cmdw",15,(460,170,1100,760)))[:500])
def cli(pos,cmds,tag,wait=1.2):
    dclick(pos[0],pos[1],4); click(595,129,3); click(800,450,1); key("Return"); time.sleep(2)
    for c in cmds:
        type_(c); key("Return"); time.sleep(wait)
    time.sleep(1); shot(f"{tag}_cli"); note(f"{tag} cli: "+" ".join(t[0] for t in words(f"{tag}_cliw",15,(460,170,1100,760)))[-500:])

# ---- v2 helpers: never close windows; devices live in x<440 or x>1120 so windows (x470-1100) never cover them
def ocr_txt(name,region=(460,170,1100,760),minconf=15):
    return " ".join(t[0] for t in words(name,minconf,region))
def raise_dev(pos,wait=3): dclick(pos[0],pos[1],wait)
def to_home(tag):
    for attempt,cand in enumerate([None,(1085,152),(1090,162),(1075,172),(1095,185),(1060,160)]):
        if cand: click(cand[0],cand[1],2)
        click(604,129,2)
        t=ocr_txt(f"{tag}_home{attempt}")
        if "Command" in t and "Prompt" in t:
            note(f"{tag}: home reached on attempt {attempt}"); return True
    note(f"{tag}: could NOT reach Desktop home"); return False
def pc_ip2(pos,ip,mask,gw,tag):
    raise_dev(pos,4); click(604,129,2); click(505,250,3)
    click(717,245,1); setf(790,275,ip); setf(790,303,mask)
    if gw: setf(790,331,gw)
    click(790,420,1); time.sleep(1); shot(f"{tag}_ipconfig"); note(f"{tag} ip: "+ocr_txt(f"{tag}_ipw")[:160])
def pc_dhcp(pos,tag):
    raise_dev(pos,4); click(604,129,2); click(505,250,3); click(701,246,1); time.sleep(10)
    shot(f"{tag}_dhcp"); note(f"{tag} dhcp: "+ocr_txt(f"{tag}_dhcpw")[:200])
def cmd2(pos,cmds,tag):
    raise_dev(pos,4)
    if not to_home(tag): return
    click(905,255,3)
    for c in cmds:
        type_(c); key("Return"); time.sleep(6 if c.startswith(("ping","tracert")) else 2)
    time.sleep(2); shot(f"{tag}_cmd"); note(f"{tag} cmd: "+ocr_txt(f"{tag}_cmdw")[-400:])
def cli2(pos,cmds,tag,wait=1.5,prompt_wait=True):
    raise_dev(pos,4); click(595,129,3); click(800,450,1); key("Return"); time.sleep(2)
    t=ocr_txt(f"{tag}_boot")
    if "initial configuration dialog" in t:
        type_("no"); key("Return"); time.sleep(6)
    for k in range(6):
        t=ocr_txt(f"{tag}_p{k}")
        if "--More--" in t[-40:]: key("space"); time.sleep(1)
        elif t.rstrip().endswith((">","#")): break
        else: key("Return"); time.sleep(2)
    for c in cmds:
        type_(c); key("Return"); time.sleep(wait)
        if c.startswith("show"):
            time.sleep(1.5)
            if "--More--" in ocr_txt(f"{tag}_m",15)[-40:]: key("space"); time.sleep(1)
    time.sleep(1.5); shot(f"{tag}_cli"); note(f"{tag} cli: "+ocr_txt(f"{tag}_cliw")[-500:])
def cabling_wait(tag,sec=45):
    time.sleep(sec); shot(f"{tag}_topology")

# ---- device layout (v2.1): left col x<440, right col x>1120 so device windows (x470-1100) never cover them
L0=(220,300); L1=(220,440); L2=(220,580)
R0=(380,300); R1=(1250,440); R2=(1250,600)
