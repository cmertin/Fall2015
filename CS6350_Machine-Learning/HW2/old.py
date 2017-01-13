#!/usr/bin/python

from __future__ import division, print_function
import numpy as np
from random import shuffle

def Perceptron(data):
    shuffle(data)
    r = .001
    w = np.zeros(len(data[0]), dtype=float)
    r_list = [1, .1, .01, .001]
    flag = 0
    #print(np.random.rand(1,len(data)))
    for m in xrange(0, len(r_list)):
        w = np.zeros(len(data[0]), dtype=float)
        r = r_list[m]
        print(r)
        updates = 0
        for i in xrange(0, len(data)):
            x = data[i]
            y = x[0]
            if y * (w.transpose().dot(x)) <= 0:
                #print('magic')
                updates += 1
                w = w + r * y * x
        print(updates)
        #print(np.linalg.norm(w[1:]))
        #print(w[1:])

def ReadData(dataFile):
    data = [] # Data array that stores all the values
    infile = open(dataFile, "r") # Creates the instance of the file and opens it

    # Begins to clean the data by stripping and reading in all the lines
    lines = [line.strip() for line in infile.readlines()]

    # Further cleans the data
    for line in lines:
        vector = [] # Initializes a vector to store each element/line

        # Splits each column/dimension of the given vector by ":" and only
        # reads in the value (0th element) and appends it to vector such that
        # vector will be a list of values
        for column in line.split(":"):
            vector.append(column.split()[0])

        # Converts the list of values to a numpy array so that the
        # mathematics in numpy can easily be used
        vector = np.asarray(vector, float)

        # Appends each "vector" to a list called data which stores all of the
        # numpy arrays so that each file that is read in will be stored in one
        # long list of numpy arrays
        data.append(np.array(vector))

    # Small test showing that the inner product and addition works
    '''
    temp_sum = data[0] + data[1]
    temp_inner = data[0] * data[1]
    print("\ndata[0]\n", data[0])
    print("\ndata[1]\n", data[1])
    print("\nSum of data[0] and data[1]")
    print(temp_sum)
    print("\nInner Product of data[0] and data[1]")
    print(temp_inner)
    '''
    return data

print("\nSanity Check. Running Perceptron Algorithm on Table 2")
fileName = "table.2"
data = ReadData(fileName)
Perceptron(data)

fileName = "./data0/train0.100"
data = ReadData(fileName)
Perceptron(data)
