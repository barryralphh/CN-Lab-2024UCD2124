
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
place("pc",700,400)
dclick(700,400,5)
click(604,129,3)
click(505,250,3)
w=words("L_ip",15); note("L ip: "+str([(t[0],t[1],t[2]) for t in w if t[2]>140 and t[2]<700])[:1800])
