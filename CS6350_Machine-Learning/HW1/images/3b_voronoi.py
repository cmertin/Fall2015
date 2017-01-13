#!/usr/bin/python

from scipy.spatial import KDTree
import matplotlib.pyplot as plt
plt.rc("savefig", dpi=150)
import numpy as np

points = np.array([[1,1],[-1,-1],[2,-2]])
tree = KDTree(points)
x = np.linspace(-2.5, 2.5, 100)
y = np.linspace(-2.5, 2.5, 100)
xx, yy = np.meshgrid(x, y)
xy = np.c_[xx.ravel(), yy.ravel()]
plt.pcolor(x, y, tree.query(xy)[1].reshape(100, 100))
plt.plot(points[:,0], points[:,1], 'ko')
plt.xlabel("X")
plt.ylabel("Y")
#plt.savefig("3b_Voronoi.png")
#plt.savefig("3b_Voronoi.ps")
plt.show()
