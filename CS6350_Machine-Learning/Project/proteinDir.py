#!/usr/bin/python
'''
Creates all the directories for all the proteins. This downloads the list
of proteins from my website, so you don't even need the file with the list
of proteins to run it.
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
#filename = "pdb_proteins.dat"
#proteins_list = ReadFile(filename)
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
