'''
DecisionTree.py
Author: Christopher Mertin
Date: September 15, 2015
Holds the functions that build and return a decision tree based off of the 
given data and the given function to calculate the information gain, where the 
largest information gain is used in calculating the root. It creates the tree 
by creating nested dictionaries. The collections library is used to help
create default dictionary entries for those cases which don't wind up existing
in the training data
'''

import collections

# Creates a new decision tree recursively. It does so by choosing the best 
# attribute in the list of values by calculating the information gain based on 
# the provided function in the last argument.
def BuildTree(dictEntry, attributes, target, infoGain):

    # Finds the most common label in the data to see what to label 
    # unidentifiable sets as.
    defaultLabel = CommonLabel(dictEntry, target)

    # Default case, if there's no attributes in the list or there's not any 
    # data, then return the default
    if not dictEntry or len(attributes)-1 <= 0:
        return defaultLabel
    
    # Calculates the best attribute based off the information gain
    bestAttribute = ChooseAttribute(dictEntry, attributes, target, infoGain)

    # Creates a tree with using the collections.defaultdict function which
    # sets the default value in the dictionary to be the default label 
    # (most common) and it is changed if that tree/branch is taken to the 
    # base. This dictionary is grouped based off the best attribute
    tree = {bestAttribute:collections.defaultdict(lambda: defaultLabel)}

    for value in ValuesList(dictEntry, bestAttribute):
        
        subAttributes = []
        
        # Does something
        subDictEntry = MatchList(dictEntry, bestAttribute, value)
        
        # Goes through the attributes and picks the ones which aren't 
        # choosen as the best, as that is going to be used in the 
        # next level of it.
        for attribute in attributes:
            if attribute != bestAttribute:
                subAttributes.append(attribute)

        # Builds the sub dictionary for the next level of the tree
        subDictionary = BuildTree(subDictEntry, subAttributes, target, infoGain)

        # Sets the value of the new entry of the tree
        tree[bestAttribute][value] = subDictionary

    return tree

# Cycles through all the attributes, calculating their information gain to 
# see which one is the best to choose. After it figures out the best one,
# it returns it
def ChooseAttribute(dictEntry, attributes, target, infoGain):

    highestGain = 0.0
    bestAttribute = None
    
    # Iterates through all the attributes
    for attribute in attributes:

        # Calculates the gain for the iterated attributes
        gain = infoGain(dictEntry, attribute, target)
        
        # Checks to see if the gain is higher than the currently stored
        # gain, and if it is not the target label that we're looking for
        # If it falls under these conditions, then it stores the values
        # as a potential candidate
        if gain >= highestGain and attribute != target:
            highestGain = gain
            bestAttribute = attribute

    return bestAttribute

# Finds the most common label in the given data and returns it
def CommonLabel(dictEntry, target):

    labelList = []

    # Iterates through the labels in the data and appends them to a list
    # so they can be used to find the most frequent label in the given set
    for label in dictEntry:
        labelList.append(label[target])
     
    return MostFrequent(labelList)
    
# Returns the item that appears most frequenty in the given list
def MostFrequent(dataList):

    highestFrequency = 0
    mostFrequentLabel = None
    
    # Iterates through a *Unique* list of labels to get the one with the
    # highest frequency
    for label in UniqueValue(dataList):
        if dataList.count(label) > highestFrequency:
            mostFrequentLabel = label
            highestFrequency = dataList.count(label)

    return mostFrequentLabel

# Removes redundant values in a list and returns a list containing only
# unique values
def UniqueValue(dataList):

    uniqueList = []

    # Cycles through the entire list of values
    for value in dataList:

        # If the current value is not in the list of unique values, and if
        # the number of times that it's in the unique list is zero, append it
        if uniqueList.count(value) == 0:
            uniqueList.append(value)

    return uniqueList

# Returns a list of values for the given attribute with it only containing 
# unique values so that it is easier to build the decision tree.
def ValuesList(dictEntry, attribute):
    
    valueList = []
    
    # For the given attribute, iterates through all the values to see which
    # ones are in there. Appends them to a list and then returns only the
    # unique ones so you know which ones should go on the node of the tree.
    for value in dictEntry:
        valueList.append(value[attribute])
    
    return UniqueValue(valueList)

# Recursively iterates through the data and returns a list of all data that has
# a matching value for a given attribute
def MatchList(dictEntry, attribute, value):
    dictEntry = dictEntry[:]
    matchList = []

    # Returns nothing, as matchList is defined as blank above
    if not dictEntry:
        return matchList
    else:
        # Pops off the first element of data so it's a single entry and checks
        # to see if it has the same matching value for the attribute
        singleEntry = dictEntry.pop()
        if singleEntry[attribute] == value:
            matchList.append(singleEntry)
            matchList.extend(MatchList(dictEntry, attribute, value))
            return matchList
        else:
            matchList.extend(MatchList(dictEntry, attribute, value))
            return matchList

# Creates a list of the classified labels of all of the data in the given
# set by using the decision tree to help classify the entries
def Classify(tree, dictEntry):

    classifiedLabels = []
    
    # Iterates over all of the entries in the data and gets their classification
    for entry in dictEntry:
        entryLabel = GetClassification(entry, tree)
        classifiedLabels.append(entryLabel)

    return classifiedLabels

# Traverses the tree by continually asking each entry for it's classification
# until it gets to the base case of it being a string, which means at the
# final leaf node
def GetClassification(entry, tree):

    if type(tree) == type("string"):
        return tree

    else:
        firstAttribute = tree.keys()[0]
        subtree = tree[firstAttribute][entry[firstAttribute]]
        return GetClassification(entry, subtree)

    
