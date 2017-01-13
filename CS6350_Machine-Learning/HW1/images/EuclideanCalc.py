#!/usr/bin/python

from __future__ import division, print_function
from math import sqrt, pow
import numpy as np

# Euclidean Distance
def Distance(p1, p2):
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[1]
    return sqrt(pow(x_diff, 2) + pow(y_diff,2))

def MidPoint(p1, p2):
    mid_x = (p1[0] + p2[0])/2.0
    mid_y = (p1[1] + p2[1])/2.0
    return [mid_x, mid_y]


points = np.array([[1,1],[1,-1],[-1,-1],[2,-2]])
hash_list = []
dist = Distance(points[0], points[1])

for i in xrange(0, len(points)):
    for j in xrange(0, len(points)):
        dist = Distance(points[i], points[j])
        if j <= i or dist in hash_list:
            continue
        else:
            hash_list.append(dist)
            print("Distance between", points[i], "and", points[j], "%0.2F" % dist)
            print("\tHalf way point:", MidPoint(points[i], points[j]))
