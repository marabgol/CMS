#!/bin/bash

hostname=$1

rm -rf $1-glidein*
echo  $1-glidein*

python3.7 json_analyze32.py $1
python3.7 plot0.py $1

echo "$1-sum.txt"


