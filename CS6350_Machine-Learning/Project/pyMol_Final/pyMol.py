#!/usr/bin/python
'''
Author: Christopher Mertin
Date: November 21, 2015
This program is a Python implementation of the software jmol. It isn't a full
implementation as it's more of a "front end" that does everything that jmol
allows you to do. The scripting language provided with jmol is not the most
fun to figure out how to manipulate, and thankfully it comes with a commandline
interface to run the same commands. This program downloads the list of ALL 
proteins from my website and then downloads all the protein information from
the RCSB protein database. It doesn't download the .pdb files and stores them,
it downloads the data files and extracts 4 images of each protein in different
locations and also a file for the domain information and for the amino acids.

I have this setup such that it doens't provide any graphical output to the 
user while running, but because of how jmol is built, this is still going to
need an active terminal for X11 support throughout the whole process. So you
can use "nohup" to put this in the background, but your terminal must stay open
and actively connected to the computer (if you are SSH'd in and running on
another system)
'''

from __future__ import print_function, division
import urllib2
from os import system
import os.path
import sys

# Gets the list of proteins from a given URL, my website was chosen because
# I had already "cleaned" the list into a desirable format for this process
def GetProteinNames(url):
    response = urllib2.urlopen(url)
    lines = response.read()
    protein_list = lines.split()
    return protein_list

# Checks to see if all the files exist in the path before calling jmol again 
# and redoing the whole directory. This is important to cutdown on time if
# you have to rerun this code.
def CheckExists(path, protein):
    topview = os.path.isfile(path + "topview.jpg")
    bottomview = os.path.isfile(path + "bottomview.jpg")
    leftview = os.path.isfile(path + "leftview.jpg")
    rightview = os.path.isfile(path + "rightview.jpg")
    standardview = os.path.isfile(path + "standardview.jpg")
    domains = os.path.isfile(path + str(protein) + "_domains.dat")
    aminos = os.path.isfile(path + str(protein) + "_aminos.dat")

    if topview and bottomview and leftview and rightview and standardview and domains and aminos:
        return True
    else:
        return False

############################################################    
# MAIN START OF THE PROGRAM                                #
############################################################

# URL where the proteins are stored at
protein_url = "http://cs.utah.edu/~cmertin/pdb_proteins.dat"
# Stores the list of proteins from the URL
protein_list = GetProteinNames(protein_url)
# Sets the locaion of jmol so that it's easily transferrable to multiple systems
jMol_location = "/uusoc/scratch/mir/cmertin/Project/jmol-14.4.0_2015.11.18/Jmol.jar"
# Sets the command line command to run jmol
jMol_run = "java -jar " + jMol_location + " -n -i -L -J "
# This is the base directory on where you want the data to be stored
base_dir = "/uusoc/scratch/mir/cmertin/Project/Protein_Data/"
# Number of segments to break the data into. This is helpful in running the 
# Same code multiple times on the same computer to expedite the runtime
segments = 10

# Checks the number of arguments given to the code when it's ran. If no
# additional arguments are given, then it treats one process to run over the
# whole list (bad idea).
if len(sys.argv) == 1:
    min = 0
    max = len(protein_list)
# Otherwise, if one additional argument is given, it breaks it up into that 
# section of segments. For example, segments is at 10, if the code is ran with
# an argument of 0, it will run from the first protein in the list to the 
# protein that is 1/10 of the way through the list.
else:
    min = int(int(sys.argv[1]) * len(protein_list) / segments)
    max = int((int(sys.argv[1]) + 1) * len(protein_list) / segments)

index = min

if min == 0:
    index = 1

# Iterates through all the proteins and calls the necessary jmol commands via
# the command line.
for i in xrange(min, max):
    protein = protein_list[i]
    print("On " + protein + ": " + str(index) + "/" + str(max))
    prot_dir = base_dir + protein + "/"

    if CheckExists(prot_dir, protein) == True:
        index += 1
        continue

    write_base = "write Image 516 639 JPG " + prot_dir

    prot_load = "Load=" + protein + "/dom; "
    prot_init = "cartoon on; color structure; backbone off; wireframe off; spacefill off; ribbon on; "
    top_cmd = "moveto 0 1 0 0 -90; center; "
    top_out = write_base + "topview.jpg; "
    right_cmd = "moveto 0 0 1 0 90; center; "
    right_out = write_base + "rightview.jpg; "
    left_cmd = "moveto 0 0 1 0 -90; center; "
    left_out = write_base + "leftview.jpg; "
    bottom_cmd = "moveto 2 1 0 0 90; center; "
    bottom_out = write_base + "bottomview.jpg; "
    standard_cmd = "moveto 2 0 0 0 0; center; "
    standard_out = write_base + "standardview.jpg; "
    write_domains = "var dom = script(\'show DOMAINS\'); write var dom " + prot_dir + protein + "_domains.dat; "
    write_amino = "var amino = script(\'show SEQUENCE\'); write var amino " + prot_dir + protein + "_aminos.dat; "

    command = jMol_run + "\"" + prot_load + prot_init + top_cmd + top_out + right_cmd + right_out + left_cmd + left_out + bottom_cmd + bottom_out + standard_cmd + standard_out + write_domains + write_amino + "\""

    system(command)
    index += 1
