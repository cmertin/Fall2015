#!/usr/bin/python
'''
Author: Christopher Mertin
Date: November 13, 2015
File: SGD.py
Stochastic Gradient Descent (SGD)
'''

from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt
from math import floor
from random import shuffle
from sys import float_info

# Calculates the margin between the weight vector and the closest point
def Margin(w, data):
    margin = float_info.max
    for i in xrange(0, len(data)):
        y = int(data[i][0])
        x = data[i][1:]
        if y == 0:
            y = -1
        tempMargin = abs(w.transpose().dot(x))/np.linalg.norm(w)
        if tempMargin <= margin:
            margin = tempMargin
    return margin

# Simply prints a 3 column table of the three values
# Accuracy, and the two parameters C and rho
def PrintTable(max_acc, max_param):
    print("\tAccuracy and Parameters:")
    print("\t------------------------")
    print("Accuracy\t  C \t\t rho")
    print("--------\t-----\t\t-----")
    for i in xrange(0, len(max_acc)):
        accuracy = "%0.5f" % max_acc[i]
        C = "%0.3f" % max_param[i][0]
        rho = "%0.3f" % max_param[i][1]
        print(accuracy + "\t\t" + C + "\t\t" + rho)

# Returns how accurately w can classify the data in test_data
def ClassifyAccuracy(w, test_data):
    total = len(test_data)
    correct = 0
    for i in xrange(0, len(test_data)):
        y = test_data[i][0]
        if y == -1:
            y = 0
        x = test_data[i][1:]
        if w.transpose().dot(x) >= 1:
            predict = 1
        else:
            predict = 0
        if predict == y:
            correct += 1
    return correct/total

# Performs cross-validaation on the data to check which parameters
# work the best. It runs SGD on each of the sets for all the combinations
# of parameters on the "training" data after segmenting it up. It returns
# a list of accuracy and parameters for each set
def CrossValidation(data, C_list, rho_list, fold=10):
    copyData = data[:] # So the data isn't ruined
    size = len(data)/fold
    paramList = []
    accuracyList = []
    for c in C_list:
        for rho in rho_list:
            foldAccuracy = [] # list of accuracies for all the folds for 1
                              # set of parameters
            for i in xrange(0, fold):
                test_data = []
                train_data = []
                test_min = int(floor(i*size)) # Gets the lower segment of test
                test_max = int(floor((i+1)*size))  # Upper segment of test
                # Copies one segment for the test data
                test_data = copyData[test_min:test_max]
                # Stores all the rest of the data as training data
                for j in xrange(0, len(data)):
                    if test_min <= j < test_max:
                        continue
                    else:
                        train_data.append(copyData[j])
                w, w_list, margin = SGD(train_data, 10, c, rho)
                foldAccuracy.append(ClassifyAccuracy(w, test_data))
            paramList.append([c,rho])
            accuracyList.append(np.average(foldAccuracy))
    return accuracyList, paramList

# Performs a feature transformation on the data such that it calculates every
# multipliciative cyclic permutaitons, ie x_{i}*x_{j} for all i and j are 
# dimensions of the resulting vector
def FeatureTransform(data, printFurthest=True):
    transform = []
    furthest = data[0][1:]

    # Finds the original point that is furthest from the origin
    if printFurthest == True:
        print("\nOriginal furthest from origin:")
        for i in xrange(0, len(data)):
            x = data[i][1:]
            if np.linalg.norm(x) > np.linalg.norm(furthest):
                furthest = x
        print(furthest)
        dist = "%0.3f" % np.linalg.norm(furthest)
        print("Distance from origin: " + dist)
    
    # Transforms the data
    for i in xrange(0, len(data)):
        y = data[i][0]
        x = data[i][1:]
        transformVector = [y]
        for j in xrange(0, len(x)):
            for k in xrange(0, len(x)):
                transformVector.append(x[j] * x[k])
        transformVector = np.asarray(transformVector,float)
        transform.append(np.array(transformVector))

    # Finds the transformed point that is furthest from the origin
    if printFurthest == True:
        print("\nFurthest from the origin after tranformation:")
        furthest = 0
        for i in xrange(0, len(transform)):
            x = transform[i][1:]
            if np.linalg.norm(x) > np.linalg.norm(furthest):
                furthest = x
        print(furthest)
        dist = "%0.3f" % np.linalg.norm(furthest)
        print("Distance from origin: " + dist)
    return transform

# Calculates the gradient of SGD
def Gradient(w, x, y, C):
    if y * w.transpose().dot(x) <= 1:
        return w - C * y * x
    else:
        return w

# Calculates the Stochastic Gradient Descent for a given number of epochs
# and returns the resulting weight vector that segments the data
def SGD(data, maxEpochs=10, C=1, rho=1):
    shuffData = data[:]
    w = np.empty(len(data[0])-1,dtype=float)
    w_list = []
    t = 0
    margin = 0
    for T in xrange(0, maxEpochs):
        shuffle(shuffData)
        for i in xrange(0, len(data)):
            r = rho/(1 + (rho * t)/C)
            y = int(shuffData[i][0])
            x = shuffData[i][1:]
            w = w - r * Gradient(w, x, y, C)
            t = t + 1
        w_list.append(w)
        
    for w_epoch in w_list:
        tempMargin = Margin(w_epoch, data)
        if tempMargin > margin:
            w = w_epoch
            margin = tempMargin

    return w, w_list, margin
            
# The zero=False parameter is for removing the zero'th dimension from the list 
# if it exists. It doesn't exist in the new data in astro, but it exists in 
# the old data. Since we're not using the bias, we can remove it.
def ReadData(dataFile, zero=False):
    data = [] # Data array that stores all the values
    infile = open(dataFile, "r") # Creates the instance of the file and opens it
    
    # Begins to clean the data by stripping and reading all the lines
    lines = [line.strip() for line in infile.readlines()]

    # Further cleans the data
    for line in lines:
        vector = [] # Initializes a vector to store each element/line
        
        # Splits each column/dimension of a given vector by ":" and only
        # Reads in the value (0th element) and appends it to vector such that
        # vector will be a list of values
        for column in line.split(":"):
            vector.append(column.split()[0])

        if zero==True:
            vector.pop(1)
        
        # Converts the list of values to a numpy array so that the
        # mathematics in numpy can easily be used
        vector = np.asarray(vector,float)

        # Appends each "vector" to a list called data which stores all of the
        # numpy arrays so that each file that is read in will be stored in 
        # one long list of numpy arrays
        data.append(np.array(vector))

    infile.close()
    return data




####################################################################
####################################################################
####################################################################
####################################################################
#                                                                  #
#                                                                  #
#                                                                  #
#                      Program Starts Here                         #
#                                                                  #
#                                                                  #
#                                                                  #
####################################################################
####################################################################
####################################################################
####################################################################

# Messages for Grader/User
train_files = ["./astro/original/train", "./astro/scaled/train", "./data0/train0.10"]
test_files = ["./astro/original/test", "./astro/scaled/test", "./data0/test0.10"]
temp_transform = train_files[0] + ".transform"

str_1 = "Note: Files such as \"" + temp_transform + "\" don't actually exist."
str_2 = "      They are calculated at execution as I didn't want to write a function"
str_3 = "      that saved them in the correct format to be parsed."
str_4 = "Also: I reduced to 5-fold cross validation and only 10 epochs as it was"
str_5 = "      taking too long to run on CADE, though my final results reflect"
str_6 = "      10-fold cross validation and 30 epochs."

print("\n" + "%"*len(str_1))
print(str_1)
print(str_2)
print(str_3)
print(str_4)
print(str_5)
print(str_6)
print("%"*len(str_1))


# Variable Initializations for learning

C_list = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]
rho_list = [0.001, 0.01, 0.1, 1.0]

crossFold = 5 # Number for cross-fold validation on the training set
epochs = 10 # Number of epochs 


# Iterates through all the files 
for files in train_files:

    ####################################################################
    # Train the Data                                                   #
    ####################################################################

    # Lets the user know what data set they're on
    print("\n")
    title = "Performing " + str(crossFold) + "-fold Cross Validation for: " + files 
    print("="*len(title))
    print(title)
    print("="*len(title))
    trainData_transform = None
    testData_transform = None
    fileIndex = train_files.index(files)

    # If "astro" is in the string
    if files.find("astro") != -1:
        trainData = ReadData(files)
        trainData_transform = FeatureTransform(trainData)
    # If ".10" is in the string
    elif files.find(".10") != -1:
        trainData = ReadData(files, True)

    # Runs k-fold cross validation on the data to see which parameters are best
    accuracyList, paramList = CrossValidation(trainData, C_list, rho_list, crossFold)

    max_acc = []
    max_param = []
    
    # Gets the top 5 best parameters and their corresponding accuracy
    for i in xrange(0, 5):
        max_index = accuracyList.index(max(accuracyList))
        max_acc.append(accuracyList[max_index])
        max_param.append(paramList[max_index])
        accuracyList.pop(max_index)
        paramList.pop(max_index)
        
    # Prints only the top 5 parameters in the form of a table
    PrintTable(max_acc, max_param)

    ####################################################################
    # Test the data                                                    #
    ####################################################################
    print("\n")
    print("\t\t----------------")
    print("\t\tTesting the data")
    print("\t\t----------------")
    C = max_param[0][0]
    rho = max_param[0][1]
    str_C = "%.3f" % C
    str_rho = "%.3f" % rho
    print("\t\t       C: " + str_C + "\n\t\t     rho: " + str_rho)

    # Reads in the test data and forms the transformation data as well by performing
    # A feature transformation on it
    # If "astro" is in the string
    if files.find("astro") != -1:
        testData = ReadData(test_files[fileIndex])
        testData_transform = FeatureTransform(trainData, False)
    # If ".10" is in the string
    elif files.find(".10") != -1:
        testData = ReadData(test_files[fileIndex], True)

    # Tests the data using Stoichastic Gradient Descent and the max parameters
    w, w_list, margin = SGD(trainData, epochs, C, rho)
    
    accuracy = ClassifyAccuracy(w, testData)
    str_accuracy = "%.4f" % accuracy
    str_margin = "%.3f" % margin
    print("\t\tAccuracy: " + str_accuracy)
    print("\t\t  Margin: " + str_margin)

    ####################################################################
    # Do the same for the transformed data                             #
    ####################################################################

    if trainData_transform != None:
        files = files + ".transform"
        print("\n")
        title = "Performing " + str(crossFold) + "-fold Cross Validation for: " + files 
        print("="*len(title))
        print(title)
        print("="*len(title))

        # Runs k-fold cross validaiton on the data to see which parameters are best
        accuracyList, paramList = CrossValidation(trainData_transform, C_list, rho_list, crossFold)

        max_acc = []
        max_param = []
    
        # Gets the top 5 best parameters and their corresponding accuracy
        for i in xrange(0, 5):
            max_index = accuracyList.index(max(accuracyList))
            max_acc.append(accuracyList[max_index])
            max_param.append(paramList[max_index])
            accuracyList.pop(max_index)
            paramList.pop(max_index)
        
        # Prints only the top 5 parameters in the form of a table
        PrintTable(max_acc, max_param)

        ####################################################################
        # Test the data                                                    #
        ####################################################################
        print("\n")
        print("\t\t----------------")
        print("\t\tTesting the data")
        print("\t\t----------------")
        C = max_param[0][0]
        rho = max_param[0][1]
        str_C = "%.3f" % C
        str_rho = "%.3f" % rho
        print("\t\t       C: " + str_C + "\n\t\t     rho: " + str_rho)
        
        # Tests the data using Stoichastic Gradient Descent and the max parameters
        w, w_list, margin = SGD(trainData_transform, epochs, C, rho)
    
        accuracy = ClassifyAccuracy(w, testData_transform)
        str_accuracy = "%.4f" % accuracy
        print("\t\tAccuracy: " + str_accuracy)
        str_margin = "%.3f" % margin
        print("\t\t  Margin: " + str_margin)
    

    
    
