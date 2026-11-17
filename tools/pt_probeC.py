
import sys; sys.path.insert(0,"tools")
from ptdrive import *
start()
for cx in (120,154,188):
    click(cx,795); note(f"C cat {cx}: "+" ".join(t[0] for t in strip(f"C_cat_{cx}")))
    for x in (18,52,86,120):
        click(x,835); note(f"C cat {cx} sub {x}: "+" ".join(t[0] for t in strip(f"C_sub_{cx}_{x}")))
