#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python

import pygraphviz as pgv
# strict (no parallel edges)
# digraph
# with attribute rankdir set to 'LR'
A=pgv.AGraph(directed=True,rankdir="LR")
A.edge_attr["fontsize"] = 8
# add node 1 with color red
A.add_node("Patrons",color="red",label="Patrons")
A.add_node("P_None",label="None",shape="house")
A.add_node("P_Full",label="Full",shape="house")
A.add_node("P_Some", label="Some",shape="house")
A.add_node("Type",label="Type",color="blue")
A.add_node("T_Italian",label="Italian",shape="house")
A.add_node("T_Thai",label="Thai",shape="house")
A.add_node("T_French",label="French",shape="house")
A.add_node("T_Chinese",label="Chinese",shape="house")
A.add_node("Friday",label="Friday",color="blue")
A.add_node("F_Yes",label="Yes",shape="house")
A.add_node("F_No",label="No",shape="house")
A.add_node("Yes_1",label="Yes",shape="square")
A.add_node("No_1",label="No",shape="square")
A.add_node("No_2",label="No",shape="square")
A.add_node("Yes_3",label="Yes",shape="square")
A.add_node("No_3",label="No",shape="square")

A.add_edge("Patrons","P_None")
A.add_edge("Patrons","P_Some")
A.add_edge("Patrons","P_Full")

A.add_edge("P_None","No_1")
A.add_edge("P_Some","Yes_1")
A.add_edge("P_Full","Type")

A.add_edge("Type","T_Chinese")
A.add_edge("Type","T_French")
A.add_edge("Type","T_Thai")
A.add_edge("Type","T_Italian")

A.add_edge("T_Chinese","No_2")
A.add_edge("T_French","No_2")
A.add_edge("T_Thai","Friday")
A.add_edge("T_Italian","Yes_3")

A.add_edge("Friday","F_Yes")
A.add_edge("Friday","F_No")

A.add_edge("F_Yes","Yes_3")
A.add_edge("F_No","No_3")

# adjust a graph parameter
#A.graph_attr['epsilon']='0.001'
print A.string() # print dot file to standard output
A.layout('dot') # layout with dot
A.draw('2e.ps') # write to file


'''
import pygraphviz as pgv
from pygraphviz import *
G=pgv.AGraph()
ndlist = [1,2,3]
for node in ndlist:
    G.add_node(node)
    label = "Label #" + str(node)
    G.get_node(node).attr['label'] = label
G.layout()
G.draw('example.png', format='png')


"""
A simple example to create a graphviz dot file and draw a graph.
"""
#    Copyright (C) 2006 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.


from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

__author__ = """Aric Hagberg (hagberg@lanl.gov)"""

import pygraphviz as pgv

A=pgv.AGraph()

A.add_edge(1,2)
A.add_edge(2,3)
A.add_edge(1,3)

print(A.string()) # print to screen
print("Wrote simple.dot")
A.write('simple.dot') # write to simple.dot

B=pgv.AGraph('simple.dot') # create a new graph from file
B.layout() # layout with default (neato)
B.draw('simple.png') # draw png
print("Wrote simple.png")
'''
