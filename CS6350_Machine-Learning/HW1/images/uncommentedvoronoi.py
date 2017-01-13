#!/usr/bin/python

from __future__ import division, print_function
from math import sqrt
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
import six
import random
plt.rc("savefig", dpi=150)

x_min = -2.5
x_max = 2.5
y_min = -2.5
y_max = 2.5
N = 200
step = (x_max - x_min)/N
colors_ = list(six.iteritems(colors.cnames))

def ManhattanDistance(x1,x2):
    dim = len(x1)
    dist = 0
    for i in xrange(0, dim):
        dist += abs(x1[i] - x2[i])
    return dist

def MertinDistance(x1, x2, p=13.0):
    dim = len(x1)
    dist = 0
    for i in xrange(0, dim):
        dist += pow(abs(x1[i] - x2[i]),p)
    return pow(dist, 1.0/p)

def ArrayIndex(looking_for, array):
    for i in xrange(0, len(array)):
        for j in xrange(0, len(looking_for)):
            if looking_for[j] != array[i][j]:
                break
            if j == (len(looking_for) - 1):
                return i
    return -1

def EuclideanMap(points, label):
    label_E = []
    for j in xrange(0, N):
        y = y_min + step * j
        for k in xrange(0, N):
            x = x_min + step * k
            test_pt = np.array([x,y])
            closest_E = 10000
            for i in xrange(0,len(points)):
                temp_E = np.linalg.norm(test_pt - points[i])
                if temp_E < closest_E:
                    closest_pt_E = points[i]
                    closest_E = temp_E
            index = ArrayIndex(closest_pt_E, points)
            label_E.append(label[index])
    return label_E


def ManhattanMap(points, label):
    M_line = []
    for j in xrange(0, N):
        y = y_min + step * j
        for k in xrange(0, N):
            x = x_min + step * k
            test_pt = np.array([x,y])
            closest_M = 10000
            for i in xrange(0, len(points)):
                temp_M = ManhattanDistance(test_pt, points[i])
                if temp_M < closest_M:
                    closest_pt_M = points[i]
                    closest_M = temp_M
            index = ArrayIndex(closest_pt_M, points)
            M_line.append(label[index])
    return M_line

def MertinMap(points, label, p=13.0):
    M_line = []
    for j in xrange(0, N):
        y = y_min + step * j
        for k in xrange(0, N):
            x = x_min + step * k
            test_pt = np.array([x,y])
            closest_M = 10000
            for i in xrange(0, len(points)):
                temp_M = MertinDistance(test_pt, points[i], p)
                if temp_M < closest_M:
                    closest_pt_M = points[i]
                    closest_M = temp_M
            index = ArrayIndex(closest_pt_M, points)
            M_line.append(label[index])
    return M_line

def PlotMap(line, points, title="Voronoi Map", base_save = "figure"):
    line_count = 0
    plt.clf()
    pt_size = .25
    marker = "s"
    color1 = colors_[random.randint(0,len(colors_)-1)]
    color2 = colors_[random.randint(0,len(colors_)-1)]
    color3 = colors_[random.randint(0,len(colors_)-1)]
    pdf_save = base_save + ".pdf"
    png_save = base_save + ".png"
    for i in xrange(0,N):
        y = y_min + i * step
        for j in xrange(0,N):
            x = x_min + j * step
            temp_pt = np.array([x,y])
            if line[line_count] == "A":
                plt.scatter(x,y,color="orange",s=pt_size,marker=marker)
            elif line[line_count] == "B":
                plt.scatter(x,y,color="cyan",s=pt_size,marker=marker)
            else:
                plt.scatter(x,y,color="lime",s=pt_size,marker=marker)
            line_count += 1

    for i in xrange(0, len(points)):
        x = points[i][0]
        y = points[i][1]
        plt.scatter(x,y,color="black",s=10)

    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.savefig(png_save)
    
points1 = np.array([[1,1],[1,-1],[-1,-1],[2,-2]])
points2 = np.array([[1,1],[-1,-1],[2,-2]])
points3 = np.array([[1.5,1.5],[-1.5,-1],[1,-2],[-.5,1]])

label_E = ["A", "A", "B", "C"]
label_M = ["A", "B", "C"]
label_K = ["A", "B", "B", "C"]


E_line = EuclideanMap(points1, label_E)
PlotMap(E_line, points1, "Euclidean Voronoi Map", "NN_1")

M_line = ManhattanMap(points2, label_M)
PlotMap(M_line, points2, "Manhattan Voronoi Map", "NN_2")

KE_line = EuclideanMap(points3, label_K)
PlotMap(KE_line, points3, "Euclidean Voronoi Map", "NN_3a")

KM_line = ManhattanMap(points3, label_K)
PlotMap(KM_line, points3, "Manhattan Voronoi Map", "NN_3b")

KM2_line = ManhattanMap(points1, label_E)
PlotMap(KM2_line, points1, "Manhattan Voronoi Map", "NN_3c")
'''
Mertin_line = MertinMap(points3, label_K)
PlotMap(Mertin_line, points3, "Mertin Voronoi Map", "NN_Mertin")

Mertin_line = MertinMap(points3, label_K, 100)
PlotMap(Mertin_line, points3, "Mertin Voronoi Map", "NN_Mertin_100")

Mertin_line = MertinMap(points3, label_K, 1000)
PlotMap(Mertin_line, points3, "Mertin Voronoi Map", "NN_Mertin_1000")


for i in xrange(1, 51):
    title = "Voronoi Map (p = " + str(i) + ")"
    file = "VoronoiMap_" + str(i)
    Voronoi_line = MertinMap(points3, label_K, i)
    PlotMap(Voronoi_line, points3, title, file)
'''
