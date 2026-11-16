
import os, re, sys
from playwright.sync_api import sync_playwright
U=os.environ["NETACAD_USER"]; P=os.environ["NETACAD_PASS"]
def log(*a):
    print(" ".join(str(x) for x in a).replace(P,"***").replace(U,"<user>"),flush=True)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--no-sandbox"])
    ctx=b.new_context(accept_downloads=True,viewport={"width":1366,"height":900})
    pg=ctx.new_page()
    pg.goto("https://www.netacad.com/login",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(5000)
    pg.locator('input[name=username]').first.fill(U)
    pg.get_by_role("button",name=re.compile("Login",re.I)).first.click(); pg.wait_for_timeout(5000)
    pg.locator('input[type=password]').first.fill(P)
    pg.get_by_role("button",name=re.compile("Login",re.I)).first.click(); pg.wait_for_timeout(10000)
    pg.goto("https://www.netacad.com/resources/lab-downloads?courseLang=en-US",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(8000)
    link=pg.get_by_text(re.compile(r"Packet Tracer 9\.0\.1 Ubuntu 64bit"))
    log("matches:",link.count())
    got=None
    try:
        with pg.expect_download(timeout=40000) as di:
            link.first.click()
        got=di.value
    except Exception as e:
        log("no direct download:",str(e)[:120])
        try: log("page text:",pg.inner_text("body")[-800:].replace("\n"," | "))
        except Exception: pass
        for name in ["Download","Accept","I agree","Agree","Continue","OK"]:
            btn=pg.get_by_role("button",name=re.compile(name,re.I))
            if btn.count():
                try:
                    with pg.expect_download(timeout=60000) as di: btn.first.click()
                    got=di.value; log("download after clicking",name); break
                except Exception as e2: log("click",name,"no dl:",str(e2)[:80])
    if got:
        got.save_as("/tmp/pt.deb"); log("saved",got.suggested_filename,os.path.getsize("/tmp/pt.deb"))
    else:
        sys.exit("download failed")
    b.close()
