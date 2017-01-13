#!/usr/bin/python
from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def fn(x,y):
    return x**2-y**2

def phi(x,y):
    return x**2 - y**4

def Functional(x, y, r):
    return (x**2-y**2 <= r**2)

def PhiFunctional(x,y,r):
    return (x**2-y**4<= r**2)

def randrange(n, vmin, vmax):
    return (vmax - vmin)*np.random.rand(n) + vmin

r = 2
in_list_x = []
in_list_y = []
in_list_z = []
out_list_x = []
out_list_y = []
out_list_z = []
n = 500
min_ = -100
max_ = 100
x_list = randrange(n, min_, max_)
y_list = randrange(n, min_, max_)

for i in xrange(0, len(x_list)):
    x = x_list[i]
    y = y_list[i]
    if Functional(x, y, r):
        in_list_x.append(x)
        in_list_y.append(y)
        in_list_z.append(fn(x,y))
    else:
        out_list_x.append(x)
        out_list_y.append(y)
        out_list_z.append(fn(x,y))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(in_list_x, in_list_y, in_list_z, c='r', marker='o')
ax.scatter(out_list_x, out_list_y, out_list_z, c='b', marker='^')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()

in_list_x = []
in_list_y = []
in_list_z = []

out_list_x = []
out_list_y = []
out_list_z = []

for i in xrange(0, len(x_list)):
    x = x_list[i]
    y = y_list[i]
    if PhiFunctional(x, y, r):
        in_list_x.append(x)
        in_list_y.append(y)
        in_list_z.append(phi(x,y))
    else:
        out_list_x.append(x)
        out_list_y.append(y)
        out_list_z.append(phi(x,y))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(in_list_x, in_list_y, in_list_z, c='r', marker='o')
ax.scatter(out_list_x, out_list_y, out_list_z, c='b', marker='^')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
