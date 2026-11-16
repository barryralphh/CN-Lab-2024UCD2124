
import time, sys, os, glob, re
sys.path.insert(0,"tools")
from ptgui import *
from playwright.sync_api import sync_playwright
U=os.environ["NETACAD_USER"]; P=os.environ["NETACAD_PASS"]
def clean(t): return t.replace(U,"<user>").replace(P,"***")
time.sleep(40)
click_text(r"No"); time.sleep(20)
sh("xdotool mousemove 792 360 click 1")
url=None
for _ in range(30):
    time.sleep(2)
    if os.path.exists("/tmp/auth_url.txt"):
        url=open("/tmp/auth_url.txt").read().strip().splitlines()[0]; break
print("auth url captured:",bool(url),flush=True)
if url:
    print("URL:",re.sub(r"(code_challenge|state|nonce)=[^&]+",r"\1=…",url)[:500],flush=True)
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True,args=["--no-sandbox"]); pg=b.new_context().new_page()
        try:
            pg.goto(url,wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(5000)
            print("page:",clean(pg.url.split("?")[0]),flush=True)
            pg.locator("input[name=username]").first.fill(U)
            pg.get_by_role("button",name=re.compile("Login",re.I)).first.click(); pg.wait_for_timeout(5000)
            pg.locator("input[type=password]").first.fill(P)
            pg.get_by_role("button",name=re.compile("Login",re.I)).first.click(); pg.wait_for_timeout(15000)
            print("final:",clean(pg.url.split("?")[0]),flush=True)
            print("text:",clean(pg.inner_text("body")[:300].replace("\n"," | ")),flush=True)
        except Exception as ex:
            print("playwright err:",clean(str(ex))[:300],flush=True)
        b.close()
time.sleep(15)
p=shot("login_d"); print("[PT]",clean(text_of(p))[:600],flush=True)
for w in sh("xdotool search --onlyvisible --name .").stdout.split():
    print("win",sh(f"xdotool getwindowname {w}").stdout.strip(),flush=True)
for f in glob.glob("ptprobe/login_*.png"): os.remove(f)
