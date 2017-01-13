#!/usr/bin/python

from __future__ import print_function, division
import urllib2
from os import system

def GetProteinNames(url):
    response = urllib2.urlopen(url)
    lines = response.read()
    protein_list = lines.split()
    return protein_list

protein_url = "http://cs.utah.edu/~cmertin/pdb_proteins.dat"
protein_list = GetProteinNames(protein_url)
jMol_location = "/media/christopher/Proteins/jmol-14.4.0_2015.11.18/Jmol.jar"
jMol_run = "java -jar " + jMol_location + " -x -J "
base_dir = "/media/christopher/Proteins/Protein_Data/"
logfile = base_dir + "protein.log"
index = 1

for protein in protein_list:
    print("On " + protein + ": " + str(index) + "/" + str(len(protein_list)))
    prot_dir = base_dir + protein + "/"
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

    command = jMol_run + "\"" + prot_load + prot_init + top_cmd + top_out + right_cmd + right_out + left_cmd + left_out + bottom_cmd + bottom_out + standard_cmd + standard_out + write_domains + write_amino + "\" > " + logfile

    system(command)
    index += 1
