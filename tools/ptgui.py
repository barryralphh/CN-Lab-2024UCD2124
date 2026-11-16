
import subprocess, os, re, time, csv, io, shutil
OUT=os.environ.get("PTOUT","ptprobe"); os.makedirs(OUT,exist_ok=True)
def sh(c,**k): return subprocess.run(c,shell=True,capture_output=True,text=True,**k)
def shot(name):
    p=f"{OUT}/{name}.png"; sh(f"import -window root {p}"); return p
def ocr(p):
    sh(f"convert {p} -resize 200% -colorspace Gray /tmp/o2.png")
    r=sh("tesseract /tmp/o2.png - --psm 11 tsv 2>/dev/null")
    rows=list(csv.DictReader(io.StringIO(r.stdout),delimiter="\t",quoting=csv.QUOTE_NONE))
    out=[]
    for x in rows:
        if not x.get("text","").strip(): continue
        for k in ("left","top","width","height"): x[k]=str(int(x[k])//2)
        out.append(x)
    return out
def text_of(p): return " ".join(x["text"] for x in ocr(p))
def dump(name):
    p=shot(name); t=text_of(p); open(f"{OUT}/{name}.txt","w").write(t); print(f"[{name}]",t[:700],flush=True); return p
def click_text(pat,occurrence=0,name="tmp"):
    p=shot(name); hits=[x for x in ocr(p) if re.fullmatch(pat,x["text"].strip(),re.I)]
    if len(hits)<=occurrence: print("no hit for",pat,flush=True); return False
    h=hits[occurrence]; x=int(h["left"])+int(h["width"])//2; y=int(h["top"])+int(h["height"])//2
    sh(f"xdotool mousemove {x} {y} click 1"); print("clicked",pat,x,y,flush=True); return True
def key(k): sh(f"xdotool key {k}")
def type_(s): subprocess.run(['xdotool','type','--delay','60','--',s])
