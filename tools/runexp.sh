#!/bin/bash
n=$1
bash exp$n/run.sh
python3 tools/render.py exp$n/out
bash tools/save.sh "exp$n: results + screenshots"
