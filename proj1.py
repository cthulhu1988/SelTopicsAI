#!/usr/bin/env python3
#Isaac G Callison
#CSCI 6350-001
#Project #1
#Due: 01/30/20
# From book:
    # TARGET -> TOP , Y, n, i
    # Source -> SIDE LEFT , X, m, j
    # n/i is leng of source X string and m/j in leng of Target Y string
    # source is the siderow X , target is the top Y row
import csv
import random
import numpy as np

def main():
    # hardcoded files to be imported
    leviDistance = "costs.csv"; confDistance = "costs2.csv"; wordList = "words.txt"

    # object with 2d array wherein matices and word lists reside.
    global leviObj
    global confObj
    leviObj = matrixObj(openCSVFile(leviDistance)); confObj = matrixObj(openCSVFile(confDistance))
    wordObjList = (openTXTFile(wordList))

    for y, wObj in enumerate(wordObjList):
    ############ LOOP THROUGH ###################
        for x in range(wObj.getListLeng()):
            n,m = wObj.getSrcWordLeng(x), wObj.getTrgtLeng()
    # GET BACK intialized matrix.
            scrMatInit = scoreMatrixInit(n,m)
    # FINISH filling up the score matix. Change based on levinstein or confusion
            targetString = wObj.targetWord
            sourceString = wObj.sourceList[x]

            scrMatrix, cost, PMatrix = fillScoreMatrix(n,m,scrMatInit, targetString, sourceString)
            print(scrMatrix)

            final_seq1, final_seq2, changes = findSequences(PMatrix, targetString, sourceString)
            changes = changes[::-1]
            final_seq1 = final_seq1[::-1]
            final_seq2 = final_seq2[::-1]
            printFinalOutput(final_seq1, final_seq2, cost,changes)
        print("-"*50)

def printFinalOutput(final_seq1, final_seq2, cost, changes):
    sepLeng = len(final_seq1)
    print(final_seq2)
    print("|"*sepLeng)
    print("{} ({})".format(final_seq1, cost))
    print(changes)
    print()

######################### CLASSES ##########################

class matrixObj:
    def __init__(self, array):
        self.array = array
    def printMatrix(self):
        print(np.shape(self.array))
        for row in self.array:
            print(row)
    def getCost(self, i, j):
        return int(self.array[i][j])


class WordObj:
    def __init__(self, list):
        self.targetWord = list[0]
        self.sourceList = list[1:]
    def getTrgtLeng(self):
        return len(self.targetWord)
    def getSrcWordLeng(self, num=0):
        return len(self.sourceList[num])
    def getListLeng(self):
        return len(self.sourceList)
    def printList(self):
        print("Target word is {}".format(self.targetWord))
        print("Source Words are: ")
        for word in self.sourceList:
            print(word, end=" ")
        print()

####################FUNCTIONS###########################################################
def findSequences(PMatrix, targetString, sourceString):
    TRG_SEQ = ""; SRC_SEQ = ""; changes = ""
    i = len(targetString); j = len(sourceString)
    current_node = PMatrix[j][i]

    print("target word {} and source word {}".format(targetString, sourceString))
    # navigate traceback array, start at bottom right.

    while i >= 0 or j >= 0:
        if PMatrix[j][i] == "\\":
            current_node = "\\"
            i-=1
            j-=1
            TRG_SEQ += targetString[i]
            SRC_SEQ += sourceString[j]
            if sourceString[j] == targetString[i]:
                changes += "k"
            else:
                changes += "s"

        elif PMatrix[j][i] == "^":
            j-=1
            changes += "d"
            #SRC_SEQ += "^"

        elif PMatrix[j][i] == "<":
            current_node = "<"
            i-=1
            changes+="i"
            SRC_SEQ += "<"
            TRG_SEQ += targetString[i-1]
        elif PMatrix[j][i] == 0:
            break

    print("i {} and j {}".format(i,j))
    while i > 0:
        TRG_SEQ += (targetString[i-1])
        SRC_SEQ += ("*")
        i -= 1
    while j > 0:
        SRC_SEQ += (sourceString[j])
        TRG_SEQ += ("*")
        j -= 1
    return TRG_SEQ,SRC_SEQ, changes

def fillScoreMatrix(n,m,scoreMat, targetString, sourceString):
    n,m = n+1,m+1
    i,j = n,m

    pointer_list = []
    w, h = scoreMat.shape
    PMatrix = [[0 for x in range(h)] for y in range(w)]

    for i in range(1,n):
        for j in range(1,m):
            scoreMat[i][j], pointer = return_min(i, j,scoreMat, targetString, sourceString)
            pointer_list.append(pointer)
            PMatrix[i][j] = pointer
    cost = (scoreMat[n-1][m-1])

    for x in range(w):
        for y in range(h):
            print(PMatrix[x][y],end=" ")
        print()
    return scoreMat, cost, PMatrix

def return_min(i, j, matrix, targetString, sourceString):

    targetLetter = ord(targetString[j-1])-96
    sourceLetter = ord(sourceString[i-1])-96
    #print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    left = matrix[i-1,j] + 1 # delete cost of source(i)
    up = matrix[i,j-1] + 1 # ins cost of target(j)
    diag = matrix[i-1,j-1] + leviObj.getCost(sourceLetter,targetLetter)
    #print("left {} up {} diag {}".format(left, up, diag))
    new_row = []
    new_row_dict ={"<":left,"^":up,"\\":diag}
    min_val = 1000
    key_value = ""
    for k,v in new_row_dict.items():
        if v < min_val:
            min_val = v
            key_value = k

    for key, value in new_row_dict.items():
        if value == min_val:
            new_row.append(key)
    # Choose a random path.
    #print(new_row)
    RAND_DIRECTION = new_row[random.randrange(0,len(new_row))]
    #print("direction choosen {}".format(RAND_DIRECTION))
    return min_val, RAND_DIRECTION

def scoreMatrixInit(n,m):
    n,m = n+1,m+1
    i,j = n,m
    score_matrix = np.zeros((n, m), dtype=int)
    for i in range(1,n):
        score_matrix[i,0] = score_matrix[i-1,0] + 1
    for j in range(1,m):
        score_matrix[0,j] = score_matrix[0, j-1] + 1
    return score_matrix

def openTXTFile(file):
    listWordObjs = []
    f = open(file)
    for row in f:
        row = row.split()
        listWordObjs.append(WordObj(row))
    return listWordObjs

def openCSVFile(file):
    f = open(file, 'r')
    lev =  csv.reader(f, delimiter=',')
    rows = [row for row in lev]
    return rows

if __name__ == '__main__':
    main()
