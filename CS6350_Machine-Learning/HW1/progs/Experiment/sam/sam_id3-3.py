#!/usr/bin/python

from __future__ import division
import sys
import math

def total_Entropy(game_List):   #Computes the total entropy of all games within game_File
    posCount, negCount = 0, 0
    
    for line in game_List:
        if line[9] == 'positive\n':
            posCount += 1
        else:
            negCount += 1
    return entropy(posCount, negCount)

def entropy(Ppos,Pneg):    #Computes the entropy for one value in a label, i.e. x in the label square 1
    Ptot = Ppos+Pneg
    frac_Pos = Ppos/Ptot
    frac_Neg = Pneg/Ptot
    entropy = -1*frac_Pos*math.log(frac_Pos,2)-frac_Neg*math.log(frac_Neg,2)
    return entropy

def order_Pi(game_File,label_Number):  #provides a list of number of [x, o, b] in game_File at label_Number
    xCount = 0
    oCount = 0
    bCount = 0
    
    with open(game_File, "r") as filestream:
        for line in filestream:
            i = line.split(',')[label_Number]
            if i == 'x':
                xCount += 1
            elif i == 'o':
                oCount += 1
            else:
                bCount += 1
    counts = [xCount,oCount,bCount]
    return counts
              
def order_Pi_Sgn(game_Data, label_Number):  #Provides the number of games where x,o, b in cell label label_Number have positive and how many have negative game outcomes.
    xPos, xNeg = 0, 0
    oPos, oNeg = 0, 0
    bPos, bNeg = 0, 0
    
    for game in game_Data:
        if game[label_Number] == 'x':
            if game[9] == 'positive\n':
                xPos+=1
            else:
                xNeg +=1
        if game[label_Number] == 'o':
                if game[9] == 'positive\n':
                    oPos += 1
                else:
                    oNeg += 1
        if game[label_Number] == 'b':
                if game[9] == 'positive\n':
                    bPos += 1
                else:
                    bNeg += 1
                    
    return [(xPos,xNeg),(oPos,oNeg),(bPos,bNeg)]

def entropy_Pi(game_Data, label_Number):   #provides the entropy at a given label where each label is a cell in the game
    
    values = order_Pi_Sgn(game_Data, label_Number)
    
    xPos, xNeg = values[0][0], values[0][1]
    xTot = xPos + xNeg
    yPos, yNeg = values[1][0], values[1][1]
    yTot = yPos + yNeg
    bPos, bNeg = values[2][0], values[2][1]
    bTot = bPos + bNeg
    
    order_Values = xTot + yTot + bTot
    
    entropyX = entropy(xPos,xNeg)
    entropyY = entropy(yPos,yNeg)
    entropyB = entropy(bPos,bNeg)
    
    entropy_Label = xTot / order_Values * entropyX + yTot / order_Values * entropyY + bTot/order_Values * entropyB
    
    return entropy_Label

def info_Gain(game_Data, label_Number):
    values = order_Pi_Sgn(game_Data, label_Number)
    
    xPos, xNeg = values[0][0], values[0][1]
    xTot = xPos + xNeg
    yPos, yNeg = values[1][0], values[1][1]
    yTot = yPos + yNeg
    bPos, bNeg = values[2][0], values[2][1]
    bTot = bPos + bNeg
    
    order_Values = xTot + yTot + bTot
    
    entropyX = entropy(xPos,xNeg)
    entropyY = entropy(yPos,yNeg)
    entropyB = entropy(bPos,bNeg)
    
    gainX = xTot / order_Values * entropyX
    gainY = yTot / order_Values * entropyY
    gainB = bTot/order_Values * entropyB
    
    return (gainX,gainY,gainB)

def decision_Tree(gain_List):   #provides a list ordered in the order of nodes in the decision tree as determined by the ID3 alg
    tree_Order = [None]*9
    
    for i in range(9):
        minGain = min(gain_List)
        tree_Order[i] = gain_List.index(minGain)
        gain_List[tree_Order[i]] = 2                  #arbitrary value larger than what any entropy value will be
    return tree_Order

def recur_Tree(tictactoeList, cell, gameState):

    #if all values are the same at the current label, create leaf with that value i.e. x, o, or b 
    listOfValsAtCell = []
    for i in range(9):
        if gameState[i] == None:
            listOfValsAtCell = list(map(lambda x: cell == tictactoeList[0][i], tictactoeList))
            print("Heyo")
            print(listOfValsAtCell)
        if False not in listOfValsAtCell:
            print(tictactoeList[i][9])
            newNode = Node("leaf",tictactoeList[i][9])
            return newNode
        else:
            tEntropy = total_Entropy(tictactoeList) #computes the total entropy of all games within given file
            labels = []
            gain_Label=[float("inf")]*9
            # we collect all labels that have not yet taken a place in the tree and calculate the info. gain for all of them
            for i in range(len(gameState)):    
                if gameState[i] == None:
                    labels.append(i)
            print(labels)
            for l in labels:
                gain_Label[l] = tEntropy - entropy_Pi(tictactoeList, l)
            #we branch on the label with desired information gain
            firstNode = decision_Tree(gain_Label)[0]
            newNode = Node(firstNode,cell)  
            #we record that this label is no longer available
            gameState[firstNode] = 2
            print(gameState)
            #loop over x, o, b under node which we branch from, considering only training games from training set with x, o, b current label (cell of game)            
            for i in ['x','o','b']:
                tempList = filter( lambda x: x[firstNode] == cell, tictactoeList)
                #still must add empty case which adds leaf with most common value.
                #recur from this node adding the recursion tree as a child to current leaf
                newNode.add_child(recur_Tree(tictactoeList, i, gameState))
            return newNode

    
class Node(object):
    def __init__(self, label, value):
        self.label = label
        self.value = value
        self.children = []
        self.tree = []
        
    def add_child(self, obj):
        self.children.append(obj)
        
    def set_Value(self, val):
        self.value = val
             
tree=[]            
def show_Tree(self):
    level = []
    for i in self.children:
        level.append("(" + str(i.label) + "," + str(i.value) + ")")
        tree.append(level)
    for i in self.children:
        if isinstance(i,Node):
            print remove_duplicates(tree[len(self.children)-1:])
            for key in show_Tree(i):
                yield tree.append(key)
        else:
            yield tree.append(i.label)
        
    #def has_child(self, obj)
    
    #def is_Leaf(self)
        #len(self.children)==0
def remove_duplicates(values):
    # order preserving
    checked = []
    for e in values:
        if e not in checked:
            checked.append(e)
    return checked     

def main(tictactoe_argv):
    labels = ['1','2','3','4','5','6','7','8','9',"win?"]
    gameState = [None]*9
    
    fileArray = []

    with open(tictactoe_argv,"r") as filestream:
        for line in filestream:
            i = line.split(',') 
            fileArray.append(i)

    del fileArray[0]
 
    #here we determine the node to start with.
    tEntropy = total_Entropy(fileArray) #computes the total entropy of all games within given file
    gain_Label = [None]*9  #list of entropy per Label (cell 1-9 in tic-tac-toe game)
    for label in range(9):
        gain_Label[label] = tEntropy - entropy_Pi(fileArray, label)
   
    rootNode = decision_Tree(gain_Label)[0]
    gameState[rootNode]=2
    fileArrayCopy = fileArray
    decisionTree = Node(rootNode,'x')
    decisionTree.add_child( recur_Tree(fileArrayCopy,rootNode,gameState))
    
    #for i in show_Tree(decisionTree):
    #    print i
    """
    decisionTree = Node(firstNode,'x')
    gameState[firstNode] = 2
    testNode = Node(4,'o')
    decisionTree.add_child(testNode)
    testNode2 = Node(3,'x')
    decisionTree.add_child(testNode2)
    testNode3 = Node(6,'o')
    testNode4 = Node(8,'x')
    testNode2.add_child(testNode3)
    testNode2.add_child(testNode4)
    print decisionTree.label
    print "#######"
    tree = build_tree(decisionTree)
           
    for i in tree:
        print i
    """
if __name__ == '__main__':
    main(sys.argv[1])
