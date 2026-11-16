#!/bin/bash
n=$1
bash exp$n/run.sh
bash tools/save.sh "exp$n: real xterm + Wireshark screenshots"
