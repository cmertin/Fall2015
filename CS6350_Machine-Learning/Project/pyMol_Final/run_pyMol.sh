#!/bin/bash
# This is a simple run script to run all instances of pyMol for each of the
# 10 different instances on a single machine. Runs each instance in the 
# background with the use of nohup.

for i in `seq 0 9`; do
    nohup python pyMol.py $i &
done
