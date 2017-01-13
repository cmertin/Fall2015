#!/usr/bin/python
'''
RunID3.py
Author: Christopher Mertin
Date: September 15, 2015
Uses DecisionTree.py and ID3.py to build a minimum spanning decision tree based
on the given training data and then tests the tree based on the test set of
data that is given to it.
'''

from __future__ import print_function
from DecisionTree import *
from ID3 import *

# Reads the first line of the file to get the attributes
def ReadAttributes(dataFile):
    infile = open(dataFile, "r")
    firstLine = infile.readline()
    # "chomps" the first line to remove the end line character with strip
    # and then splits it on "," and turns it into a list and returns it
    return firstLine.strip().split(",")

# Reads the data in the given file and separates them into dictionaries 
# corresponding to each value for each attribute of each row
def ReadData(dataFile, attributes):
    data = []

    # Reads the file and strips away the endline characters
    infile = open(dataFile, "r")
    lines = [line.strip() for line in infile.readlines()]

    # Removes the attribute line in the first row
    del lines[0]

    for line in lines:
        values = []
        for column in line.split(","):
            values.append(column.strip())
        values = zip(attributes, values)
        values = dict(values)
        data.append(values)

    #print("Successfully read data from the file " + dataFile)
    return data 

######################## Base Variables ############################
trainBaseName = "Data/train/tic-tac-toe-train-"
testBaseName = "Data/test/tic-tac-toe-test"
sample = "Data/test/small_sample.txt"
trainingData = []
testData = []
target = "Win"

######################## Reads The Data ############################
testFile = testBaseName + ".txt"
attributes = ReadAttributes(testFile)
testData.extend(ReadData(testFile, attributes))

for i in xrange(1,7):
    trainingFile = trainBaseName + str(i) + ".txt"
    trainingData.extend(ReadData(trainingFile, attributes))

######################## Builds Tree ###############################
decisionTree = BuildTree(trainingData, attributes, target, InformationGain)

##################### Test Training Data ###########################
classifiedTest = Classify(decisionTree, testData)
testDataActual = []
testTotal = len(classifiedTest)
testCorrect = 0
testWrong = 0

for i in xrange(0, len(testData)):
    testDataActual.append(testData[i]["Win"])

for i in xrange(0, testTotal):
    if classifiedTest[i] == testDataActual[i]:
        testCorrect += 1
    else:
        testWrong += 1

print("Out of the test set, " + str(testCorrect) + "/" + str(testTotal) + 
      " were correct, while " + str(testWrong) + "/" + str(testTotal) + 
      " were wrong")
