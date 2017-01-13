#!/usr/bin/python
from __future__ import print_function, division
import nuclide_data

dataFile = "cleandata.dat"
dataOut = "NuclearData.dat"
PN_list = []
infile = open(dataFile, "r")

lines = [line.strip() for line in infile.readlines()]

lines.pop(0)

for line in lines:
    vector = []
    for column in line.split(","):
        vector.append(column.split()[0])

    PN_list.append([vector[1], vector[2]])

infile.close()
count = 0
nuclear_data = []
for nuclei in PN_list:
    Z = int(nuclei[0])
    N = int(nuclei[1])
    try: 
        nuclide = nuclide_data.nuc(Z,N)
        print(nuclide['weight'])
        nuclear_data.append(nuclide_data.nuc(Z,N))
        print(nuclide_data.nuc(Z, N))
    except KeyError:
        continue

print(len(nuclear_data))
#print(lines)
