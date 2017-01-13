#!/usr/bin/python

from __future__ import division, print_function
import sys

data = []
datafile = "alldata.dat"
dataout = "cleandata.dat"
infile = open(datafile, "r")
rm_list = []

lines = [line.strip() for line in infile.readlines()]

infile.close()

for i in xrange(0, len(lines)):
    if lines[i].find("\t") == -1:
        rm_list.append(i)

rm_list.reverse()

for index in rm_list:
    lines.pop(index)

for line in lines:
    data.append(line.split())

last = 0

for nuclei in data:
    if str(nuclei[0]) == 'a':
        nuclei[0] = last
    else:
        last = nuclei[0]

outfile = open(dataout,"w")

outfile.write("A,Z,N\n")

for i in xrange(0, len(data)):
    Z = data[i][0]
    N = data[i][1]
    A = int(Z) + int(N)
    str_out = str(A) + "," + str(Z) + "," + str(N) + "\n"
    outfile.write(str_out)

outfile.close()
