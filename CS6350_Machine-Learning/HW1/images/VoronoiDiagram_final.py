#!/usr/bin/python

'''
VoronoiDiagram.py
Author: Christopher Mertin
Date: September 13, 2015
Email: cmertin@cs.utah.edu

I created this program because there was no good software out there that helped visualize Voronoi Diagrams for
various LP-spaces, and there wasn't one that allowed you to group them in the same label. While this program isn't 
perfect, and you will find some points out of place, it will give you a general idea on what the Voronoi Map looks
like, and you will be able to remove the irregularities without questioning it. If the computation is taking too long,
you can change the value of N, but you will also have to change the pt_size in the PlotMap function. At N=200, it
takes roughly 5 minutes to plot one figure.
'''

from __future__ import division, print_function
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
import six
import random
plt.rc("savefig", dpi=150)

x_min = -2.5 # Min/max x and y values for the grid
x_max = 2.5
y_min = -2.5
y_max = 2.5
N = 200 # Grid spacing along one axis. Total grid is N^2
step = (x_max - x_min)/N
colors_ = list(six.iteritems(colors.cnames))

# Calculates the LP distance for a given value of p
def LPDistance(x1, x2, p):
    dim = len(x1)
    dist = 0
    for i in xrange(0, dim):
        dist += pow(abs(x1[i] - x2[i]), p)
    return pow(dist, 1.0/p)

# Iterates over all of the points in the grid and calculates which point corresponds to which label. If no p is given,
# defaults to Euclidean norm where p = 2.
def VoronoiMap(points, label, p=2.0):
    line = []
    for i in xrange(0, N):
        y = y_min + step * i
        for j in xrange(0, N):
            x = x_min + step * j
            test_pt = np.array([x,y])
            closest_label = 10000
            for k in xrange(0, len(points)):
                temp_label = LPDistance(test_pt, points[k], p)
                if temp_label < closest_label:
                    closest_pt_label = points[k]
                    closest_label = temp_label
            index = VectorIndex(closest_pt_label, points)
            line.append(label[index])
    return line

# Finds the index of a vector in a given list of vectors. The list of labels directly corresponds to the point in the
# list of points. So if we find which one is matched as the closest, we have the label
def VectorIndex(looking_for, array):
    for i in xrange(0, len(array)):
        for j in xrange(0, len(looking_for)):
            if looking_for[j] != array[i][j]:
                break
            if j == (len(looking_for) - 1):
                return i
    return -1

# Plots the Voronoi Diagram with matplotlib. I was going to implement a random color generator and save the colors
# and thus make it useful for X number of points, but as I only needed 3 I included the base libraries for implementing
# it. Maybe in the future.
def PlotMap(line, points, title="Voronoi Map", base_save="figure"):
    line_count = 0
    plt.clf()
    png_save = base_save + ".png"
    pt_size = .5
    marker = "s"
    color1 = colors_[random.randint(0,len(colors_)-1)]
    color2 = colors_[random.randint(0,len(colors_)-1)]
    color3 = colors_[random.randint(0,len(colors_)-1)]
    for i in xrange(0,N):
        y = y_min + i * step
        for j in xrange(0,N):
            x = x_min + j * step
            temp_pt = np.array([x,y])
            if line[line_count] == "A":
                plt.scatter(x,y,color="orange",s=pt_size,marker=marker)
            elif line[line_count] == "B":
                plt.scatter(x,y,color="yellow",s=pt_size,marker=marker)
            else:
                plt.scatter(x,y,color="lime",s=pt_size,marker=marker)
            line_count += 1

    for i in xrange(0, len(points)): # Plots the inital points at the end in black so they will be ontop of the rest
        x = points[i][0]
        y = points[i][1]
        plt.scatter(x,y,color="black",s=10)

    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.savefig(png_save) # Saves the file to a .png in the working directory
    #plt.show()
    
# The default points for the Voronoi Diagram    
points1 = np.array([[1,1],[1,-1],[-1,-1],[2,-2]])
points2 = np.array([[1,1],[-1,-1],[2,-2]])
points3 = np.array([[1.5,1.5],[-1.5,-1],[1,-2],[-.5,1]])

# The labels for the different Voronoi plots
label_E = ["A", "A", "B", "C"]
label_M = ["A", "B", "C"]
label_K = ["A", "B", "B", "C"]


print("Plotting the given data in the Nearest Neighbors part (a)")
E_line = VoronoiMap(points1, label_E, 2)
PlotMap(E_line, points1, "Euclidean Voronoi Map", "NN_3a")

M_line = VoronoiMap(points2, label_M, 1)
PlotMap(M_line, points2, "Manhattan Voronoi Map", "NN_3b")

print("Testing a randomly chosen set of labels and points to see")
print("if they will produce different Manhattan and Euclidean Voronoi Maps")
KM_line = VoronoiMap(points3, label_K, 1)
PlotMap(KM_line, points3, "Manhattan Voronoi Map", "NN_3c1")

KE_line = VoronoiMap(points3, label_K, 2)
PlotMap(KE_line, points3, "Euclidean Voronoi Map", "NN_3c2")

print("Testing the original plot with a Manhattan Voronoi Map")
KM2_line = VoronoiMap(points1, label_E, 1)
PlotMap(KM2_line, points1, "Manhattan Voronoi Map", "NN_3c3")
