#!/usr/bin/python

from __future__ import division, print_function
import numpy as np

def Find(string, looking_for):
    if looking_for in string:
        return 1
    else:
        return -1

def ReadFile(filename):
    data = []
    infile = open(filename, "r")

    lines = [line.strip() for line in infile.readlines()]

    for line in lines:
        data.append(line.split())

    infile.close()
    return data

filename = "pdb_entry_type.txt"
final_lines = "pdb_proteins.dat"
final_file = "pdb_proteins.txt"
protein_data = ReadFile(filename)
final = []

for data in protein_data:
    if Find(data[1], "prot") == 1:
        if Find(data[1], "nuc") == -1:
            final.append(data[0])

outfile = open(final_file, "w")

outfile.write("[")

for i in xrange(0, len(final)):
    if i < len(final) - 1:
        outfile.write(final[i] + " ")
    else:
        outfile.write(final[i] + "]")

outfile.close()

outfile = open(final_lines, "w")

for data in final:
    outfile.write(data + "\n")

outfile.close()
