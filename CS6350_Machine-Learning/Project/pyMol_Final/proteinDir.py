#!/usr/bin/python
'''
Downloads a list of the proteins in the RCSB database and creates a directory
for each of the proteins so that the information for each protein can be 
stored in each directory. This MUST be used before running pyMol.py since
how it stores the data is based on this directory structure.
'''

from __future__ import print_function
import urllib2
import os

def ReadFile(filename):
    data = []
    infile = open(filename, "r")
    
    lines = [line.strip() for line in infile.readlines()]

    for line in lines:
        data.append(line)

    return data
    
url = "http://cs.utah.edu/~cmertin/pdb_proteins.dat"
top_dir = "Protein_Data"

response = urllib2.urlopen(url)
lines = response.read()

protein_list = lines.split()

if not os.path.exists(top_dir):
    os.makedirs(top_dir)

for protein in protein_list:
    path = top_dir + "/" + protein
    if not os.path.exists(path):
        os.makedirs(path)
