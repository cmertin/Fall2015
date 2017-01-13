'''
ID3.py
Author: Christohper Mertin
Date: September 15, 2015
Uses the ID3 algorithm to decide on the nodes that should be used when building
the decision tree
'''

from __future__ import division
from math import log

# Calculates the entropy of the given dictionary entry based on the definiton
# of entropy from the ID3 algorithm
def Entropy(dictEntry, target):

    size = len(dictEntry)
    labelFrequency = {}
    entryEntropy = 0

    for singleEntry in dictEntry:
        if (labelFrequency.has_key(singleEntry[target])):
            labelFrequency[singleEntry[target]] += 1
        else:
            labelFrequency[singleEntry[target]] = 1
            
    for freq in labelFrequency.values():
        entryEntropy += (-freq/size) * log(freq/size, 2)

    return entryEntropy

# Calculates the information gain of the attribute from the definition which
# is the entropy of the overall data minus the sum over all of the entropy 
# values for all the values of the given attribute
def InformationGain(dictEntry, attribute, target):

    labelFrequency = {}
    entryEntropy = 0.0

    for singleEntry in dictEntry:
        if (labelFrequency.has_key(singleEntry[attribute])):
            labelFrequency[singleEntry[attribute]] += 1
        else:
            labelFrequency[singleEntry[attribute]] = 1

    for entryValue in labelFrequency.keys():
        valueProbability = labelFrequency[entryValue] / sum(labelFrequency.values())
        valueDictEntry = []
        for singleEntry in dictEntry:
            if singleEntry[attribute] == entryValue:
                valueDictEntry.append(singleEntry)
        
        entryEntropy += valueProbability * Entropy(valueDictEntry, target)

    return (Entropy(dictEntry, target) - entryEntropy)
