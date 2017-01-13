#!/usr/bin/python

from __future__ import division, print_function
from math import sqrt
import numpy as np

def ManhattanDistance(x1,x2):
    dim = len(x1)
    dist = 0
    for i in xrange(0, dim):
        dist += abs(x1[i] - x2[i])
    return dist

def Midpoint(x1,x2):
    dim = len(x1)
    midpoint = []
    for i in xrange(0, dim):
        new_point = (x1[i] + x2[i])/2.0
        midpoint.append(new_point)
    return midpoint

points = np.array([[1,1],[-1,-1],[2,-2]])

for i in xrange(0, len(points)):
    for j in xrange(i+1, len(points)):
        dist = ManhattanDistance(points[i],points[j])
        print("Manhattan Distance",points[i],points[j],dist)
        print("Midpoint:",Midpoint(points[i],points[j]))
