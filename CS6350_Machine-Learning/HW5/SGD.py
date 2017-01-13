#!/usr/bin/python
'''
Author: Christopher Mertin
Date: December 10, 2015
File: SGD.py
Stochastic Gradient Descent (SGD)
'''

from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt
from math import floor
from random import shuffle

# Prints the top 5 maximum accuracies and list of parameters
# given a list of accuracies and the corresponding list of
# parameters
def PrintTable(accuracyList, paramList):
    max_acc = []
    max_param = []
    param_length = 0

    # Iterates over the lists to get the maximum 5
    for i in xrange(0, 5):
        max_index = accuracyList.index(max(accuracyList))
        max_acc.append(accuracyList[max_index])
        max_param.append(paramList[max_index])
        accuracyList.pop(max_index)
        paramList.pop(max_index)
        if len(str(max_param[i])) > param_length:
            param_length = len(str(max_param[i]))

    title_length = len("[gamma_0, sigma]")
    hyp_num = max(title_length, param_length)

    # Prints the table with the accuracies and the paramters
    print("\tAccuracy and Parameters:")
    print("\t------------------------")
    print("Accuracy\t[gamma_0, sigma]")
    print("--------\t" + '-'*hyp_num)
    for i in xrange(0, len(max_acc)):
        accuracy = "%0.5f" % max_acc[i]
        param = str(max_param[i])
        print(accuracy + "\t\t" + param)

# Takes in a given weight vector and a given test data set and returns
# the accuracy that the weight vector had in classifying the test data.
# Returns the fractional accuracy of the data set
def ClassifyAccuracy(w, test_data):
    total = len(test_data)
    correct = 0
    for i in xrange(0, len(test_data)):
        y = test_data[i][0]
        if y == 0:
            y = -1
        x = test_data[i][1:]
        if w.transpose().dot(x) >= 1:
            predict = 1
        else:
            predict = -1
        if predict == y:
            correct += 1
    return correct/total

# This uses cross validation to see which parameters are the best to choose
# for the final training data set. It iterates over a list of values for
# gamma_0 and sigma and calls the SGD function for k-fold cross validation
# and tests the accuracy on the segment that is left out
def CrossValidation(data, sigma_list, max_epochs, fold, gamma_list):
    copyData = data[:]
    size = len(data)/fold # size of one "group" of elements
    paramList = [] # holds the list of parameters
    accuracyList = [] # holds the accuracy from each parameter combination
    print("\tPerforming " + str(fold) + "-fold cross validation")
    
    for gamma_0 in gamma_list:
        for sigma in sigma_list:
            print("\t\t[gamma_0, sigma]: " + str([gamma_0,sigma]))
            foldAccuracy = []
            for i in xrange(0, fold):
                test_data = []
                train_data = []
                test_min = int(floor(i*size)) # minimum index for the test data
                test_max = int(floor((i+1)*size)) # max index for test data
                # copies the test data to a list
                test_data = copyData[test_min:test_max]
                # iterates through the list and builds the training data
                # (ie the data set excluding the test set
                for j in xrange(0, len(data)):
                    if test_min <= j < test_max:
                        continue
                    else:
                        train_data.append(copyData[j])
                # Gets the weight vector w from the training data
                w = SGD(train_data, sigma, max_epochs, gamma_0)
                # Tests the accuracy of the weight vector for each fold of
                # cross validation
                foldAccuracy.append(ClassifyAccuracy(w, test_data))
            paramList.append([gamma_0,sigma]) # list of all parameters used
            # averages the accuracy of each fold of cross validation which is
            # the accuracy for that pair of hyper parameters
            accuracyList.append(np.average(foldAccuracy)) 
        print("\n\t")
    print(str(fold) + "-fold cross validation is complete!\n")
    return accuracyList, paramList

# Gradient function which returns the gradient of J(w) to be used in the
# SGD algorithm. Has a try/except function to catch overflows for if the
# exponential gets too large. If this happens, it uses an alterate form
# of the function which won't contain overflow errors for those instances
def Gradient_J(w, data, sigma):
    y = data[0]
    if y == 0:
        y = -1
    x = data[1:]
    # Try/except function which builds the "first term" of the gradient
    with np.errstate(over="raise"):
        try:
            exponential = np.exp(y * (w.transpose().dot(x)))
            first_term = (-y * x)/(exponential + 1)
        except FloatingPointError:
            exponential = np.exp(-y * w.transpose().dot(x))
            first_term = (-y * x * exponential)/(1 + exponential)
    second_term = 2 * np.linalg.norm(w)/(sigma * sigma)
    return first_term + second_term

# The function J(w) which is the function used to classify the data.
# It is required to sum over all of the records in the data set to get the value
# of it. The most important part of this function is to be minimized in the
# final SGD call, which looks at all the w's for each epoch. Has another
# try/except function for catching overflow errors, where if the exponential is
# too small, the log function would blow up. This is approximated by
# if log(1+e^(-z)) overflows, then approximate it as -z
def J(w, data, sigma):
    total = 0
    for record in data:
        y = record[0]
        if y == 0:
            y = -1
        x = record[1:]
        with np.errstate(over="raise"):
            try:
                exponential = np.exp(-y * (w.transpose().dot(x)))
                log_fn = np.log(1 + exponential)
            except:
                log_fn = -y * (w.transpose().dot(x))
        total += log_fn 
    return total + pow(np.linalg.norm(w),2)/(sigma * sigma)

# Calculates the stochastic gradient descent method for a given data set
# where it treats each data record as the total data set and updates based on
# the gradient of that single data point. It takes in a maximum number of
# epochs where it shuffles the data each time and builds the weight vector
# from each of the iterations, then attempts to minimize J(w), where the w
# that minimizes it is the weight vector that is returned
def SGD(data, sigma, max_epochs, gamma_0, plot=False):
    w = np.zeros((len(data[0])-1),float) # Initialize w
    w_list = [] # list of weight vectors
    neg_log_likelihood = [] # list of the negative log likelihood function
    min_J = None
    min_w = None
    t = 0
    # Iterates for each epoch
    for epoch in xrange(0, max_epochs):
        shuffle(data) # shuffles the data
        # Iterates through each record in the data set
        for index in xrange(0, len(data)):
            record = data[index] # the current record
            C = sigma * sigma
            gamma = gamma_0/(1+(gamma_0*t)/C) # learning rate
            w = w - gamma * Gradient_J(w, record, sigma) # update weight vector
            t += 1
            
        if plot == True:
            # appends to a list of the negative log-likelihood function if and
            # only if it's the last time that SGD is being called for the
            # data set, as the information is essentially useless for
            # cross validation
            neg_log_likelihood.append(np.log(J(w, data, sigma)))
        w_list.append(w)
    # Iterates through the list of w's and chooses the one that minimizes J(w)
    for w in w_list:
        temp_J = J(w, data, sigma)
        if min_J == None:
            min_J = temp_J
            min_w = w
            continue
        if min_J > temp_J:
            min_J = temp_J
            min_w = w
    # plot represents if it's the last time that SGD is being called
    # ie for the final weight vector on the entire training set. If it's not
    # then we don't need the neg_log_likelihood data
    if plot == False:
        return min_w
    else:
        return min_w, neg_log_likelihood
        

# Reads in the data and builds each line into a numpy vector to make the
# calculations easier and ability to use the numpy math library
def ReadData(dataFile):
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

max_epochs = 10
sigma_list = [1e5,1e6,1e7,1e8,1e9,1e10]
gamma_list = [0.001,0.01,1e5,1e6,1e7,1e8,1e10]
fold = 5
fold_max_epochs = 5
orig_plot = []
scaled_plot = []
plot_file = "SGD-results.pdf"
training_set = ["astro/original/train", "astro/scaled/train"]
test_set = ["astro/original/test", "astro/scaled/test"]

for index in xrange(0,len(training_set)):
    training_file = training_set[index]
    test_file = test_set[index]
    start_string = "Running over " + training_file
    print('\n')
    print('='*len(start_string))
    print(start_string)
    print('='*len(start_string))

    # Reads in the training data and the test data
    training_data = ReadData(training_file)
    test_data = ReadData(test_file)

    # Returns the list of accuracies and parameters from cross validation
    accuracyList, paramList = CrossValidation(training_data, sigma_list,
                                              fold_max_epochs, fold, gamma_list)

    # Chooses the parameters that had the highest accuracy and prints the top
    # 5 most accurate combinations
    max_index = accuracyList.index(max(accuracyList))
    gamma_0 = paramList[max_index][0]
    sigma = paramList[max_index][1]
    PrintTable(accuracyList, paramList)

    # Calls SGD to get the weight vector on the entire training data using
    # the hyper paramters from the cross validation function
    w, neg_log_likelihood = SGD(training_data, sigma, max_epochs, gamma_0, True)

    # organizes the negative log likelihood function for the final plot
    if index == 0:
        orig_plot = neg_log_likelihood
    else:
        scaled_plot = neg_log_likelihood

    # Tests the accuracy of the weight vector and prints the accuracy
    print("Classifying on " + test_file)
    acc = ClassifyAccuracy(w, test_data)
    accuracy = "%0.5f" % acc
    print("Accuracy: " + accuracy)

# Plots the data to a pdf and saves it to the file plot_file
print("Saving figure to " + plot_file)
plt.clf()
plt.plot(range(1,max_epochs+1), orig_plot, label=test_set[0])
plt.plot(range(1,max_epochs+1), scaled_plot, 'g--', label=test_set[1])
plt.xlabel("Epoch")
plt.ylabel("Negative Log-Likelihood Function")
plt.title("Negative Log-Likelihood Function For Each Epoch")
plt.legend(loc=0)
plt.savefig(plot_file, format="pdf")

plt.clf()
print("Saving figure to SGD-results-orig.pdf")
plt.plot(range(1,max_epochs+1), orig_plot, label=test_set[0])
plt.xlabel("Epoch")
plt.ylabel("Negative Log-Likelihood Function")
plt.title("Negative Log-Likelihood Function For Each Epoch")
plt.legend(loc=0)
plt.savefig("SGD-results-orig.pdf", format="pdf")

plt.clf()
print("Saving figure to SGD-results-scaled.pdf")
plt.plot(range(1,max_epochs+1), scaled_plot, 'g--', label=test_set[1])
plt.xlabel("Epoch")
plt.ylabel("Negative Log-Likelihood Function")
plt.title("Negative Log-Likelihood Function For Each Epoch")
plt.legend(loc=0)
plt.savefig("SGD-results-scaled.pdf", format="pdf")

print("DONE")
