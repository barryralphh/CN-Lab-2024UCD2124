
import time, sys, os, re
sys.path.insert(0,"tools")
from ptgui import *
from playwright.sync_api import sync_playwright
U=os.environ["NETACAD_USER"]; P=os.environ["NETACAD_PASS"]
def clean(t): return t.replace(U,"<user>").replace(P,"***")
def pt_login():
    time.sleep(40)
    if not click_text(r"No"): sh("xdotool mousemove 997 437 click 1")
    time.sleep(20)
    sh("xdotool mousemove 792 360 click 1")
    url=None
    for _ in range(30):
        time.sleep(2)
        if os.path.exists("/tmp/auth_url.txt"):
            url=open("/tmp/auth_url.txt").read().strip().splitlines()[0]; break
    if not url: print("no auth url"); return False
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True,args=["--no-sandbox"]); pg=b.new_context().new_page()
        pg.goto(url,wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(4000)
        pg.locator("input[name=username]").first.fill(U)
        pg.get_by_role("button",name=re.compile("Login",re.I)).first.click(); pg.wait_for_timeout(4000)
        pg.locator("input[type=password]").first.fill(P)
        pg.get_by_role("button",name=re.compile("Login",re.I)).first.click(); pg.wait_for_timeout(12000)
        print("login result:",pg.inner_text("body")[:80].replace("\n"," "),flush=True); b.close()
    time.sleep(15); return True
def words(name,minconf=30,region=None):
    p=shot(name); out=[]
    for x in ocr(p,2):
        if float(x["conf"])<minconf: continue
        l,t,w,h=int(x["left"]),int(x["top"]),int(x["width"]),int(x["height"])
        if region and not (region[0]<=l<=region[2] and region[1]<=t<=region[3]): continue
        out.append((x["text"],l,t,w,h))
    return out
