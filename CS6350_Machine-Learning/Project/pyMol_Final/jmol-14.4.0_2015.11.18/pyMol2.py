#!/usr/bin/python

from __future__ import print_function, division
from os import system

Jmol_command = "java -jar Jmol.jar -x "
extension = ".pdb"
protein = "101m"
domains_file = protein + "_domains.dat"
amino_file = protein + "_amino.dat"
load_domains = "load " + protein +"/dom; "
directory = "Protein_Data/" + protein + "/"
pdb_file = directory + protein + extension
command_1 = " -J \"cartoon on; color structure; backbone off; wireframe off; spacefill off; ribbon on; "
write_base = "write Image 516 639 JPG "
topview_cmd = "moveto 0 1 0 0 -90; "
topview_out = write_base + "\"" + directory + "topview.jpg" + "\"; "
rightview_cmd = "moveto 0 0 1 0 90; "
rightview_out = write_base  + "\"" + directory + "rightview.jpg" + "\"; "
leftview_cmd = "moveto 0 0 1 0 -90; "
leftview_out = write_base + "\"" + directory + "leftview.jpg" + "\"; "
bottomview_cmd = "moveto 2 1 0 0 90; "
bottomview_out = write_base + "\"" + directory + "bottomview.jpg" + "\"; "
standardview_cmd = "moveto 2 0 0 0 0; "
standardview_out = write_base + "\"" + directory + "standardview.jpg" + "\"; "
domains_cmd = "var dom = script(\"show DOMAINS\"); write var dom " + directory + domains_file + "; "
amino_cmd = "amino=script(\"show SEQUENCE\"); write var amino " + directory + amino_file + "; "

command = Jmol_command + pdb_file + command_1 + topview_cmd + topview_out + rightview_cmd + rightview_out + leftview_cmd + leftview_out + bottomview_cmd + bottomview_out + standardview_cmd + standardview_out + "\""

system(command)
