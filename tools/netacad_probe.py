
import os, re, sys, time
from playwright.sync_api import sync_playwright
U=os.environ["NETACAD_USER"]; P=os.environ["NETACAD_PASS"]
def log(*a):
    s=" ".join(str(x) for x in a).replace(P,"***").replace(U,"<user>"); print(s,flush=True)
def snap(pg,tag):
    try:
        t=pg.inner_text("body")[:600].replace("\n"," | ")
    except Exception as e: t=str(e)
    log(f"[{tag}] url={pg.url.split('?')[0]} title={pg.title()!r}"); log("   text:",t)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--no-sandbox"])
    ctx=b.new_context(accept_downloads=True,viewport={"width":1366,"height":900})
    pg=ctx.new_page()
    pg.goto("https://www.netacad.com/login",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(6000); snap(pg,"login")
    # email step
    for sel in ['input[type=email]','input[name=email]','input[name=username]','input[id*=mail i]','input[type=text]']:
        if pg.locator(sel).count():
            pg.locator(sel).first.fill(U); log("filled email via",sel); break
    for name in ["Next","Continue","Sign in","Log in","Login"]:
        btn=pg.get_by_role("button",name=re.compile(name,re.I))
        if btn.count(): btn.first.click(); log("clicked",name); break
    pg.wait_for_timeout(6000); snap(pg,"after-email")
    if pg.locator('input[type=password]').count():
        pg.locator('input[type=password]').first.fill(P)
        for name in ["Sign in","Log in","Login","Next","Continue","Submit"]:
            btn=pg.get_by_role("button",name=re.compile(name,re.I))
            if btn.count(): btn.first.click(); log("clicked",name); break
        pg.wait_for_timeout(10000); snap(pg,"after-password")
    pg.goto("https://www.netacad.com/resources/lab-downloads?courseLang=en-US",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(8000); snap(pg,"lab-downloads")
    links=pg.eval_on_selector_all("a,button","els=>els.map(e=>(e.innerText||'').trim()+' -> '+(e.href||'')).filter(t=>/packet|tracer|ubuntu|linux|download/i.test(t))")
    for l in links[:40]: log("LINK:",l[:200])
    b.close()
