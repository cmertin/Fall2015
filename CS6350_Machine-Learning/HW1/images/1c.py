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
A.add_node("x1",color='red',label="X1") 
A.add_node("x2_1",color='blue',label="X2")
A.add_node("x3_1",color="blue", label="X3")
A.add_node("x2_2",color='blue',label="X2")
A.add_node("x3_2",color="blue", label="X3")
A.add_node("0_1",label="0", shape="square") 
A.add_node("1_1",label="1", shape="square") 
A.add_node("0_2",label="0", shape="square") 
A.add_node("1_2",label="1", shape="square") 


A.add_edge("x1","x2_1",label="X1 = 1")
A.add_edge("x2_1","1_1",label="X2 = 1")
A.add_edge("x2_1","x3_1",label="X2 = 0")
A.add_edge("x3_1","1_1",label="X3 = 1")
A.add_edge("x3_1","0_1",label="X3 = 0")

A.add_edge("x1","x2_2",label="X1 = 0")
A.add_edge("x2_2","0_2",label="X2 = 0")
A.add_edge("x2_2","x3_2",label="X2 = 1")
A.add_edge("x3_2","1_2",label="X3 = 1")
A.add_edge("x3_2","0_2",label="X3 = 0")
# adjust a graph parameter
#A.graph_attr['epsilon']='0.001'
print A.string() # print dot file to standard output
A.layout('dot') # layout with dot
A.draw('1c-LR.ps') # write to file


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
