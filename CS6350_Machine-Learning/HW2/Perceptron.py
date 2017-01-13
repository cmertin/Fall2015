#!/usr/bin/python
'''
Author: Christopher Mertin
Date: October 1, 2015
File: Perceptron.py
This program runs the normal Perceptron, Margin Perceptron, and the Agressive
Margin Perceptron algorithms over the n dimensional data in folders data0 and
data1, and then tests the accuracy and the number of updates for each one.
It then creates a plot for each one and shows how the accuracy and the number
of updates compare for each one.
'''

from __future__ import division, print_function
import numpy as np
from random import shuffle
import matplotlib.pyplot as plt

# Tests the weight vector by running over the test data and doing
# w^T*x, where if this is >= mu, then it guess 1 and if <mu then it
# guesses -1. It counts the number of times that it's correct and 
# then returns the total number of times that made the correct prediction
def TestWeightVector_Mu(w, mu, test_data):
    correct = 0
    
    for i in xrange(0, len(test_data)):
        x = test_data[i][1:]
        y = test_data[i][0]
        guess = w.transpose().dot(x)
        if guess >= mu and y == 1:
            correct += 1
        elif guess < mu and y == -1:
            correct += 1
            
    return correct

# Tests the weight vector by running over the test data and doing 
# w^T*x, where if this is >= 0 then it guesses 1 and if <0 then it guesses
# -1. It counts the number of times that it's correct and then returns the 
# total number of times that made the correct prediction
def TestWeightVector(w, test_data):
    correct = 0
    
    for i in xrange(0, len(test_data)):
        x = test_data[i][1:]
        y = test_data[i][0]
        guess = w.transpose().dot(x)
        if guess >= 0 and y == 1:
            correct += 1
        elif guess < 0 and y == -1:
            correct += 1
            
    return correct
        

# Optimizes the value of r for the least number of updates, the theory is
# that it tests over a given list of values for r in a list and chooses the
# one with the least number of updates. The conclusion being that a learning
# rate which needs minimal updates for the training data set will not need
# as much as when classifying future data - under the assumption thate the
# data in the future is relatively the same
def OptimizeR(data, r_list=[1, .1, .01, .001], w=None):
    if w == None:
        w = np.zeros(len(data[0]))
    num_updates = []
    for r in r_list:
        w1 = w[:]
        temp_updates, temp_w = Perceptron(data, r, w1)
        num_updates.append(temp_updates)
    index = num_updates.index(min(num_updates))
    return r_list[index]      

# Optimizes the values of r and mu for the least number of updates, with the 
# theory being the same as the OptimizeR function, with the only difference
# being that it is optimizing both r and mu instead
def OptimizeR_Mu(data, r_list, mu_list, w):
    num_updates = []
    combo = []
    
    for r in r_list:
        for mu in mu_list:
            w1 = w[:]
            updates, w1 = MarginPerceptron(data, r, mu, w1)
            num_updates.append(updates)
            temp = [r, mu]
            combo.append(temp)
    index = num_updates.index(min(num_updates))
    return combo[index][0], combo[index][1]

# Optimizes the values of r, mu, and eta for the least number of updates, with
# the thoery being the same as the OptimizeR and OptimizeR_Mu functions, with 
# the only difference being it is also optimizing for eta
def OptimizeR_Mu_Eta(data, r_list, mu_list, w):
    num_updates = []
    combo = []
    
    for r in r_list:
        for mu in mu_list:
            w1 = w[:]
            updates, w1 = AgressivePerceptron(data, r, mu, w1)
            num_updates.append(updates)
            temp = [r, mu]
            combo.append(temp)
    index = num_updates.index(min(num_updates))
    return combo[index][0], combo[index][1]

# Uses the Perceptron algorithm to change the weight vector, w, and the given
# data. It updates w based on if y*w^T*x is <= 0 which would be classified as
# an error
def Perceptron(data, r=0.1, w=None):
    if w == None: # Because laziness and to test with a zero weight vector
        w = np.zeros(len(data[0]), dtype=float)
    if len(w)%10 > 1: # Also because laziness, when w is created, it is done 
        w = np.array(w[1:]) # with the len(data[0]) which contains y still
    updates = 0

    for i in xrange(0, len(data)):
        x = data[i][1:] # Removes y from the first index
        y = data[i][0] # Stores y
        if y * (w.transpose().dot(x)) <= 0: # Performs the comparison
            updates += 1 # If it needs to be updated, increments
            w = w + r * y * x # Updates the weight vector

    return updates, w # Returns the updated weight vector and the num updates
    
# Uses the Margin Perceptron algorithm, which is similar to the normal 
# Perceptron algorithm above, except instead of testing around the range of 0,
# it tests it for some pre-determined factor mu
def MarginPerceptron(data, r, mu, w):
    if len(w)%10 > 1:
        w = np.array(w[1:])
    updates = 0
    
    for i in xrange(0, len(data)):
        x = data[i][1:]
        y = data[i][0]
        if y * (w.transpose().dot(x)) <= mu:
            updates += 1
            w = w + r * y * x
            
    return updates, w

# Uses the Agressive Margin Perceptron Algorithm, which is similar to the 
# Perceptron algorithm and more similar to the Margin Perceptron Algorithm,
# with the difference being that in an update it uses a new learning rate, eta,
# to update the weight vector instead of r
def AgressivePerceptron(data, r, mu, w):
    if len(w)%10 > 1:
        w = np.array(w[1:])
    updates = 0

    for i in xrange(0, len(data)):
        x = data[i][1:]
        y = data[i][0]
        if y * (w.transpose().dot(x)) <= mu:
            eta = (mu - y * (w.transpose().dot(x)))/(x.transpose().dot(x)+1)
            w = w + eta * y * x
            updates += 1

    return updates, w

def ReadData(dataFile):
    data = [] # Data array that stores all the values
    infile = open(dataFile, "r") #Creates the instance of the file and opens it

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
        
    return data

# Runs the Perceptron Algorithm over Table 2 in the homework and prints 
# the number of updates that were made and the weight vector
print("\nSanity Check. Running Perceptron Algorithm on Table 2")
r_list = [1, .1, .01, .001]
fileName = "table.2"
data = ReadData(fileName)
index = OptimizeR(data, r_list)
r = r_list[index]
num_updates, w = Perceptron(data, r)
print("Number of Updates: " + str(num_updates))
print("Weight Vector:")
print(w)

# list of r and mu that are going to be tested over, only do 5 each.
r_list = np.linspace(0,1,5)
mu_list = np.linspace(0,.01,5)

# Runs the Perceptron and Margin Perceptron over the 10 dimensional data 
# and reports the number of updates for each of the algorithms, and the 
# accuracy of the final weight vector.

print("\nRunning over the 10-Dimensional data")
train_file = "./data0/train0.10"
test_file = "./data0/test0.10"
train_data = ReadData(train_file)
test_data = ReadData(test_file)
w_rand = np.random.rand(len(train_data[0]))

r = OptimizeR(train_data, r_list, w_rand)
updates, w = Perceptron(train_data, r, w_rand)
correct = TestWeightVector(w, test_data)
print("Normal Perceptron")
print("Updates: " + str(updates) + " Accuracy: " + str(correct/len(test_data)))

r, mu = OptimizeR_Mu(train_data, r_list, mu_list, w_rand)
updates, w = MarginPerceptron(train_data, r, mu, w_rand)
correct = TestWeightVector_Mu(w, mu, test_data)
print("Margin Perceptron")
print("Updates: " + str(updates) + " Accuracy: " + str(correct/len(test_data)))



# Loops over the two data sets but keeps them separate
for data_num in [0,1]:

    # Initializes the variables for each data set
    dimensions = []
    normal_updates = []
    normal_accuracy = []
    margin_updates = []
    margin_accuracy = []
    agressive_updates = []
    agressive_accuracy = []

    base_train = "./data" + str(data_num) + "/train" + str(data_num) + "."
    base_test = "./data" + str(data_num) + "/test" + str(data_num) + "."

    print("\nRunning Perceptron over the d" + str(data_num) + " data")
    # Runs over all the dimensions of data [10, 20, ..., 100]
    for i in range(10,101,10): 
        print("    Dimension: " + str(i))
        dimensions.append(i)
        train_file = base_train + str(i)
        train_data = ReadData(train_file)
        test_file = base_test + str(i)
        test_data = ReadData(test_file)
        temp_normal_updates = 0
        temp_normal_accuracy = 0
        temp_margin_updates = 0
        temp_margin_accuracy = 0
        temp_agressive_updates = 0
        temp_agressive_accuracy = 0

        # Runs 10 sets over each dimension to average out the randomness
        for j in xrange(0, 10):
            # Shuffles the data at each epoc
            shuffle(train_data)
        
            # Creates a random weight vector to initialize with
            w_rand = np.random.rand(len(train_data[0]))

            # Optimizes r and then runs the Perceptron Algorithm to get w
            r = OptimizeR(train_data, r_list, w_rand)        
            updates, w = Perceptron(train_data, r, w_rand)
            correct = TestWeightVector(w, test_data)
            temp_normal_updates += updates
            temp_normal_accuracy += correct/len(test_data)
        
            # Optimizes r and mu and runs Margin Perceptron
            r, mu = OptimizeR_Mu(train_data, r_list, mu_list, w_rand)
            updates, w = MarginPerceptron(train_data, r, mu, w_rand)
            correct = TestWeightVector_Mu(w, mu, test_data)
            temp_margin_updates += updates
            temp_margin_accuracy += correct/len(test_data)

            # Optimizes r, mu, eta and runs Agressive Perceptron
            r, mu = OptimizeR_Mu_Eta(train_data, r_list, mu_list, w_rand)
            updates, w = AgressivePerceptron(train_data, r, mu, w_rand)
            correct = TestWeightVector_Mu(w, mu, test_data)
            temp_agressive_updates += updates
            temp_agressive_accuracy += correct/len(test_data)
        
        # Averages over the number of runs for each dimension to get rid
        # of the randomness and make the plots nicer looking. 
        normal_updates.append(temp_normal_updates/10)
        normal_accuracy.append(temp_normal_accuracy/10)

        margin_updates.append(temp_margin_updates/10)
        margin_accuracy.append(temp_margin_accuracy/10)

        agressive_updates.append(temp_agressive_updates/10)
        agressive_accuracy.append(temp_agressive_accuracy/10)


    # Plots the num updates plot for the normal, margin, and agressive
    # Perceptron algorithms
    plt.clf()
    update_plot = "d" + str(data_num) + "_updates.pdf"
    accuracy_plot = "d" + str(data_num) + "_accuracy.pdf"
    plt.semilogy(dimensions, normal_updates, label="Normal")
    plt.semilogy(dimensions, margin_updates, label="Margin")
    plt.semilogy(dimensions, agressive_updates, label="Agressive")
    plt.xlabel("Dimensions")
    plt.ylabel("Updates")
    plt.title("Perceptron Algorithm Updates - d" + str(data_num) +" data")
    plt.legend(loc=4)
    plt.savefig(update_plot, format="pdf")

    # Plots the Accuracy plot for the normal, margin, and agressive perceptron
    # algorithms
    plt.clf()
    plt.plot(dimensions, normal_accuracy, label="Normal")
    plt.plot(dimensions, margin_accuracy, label="Margin")
    plt.plot(dimensions, agressive_accuracy, label="Agressive")
    plt.xlabel("Dimensions")
    plt.ylabel("Accuracy")
    plt.title("Perceptron Algorithm Accuracy - d" + str(data_num) + " data")
    plt.legend(loc=1)
    plt.savefig(accuracy_plot, format="pdf")

    print("Plots " + update_plot + " and " + accuracy_plot + " saved")

print("Done!")
