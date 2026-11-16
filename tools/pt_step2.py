
import time, sys, os
sys.path.insert(0,"tools")
from ptgui import *
U=os.environ["NETACAD_USER"]; P=os.environ["NETACAD_PASS"]
time.sleep(40)
click_text(r"No"); time.sleep(20)
dump("s2_login_window")
click_text(r"LOGIN",name="tmp"); time.sleep(20)
dump("s3_after_login_click")
type_(U); key("Return"); time.sleep(8)
dump("s4_after_email")
type_(P); key("Return"); time.sleep(25)
p=shot("s5_after_password"); t=text_of(p); print("[s5]",t[:600].replace(U,"<user>"),flush=True)
open("ptprobe/s5_after_password.txt","w").write(t.replace(U,"<user>"))
