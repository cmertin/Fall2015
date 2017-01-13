#!/usr/bin/python
'''
The files are written in such a way that the spaces count as the following:
1 unused
2-4 N-Z (3)
5-9 N (5)
10-14 Z (5)
15-19 A (5)
20 unused
21-23 element (3)
24-27 origin (4)
28 unused
29-41 mass excess (13)
42-52 mass excess uncert. (11)
53-63 binding energy (11)
64-72 binding energy uncert. (9)
73 unused
74-75 beta decay mode (2)
76-86 beta-decay energy (11)
87-95 beta-decay energy uncert. (9)
96 unused
97-99 A (3)
100 unused
101-112 atomic mass (12)
113-123 atomic mass uncert. (11)

Side note: This is for spaces and in FORTRAN the counting starts at 1
'''
from __future__ import print_function, division
import numpy as np

def ReadFile(dataFile):
    data = []
    infile = open(dataFile, "r")

    lines = [line.strip() for line in infile.readlines()]
    infile.close()
    index = 0

    for i in xrange(0, len(lines)):
        if "1N-Z" in lines[i]:
            break
        else:
            index += 1

    for i in xrange(0, index+2):
        lines.pop(0)

    return lines

def ParseLine(line):
    if str(line[0]) == '0':
        line = line[1:]
    data = []
    data.append(line[0:3].replace(" ","")) # N-Z
    print(line[0:3])
    line = line[3:]
    data.append(line[0:5].replace(" ","")) # N
    line = line[5:]
    data.append(line[0:5].replace(" ","")) # Z
    line = line[5:]
    data.append(line[0:5].replace(" ","")) # A
    line = line[5:]
    line = line[1:] # Character 20 is unused
    data.append(line[0:3].replace(" ","")) # Element
    line = line[3:]
    data.append(line[0:4].replace(" ","")) # Origin
    line = line[4:]
    line = line[1:] # Character 28 is unused
    data.append(line[0:13].replace(" ","")) # Mass Excess (keV)
    line = line[13:]
    data.append(line[0:11].replace(" ","")) # Mass Excess Uncert. (keV)
    line = line[11:]
    data.append(line[0:11].replace(" ","")) # Binding Energy (keV)
    line = line[11:]
    data.append(line[0:9].replace(" ","")) # Binding Energy Uncert. (keV)
    line = line[9:]
    line = line[1:] # Character 73 is unused
    data.append(line[0:2].replace(" ","")) # Beta decay mode
    line = line[2:]
    data.append(line[0:11].replace(" ","")) # Beta Decay Energy (keV)
    line = line[11:]
    data.append(line[0:9].replace(" ","")) # Beta Decay Uncert (keV)
    line = line[9:]
    line = line[1:] # Character 96 is unused
    data.append(line[0:3].replace(" ","")) # A
    line = line[3:]
    line = line[1:] # Character 100 is unused
    data.append(line[0:12].replace(" ","")) # Atomic Mass (u)
    line = line[12:]
    data.append(line[0:11].replace(" ","")) # Atomic Mass Uncert. (u)
    #line = line[11:]
    #data.append(line.replace(" ","")) # Rest of line
   
    return data

    
files = ["mass_exp.mas95"]
files2 = ["mass_exp.mas95", "mass_rmd.mas95", "mass.mas03", "mass.mass03round", "mass.mas12"]
title = "N-Z,N,Z,A,Element,Origin,Mass Excess (keV),Mass Excess Uncert. (keV),Binding Energy (keV),Binding Energy Uncert. (keV),Beta Decay (keV),Beta Decay Uncert. (keV),A,Atomic Mass (u), Atomic Mass Uncert. (u)\n"

for old_file in files:

    data = ReadFile(files[0])
    new_file = old_file + ".clean"
    outfile = open(new_file, "w")
    clean_data = []
    for nuclei in data:
        clean_data.append(ParseLine(nuclei))
    
    outfile.write(title)
    for parsed_data in clean_data:
        for i in xrange(0, len(parsed_data)):
            item = parsed_data[i]
            if item == "":
                item = " "
            if i != len(parsed_data)-1:
                outfile.write(str(item) + ',')
            else:
                outfile.write(str(item) + '\n')
    outfile.close()
    print("Parsed " + old_file + " into " + new_file)
